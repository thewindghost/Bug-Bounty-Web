from app.config import Config

log_file_path = Config.LOG_FILE_RELATIVE_PATH

def count_log_entries(filename=log_file_path):
    
    try:
        with open(filename, 'r') as f:
            lines = f.readline()
        count = sum(1 for line in lines if line.startswith('[Entry'))
        return count
    
    except FileExistsError:
        return 0