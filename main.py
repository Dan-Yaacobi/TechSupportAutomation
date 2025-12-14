from settings import ADMIN_PASSWORD, SUBJECT_PRESETS_DEFAULT, EMAIL_RECIPIENTS_DEFAULT
from app_ui import run_app


def main():
    state = {
        "subjects": SUBJECT_PRESETS_DEFAULT.copy(),
        "recipients": EMAIL_RECIPIENTS_DEFAULT.copy(),
    }
    run_app(state, ADMIN_PASSWORD)


if __name__ == "__main__":
    main()
