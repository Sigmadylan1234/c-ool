import tkinter as tk
from tkinter import messagebox
import json
import os

CONFIG_FILE = "rfid_config.json"
BOOKS_FILE = "books.json"

CARD_CLOSE = "card_close"
CARD_BOOKS = "card_books"

class RFIDApp:
    def __init__(self, master):
        self.master = master
        self.master.title("RFID Login")
        self.master.attributes('-fullscreen', True)
        self.master.protocol("WM_DELETE_WINDOW", lambda: None)
        self.master.configure(bg='green')

        self.rfid_cards = self.load_rfid_cards()

        if not self.rfid_cards:
            self.setup_rfid_screen()
        else:
            self.login_screen()

    def load_rfid_cards(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f).get("rfid_cards", [])
        return []

    def save_rfid_cards(self, cards):
        with open(CONFIG_FILE, 'w') as f:
            json.dump({"rfid_cards": cards}, f)

    def setup_rfid_screen(self):
        self.clear_screen()
        label = tk.Label(self.master, text="Scan your RFID cards to register (2 required)", font=("Arial", 24), bg='green')
        label.pack(pady=20)
        self.cards_scanned = []
        self.master.after(1000, self.fake_rfid_scan)

    def fake_rfid_scan(self):
        # Simulate scanning two cards
        if len(self.cards_scanned) == 0:
            self.cards_scanned.append(CARD_CLOSE)
            self.master.after(1000, self.fake_rfid_scan)
        elif len(self.cards_scanned) == 1:
            self.cards_scanned.append(CARD_BOOKS)
            self.rfid_cards = self.cards_scanned
            self.save_rfid_cards(self.rfid_cards)
            messagebox.showinfo("Setup", f"Cards {self.rfid_cards} registered!")
            self.login_screen()

    def login_screen(self):
        self.clear_screen()
        tk.Label(self.master, text="Enter password or scan RFID", font=("Arial", 24), bg='green').pack(pady=20)
        self.entry = tk.Entry(self.master, show="*", font=("Arial", 18))
        self.entry.pack(pady=10)
        self.entry.bind("<Return>", self.check_password)
        self.master.bind('<Escape>', self.close_program)
        tk.Label(self.master, text="[LOGO]", font=("Arial", 24), bg='green').pack(pady=20)

        # Simulate RFID scan after delay (for demonstration)
        self.master.after(3000, self.simulate_rfid_read, CARD_BOOKS)  # Change to CARD_CLOSE to test closing

    def simulate_rfid_read(self, scanned_card):
        if scanned_card in self.rfid_cards:
            if scanned_card == CARD_CLOSE:
                self.show_close_card_menu()
            elif scanned_card == CARD_BOOKS:
                self.launch_alternate_access()

    def show_close_card_menu(self):
        menu_win = tk.Toplevel(self.master)
        menu_win.title("Card Action Menu")
        menu_win.geometry("300x150")
        menu_win.configure(bg='green')
        menu_win.grab_set()  # Focus on this window

        tk.Label(menu_win, text="Choose an action:", font=("Arial", 14), bg='green').pack(pady=10)

        def close_app():
            menu_win.destroy()
            self.close_program()

        def open_books():
            menu_win.destroy()
            self.launch_alternate_access()

        btn_close = tk.Button(menu_win, text="Close Program", command=close_app, bg="red", fg="white", width=20)
        btn_close.pack(pady=5)

        btn_books = tk.Button(menu_win, text="Open Books", command=open_books, bg="darkgreen", fg="white", width=20)
        btn_books.pack(pady=5)

    def check_password(self, event=None):
        password = self.entry.get()
        if password == "The_super_commputer123@":
            self.close_program()
        elif password == "backupPass2025":
            messagebox.showinfo("Login", "Access Granted!")
        elif password == "devmode123":
            self.launch_developer_mode()
        elif password == "5526":
            self.launch_alternate_access()
        else:
            messagebox.showerror("Login", "Access Denied")

    def close_program(self, event=None):
        self.master.destroy()

    def clear_screen(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def launch_developer_mode(self):
        dev = tk.Toplevel(self.master)
        dev.title("Developer Mode")
        dev.geometry("300x200")
        tk.Label(dev, text="Developer Mode", font=("Arial", 16)).pack(pady=20)
        tk.Button(dev, text="Close Program", command=self.master.destroy).pack(pady=10)

    def launch_alternate_access(self):
        alt = tk.Toplevel(self.master)
        alt.title("Alternate Access")
        alt.geometry("500x400")
        alt.configure(bg='green')

        entries = []

        def add_entry_row(name="", code="", active=False):
            frame = tk.Frame(alt, bg='green')
            name_entry = tk.Entry(frame, width=15)
            code_entry = tk.Entry(frame, width=15)
            check_var = tk.BooleanVar(value=active)
            checkbox = tk.Checkbutton(frame, variable=check_var, bg='green')
            name_entry.insert(0, name)
            code_entry.insert(0, code)
            name_entry.pack(side=tk.LEFT, padx=5)
            code_entry.pack(side=tk.LEFT, padx=5)
            checkbox.pack(side=tk.LEFT)
            frame.pack(pady=5)
            entries.append((name_entry, code_entry, check_var))

        def save_entries():
            data = []
            for name, code, check in entries:
                data.append({
                    "name": name.get(),
                    "code": code.get(),
                    "active": check.get()
                })
            with open(BOOKS_FILE, 'w') as f:
                json.dump(data, f, indent=2)
            messagebox.showinfo("Saved", "Entries saved to books.json")

        tk.Label(alt, text="Alternate Access - Add Users", font=("Arial", 14), bg='green').pack(pady=10)

        if os.path.exists(BOOKS_FILE):
            try:
                with open(BOOKS_FILE, 'r') as f:
                    saved_entries = json.load(f)
                for item in saved_entries:
                    add_entry_row(item.get("name", ""), item.get("code", ""), item.get("active", False))
            except:
                messagebox.showerror("Error", "Failed to load books.json.")
        else:
            for _ in range(3):
                add_entry_row()

        tk.Button(alt, text="Add More", command=add_entry_row, bg="lightgray").pack(pady=5)
        tk.Button(alt, text="Save", command=save_entries, bg="darkgreen", fg="white").pack(pady=5)
        tk.Button(alt, text="❌ Close", command=alt.destroy, bg="red", fg="white").pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = RFIDApp(root)
    root.mainloop()
