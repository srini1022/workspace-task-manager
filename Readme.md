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

