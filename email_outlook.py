import win32com.client as win32


def send_outlook_email(subject: str, body: str, recipients: list[str]) -> bool:
    try:
        outlook = win32.Dispatch("Outlook.Application")
        mail = outlook.CreateItem(0)  # 0 = Mail item

        mail.Subject = subject
        mail.Body = body

        for r in recipients:
            mail.Recipients.Add(r)

        mail.Send()
        return True

    except Exception as e:
        print("Error sending email:", e)
        return False
