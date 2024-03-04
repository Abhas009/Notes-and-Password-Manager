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

        self.signup_button = tk.Button(root, text="Sign Up", command=self.signup, font=("Verdana", 12))
        self.signup_button.pack()

        self.forgot_password_button = tk.Button(root, text="Forgot Password", command=self.forgot_password, font=("Verdana", 12))
        self.forgot_password_button.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check credentials
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        if user:
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
                notes_manager = NotesManager(notes_manager_window, username)
                notes_manager_window.mainloop()

            def open_password_manager():
                root.destroy()
                password_manager_window = tk.Tk()
                password_manager_window.geometry("500x400")
                password_manager_window.config(bg="cyan")
                password_manager_window.title("Password Manager")
                password_manager = PasswordManager(password_manager_window, username)
                password_manager_window.mainloop()

            notes_manager_button = tk.Button(root, text="Notes Manager", command=open_notes_manager, font=("Verdana", 12))
            notes_manager_button.pack(pady=20)

            password_manager_button = tk.Button(root, text="Password Manager", command=open_password_manager, font=("Verdana", 12))
            password_manager_button.pack(pady=20)

            root.mainloop()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def signup(self):
        signup_window = tk.Tk()
        signup_window.title("Sign Up")
        signup_window.geometry("300x200")

        username_label = tk.Label(signup_window, text="Username:")
        username_label.pack()
        username_entry = tk.Entry(signup_window)
        username_entry.pack()

        password_label = tk.Label(signup_window, text="Password:")
        password_label.pack()
        password_entry = tk.Entry(signup_window, show="*")
        password_entry.pack()

        def create_account():
            username = username_entry.get()
            password = password_entry.get()
            # Check if username already exists in the database
            c.execute("SELECT * FROM users WHERE username=?", (username,))
            existing_user = c.fetchone()
            if existing_user:
                messagebox.showerror("Error", "Username already exists")
            else:
                # Insert new user into the database
                c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
                messagebox.showinfo("Success", "Account created successfully")
                signup_window.destroy()

        signup_button = tk.Button(signup_window, text="Sign Up", command=create_account)
        signup_button.pack()

        signup_window.mainloop()

    def forgot_password(self):
        forgot_password_window = tk.Tk()
        forgot_password_window.title("Forgot Password")
        forgot_password_window.geometry("300x200")

        username_label = tk.Label(forgot_password_window, text="Enter Username:")
        username_label.pack()
        username_entry = tk.Entry(forgot_password_window)
        username_entry.pack()

        def reset_password():
            username = username_entry.get()
            # Check if username exists in the database
            c.execute("SELECT * FROM users WHERE username=?", (username,))
            existing_user = c.fetchone()
            if existing_user:
                # Generate a new password (you might want to improve this logic)
                new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
                # Update the password in the database
                c.execute("UPDATE users SET password=? WHERE username=?", (new_password, username))
                conn.commit()
                messagebox.showinfo("Password Reset", f"Your new password is: {new_password}")
                forgot_password_window.destroy()
            else:
                messagebox.showerror("Error", "Username not found")

        reset_button = tk.Button(forgot_password_window, text="Reset Password", command=reset_password)
        reset_button.pack()

        forgot_password_window.mainloop()

class NotesManager:
    def __init__(self, root, username):
        self.root = root
        self.root.title("Notes Manager")
        self.root.config(bg="cyan")

        self.username = username

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

        self.view_notes_button = tk.Button(root, text="View Notes", font=("Verdana", 12), command=self.view_notes)
        self.view_notes_button.pack(pady=20)

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

    def view_notes(self):
        view_notes_window = tk.Tk()
        view_notes_window.title("View Notes")
        view_notes_window.geometry("500x400")
        view_notes_window.config(bg="cyan")

        c.execute("SELECT * FROM notes")
        notes = c.fetchall()

        for note in notes:
            title, date, note_text = note[1], note[2], note[3]
            note_label = tk.Label(view_notes_window, text=f"Title: {title}\nDate: {date}\n{note_text}\n\n", font=("Verdana", 12), bg="cyan")
            note_label.pack()

        view_notes_window.mainloop()

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
            notes_manager = NotesManager(notes_manager_window, self.username)
            notes_manager_window.mainloop()

        def open_password_manager():
            root.destroy()
            password_manager_window = tk.Tk()
            password_manager_window.geometry("500x400")
            password_manager_window.config(bg="cyan")
            password_manager_window.title("Password Manager")
            password_manager = PasswordManager(password_manager_window, self.username)
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
    def __init__(self, root, username):
        self.root = root
        self.root.title("Password Manager")
        self.root.config(bg="cyan")

        self.username = username

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

        self.view_passwords_button = tk.Button(root, text="View Passwords", font=("Verdana", 12), command=self.view_passwords)
        self.view_passwords_button.pack(pady=20)

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

    def view_passwords(self):
        view_passwords_window = tk.Tk()
        view_passwords_window.title("View Passwords")
        view_passwords_window.geometry("500x400")
        view_passwords_window.config(bg="cyan")

        c.execute("SELECT * FROM passwords")
        passwords = c.fetchall()

        for password in passwords:
            username, website, password_text = password[1], password[2], password[3]
            password_label = tk.Label(view_passwords_window, text=f"Username: {username}\nWebsite: {website}\nPassword: {password_text}\n\n", font=("Verdana", 12), bg="cyan")
            password_label.pack()

        view_passwords_window.mainloop()

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
            notes_manager = NotesManager(notes_manager_window, self.username)
            notes_manager_window.mainloop()

        def open_password_manager():
            root.destroy()
            password_manager_window = tk.Tk()
            password_manager_window.geometry("500x400")
            password_manager_window.config(bg="cyan")
            password_manager_window.title("Password Manager")
            password_manager = PasswordManager(password_manager_window, self.username)
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
