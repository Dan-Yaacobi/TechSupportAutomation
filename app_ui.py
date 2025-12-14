import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from email_outlook import send_outlook_email
from registry_store import save_to_registry

def run_app(state: dict, admin_password: str):
    """
    state = {
      "subjects": list[str],
      "recipients": list[str]
    }
    """

    def send_request():
        title = title_var.get().strip()
        description = desc_text.get("1.0", tk.END).strip()

        if not title:
            messagebox.showwarning("חסר מידע", "אנא מלא כותרת לפנייה.")
            return

        if not description:
            messagebox.showwarning("חסר מידע", "אנא מלא תיאור לפנייה.")
            return

        ok = send_outlook_email(title, description, state["recipients"])
        if ok:
            messagebox.showinfo("נשלח", "הפנייה נשלחה בהצלחה.")
        else:
            messagebox.showerror("שגיאה", "שליחת המייל נכשלה. בדוק את Outlook/הרשאות.")

    def on_subject_selected(event):
        selected = subject_combo.get()
        if selected:
            title_var.set(selected)

    def manage_admin():
        pwd = simpledialog.askstring("סיסמה", "אנא הכנס סיסמה:", show="*")
        if pwd is None:
            return
        if pwd != admin_password:
            messagebox.showerror("שגיאה", "סיסמה שגויה.")
            return
        open_admin_panel()

    def open_admin_panel():
        editor = tk.Toplevel(root)
        editor.title("ניהול נמענים ונושאים")
        editor.geometry("450x400")
        editor.minsize(400, 350)

        frame = ttk.Frame(editor, padding=10)
        frame.pack(fill="both", expand=True)

        # Recipients
        recipients_label = ttk.Label(frame, text="כתובות מייל (אחת בכל שורה):")
        recipients_label.pack(anchor="e", pady=(0, 5))

        recipients_text = tk.Text(frame, wrap="none", font=("Arial", 11), height=7)
        recipients_text.pack(fill="x", expand=False)
        recipients_text.insert("1.0", "\n".join(state["recipients"]))

        # Subjects
        subjects_label = ttk.Label(frame, text="נושאים לבחירה (אחד בכל שורה):")
        subjects_label.pack(anchor="e", pady=(10, 5))

        subjects_text = tk.Text(frame, wrap="none", font=("Arial", 11), height=7)
        subjects_text.pack(fill="both", expand=True)
        subjects_text.insert("1.0", "\n".join(state["subjects"]))

        def save_and_close():
            new_recipients = [ln.strip() for ln in recipients_text.get("1.0", tk.END).splitlines() if ln.strip()]
            if not new_recipients:
                messagebox.showwarning("אזהרה", "חייב להיות לפחות נמען אחד.")
                return

            new_subjects = [ln.strip() for ln in subjects_text.get("1.0", tk.END).splitlines() if ln.strip()]
            if not new_subjects:
                messagebox.showwarning("אזהרה", "חייב להיות לפחות נושא אחד.")
                return

            state["recipients"] = new_recipients
            state["subjects"] = new_subjects
            subject_combo["values"] = state["subjects"]

            save_to_registry(state["recipients"], state["subjects"])

            messagebox.showinfo("נשמר", "הרשימות עודכנו בהצלחה.")
            editor.destroy()

        buttons_frame = ttk.Frame(frame)
        buttons_frame.pack(fill="x", pady=5)

        ttk.Button(buttons_frame, text="שמור", command=save_and_close).pack(side="right", padx=(5, 0))
        ttk.Button(buttons_frame, text="סגור", command=editor.destroy).pack(side="right")

    # -------- UI --------
    root = tk.Tk()
    root.title("טופס פנייה לתמיכה")
    root.geometry("600x400")
    root.minsize(500, 350)
    root.configure(bg="#f1f4f6")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TLabel", font=("Arial", 11))
    style.configure("TButton", padding=5, font=("Arial", 11))
    style.configure("TCombobox", padding=3, font=("Arial", 11))

    main_frame = ttk.Frame(root, padding=15)
    main_frame.pack(fill="both", expand=True)

    header_label = ttk.Label(
        main_frame,
        text="טופס פנייה לתמיכה",
        font=("Arial", 18, "bold"),
        anchor="center"
    )
    header_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

    subject_label = ttk.Label(main_frame, text=":בחר נושא מהיר")
    subject_label.grid(row=1, column=1, sticky="e", pady=(0, 5))

    subject_combo = ttk.Combobox(main_frame, values=state["subjects"], state="readonly")
    subject_combo.set("בחר נושא...")
    subject_combo.grid(row=1, column=0, sticky="we", pady=(0, 5))
    subject_combo.bind("<<ComboboxSelected>>", on_subject_selected)

    main_frame.columnconfigure(0, weight=3)
    main_frame.columnconfigure(1, weight=1)

    title_label = ttk.Label(main_frame, text=":כותרת הפנייה")
    title_label.grid(row=2, column=1, sticky="e", pady=(10, 2))

    title_var = tk.StringVar()
    title_entry = ttk.Entry(main_frame, textvariable=title_var, justify="right")
    title_entry.grid(row=3, column=0, columnspan=2, sticky="we", pady=(0, 10))

    desc_label = ttk.Label(main_frame, text=":תיאור מפורט")
    desc_label.grid(row=4, column=1, sticky="e", pady=(0, 2))

    desc_frame = ttk.Frame(main_frame)
    desc_frame.grid(row=5, column=0, columnspan=2, sticky="nsew")
    main_frame.rowconfigure(5, weight=1)

    desc_text = tk.Text(desc_frame, wrap="word", font=("Arial", 11), height=8)
    desc_text.pack(fill="both", expand=True)
    desc_text.configure(bg="#ffffff", relief="solid", bd=1)

    buttons_frame = ttk.Frame(main_frame)
    buttons_frame.grid(row=6, column=0, columnspan=2, pady=10, sticky="e")

    ttk.Button(buttons_frame, text="שלח", command=send_request).pack(side="right", padx=(5, 0))
    ttk.Button(buttons_frame, text="ניהול", command=manage_admin).pack(side="right", padx=(5, 0))
    ttk.Button(buttons_frame, text="יציאה", command=root.destroy).pack(side="right")

    root.mainloop()
