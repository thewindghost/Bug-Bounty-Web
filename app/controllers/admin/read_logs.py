from flask import render_template
from app.config import Config
import os

def read_logs_info():
    try:
        if not os.path.exists(Config.LOG_FILE_RELATIVE_PATH):
            return "Not Found File Logs", 404

        with open(Config.LOG_FILE_RELATIVE_PATH, 'r') as f:
            log_data = f.read()

        entries = log_data.strip().split("---------------------------")
        entries = [e.strip() for e in entries if e.strip()]

        return render_template("admin/logs.html", entries=entries)

    except Exception as e:
        return f"Error reading logs: {str(e)}", 500
