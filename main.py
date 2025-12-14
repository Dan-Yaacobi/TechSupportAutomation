# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox,simpledialog
import win32com.client as win32

ADMIN_PASSWORD = "1234"

# הגדרות כלליות
SUBJECT_PRESETS = [
    "בעיה במייל",
    "תקלת מערכת",
    "תקלה בסאפ",
    "פנייה כללית",
]

EMAIL_RECIPIENTS = [
    "dany@lahav.ac.il",
    # הוסף כאן מיילים כרצונך
]

def send_outlook_email(subject: str, body: str, recipients: list[str]):
    """
    Sends an email through the local Outlook client.
    `recipients` should be a list of email strings.
    """
    try:
        outlook = win32.Dispatch("Outlook.Application")
        mail = outlook.CreateItem(0)  # 0 = Mail item

        mail.Subject = subject
        mail.Body = body

        # add each recipient
        for r in recipients:
            mail.Recipients.Add(r)

        mail.Send()  # send immediately

        return True

    except Exception as e:
        print("Error sending email:", e)
        return False

def send_complaint():
    title = title_var.get().strip()
    description = desc_text.get("1.0", tk.END).strip()

    if not title:
        messagebox.showwarning("חסר מידע", "אנא מלא כותרת לתלונה.")
        return

    if not description:
        messagebox.showwarning("חסר מידע", "אנא מלא תיאור לתלונה.")
        return

    messagebox.showinfo("נשלח", "התלונה נשלחה בהצלחה.")
    # איפוס השדות אם תרצה:
    # title_var.set("")
    # desc_text.delete("1.0", tk.END)
    send_outlook_email(title,description,EMAIL_RECIPIENTS)

def on_subject_selected(event):
    selected = subject_combo.get()
    if selected:
        title_var.set(selected)

def manage_recipients():
    """Password-protected entry point to edit recipients."""
    pwd = simpledialog.askstring("סיסמה", "אנא הכנס סיסמה:", show="*")
    if pwd is None:
        return  # בוטל
    if pwd != ADMIN_PASSWORD:
        messagebox.showerror("שגיאה", "סיסמה שגויה.")
        return

    open_recipients_editor()

def open_recipients_editor():
    """Admin panel: edit EMAIL_RECIPIENTS and SUBJECT_PRESETS."""
    editor = tk.Toplevel(root)
    editor.title("ניהול נמענים ונושאים")
    editor.geometry("450x400")
    editor.minsize(400, 350)

    frame = ttk.Frame(editor, padding=10)
    frame.pack(fill="both", expand=True)

    # ----- Recipients -----
    recipients_label = ttk.Label(frame, text="כתובות מייל (אחת בכל שורה):")
    recipients_label.pack(anchor="e", pady=(0, 5))

    recipients_text = tk.Text(frame, wrap="none", font=("Arial", 11), height=7)
    recipients_text.pack(fill="x", expand=False)
    recipients_text.insert("1.0", "\n".join(EMAIL_RECIPIENTS))

    # ----- Subject presets -----
    subjects_label = ttk.Label(frame, text="נושאים לבחירה (אחד בכל שורה):")
    subjects_label.pack(anchor="e", pady=(10, 5))

    subjects_text = tk.Text(frame, wrap="none", font=("Arial", 11), height=7)
    subjects_text.pack(fill="both", expand=True)
    subjects_text.insert("1.0", "\n".join(SUBJECT_PRESETS))

    def save_and_close():
        global EMAIL_RECIPIENTS, SUBJECT_PRESETS

        # נמענים
        data_recipients = recipients_text.get("1.0", tk.END)
        new_recipients = [
            line.strip()
            for line in data_recipients.splitlines()
            if line.strip()
        ]

        if not new_recipients:
            messagebox.showwarning("אזהרה", "חייב להיות לפחות נמען אחד.")
            return

        # נושאים
        data_subjects = subjects_text.get("1.0", tk.END)
        new_subjects = [
            line.strip()
            for line in data_subjects.splitlines()
            if line.strip()
        ]

        if not new_subjects:
            messagebox.showwarning("אזהרה", "חייב להיות לפחות נושא אחד.")
            return

        EMAIL_RECIPIENTS = new_recipients
        SUBJECT_PRESETS = new_subjects

        # עדכון הקומבו-בוקס של הנושאים
        subject_combo["values"] = SUBJECT_PRESETS

        print("עודכנו נמענים:", EMAIL_RECIPIENTS)
        print("עודכנו נושאים:", SUBJECT_PRESETS)

        messagebox.showinfo("נשמר", "רשימת הנמענים והנושאים עודכנה בהצלחה.")
        editor.destroy()

    buttons_frame = ttk.Frame(frame)
    buttons_frame.pack(fill="x", pady=5)

    save_btn = ttk.Button(buttons_frame, text="שמור", command=save_and_close)
    save_btn.pack(side="right", padx=(5, 0))

    close_btn = ttk.Button(buttons_frame, text="סגור", command=editor.destroy)
    close_btn.pack(side="right")


