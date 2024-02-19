import tkinter as tk
from tkinter import messagebox
import sqlite3
import os
import random
import string

# Create a SQLite database to store notes and passwords
conn = sqlite3.connect('manager.db')
c = conn.cursor()

# Create table for notes if not exists
c.execute('''CREATE TABLE IF NOT EXISTS notes
             (id INTEGER PRIMARY KEY, title TEXT, date TEXT, note TEXT)''')

# Create table for passwords if not exists
c.execute('''CREATE TABLE IF NOT EXISTS passwords
             (id INTEGER PRIMARY KEY, username TEXT, website TEXT, password TEXT)''')

class AuthenticationPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("300x200")
        self.root.config(bg="cyan")

        self.username_label = tk.Label(root, text="Username:", font=("Verdana", 12), bg="cyan")
        self.username_label.pack()
        self.username_entry = tk.Entry(root, font=("Verdana", 12))
        self.username_entry.pack()

        self.password_label = tk.Label(root, text="Password:", font=("Verdana", 12), bg="cyan")
        self.password_label.pack()
        self.password_entry = tk.Entry(root, show="*", font=("Verdana", 12))
        self.password_entry.pack()

        self.login_button = tk.Button(root, text="Login", command=self.login, font=("Verdana", 12))
        self.login_button.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check credentials (for demo purposes, a hardcoded username and password are used)
        if username == "admin" and password == "password":
            self.root.destroy()
            root = tk.Tk()
            root.geometry("500x400")
            root.config(bg="cyan")
            root.title("Notes and Password Manager")

            def open_notes_manager():
                root.destroy()
                notes_manager_window = tk.Tk()
                notes_manager_window.geometry("500x400")
                notes_manager_window.config(bg="cyan")
                notes_manager_window.title("Notes Manager")
                notes_manager = NotesManager(notes_manager_window)
                notes_manager_window.mainloop()

            def open_password_manager():
                root.destroy()
                password_manager_window = tk.Tk()
                password_manager_window.geometry("500x400")
                password_manager_window.config(bg="cyan")
                password_manager_window.title("Password Manager")
                password_manager = PasswordManager(password_manager_window)
                password_manager_window.mainloop()

            notes_manager_button = tk.Button(root, text="Notes Manager", command=open_notes_manager, font=("Verdana", 12))
            notes_manager_button.pack(pady=20)

            password_manager_button = tk.Button(root, text="Password Manager", command=open_password_manager, font=("Verdana", 12))
            password_manager_button.pack(pady=20)

            root.mainloop()
        else:
            messagebox.showerror("Error", "Invalid username or password")

class NotesManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Notes Manager")
        self.root.config(bg="cyan")

        self.notes_title_label = tk.Label(root, text="Title:", font=("Verdana", 12), bg="cyan")
        self.notes_title_label.pack()
        self.notes_title_entry = tk.Entry(root, font=("Verdana", 12))
        self.notes_title_entry.pack()

        self.notes_date_label = tk.Label(root, text="Date:", font=("Verdana", 12), bg="cyan")
        self.notes_date_label.pack()
        self.notes_date_entry = tk.Entry(root, font=("Verdana", 12))
        self.notes_date_entry.pack()

        self.notes_text_label = tk.Label(root, text="Notes:", font=("Verdana", 12), bg="cyan")
        self.notes_text_label.pack()
        self.notes_text = tk.Text(root, font=("Verdana", 12), height=10)
        self.notes_text.pack()

        self.save_button = tk.Button(root, text="Save", font=("Verdana", 12), command=self.save_notes)
        self.save_button.pack(pady=20)

        self.delete_notes_button = tk.Button(root, text="Delete Note", font=("Verdana", 12), command=self.delete_note)
        self.delete_notes_button.pack(pady=20)

        self.back_button = tk.Button(root, text="Back", font=("Verdana", 12), command=self.back)
        self.back_button.pack(pady=20)

        self.logout_button = tk.Button(root, text="Log Out", font=("Verdana", 12), command=self.logout)
        self.logout_button.pack(pady=20)

        self.load_notes()

    def save_notes(self):
        title = self.notes_title_entry.get()
        date = self.notes_date_entry.get()
        note = self.notes_text.get("1.0", tk.END)

        # Insert note into database
        c.execute("INSERT INTO notes (title, date, note) VALUES (?, ?, ?)", (title, date, note))
        conn.commit()

        messagebox.showinfo("Success", "Note saved successfully!")

    def load_notes(self):
        # Fetch all notes from database
        c.execute("SELECT * FROM notes")
        notes = c.fetchall()

        for note in notes:
            title, date, note_text = note[1], note[2], note[3]
            self.notes_text.insert(tk.END, f"Title: {title}\nDate: {date}\n{note_text}\n\n")

    def delete_note(self):
        title = self.notes_title_entry.get()
        c.execute("DELETE FROM notes WHERE title=?", (title,))
        conn.commit()
        messagebox.showinfo("Success", "Note deleted successfully!")
        self.notes_text.delete(1.0, tk.END)

    def back(self):
        self.root.destroy()
        root = tk.Tk()
        root.geometry("500x400")
        root.config(bg="cyan")
        root.title("Notes and Password Manager")

        def open_notes_manager():
            root.destroy()
            notes_manager_window = tk.Tk()
            notes_manager_window.geometry("500x400")
            notes_manager_window.config(bg="cyan")
            notes_manager_window.title("Notes Manager")
            notes_manager = NotesManager(notes_manager_window)
            notes_manager_window.mainloop()

        def open_password_manager():
            root.destroy()
            password_manager_window = tk.Tk()
            password_manager_window.geometry("500x400")
            password_manager_window.config(bg="cyan")
            password_manager_window.title("Password Manager")
            password_manager = PasswordManager(password_manager_window)
            password_manager_window.mainloop()

        notes_manager_button = tk.Button(root, text="Notes Manager", command=open_notes_manager, font=("Verdana", 12))
        notes_manager_button.pack(pady=20)

        password_manager_button = tk.Button(root, text="Password Manager", command=open_password_manager, font=("Verdana", 12))
        password_manager_button.pack(pady=20)

        root.mainloop()

    def logout(self):
        conn.close()
        self.root.destroy()
        AuthenticationPage(tk.Tk())

class PasswordManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Manager")
        self.root.config(bg="cyan")

        self.username_label = tk.Label(root, text="Username:", font=("Verdana", 12), bg="cyan")
        self.username_label.pack()
        self.username_entry = tk.Entry(root, font=("Verdana", 12))
        self.username_entry.pack()

        self.website_label = tk.Label(root, text="Website:", font=("Verdana", 12), bg="cyan")
        self.website_label.pack()
        self.website_entry = tk.Entry(root, font=("Verdana", 12))
        self.website_entry.pack()

        self.password_label = tk.Label(root, text="Password:", font=("Verdana", 12), bg="cyan")
        self.password_label.pack()
        self.password_entry = tk.Entry(root, show="*", font=("Verdana", 12))
        self.password_entry.pack()

        self.password_strength_label = tk.Label(root, text="", font=("Verdana", 12), bg="cyan")
        self.password_strength_label.pack()

        self.password_entry.bind("<KeyRelease>", self.check_strength)

        self.save_button = tk.Button(root, text="Save", font=("Verdana", 12), command=self.save_password)
        self.save_button.pack(pady=20)

        self.delete_password_button = tk.Button(root, text="Delete Password", font=("Verdana", 12), command=self.delete_password)
        self.delete_password_button.pack(pady=20)

        self.back_button = tk.Button(root, text="Back", font=("Verdana", 12), command=self.back)
        self.back_button.pack(pady=20)

        self.logout_button = tk.Button(root, text="Log Out", font=("Verdana", 12), command=self.logout)
        self.logout_button.pack(pady=20)

    def check_strength(self, event):
        password = self.password_entry.get()
        strength = "Weak" if len(password) < 8 else "Strong"
        self.password_strength_label.config(text="Password Strength: " + strength)

    def save_password(self):
        username = self.username_entry.get()
        website = self.website_entry.get()
        password = self.password_entry.get()

        # Insert password into database
        c.execute("INSERT INTO passwords (username, website, password) VALUES (?, ?, ?)", (username, website, password))
        conn.commit()

        messagebox.showinfo("Success", "Password saved successfully!")

    def delete_password(self):
        website = self.website_entry.get()
        c.execute("DELETE FROM passwords WHERE website=?", (website,))
        conn.commit()
        messagebox.showinfo("Success", "Password deleted successfully!")
        self.username_entry.delete(0, tk.END)
        self.website_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

    def back(self):
        self.root.destroy()
        root = tk.Tk()
        root.geometry("500x400")
        root.config(bg="cyan")
        root.title("Notes and Password Manager")

        def open_notes_manager():
            root.destroy()
            notes_manager_window = tk.Tk()
            notes_manager_window.geometry("500x400")
            notes_manager_window.config(bg="cyan")
            notes_manager_window.title("Notes Manager")
            notes_manager = NotesManager(notes_manager_window)
            notes_manager_window.mainloop()

        def open_password_manager():
            root.destroy()
            password_manager_window = tk.Tk()
            password_manager_window.geometry("500x400")
            password_manager_window.config(bg="cyan")
            password_manager_window.title("Password Manager")
            password_manager = PasswordManager(password_manager_window)
            password_manager_window.mainloop()

        notes_manager_button = tk.Button(root, text="Notes Manager", command=open_notes_manager, font=("Verdana", 12))
        notes_manager_button.pack(pady=20)

        password_manager_button = tk.Button(root, text="Password Manager", command=open_password_manager, font=("Verdana", 12))
        password_manager_button.pack(pady=20)

        root.mainloop()

    def logout(self):
        conn.close()
        self.root.destroy()
        AuthenticationPage(tk.Tk())

root = tk.Tk()
auth_page = AuthenticationPage(root)
root.mainloop()

# Close the database connection
conn.close()
