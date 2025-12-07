# Workspace Task Manager

A workspace-based task management system built with Flask and MySQL, supporting role-based access control (RBAC), task assignment, and workflow-driven progress tracking.

---

## 🚀 Features

### 🔐 User Authentication & Authorization
- Secure login and registration
- Session-based authentication

### 🏢 Workspace Management
- Create and delete workspaces
- Workspace-level task isolation

### 👥 Role-Based Access Control (RBAC)
- Admin and Member roles
- Admin-only privileged actions

### ✅ Task Lifecycle Management
- Create, assign, and delete tasks
- Task workflow states:
  - TODO
  - IN_PROGRESS
  - DONE

### 🎯 Task Assignment & Ownership
- Assign tasks to workspace members
- Only assigned users can update task status

### 📋 Personal Task Dashboard
- "My Tasks" view for assigned work across all workspaces

### 🗑 Safe Destructive Operations
- Admin-only task deletion
- Admin-only workspace deletion
- Cascading cleanup to prevent orphaned data

---

## 🛠 Tech Stack

- Backend: Python, Flask
- Database: MySQL (SQLAlchemy ORM)
- Authentication: Flask-Login
- Frontend: HTML, Jinja2, Bootstrap
- Version Control: Git, GitHub

---

## 🗂 Project Structure

workspace-task-manager/
│
├── app.py
├── config.py
├── models.py
├── auth_routes.py
├── task_routes.py
│
├── templates/
│ ├── base.html
│ ├── login.html
│ ├── register.html
│ ├── workspaces.html
│ ├── create_workspace.html
│ ├── workspace_dashboard.html
│ ├── add_member.html
│ └── my_tasks.html
│
├── static/
│
├── db/
│ └── schema.sql
│
├── requirements.txt
├── README.md
└── .gitignore


---

## ⚙️ Database Schema

The database schema is available at:



db/schema.sql


It includes:
- Users
- Workspaces
- Workspace members (with roles)
- Tasks (assignment + status workflow)

---

## ▶️ Getting Started (Local Setup)

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/workspace-task-manager.git
cd workspace-task-manager

2. Create Virtual Environment
python3 -m venv venv
source venv/bin/activate

3. Install Dependencies
pip install -r requirements.txt

4. Configure Database

Create a MySQL database (e.g. task_manager_db)

Update credentials in config.py

5. Run the Application
python app.py


Application runs at:

http://127.0.0.1:5000

🔐 Access Control Summary
Action	Admin	Member
Create workspace	✅	❌
Delete workspace	✅	❌
Add members	✅	❌
Create / assign tasks	✅	❌
Update task status	✅	✅ (assigned)
Delete tasks	✅	❌
View tasks	✅	✅
💡 Future Enhancements

Task comments and activity logs

Search and filtering

Pagination for large workspaces

Deployment (Render / AWS / Railway)

📌 Why This Project?

This project demonstrates:

Real-world backend architecture

Secure role-based access control

Clean separation of concerns

Practical use of Flask with relational databases

It is designed as a production-style MVP, not a basic to-do application.

👨‍💻 Author

Srinidhi M D


---

### ✅ WHAT TO DO NOW
1. Open `README.md`
2. **Delete everything**
3. Paste the above content
4. Save
5. Commit:

```bash
git add README.md
git commit -m "Add clean project README"
git push