# יצירת חלון
root = tk.Tk()
root.title("טופס תלונות")
root.geometry("600x400")  # גודל בינוני
root.minsize(500, 350)

# קצת סטייל
root.configure(bg="#f1f4f6")

style = ttk.Style()
style.theme_use("clam")

style.configure("TLabel", font=("Arial", 11))
style.configure("TButton", padding=5, font=("Arial", 11))
style.configure("TCombobox", padding=3, font=("Arial", 11))

main_frame = ttk.Frame(root, padding=15)
main_frame.pack(fill="both", expand=True)

# שורה 0: כותרת עליונה
header_label = ttk.Label(
    main_frame,
    text="טופס תלונות",
    font=("Arial", 18, "bold"),
    anchor="center"
)
header_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

# שורה 1: תיבת נושא מהיר (קומבו-בוקס)
subject_label = ttk.Label(main_frame, text=":בחר נושא מהיר")
subject_label.grid(row=1, column=1, sticky="e", pady=(0, 5))

subject_combo = ttk.Combobox(main_frame, values=SUBJECT_PRESETS, state="readonly")
subject_combo.set("בחר נושא...")
subject_combo.grid(row=1, column=0, sticky="we", pady=(0, 5))
subject_combo.bind("<<ComboboxSelected>>", on_subject_selected)

# התאמת עמודות
main_frame.columnconfigure(0, weight=3)
main_frame.columnconfigure(1, weight=1)

# שורה 2: כותרת התלונה (label)
title_label = ttk.Label(main_frame, text=":כותרת התלונה")
title_label.grid(row=2, column=1, sticky="e", pady=(10, 2))

# שורה 3: תיבת כותרת (Entry ארוך וצר)
title_var = tk.StringVar()
title_entry = ttk.Entry(main_frame, textvariable=title_var, justify="right")
title_entry.grid(row=3, column=0, columnspan=2, sticky="we", pady=(0, 10))

# שורה 4: תיאור מפורט (label)
desc_label = ttk.Label(main_frame, text=":תיאור מפורט")
desc_label.grid(row=4, column=1, sticky="e", pady=(0, 2))

# שורה 5: תיבת טקסט גדולה לתיאור
desc_frame = ttk.Frame(main_frame)
desc_frame.grid(row=5, column=0, columnspan=2, sticky="nsew")

main_frame.rowconfigure(5, weight=1)

desc_text = tk.Text(
    desc_frame,
    wrap="word",
    font=("Arial", 11),
    height=8
)
desc_text.pack(fill="both", expand=True)

# קצת רקע לבן לטקסט
desc_text.configure(bg="#ffffff", relief="solid", bd=1)

# שורה 6: כפתורים (שלח / יציאה)
buttons_frame = ttk.Frame(main_frame)
buttons_frame.grid(row=6, column=0, columnspan=2, pady=10, sticky="e")

send_button = ttk.Button(buttons_frame, text="שלח", command=send_complaint)
send_button.pack(side="right", padx=(5, 0))


exit_button = ttk.Button(buttons_frame, text="יציאה", command=root.destroy)
exit_button.pack(side="right")

manage_button = ttk.Button(buttons_frame, text="ניהול", command=manage_recipients)
manage_button.pack(side="right", padx=(5, 0))
# התחלת התוכנית
root.mainloop()
