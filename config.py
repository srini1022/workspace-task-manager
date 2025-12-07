# config.py

class Config:
    # Used by Flask for session security
    SECRET_KEY = "super-secret-key-change-this"

    # ✅ MySQL database connection
    # FORMAT:
    # mysql+pymysql://USER:PASSWORD@HOST:PORT/DB_NAME

    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://root:root@localhost:3306/task_manager_db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
