from settings import ADMIN_PASSWORD, SUBJECT_PRESETS_DEFAULT, EMAIL_RECIPIENTS_DEFAULT
from app_ui import run_app
from registry_store import load_from_registry

def main():
    state = {
        "subjects": SUBJECT_PRESETS_DEFAULT.copy(),
        "recipients": EMAIL_RECIPIENTS_DEFAULT.copy(),
    }
    
    saved_recipients, saved_subjects = load_from_registry()
    if saved_recipients:
        state["recipients"] = saved_recipients
    if saved_subjects:
        state["subjects"] = saved_subjects

    run_app(state, ADMIN_PASSWORD)


if __name__ == "__main__":
    main()
