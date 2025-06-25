from app.config import Config

log_file_path = Config.LOG_FILE_RELATIVE_PATH

def count_log_entries(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        entries = content.split('---------------------------')
        return len([e for e in entries if e.strip()])
    except FileNotFoundError:
        return 0
