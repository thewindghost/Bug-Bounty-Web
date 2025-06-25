from flask import request, render_template, session, render_template_string
from app.utils.check_xml_encoding import get_xml_encoding_lxml
from app.services.write_log_entries import count_log_entries
from werkzeug.security import generate_password_hash
from app.services.update_user_profile import update_user_profile
from lxml import etree
from app.config import Config
from datetime import datetime
from bleach import clean

def handle_setting_user():
    
    try:
        if not request.content_type.startswith('application/xml'):
            return render_template('user/setting_user.html', error="Invalid content type. Only application/xml is accepted.")

        raw_data = request.data
        if not raw_data:
            raise ValueError("No XML data provided.")

        encoding = get_xml_encoding_lxml(raw_data)
        if encoding.lower() != 'utf-8':
            return render_template('user/setting_user.html', error=f"Only UTF-8 is allowed. Got: {encoding}")

        update_setting_V1 = etree.XMLParser(resolve_entities=True, load_dtd=False, no_network=False)
        root_V1 = etree.fromstring(raw_data, parser=update_setting_V1)
        update_setting_V2 = etree.XMLParser(resolve_entities=False, load_dtd=False, no_network=True)
        root_V2 = etree.fromstring(raw_data, parser=update_setting_V2)

        #username = clean(render_template_string(session.get("username")))
        username = session.get("username")
        is_admin = session.get("is_admin")
        new_email = root_V2.findtext("email")
        new_birth_date = root_V2.findtext("birth_date")
        new_setting = root_V1.findtext("setting")
        new_raw_password = root_V2.findtext("password")

        entry_number = count_log_entries(Config.LOG_FILE_RELATIVE_PATH) + 1
        timestamp = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

        log_entry = (
            f"\n[Entry #{entry_number}]\n"
            f"Username: {username} | Is_admin: {is_admin}\n"
            f"New Email: {new_email}\n"
            f"Birth Date: {new_birth_date}\n"
            f"Setting: {new_setting}\n"
            f"Password: {new_raw_password}\n"
            f"Time: {timestamp}\n"
            f"---------------------------\n"
        )
        with open(Config.LOG_FILE_RELATIVE_PATH, "a") as f:
            f.write(log_entry)

        new_password = generate_password_hash(new_raw_password)

        success_update = update_user_profile(
            username=username,
            email=new_email,
            birth_date=new_birth_date,
            password=new_password
        )
            
        if not success_update:
            return render_template("user/setting_user.html", error="No fields updated.")

        return render_template("user/setting_user.html", success="Your settings were updated.")

    except Exception as e:
        e = "Internal Server Error", 500
        return render_template("user/setting_user.html", error=e)
