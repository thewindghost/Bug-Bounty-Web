from flask import make_response
from app.config import Config


def read_logs_info():
    
    try:
        with open(Config.LOG_FILE_RELATIVE_PATH, 'r') as f:
            log_data = f.read()
        response= make_response(log_data)
        response.headers['Content-Type'] = 'text/html'
        return response
    
    except FileNotFoundError:
        return "Not Found File Logs", 404