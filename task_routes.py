from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from models import db, Workspace, WorkspaceMember, Task, User

tasks = Blueprint("tasks", __name__)

# ---------------------------------------------------
# Helper functions (USED EVERYWHERE)
# ---------------------------------------------------
def get_membership(user_id, workspace_id):
    return WorkspaceMember.query.filter_by(
        user_id=user_id,
        workspace_id=workspace_id
    ).first()


def is_admin(user_id, workspace_id):
    member = get_membership(user_id, workspace_id)
    return member and member.role == "admin"


# ---------------------------------------------------
# List all workspaces for logged-in user
# ---------------------------------------------------
@tasks.route("/workspaces")
@login_required
def my_workspaces():
    workspaces = (
        db.session.query(Workspace)
        .join(WorkspaceMember)
        .filter(WorkspaceMember.user_id == current_user.id)
        .all()
    )
    return render_template("workspaces.html", workspaces=workspaces)


# ---------------------------------------------------
# Create workspace (creator = admin)
# ---------------------------------------------------
@tasks.route("/workspace/create", methods=["GET", "POST"])
@login_required
def create_workspace():
    if request.method == "POST":
        workspace = Workspace(
            name=request.form["name"],
            created_by=current_user.id
        )
        db.session.add(workspace)
        db.session.commit()

        admin_member = WorkspaceMember(
            user_id=current_user.id,
            workspace_id=workspace.id,
            role="admin"
        )
        db.session.add(admin_member)
        db.session.commit()

        return redirect(url_for("tasks.my_workspaces"))

    return render_template("create_workspace.html")


# ---------------------------------------------------
# Workspace Dashboard (Tasks + Assignment)
# ---------------------------------------------------
@tasks.route("/workspace/<int:workspace_id>/dashboard", methods=["GET", "POST"])
@login_required
def workspace_dashboard(workspace_id):

    # ✅ membership check
    member = get_membership(current_user.id, workspace_id)
    if not member:
        return "Unauthorized", 403

    # ✅ all members of workspace (for assignment)
    workspace_members = (
        db.session.query(User)
        .join(WorkspaceMember)
        .filter(WorkspaceMember.workspace_id == workspace_id)
        .all()
    )

        # ✅ create task (admin can assign)
    if request.method == "POST":

        # ✅ ONLY ADMIN CAN CREATE TASKS
        if member.role != "admin":
            return "Unauthorized", 403

        assigned_to = request.form.get("assigned_to")

        task = Task(
            title=request.form["title"],
            description=request.form["description"],
            created_by=current_user.id,
            workspace_id=workspace_id,
            assigned_to=int(assigned_to) if assigned_to else None
        )

        db.session.add(task)
        db.session.commit()

        return redirect(
            url_for("tasks.workspace_dashboard", workspace_id=workspace_id)
        )

    tasks_list = (
        db.session.query(Task, User)
        .outerjoin(User, Task.assigned_to == User.id)
        .filter(Task.workspace_id == workspace_id)
        .all()
    )


    return render_template(
        "workspace_dashboard.html",
        tasks=tasks_list,
        member=member,
        workspace_id=workspace_id,
        workspace_members=workspace_members
    )



# ---------------------------------------------------
# Add member (ADMIN ONLY)
# ---------------------------------------------------
@tasks.route("/workspace/<int:workspace_id>/add-member", methods=["GET", "POST"])
@login_required
def add_member(workspace_id):

    if not is_admin(current_user.id, workspace_id):
        return "Unauthorized", 403

    if request.method == "POST":
        username = request.form["username"]
        user = User.query.filter_by(username=username).first()

        if not user:
            return "User not found", 404

        # prevent duplicates
        existing = WorkspaceMember.query.filter_by(
            user_id=user.id,
            workspace_id=workspace_id
        ).first()

        if not existing:
            new_member = WorkspaceMember(
                user_id=user.id,
                workspace_id=workspace_id,
                role="member"
            )
            db.session.add(new_member)
            db.session.commit()

        return redirect(
            url_for("tasks.workspace_dashboard", workspace_id=workspace_id)
        )

    return render_template("add_member.html", workspace_id=workspace_id)



@tasks.route("/task/<int:task_id>/status/<string:new_status>")
@login_required
def update_task_status(task_id, new_status):

    task = Task.query.get_or_404(task_id)

    # ✅ membership check
    member = get_membership(current_user.id, task.workspace_id)
    if not member:
        return "Unauthorized", 403

    # ✅ allow only valid status values
    if new_status not in ["TODO", "IN_PROGRESS", "DONE"]:
        return "Invalid status", 400

    task.status = new_status
    db.session.commit()

    return redirect(
        url_for("tasks.workspace_dashboard", workspace_id=task.workspace_id)
    )

@tasks.route("/task/<int:task_id>/delete")
@login_required
def delete_task(task_id):

    task = Task.query.get_or_404(task_id)

    # ✅ membership check
    member = get_membership(current_user.id, task.workspace_id)
    if not member:
        return "Unauthorized", 403

    # ✅ ONLY ADMIN CAN DELETE
    if member.role != "admin":
        return "Unauthorized", 403

    db.session.delete(task)
    db.session.commit()

    return redirect(
        url_for("tasks.workspace_dashboard", workspace_id=task.workspace_id)
    )

@tasks.route("/my-tasks")
@login_required
def my_tasks():

    tasks_list = Task.query.filter_by(
        assigned_to=current_user.id
    ).order_by(Task.created_at.desc()).all()

    return render_template(
        "my_tasks.html",
        tasks=tasks_list
    )

@tasks.route("/workspace/<int:workspace_id>/delete")
@login_required
def delete_workspace(workspace_id):

    workspace = Workspace.query.get_or_404(workspace_id)

    # ✅ membership + admin check
    member = get_membership(current_user.id, workspace_id)
    if not member or member.role != "admin":
        return "Unauthorized", 403

    # ✅ delete dependent data first
    Task.query.filter_by(workspace_id=workspace_id).delete()
    WorkspaceMember.query.filter_by(workspace_id=workspace_id).delete()

    db.session.delete(workspace)
    db.session.commit()

    return redirect(url_for("tasks.my_workspaces"))
