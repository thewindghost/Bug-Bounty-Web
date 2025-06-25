from flask import jsonify
from app.config import Config
import os
    
def clear_logs_admin():

    try:
        log_file = Config.LOG_FILE_RELATIVE_PATH

        if not os.path.exists(log_file):
            return jsonify({"status": "error", "message": "Log file not found."}), 404

        open(log_file, 'w').close()

        return jsonify({"status": "success", "message": "Logs cleared successfully."}), 200

    except Exception as e:
        e = "Internal Server Error"
        return jsonify({"status": "error", "message": str(e)}), 500