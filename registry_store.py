import winreg

REG_PATH = r"Software\SupportRequestForm"  # אתה יכול לשנות שם


def load_from_registry():
    """
    Returns (recipients, subjects) or (None, None) if nothing saved yet.
    """
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH)

        recipients = None
        subjects = None

        try:
            v, t = winreg.QueryValueEx(key, "email_recipients")
            if t == winreg.REG_MULTI_SZ and isinstance(v, list) and v:
                recipients = v
        except FileNotFoundError:
            pass

        try:
            v, t = winreg.QueryValueEx(key, "subject_presets")
            if t == winreg.REG_MULTI_SZ and isinstance(v, list) and v:
                subjects = v
        except FileNotFoundError:
            pass

        key.Close()
        return recipients, subjects

    except FileNotFoundError:
        return None, None


def save_to_registry(recipients: list[str], subjects: list[str]) -> None:
    key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_PATH)
    winreg.SetValueEx(key, "email_recipients", 0, winreg.REG_MULTI_SZ, recipients)
    winreg.SetValueEx(key, "subject_presets", 0, winreg.REG_MULTI_SZ, subjects)
    key.Close()
