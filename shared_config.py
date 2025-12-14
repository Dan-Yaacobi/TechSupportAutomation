import json
import os
import hashlib

SHARED_CONFIG_PATH = r"\\lahavfs.tau.ac.il\lahav-2\Administration\shared_config\config.json"


def load_shared_config():
    """
    Returns (recipients, subjects, admin_password_hash) or (None, None, None)
    if not available / invalid.
    """
    try:
        if not os.path.exists(SHARED_CONFIG_PATH):
            return None, None, None

        with open(SHARED_CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

        recipients = data.get("email_recipients")
        subjects = data.get("subject_presets")
        admin_hash = data.get("admin_password_hash")

        if not isinstance(recipients, list) or not recipients:
            recipients = None
        if not isinstance(subjects, list) or not subjects:
            subjects = None
        if not (isinstance(admin_hash, str) and len(admin_hash) == 64):
            admin_hash = None

        return recipients, subjects, admin_hash

    except Exception as e:
        print("Shared config load failed:", e)
        return None, None, None



def save_shared_config(recipients: list[str], subjects: list[str], admin_password_hash: str) -> bool:
    """
    Saves config to shared drive. Returns True on success.
    """
    try:
        """Assuming the shared_config folder already exists"""
        data = {
            "email_recipients": recipients,
            "subject_presets": subjects,
            "admin_password_hash": admin_password_hash,
        }

        with open(SHARED_CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return True

    except Exception as e:
        print("Shared config save failed:", e)
        return False

def hash_password(pwd: str) -> str:
    return hashlib.sha256(pwd.encode("utf-8")).hexdigest()