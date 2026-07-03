import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

CONTACTS_FILE = "contacts.json"
contacts = {}


# ============ توابع مدیریت فایل ============
def load_contacts():
    global contacts
    if os.path.exists(CONTACTS_FILE):
        try:
            with open(CONTACTS_FILE, 'r', encoding='utf-8') as file:
                contacts = json.load(file)
        except:
            contacts = {}
    else:
        contacts = {}


def save_contacts():
    try:
        with open(CONTACTS_FILE, 'w', encoding='utf-8') as file:
            json.dump(contacts, file, ensure_ascii=False, indent=2)
        return True
    except:
        return False


# ============ کلاس برنامه اصلی ============
class ContactApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📒 دفترچه مخاطبین - مدیریت حرفه‌ای")
        self.root.geometry("700x500")
        self.root.resizable(True, True)

        # بارگذاری اطلاعات
        load_contacts()

        # طراحی رابط
        self.create_widgets()
        self.refresh_table()

        # ✅ رویداد بستن با پیغام ذخیره‌سازی
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        """وقتی کاربر دکمه‌ی بستن (X) رو می‌زنه، پیغام ذخیره‌سازی نمایش داده میشه"""
        if save_contacts():
            messagebox.showinfo("موفقیت", "✅ مخاطب‌ها با موفقیت ذخیره شدند!")
            self.root.destroy()
        else:
            messagebox.showerror("خطا", "❌ خطا در ذخیره‌سازی مخاطب‌ها!")
            # حتی با خطا هم پنجره رو می‌بندیم (اختیاری)
            self.root.destroy()

    def create_widgets(self):
        # ===== فریم بالا (جستجو) =====
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10, padx=10, fill=tk.X)

        tk.Label(top_frame, text="جستجو:", font=("Arial", 11)).pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(top_frame, width=30, font=("Arial", 11))
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind("<KeyRelease>", self.search_contacts)

        # ===== جدول نمایش مخاطب‌ها =====
        self.tree = ttk.Treeview(self.root, columns=("name", "phone", "email"), show="headings", height=12)
        self.tree.heading("name", text="نام")
        self.tree.heading("phone", text="شماره تلفن")
        self.tree.heading("email", text="ایمیل")

        self.tree.column("name", width=150, anchor="center")
        self.tree.column("phone", width=150, anchor="center")
        self.tree.column("email", width=200, anchor="center")

        self.tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # دابل کلیک برای ویرایش
        self.tree.bind("<Double-1>", lambda event: self.edit_contact())

        # ===== فریم دکمه‌ها =====
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="➕ اضافه کردن", command=self.add_contact,
                  bg="#4CAF50", fg="white", font=("Arial", 10), width=15).pack(side=tk.LEFT, padx=5)

        tk.Button(btn_frame, text="✏️ ویرایش", command=self.edit_contact,
                  bg="#FF9800", fg="white", font=("Arial", 10), width=15).pack(side=tk.LEFT, padx=5)

        tk.Button(btn_frame, text="🗑️ حذف", command=self.delete_contact,
                  bg="#f44336", fg="white", font=("Arial", 10), width=15).pack(side=tk.LEFT, padx=5)

        tk.Button(btn_frame, text="🔄 تازه‌سازی", command=self.refresh_table,
                  bg="#2196F3", fg="white", font=("Arial", 10), width=15).pack(side=tk.LEFT, padx=5)

        # ===== برچسب تعداد مخاطب‌ها =====
        self.count_label = tk.Label(self.root, text="", font=("Arial", 10, "italic"))
        self.count_label.pack(pady=5)

    # ============ نمایش اطلاعات در جدول ============
    def refresh_table(self, search_text=""):
        # پاک کردن جدول
        for item in self.tree.get_children():
            self.tree.delete(item)

        # فیلتر کردن بر اساس جستجو
        filtered_contacts = {}
        if search_text.strip() == "":
            filtered_contacts = contacts
        else:
            for phone, info in contacts.items():
                if search_text.lower() in info['name'].lower() or search_text in phone:
                    filtered_contacts[phone] = info

        # مرتب‌سازی بر اساس اسم
        sorted_contacts = sorted(filtered_contacts.items(), key=lambda x: x[1]['name'].lower())

        # نمایش در جدول
        for phone, info in sorted_contacts:
            self.tree.insert("", "end", values=(info['name'], phone, info['email']))

        # به‌روزرسانی تعداد
        self.count_label.config(text=f"تعداد مخاطب‌ها: {len(filtered_contacts)} نفر")

    # ============ جستجوی لحظه‌ای ============
    def search_contacts(self, event):
        search_text = self.search_entry.get()
        self.refresh_table(search_text)

    # ============ اضافه کردن مخاطب ============
    def add_contact(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("➕ اضافه کردن مخاطب جدید")
        add_window.geometry("350x250")
        add_window.resizable(False, False)

        tk.Label(add_window, text="نام:", font=("Arial", 11)).pack(pady=10)
        name_entry = tk.Entry(add_window, width=30, font=("Arial", 11))
        name_entry.pack(pady=5)

        tk.Label(add_window, text="شماره تلفن:", font=("Arial", 11)).pack(pady=5)
        phone_entry = tk.Entry(add_window, width=30, font=("Arial", 11))
        phone_entry.pack(pady=5)

        tk.Label(add_window, text="ایمیل:", font=("Arial", 11)).pack(pady=5)
        email_entry = tk.Entry(add_window, width=30, font=("Arial", 11))
        email_entry.pack(pady=5)

        def save_new():
            name = name_entry.get().strip()
            phone = phone_entry.get().strip()
            email = email_entry.get().strip()

            if name == "" or phone == "" or email == "":
                messagebox.showerror("خطا", "همه فیلدها اجباری هستند!")
                return

            if phone in contacts:
                messagebox.showerror("خطا", f"شماره {phone} قبلاً ثبت شده است!")
                return

            contacts[phone] = {"name": name, "email": email}
            if save_contacts():
                messagebox.showinfo("موفقیت", "✅ مخاطب با موفقیت اضافه شد!")
                add_window.destroy()
                self.refresh_table()
            else:
                messagebox.showerror("خطا", "❌ خطا در ذخیره‌سازی!")

        tk.Button(add_window, text="💾 ذخیره", command=save_new,
                  bg="#4CAF50", fg="white", font=("Arial", 11), width=15).pack(pady=20)

    # ============ ویرایش مخاطب ============
    def edit_contact(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("هشدار", "لطفاً یک مخاطب را انتخاب کنید!")
            return

        values = self.tree.item(selected[0], "values")
        old_phone = values[1]
        info = contacts[old_phone]

        edit_window = tk.Toplevel(self.root)
        edit_window.title("✏️ ویرایش مخاطب")
        edit_window.geometry("350x280")
        edit_window.resizable(False, False)

        tk.Label(edit_window, text=f"شماره: {old_phone} (غیرقابل تغییر)",
                 font=("Arial", 10, "bold"), fg="blue").pack(pady=10)

        tk.Label(edit_window, text="نام:", font=("Arial", 11)).pack(pady=5)
        name_entry = tk.Entry(edit_window, width=30, font=("Arial", 11))
        name_entry.insert(0, info['name'])
        name_entry.pack(pady=5)

        tk.Label(edit_window, text="ایمیل:", font=("Arial", 11)).pack(pady=5)
        email_entry = tk.Entry(edit_window, width=30, font=("Arial", 11))
        email_entry.insert(0, info['email'])
        email_entry.pack(pady=5)

        def save_edit():
            new_name = name_entry.get().strip()
            new_email = email_entry.get().strip()

            if new_name == "" or new_email == "":
                messagebox.showerror("خطا", "نام و ایمیل اجباری هستند!")
                return

            contacts[old_phone]['name'] = new_name
            contacts[old_phone]['email'] = new_email

            if save_contacts():
                messagebox.showinfo("موفقیت", "✅ مخاطب ویرایش شد!")
                edit_window.destroy()
                self.refresh_table()
            else:
                messagebox.showerror("خطا", "❌ خطا در ذخیره‌سازی!")

        tk.Button(edit_window, text="💾 ذخیره تغییرات", command=save_edit,
                  bg="#FF9800", fg="white", font=("Arial", 11), width=18).pack(pady=20)

    # ============ حذف مخاطب ============
    def delete_contact(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("هشدار", "لطفاً یک مخاطب را انتخاب کنید!")
            return

        values = self.tree.item(selected[0], "values")
        phone = values[1]
        name = values[0]

        confirm = messagebox.askyesno("تأیید حذف", f"آیا از حذف '{name}' مطمئنی؟")
        if confirm:
            del contacts[phone]
            if save_contacts():
                messagebox.showinfo("موفقیت", "✅ مخاطب حذف شد!")
                self.refresh_table()
            else:
                messagebox.showerror("خطا", "❌ خطا در ذخیره‌سازی!")


# ============ اجرای برنامه ============
if __name__ == "__main__":
    root = tk.Tk()
    app = ContactApp(root)
    root.mainloop()