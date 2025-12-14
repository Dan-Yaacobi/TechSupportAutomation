from settings import ADMIN_PASSWORD, SUBJECT_PRESETS_DEFAULT, EMAIL_RECIPIENTS_DEFAULT
from app_ui import run_app
from shared_config import load_shared_config
from registry_store import load_from_registry, save_to_registry
from shared_config import load_shared_config, hash_password

def main():
    state = {
        "subjects": SUBJECT_PRESETS_DEFAULT.copy(),
        "recipients": EMAIL_RECIPIENTS_DEFAULT.copy(),
        "admin_password_hash": hash_password(ADMIN_PASSWORD),
    }

    shared_recipients, shared_subjects, shared_admin_hash = load_shared_config()

    if shared_recipients:
        state["recipients"] = shared_recipients
    if shared_subjects:
        state["subjects"] = shared_subjects
    if shared_admin_hash:
        state["admin_password_hash"] = shared_admin_hash

    if shared_recipients or shared_subjects:
        save_to_registry(state["recipients"], state["subjects"])
    else:
        # 2) fallback to registry
        reg_recipients, reg_subjects = load_from_registry()
        if reg_recipients:
            state["recipients"] = reg_recipients
        if reg_subjects:
            state["subjects"] = reg_subjects
    run_app(state, ADMIN_PASSWORD)


if __name__ == "__main__":
    main()
