import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

import ttkbootstrap as tb
from ttkbootstrap.constants import *

from email_outlook import send_outlook_email

from shared_config import save_shared_config, hash_password
from registry_store import save_to_registry

def run_app(state: dict, admin_password: str):
    """
    state = {
      "subjects": list[str],
      "recipients": list[str]
    }
    """
    def make_chip(parent, text):
        return tk.Label(
            parent,
            text=text,
            font=("Segoe UI", 10, "bold"),
            bg="#ffffff",
            fg="#4b5563"       # muted gray, modern
        )
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
            title_var.set("")
            desc_text.delete("1.0", tk.END)
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
        if hash_password(pwd) != state["admin_password_hash"]:
            messagebox.showerror("שגיאה", "סיסמה שגויה.")
            return
        open_admin_panel()

    def change_admin_password():
        current = simpledialog.askstring("שינוי סיסמה", "הכנס סיסמה נוכחית:", show="*")
        if current is None:
            return
        if hash_password(current) != state["admin_password_hash"]:
            messagebox.showerror("שגיאה", "סיסמה נוכחית שגויה.")
            return

        new1 = simpledialog.askstring("שינוי סיסמה", "הכנס סיסמה חדשה:", show="*")
        if new1 is None:
            return
        new1 = new1.strip()
        if len(new1) < 4:
            messagebox.showwarning("אזהרה", "סיסמה חייבת להיות לפחות 4 תווים.")
            return

        new2 = simpledialog.askstring("שינוי סיסמה", "אשר סיסמה חדשה:", show="*")
        if new2 is None:
            return
        if new1 != new2:
            messagebox.showerror("שגיאה", "הסיסמאות לא תואמות.")
            return

        # update in-memory hash
        state["admin_password_hash"] = hash_password(new1)

        # publish to shared config (source of truth)
        ok = save_shared_config(state["recipients"], state["subjects"], state["admin_password_hash"])
        if not ok:
            messagebox.showwarning(
                "אזהרה",
                "לא הצלחתי לשמור לדרייב המשותף.\nהסיסמה עודכנה רק במחשב הזה עד שתהיה גישה לדרייב."
            )
            # optional: if you have registry caching, also save there here

        messagebox.showinfo("נשמר", "הסיסמה עודכנה בהצלחה.")

    def open_admin_panel():
        editor = tk.Toplevel(root)
        editor.title("ניהול נמענים ונושאים")
        editor.geometry("550x500")
        editor.minsize(400, 350)

        frame = tb.Frame(editor, padding=10)
        frame.pack(fill="both", expand=True)

        # Recipients
        recipients_label = make_chip(frame,text="כתובות מייל (אחת בכל שורה):")
        recipients_label.pack(anchor="e", pady=(0, 5))

        recipients_text = tk.Text(frame, wrap="none", font=("Segoe UI", 11), height=7)
        recipients_text.pack(fill="x", expand=False)
        recipients_text.insert("1.0", "\n".join(state["recipients"]))

        # Subjects
        subjects_label = make_chip(frame,text="נושאים לבחירה (אחד בכל שורה):")
        subjects_label.pack(anchor="e", pady=(10, 5))

        subjects_text = tk.Text(frame, wrap="none", font=("Segoe UI", 11), height=7)
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

            # save to shared drive first
            ok = save_shared_config(
                state["recipients"],
                state["subjects"],
                state["admin_password_hash"]
            )
            if not ok:
                messagebox.showwarning(
                    "אזהרה",
                    "לא הצלחתי לשמור לדרייב המשותף.\nההגדרות נשמרו מקומית בלבד."
                )

            # always cache locally
            save_to_registry(state["recipients"], state["subjects"])

            messagebox.showinfo("נשמר", "הרשימות עודכנו בהצלחה.")
            editor.destroy()

        buttons_frame = tb.Frame(frame)
        buttons_frame.pack(fill="x", pady=5)

        tb.Button(buttons_frame, text="שמור", command=save_and_close).pack(side="right", padx=(5, 0))
        tb.Button(buttons_frame, text="סגור", command=editor.destroy).pack(side="right", padx=(5, 0))
        tb.Button(buttons_frame, text="שנה סיסמה", command=change_admin_password).pack(side="right", padx=(5, 0))

    # -------- UI --------
    root = tb.Window(themename="flatly") 
    root.title("טופס פנייה לתמיכה")
    root.geometry("600x400")
    root.minsize(500, 350)
    root.configure(bg="#eef1f5")

    style = ttk.Style(root)

    style.configure(
        "White.TCombobox",
        fieldbackground="#ffffff",
        background="#ffffff"
    )

    card = tk.Frame(root, bg="#000000")
    card.pack(fill="both", expand=True, padx=18, pady=18)
    card.configure(highlightthickness=1, highlightbackground="#000000")
    card.columnconfigure(0, weight=3)
    card.rowconfigure(5, weight=1)

    header_bar = tk.Frame(card, bg="#f6f8fa")  # subtle tint
    header_bar.grid(row=0, column=0, columnspan=2, sticky="we", pady=(0, 12))
    header_bar.configure(highlightthickness=1, highlightbackground="#d0d7de")  # subtle border

    header_label = tk.Label(
        header_bar,
        text="טופס פנייה לתמיכה",
        font=("Segoe UI", 18, "bold"),
        bg="#f6f8fa",
        fg="#111827",
        anchor="center"
    )
    header_label.pack(fill="x", padx=12, pady=10)

    #header_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

    subject_label = make_chip(card, text=":בחר נושא מהיר")
    subject_label.grid(row=1, column=1, sticky="e", pady=(0, 5))


    subject_combo = tb.Combobox(
    card,
    values=state["subjects"],
    state="readonly",
    bootstyle="light",
    style="White.TCombobox"
    )
    subject_combo.set("בחר נושא...")
    subject_combo.grid(row=1, column=0, sticky="we", pady=(0, 5))
    subject_combo.bind("<<ComboboxSelected>>", on_subject_selected)

    card.columnconfigure(0, weight=3)
    card.columnconfigure(1, weight=1)

    title_label = make_chip(card, text=":כותרת הפנייה")
    title_label.grid(row=2, column=1, sticky="e", pady=(10, 2))

    title_var = tk.StringVar()
    title_entry = tb.Entry(card, textvariable=title_var, justify="right", bootstyle="light")
    title_entry.grid(row=3, column=0, columnspan=2, sticky="we", pady=(0, 10))

    desc_label = make_chip(card,text=":תיאור מפורט")
    desc_label.grid(row=4, column=1, sticky="e", pady=(0, 2))

    desc_frame = tb.Frame(card)
    desc_frame.grid(row=5, column=0, columnspan=2, sticky="nsew")
    card.rowconfigure(5, weight=1)

    FONT = ("Segoe UI", 11)
    MONO = ("Consolas", 11)  # optional for admin multiline lists

    desc_text = tk.Text(
        desc_frame,
        wrap="word",
        font=FONT,
        height=8,
        bd=0,
        highlightthickness=1,
        highlightbackground="#d0d7de",
        highlightcolor="#2f6fed",
        padx=12,
        pady=10
    )
    desc_text.pack(fill="both", expand=True)
    desc_text.configure(bg="#ffffff", relief="solid", bd=1)

    buttons_frame = tb.Frame(card)
    buttons_frame.grid(row=6, column=0, columnspan=2, pady=10, sticky="e")

    tb.Button(buttons_frame, text="שלח", command=send_request, bootstyle=SUCCESS ).pack(side="right", padx=(5, 0))
    tb.Button(buttons_frame, text="ניהול", command=manage_admin, bootstyle=SECONDARY).pack(side="right", padx=(5, 0))
    tb.Button(buttons_frame, text="יציאה", command=root.destroy, bootstyle=DANGER).pack(side="right")

    root.mainloop()
