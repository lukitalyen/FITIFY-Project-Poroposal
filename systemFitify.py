import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage, Label, filedialog
from tkcalendar import DateEntry
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import mysql.connector
from datetime import datetime
from PIL import Image, ImageTk
import os
import sv_ttk

# Database configuration
host = "localhost"
user = "root"
database = "try2"

conn = mysql.connector.connect(
    host=host,
    user=user,
    database=database
)

class FitnessApp:
    def __init__(self, root):
        self.bmi = None
        self.images = {}
        self.root = root
        self.startup_page()
        self.root.title('Fitify')
        self.calculated_tdee = 0
        self.uploaded_pictures_directory = r"C:\\Users\\Dream Events\\Desktop\\FPJ\\UPP"
        os.makedirs(self.uploaded_pictures_directory, exist_ok=True)
        self.new_profile_picture_path = None

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def startup_page(self):
        self.clear_frame()

        content_frame = ttk.Frame(self.root)
        content_frame.pack(padx=10, pady=250)

        logo_path = r"C:\\Users\\Dream Events\\Desktop\\FPJ\\logo-light.png"
        self.logo = tk.PhotoImage(file=logo_path)

        logo_canvas = tk.Canvas(content_frame, width=self.logo.width(), height=self.logo.height(), highlightthickness=0)
        logo_canvas.pack(side=tk.LEFT, padx=10, pady=10)
        logo_canvas.create_image(0, 0, anchor=tk.NW, image=self.logo)

        left_frame = ttk.Frame(content_frame)
        left_frame.pack(side=tk.LEFT, padx=10)

        username_label = ttk.Label(left_frame, text='Username:', font=('Arial', 12))
        username_label.pack(pady=5)

        username_entry = ttk.Entry(left_frame, font=('Arial', 12))
        username_entry.pack(pady=5)

        pin_label = ttk.Label(left_frame, text='4-digit PIN:', font=('Arial', 12))
        pin_label.pack(pady=5)

        pin_entry = ttk.Entry(left_frame, font=('Arial', 12), show='*')
        pin_entry.pack(pady=5)

        pin_warning_label = ttk.Label(left_frame, text='', font=('Arial', 12))
        pin_warning_label.pack(pady=5)

        login_button = ttk.Button(left_frame, text='Log In', command=lambda: self.authenticate_user(username_entry.get(), pin_entry.get(), pin_warning_label))
        login_button.pack(pady=5)

        signup_button = ttk.Button(left_frame, text='Sign Up', command=self.signup_page)
        signup_button.pack(pady=5)

        admin_button = ttk.Button(left_frame, text='Admin', command=self.admin_login_page)
        admin_button.pack(pady=5)

    def admin_login_page(self):
        self.clear_frame()

        admin_label = ttk.Label(self.root, text='Admin Login', font=('Helvetica', 18))
        admin_label.pack(pady=20)

        password_label = ttk.Label(self.root, text='Password:', font=('Helvetica', 12))
        password_label.pack()

        password_entry = ttk.Entry(self.root, show='*', font=('Helvetica', 12))
        password_entry.pack(pady=10)

        login_button = ttk.Button(self.root, text='Login', command=lambda: self.admin_login(password_entry.get()))
        login_button.pack(pady=10)

        back_button = ttk.Button(self.root, text='Back', command=self.startup_page)
        back_button.pack(pady=10)

    def admin_login(self, password):
        admin_password = "admin123"  # Replace this with a secure password retrieval method
        if password == admin_password:
            self.admin_dashboard()
        else:
            error_label = ttk.Label(self.root, text='Incorrect password. Please try again.', font=('Helvetica', 12), foreground='red')
            error_label.pack(pady=10)

    def create_admin_buttons(self, parent_frame):
        style = ttk.Style()
        style.configure('NoBorder.TButton', background='#F0F0F0', bd=0, foreground='#ffffff', font=('Arial', 12))

        icons = [
            (r"C:\Users\Dream Events\Desktop\FPJ\BUTTONS-ADMIN\1 ADMIN BUTTON.png", self.view_users),
            (r"C:\Users\Dream Events\Desktop\FPJ\BUTTONS-ADMIN\2 ADMIN BUTTON.png", self.edit_user_page),
            (r"C:\Users\Dream Events\Desktop\FPJ\BUTTONS-ADMIN\3 ADMIN BUTTON.png", self.delete_user_page),
            (r"C:\Users\Dream Events\Desktop\FPJ\BUTTONS-ADMIN\4 ADMIN BUTTON.png", self.show_user_dropdown_for_activities),
            (r"C:\Users\Dream Events\Desktop\FPJ\BUTTONS-ADMIN\5 ADMIN BUTTON.png", self.reset_user_logs)  # Updated to reset user logs
        ]

        icon_size = (150, 105)

        for icon_path, command in icons:
            icon = Image.open(icon_path)
            icon = icon.resize(icon_size, Image.LANCZOS)
            icon = ImageTk.PhotoImage(icon)

            button = ttk.Button(parent_frame, text='', image=icon, compound=tk.LEFT, command=command, style='NoBorder.TButton')
            button.image = icon
            button.pack(pady=5, fill=tk.X, padx=10, ipady=10)

    def reset_user_logs(self):
        self.clear_frame()

        sidebar_frame = tk.Frame(self.root, width=200, bg='#22668D')
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        buttons_frame = tk.Frame(sidebar_frame, bg='#22668D')
        buttons_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.create_admin_buttons(buttons_frame)

        sign_out_button = ttk.Button(buttons_frame, text='Sign Out', command=self.startup_page, style='NoBorder.TButton')
        sign_out_button.pack(pady=15, fill=tk.X)

        header_image_path = r"C:\Users\Dream Events\Desktop\FPJ\HEADERS-ADMIN\resetUserLogs-01.png"
        if os.path.isfile(header_image_path):
            header_image = ImageTk.PhotoImage(Image.open(header_image_path).resize((789, 100)))
            header_label = tk.Label(self.root, image=header_image)
            header_label.image = header_image
            header_label.pack()

        content_frame = ttk.Frame(self.root)
        content_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        prompt_label = ttk.Label(content_frame, text="Enter the User ID to reset their logs:", font=('Arial', 12))
        prompt_label.pack(pady=10)

        user_id_entry = ttk.Entry(content_frame, font=('Arial', 12))
        user_id_entry.pack(pady=10)

        reset_button = ttk.Button(content_frame, text="Reset Logs", command=lambda: self.confirm_reset_user_logs(user_id_entry.get()))
        reset_button.pack(pady=10)

        back_button = ttk.Button(content_frame, text="Back", command=self.admin_dashboard)
        back_button.pack(pady=10)

    def confirm_reset_user_logs(self, user_id):
        if not user_id:
            tk.messagebox.showerror("Error", "User ID is required.")
            return

        if not user_id.isdigit():
            tk.messagebox.showerror("Error", "User ID must be a number.")
            return

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT username FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            cursor.close()

            if user:
                username = user[0]
                if tk.messagebox.askyesno("Confirm Reset", f"Are you sure you want to reset logs for user {username}?"):
                    self.reset_logs(username)
            else:
                tk.messagebox.showerror("Error", "User ID not found.")
        except mysql.connector.Error as err:
            tk.messagebox.showerror("Error", f"Database error: {err}")

    def reset_logs(self, username):
        try:
            cursor = conn.cursor()

            # Reset workout logs
            cursor.execute("DELETE FROM workouts WHERE username = %s", (username,))
        
            # Reset sleep logs
            cursor.execute("DELETE FROM sleep_logs WHERE username = %s", (username,))
        
            # Reset health metrics
            cursor.execute("DELETE FROM health_metrics WHERE username = %s", (username,))

            conn.commit()
            cursor.close()

            tk.messagebox.showinfo("Success", f"Logs for user {username} have been reset.")
        except mysql.connector.Error as err:
            tk.messagebox.showerror("Error", f"Failed to reset logs: {err}")




    def admin_dashboard(self):
        self.clear_frame()

        sidebar_frame = tk.Frame(self.root, width=200, bg='#22668D')
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        buttons_frame = tk.Frame(sidebar_frame, bg='#22668D')
        buttons_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.create_admin_buttons(buttons_frame)

        sign_out_button = ttk.Button(buttons_frame, text='Sign Out', command=self.startup_page, style='NoBorder.TButton')
        sign_out_button.pack(pady=15, fill=tk.X)

        content_frame = ttk.Frame(self.root)
        content_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Load and display the photo
        photo_path = r"C:\Users\Dream Events\Desktop\FPJ\HEADERS-ADMIN\LIMITED TIME ONLY.png"  # Update with the actual path to your photo
        photo = Image.open(photo_path)
        photo = ImageTk.PhotoImage(photo)
        photo_label = tk.Label(content_frame, image=photo)
        photo_label.image = photo  # Keep a reference to the image to prevent garbage collection
        photo_label.pack(fill=tk.BOTH, expand=True)


        # Add your admin dashboard content here

    def view_users(self):
        self.clear_frame()

        sidebar_frame = tk.Frame(self.root, width=200, bg='#22668D')
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        buttons_frame = tk.Frame(sidebar_frame, bg='#22668D')
        buttons_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.create_admin_buttons(buttons_frame)

        sign_out_button = ttk.Button(buttons_frame, text='Sign Out', command=self.startup_page, style='NoBorder.TButton')
        sign_out_button.pack(pady=15, fill=tk.X)

        header_image_path = r"C:\Users\Dream Events\Desktop\FPJ\HEADERS-ADMIN\viewAllUsers.png"
        if os.path.isfile(header_image_path):
            header_image = ImageTk.PhotoImage(Image.open(header_image_path).resize((789, 100)))
            header_label = tk.Label(self.root, image=header_image)
            header_label.image = header_image
            header_label.pack()

        users_frame = ttk.Frame(self.root)
        users_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        columns = ("ID", "Username", "Email")
        tree = ttk.Treeview(users_frame, columns=columns, show='headings')
        tree.heading("ID", text="ID")
        tree.heading("Username", text="Username")
        tree.heading("Email", text="Email")
        tree.pack(fill=tk.BOTH, expand=True)

        cursor = conn.cursor()
        cursor.execute("SELECT id, username, email FROM users")
        users = cursor.fetchall()
        cursor.close()

        for user in users:
            tree.insert("", tk.END, values=user)

        back_button = ttk.Button(users_frame, text="Back", command=self.admin_dashboard)
        back_button.pack(pady=10)


    def filter_users(self, search_term):
        cursor = conn.cursor()
        query = "SELECT id, username, email FROM users WHERE username LIKE %s OR email LIKE %s"
        cursor.execute(query, (f"%{search_term}%", f"%{search_term}%"))
        users = cursor.fetchall()
        cursor.close()

        self.display_users(users)

    def display_users(self, users):
        self.clear_frame()

        users_frame = ttk.Frame(self.root)
        users_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        columns = ("ID", "Username", "Email")
        tree = ttk.Treeview(users_frame, columns=columns, show='headings')
        tree.heading("ID", text="ID")
        tree.heading("Username", text="Username")
        tree.heading("Email", text="Email")
        tree.pack(fill=tk.BOTH, expand=True)

        for user in users:
            tree.insert("", tk.END, values=user)

        back_button = ttk.Button(users_frame, text="Back", command=self.admin_dashboard)
        back_button.pack(pady=10)

    def edit_user_page(self):
        self.clear_frame()

        sidebar_frame = tk.Frame(self.root, width=200, bg='#22668D')
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        buttons_frame = tk.Frame(sidebar_frame, bg='#22668D')
        buttons_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.create_admin_buttons(buttons_frame)

        sign_out_button = ttk.Button(buttons_frame, text='Sign Out', command=self.startup_page, style='NoBorder.TButton')
        sign_out_button.pack(pady=15, fill=tk.X)

        header_image_path = r"C:\Users\Dream Events\Desktop\FPJ\HEADERS-ADMIN\editUser.png"
        if os.path.isfile(header_image_path):
            header_image = ImageTk.PhotoImage(Image.open(header_image_path).resize((789, 100)))
            header_label = tk.Label(self.root, image=header_image)
            header_label.image = header_image
            header_label.pack()

        edit_user_frame = ttk.Frame(self.root)
        edit_user_frame.pack(padx=10, pady=10)

        user_id_label = ttk.Label(edit_user_frame, text="User ID:")
        user_id_label.grid(row=0, column=0, padx=10, pady=10)
        self.edit_user_id_entry = ttk.Entry(edit_user_frame)
        self.edit_user_id_entry.grid(row=0, column=1, padx=10, pady=10)

        username_label = ttk.Label(edit_user_frame, text="New Username:")
        username_label.grid(row=1, column=0, padx=10, pady=10)
        self.edit_username_entry = ttk.Entry(edit_user_frame)
        self.edit_username_entry.grid(row=1, column=1, padx=10, pady=10)

        email_label = ttk.Label(edit_user_frame, text="New Email:")
        email_label.grid(row=2, column=0, padx=10, pady=10)
        self.edit_email_entry = ttk.Entry(edit_user_frame)
        self.edit_email_entry.grid(row=2, column=1, padx=10, pady=10)

        self.edit_user_warning_label = ttk.Label(edit_user_frame, text='', font=('Arial', 12), foreground='red')
        self.edit_user_warning_label.grid(row=3, column=0, columnspan=2, pady=10)

        self.edit_user_success_label = ttk.Label(edit_user_frame, text='', font=('Arial', 12), foreground='green')
        self.edit_user_success_label.grid(row=4, column=0, columnspan=2, pady=10)

        update_user_button = ttk.Button(edit_user_frame, text="Update User", command=self.confirm_update_user)
        update_user_button.grid(row=5, column=0, columnspan=2, pady=10)

        back_button = ttk.Button(edit_user_frame, text="Back", command=self.admin_dashboard)
        back_button.grid(row=6, column=0, columnspan=2, pady=10)


    def confirm_update_user(self):
        user_id = self.edit_user_id_entry.get()
        new_username = self.edit_username_entry.get()
        new_email = self.edit_email_entry.get()

        if not user_id or not new_username or not new_email:
            self.edit_user_warning_label.config(text='All fields are required.')
            self.edit_user_success_label.config(text='')
            return

        if not user_id.isdigit():
            self.edit_user_warning_label.config(text='User ID must be a number.')
            self.edit_user_success_label.config(text='')
            return

        if not self.validate_email(new_email):
            self.edit_user_warning_label.config(text='Invalid email format.')
            self.edit_user_success_label.config(text='')
            return

        if tk.messagebox.askyesno("Confirm Update", f"*ATTENTION*\n By changing the username, it will reset the user's workout logs. \n\n Update user {user_id} with new username '{new_username}' and new email '{new_email}'?"):
            self.update_user(user_id, new_username, new_email)

    def update_user(self, user_id, new_username, new_email):
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET username=%s, email=%s WHERE id=%s", (new_username, new_email, user_id))
            conn.commit()
            cursor.close()

            self.edit_user_success_label.config(text='User updated successfully')
            self.edit_user_warning_label.config(text='')

            self.edit_user_id_entry.delete(0, tk.END)
            self.edit_user_id_entry.insert(0, user_id)

            self.edit_username_entry.delete(0, tk.END)
            self.edit_username_entry.insert(0, new_username)

            self.edit_email_entry.delete(0, tk.END)
            self.edit_email_entry.insert(0, new_email)

        except mysql.connector.Error as err:
            self.edit_user_warning_label.config(text=f"Failed to update user: {err}")
            self.edit_user_success_label.config(text='')

    def validate_email(self, email):
        return '@' in email and '.' in email

    def delete_user_page(self):
        self.clear_frame()

        sidebar_frame = tk.Frame(self.root, width=200, bg='#22668D')
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        buttons_frame = tk.Frame(sidebar_frame, bg='#22668D')
        buttons_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.create_admin_buttons(buttons_frame)

        sign_out_button = ttk.Button(buttons_frame, text='Sign Out', command=self.startup_page, style='NoBorder.TButton')
        sign_out_button.pack(pady=15, fill=tk.X)

        header_image_path = r"C:\Users\Dream Events\Desktop\FPJ\HEADERS-ADMIN\deleteUser.png"
        if os.path.isfile(header_image_path):
            header_image = ImageTk.PhotoImage(Image.open(header_image_path).resize((789, 100)))
            header_label = tk.Label(self.root, image=header_image)
            header_label.image = header_image
            header_label.pack()

        delete_user_frame = ttk.Frame(self.root)
        delete_user_frame.pack(padx=10, pady=10)

        user_id_label = ttk.Label(delete_user_frame, text="User ID:")
        user_id_label.grid(row=0, column=0, padx=10, pady=10)
        self.delete_user_id_entry = ttk.Entry(delete_user_frame)
        self.delete_user_id_entry.grid(row=0, column=1, padx=10, pady=10)

        self.delete_user_warning_label = ttk.Label(delete_user_frame, text='', font=('Arial', 12), foreground='red')
        self.delete_user_warning_label.grid(row=1, column=0, columnspan=2, pady=10)

        self.delete_user_success_label = ttk.Label(delete_user_frame, text='', font=('Arial', 12), foreground='green')
        self.delete_user_success_label.grid(row=2, column=0, columnspan=2, pady=10)

        delete_user_button = ttk.Button(delete_user_frame, text="Delete User", command=self.confirm_delete_user)
        delete_user_button.grid(row=3, column=0, columnspan=2, pady=10)

        back_button = ttk.Button(delete_user_frame, text="Back", command=self.admin_dashboard)
        back_button.grid(row=4, column=0, columnspan=2, pady=10)


    def confirm_delete_user(self):
        user_id = self.delete_user_id_entry.get()

        if not user_id:
            self.delete_user_warning_label.config(text='User ID is required.')
            self.delete_user_success_label.config(text='')
            return

        if not user_id.isdigit():
            self.delete_user_warning_label.config(text='User ID must be a number.')
            self.delete_user_success_label.config(text='')
            return

        if tk.messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete user {user_id}?"):
            self.delete_user(user_id)

    def delete_user(self, user_id):
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
            conn.commit()
            cursor.close()

            self.delete_user_success_label.config(text='User deleted successfully')
            self.delete_user_warning_label.config(text='')

            self.delete_user_id_entry.delete(0, tk.END)
            self.delete_user_id_entry.insert(0, user_id)

        except mysql.connector.Error as err:
            self.delete_user_warning_label.config(text=f"Failed to delete user: {err}")
            self.delete_user_success_label.config(text='')


    def show_user_dropdown_for_activities(self):
        self.clear_frame()

        sidebar_frame = tk.Frame(self.root, width=200, bg='#22668D')
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        buttons_frame = tk.Frame(sidebar_frame, bg='#22668D')
        buttons_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.create_admin_buttons(buttons_frame)

        sign_out_button = ttk.Button(buttons_frame, text='Sign Out', command=self.startup_page, style='NoBorder.TButton')
        sign_out_button.pack(pady=15, fill=tk.X)

        header_image_path = r"C:\Users\Dream Events\Desktop\FPJ\HEADERS-ADMIN\viewUserActivities.png"
        if os.path.isfile(header_image_path):
            header_image = ImageTk.PhotoImage(Image.open(header_image_path).resize((789, 100)))
            header_label = tk.Label(self.root, image=header_image)
            header_label.image = header_image
            header_label.pack()

        activities_frame = ttk.Frame(self.root)
        activities_frame.pack(padx=10, pady=10)

        user_id_label = ttk.Label(activities_frame, text="User ID:")
        user_id_label.grid(row=0, column=0, padx=10, pady=10)

        self.activities_user_id_entry = ttk.Entry(activities_frame)
        self.activities_user_id_entry.grid(row=0, column=1, padx=10, pady=10)

        view_activities_button = ttk.Button(activities_frame, text="View Activities", command=self.view_user_activities)
        view_activities_button.grid(row=1, column=0, columnspan=2, pady=10)

        back_button = ttk.Button(activities_frame, text="Back", command=self.admin_dashboard)
        back_button.grid(row=2, column=0, columnspan=2, pady=10)


    def view_user_activities(self):
        user_id = self.activities_user_id_entry.get()

        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users WHERE id=%s", (user_id,))
        user = cursor.fetchone()
        if user:
            username = user[0]
            self.display_activity_logs(username)
        else:
            tk.messagebox.showerror("Error", "User not found")

        cursor.close()

    def display_activity_logs(self, username):
        self.clear_frame()

        sidebar_frame = tk.Frame(self.root, width=200, bg='#22668D')
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        buttons_frame = tk.Frame(sidebar_frame, bg='#22668D')
        buttons_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.create_admin_buttons(buttons_frame)

        sign_out_button = ttk.Button(buttons_frame, text='Sign Out', command=self.startup_page, style='NoBorder.TButton')
        sign_out_button.pack(pady=15, fill=tk.X)

        content_frame = ttk.Frame(self.root)
        content_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        header_image_path = r"C:\Users\Dream Events\Desktop\FPJ\HEADERS-ADMIN\viewUserActivities.png"
        if os.path.isfile(header_image_path):
            header_image = ImageTk.PhotoImage(Image.open(header_image_path).resize((789, 100)))
            header_label = tk.Label(self.root, image=header_image)
            header_label.image = header_image
            header_label.pack()

        logs_frame = ttk.Frame(self.root)
        logs_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Create a notebook widget for tabbed display of different logs
        notebook = ttk.Notebook(logs_frame)
        notebook.pack(fill=tk.BOTH, expand=True)

        # Workouts tab
        workouts_tab = ttk.Frame(notebook)
        notebook.add(workouts_tab, text='Workouts')

        # Weight tab
        weight_tab = ttk.Frame(notebook)
        notebook.add(weight_tab, text='Weight')

        # Sleep tab
        sleep_tab = ttk.Frame(notebook)
        notebook.add(sleep_tab, text='Sleep')

        # Create matplotlib figures and axes for each tab
        fig1, ax1 = plt.subplots(figsize=(8, 4))
        fig2, ax2 = plt.subplots(figsize=(8, 4))
        fig3, ax3 = plt.subplots(figsize=(8, 4))

        # Call the existing display functions with the correct parameters
        self.display_workout_logs(ax1, username)
        self.display_weight_logs(ax2, username)
        self.display_sleep_logs(ax3, username)

        # Embed the matplotlib figures in the respective tabs
        canvas1 = FigureCanvasTkAgg(fig1, master=workouts_tab)
        canvas1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        canvas1.draw()

        canvas2 = FigureCanvasTkAgg(fig2, master=weight_tab)
        canvas2.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        canvas2.draw()

        canvas3 = FigureCanvasTkAgg(fig3, master=sleep_tab)
        canvas3.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        canvas3.draw()



    def display_workout_logs(self, ax, username):
        try:
            cursor = conn.cursor()
            select_workouts_query = "SELECT exercise_type, SUM(duration) FROM workouts WHERE username = %s GROUP BY exercise_type"
            cursor.execute(select_workouts_query, (username,))
            workout_data = cursor.fetchall()
            cursor.close()

            if workout_data:
                workout_types = [entry[0] for entry in workout_data]
                durations = [entry[1] for entry in workout_data]

                ax.bar(workout_types, durations, color='skyblue')
                ax.set_xlabel('Workout Types')
                ax.set_ylabel('Total Duration (minutes)')
                ax.set_title(f'Workout Logs for {username}')
            else:
                ax.text(0.5, 0.5, 'No workout data available.', ha='center', va='center', fontsize=12)
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def display_weight_logs(self, ax, username):
        try:
            cursor = conn.cursor()
            select_weight_logs_query = "SELECT weight, date FROM health_metrics WHERE username = %s"
            cursor.execute(select_weight_logs_query, (username,))
            weight_data = cursor.fetchall()
            cursor.close()

            if weight_data:
                dates = [entry[1].strftime("%m/%d") if entry[1] is not None else 'N/A' for entry in weight_data]
                weights = [entry[0] for entry in weight_data]

                ax.plot(dates, weights, marker='o', color='orange')
                ax.set_xlabel('Date')
                ax.set_ylabel('Weight (kg)')
                ax.set_title(f'Weight Logs for {username}')
            else:
                ax.text(0.5, 0.5, 'No weight data available.', ha='center', va='center', fontsize=12)
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def display_sleep_logs(self, ax, username):
        try:
            cursor = conn.cursor()
            select_sleep_logs_query = "SELECT sleep_duration, date FROM sleep_logs WHERE username = %s"
            cursor.execute(select_sleep_logs_query, (username,))
            sleep_data = cursor.fetchall()
            cursor.close()

            if sleep_data:
                dates = [entry[1].strftime("%m/%d") if entry[1] is not None else 'N/A' for entry in sleep_data]
                sleep_durations = [entry[0] for entry in sleep_data]

                ax.bar(dates, sleep_durations, color='purple')
                ax.set_xlabel('Date')
                ax.set_ylabel('Sleep Duration (hours)')
                ax.set_title(f'Sleep Logs for {username}')
            else:
                ax.text(0.5, 0.5, 'No sleep data available.', ha='center', va='center', fontsize=12)
        except mysql.connector.Error as err:
            print(f"Error: {err}")


    def view_logs(self, username):
        self.clear_frame()

        logs_frame = ttk.Frame(self.root)
        logs_frame.pack(padx=10, pady=10)

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM workouts WHERE username=%s", (username,))
        workouts = cursor.fetchall()

        cursor.execute("SELECT * FROM sleep_logs WHERE username=%s", (username,))
        sleep_logs = cursor.fetchall()

        cursor.execute("SELECT * FROM health_metrics WHERE username=%s", (username,))
        health_metrics = cursor.fetchall()
        cursor.close()

        ttk.Label(logs_frame, text="Workouts:").pack()
        for workout in workouts:
            ttk.Label(logs_frame, text=workout).pack()

        ttk.Label(logs_frame, text="Sleep Logs:").pack()
        for log in sleep_logs:
            ttk.Label(logs_frame, text=log).pack()

        ttk.Label(logs_frame, text="Health Metrics:").pack()
        for metric in health_metrics:
            ttk.Label(logs_frame, text=metric).pack()

        back_button = ttk.Button(logs_frame, text="Back", command=self.admin_dashboard)
        back_button.pack(pady=10)

    def view_system_logs(self):
        self.clear_frame()

        logs_frame = ttk.Frame(self.root)
        logs_frame.pack(padx=10, pady=10)

        try:
            with open("system_logs.txt", "r") as file:
                logs = file.readlines()
                for log in logs:
                    ttk.Label(logs_frame, text=log.strip()).pack()
        except FileNotFoundError:
            ttk.Label(logs_frame, text="No system logs found.").pack()

        back_button = ttk.Button(logs_frame, text="Back", command=self.admin_dashboard)
        back_button.pack(pady=10)


    def signup_page(self):
        self.clear_frame()

        back_button = ttk.Button(self.root, text='Back to Startup', command=self.startup_page)
        back_button.pack(pady=10)

        label = ttk.Label(self.root, text='Sign Up Page', font=('Arial', 14))
        label.pack(pady=10)

        username_label = ttk.Label(self.root, text='Username:', font=('Arial', 12))
        username_label.pack(pady=5)

        username_entry = ttk.Entry(self.root, font=('Arial', 12))
        username_entry.pack(pady=5)

        pin_label = ttk.Label(self.root, text='4-digit PIN:', font=('Arial', 12))
        pin_label.pack(pady=5)

        pin_entry = ttk.Entry(self.root, font=('Arial', 12), show='*')
        pin_entry.pack(pady=5)

        email_label = ttk.Label(self.root, text='Email:', font=('Arial', 12))
        email_label.pack(pady=5)

        email_entry = ttk.Entry(self.root, font=('Arial', 12))
        email_entry.pack(pady=5)

        initial_weight_label = ttk.Label(self.root, text='Initial Weight (kg):', font=('Arial', 12))
        initial_weight_label.pack(pady=5)

        initial_weight_entry = ttk.Entry(self.root, font=('Arial', 12))
        initial_weight_entry.pack(pady=5)

        username_warning_label = ttk.Label(self.root, text='', font=('Arial', 12), foreground='red')
        username_warning_label.pack(pady=10)

        signup_success_label = ttk.Label(self.root, text='', font=('Arial', 12, 'bold'), foreground='green')
        signup_success_label.pack(pady=10)

        signup_button = ttk.Button(self.root, text='Sign Up', command=lambda: self.validate_and_save_user(
            username_entry.get(), pin_entry.get(), email_entry.get(), initial_weight_entry.get(),
            username_warning_label, signup_success_label))
        signup_button.pack(pady=10)

    def validate_and_save_user(self, username, pin, email, initial_weight, username_warning_label, signup_success_label):
        # Validation checks
        if not username or not pin or not email or not initial_weight:
            username_warning_label.config(text='Invalid input. Please fill in all fields.')
            signup_success_label.config(text='')
            return

        if len(pin) != 4 or not pin.isdigit():
            username_warning_label.config(text='Invalid PIN. Please enter a 4-digit numeric PIN.')
            signup_success_label.config(text='')
            return

        self.save_user(username, pin, email, initial_weight, username_warning_label, signup_success_label)

    def save_user(self, username, pin, email, initial_weight, username_warning_label, signup_success_label):
        try:
            cursor = conn.cursor()

            check_user_query = "SELECT * FROM users WHERE username = %s"
            cursor.execute(check_user_query, (username,))
            existing_user = cursor.fetchone()

            if existing_user:
                username_warning_label.config(text='Username already exists. Please choose a different username.')
                signup_success_label.config(text='')
                return

            username_warning_label.config(text='')

            insert_user_query = "INSERT INTO users (username, pin, email, initial_weight) VALUES (%s, %s, %s, %s)"
            user_data = (username, pin, email, initial_weight)
            cursor.execute(insert_user_query, user_data)

            conn.commit()

            print("User saved successfully!")
            signup_success_label.config(text='Account created successfully!')

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if 'cursor' in locals():
                cursor.close()

    def login_page(self):
        self.clear_frame()

        back_button = ttk.Button(self.root, text='Back to Startup', command=self.startup_page)
        back_button.pack(pady=10)

        label = ttk.Label(self.root, text='Log In Page', font=('Arial', 14))
        label.pack(pady=10)

        username_label = ttk.Label(self.root, text='Username:', font=('Arial', 12))
        username_label.pack(pady=5)

        username_entry = ttk.Entry(self.root, font=('Arial', 12))
        username_entry.pack(pady=5)

        pin_label = ttk.Label(self.root, text='4-digit PIN:', font=('Arial', 12))
        pin_label.pack(pady=5)

        pin_entry = ttk.Entry(self.root, font=('Arial', 12), show='*')  # Show '*' for PIN
        pin_entry.pack(pady=5)

        login_button = ttk.Button(self.root, text='Log In', command=lambda: self.authenticate_user(username_entry.get(), pin_entry.get()))
        login_button.pack(pady=10)

    def authenticate_user(self, username, pin, pin_warning_label):
        try:
            cursor = conn.cursor()

            if not pin.isdigit() or len(pin) != 4:
                pin_warning_label.config(text='Invalid PIN. Please enter a 4-digit PIN.', foreground='red')
                return

            pin_warning_label.config(text=' Invalid PIN ', foreground='red')

            authenticate_query = "SELECT * FROM users WHERE username = %s AND pin = %s"
            user_data = (username, pin)
            cursor.execute(authenticate_query, user_data)

            result = cursor.fetchone()

            if result:
                print("Authentication successful!")
                self.main_menu(username)
            else:
                print("Authentication failed. Invalid username or PIN.")

                if pin_warning_label:
                    pin_warning_label.config(text='Invalid PIN. Please try again.', foreground='red')

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if 'cursor' in locals():
                cursor.close()

    def create_buttons(self, parent_frame, username):
        style = ttk.Style()
        style.configure('NoBorder.TButton', background='#F0F0F0', bd=0, foreground='#ffffff', font=('Arial', 12))

        # Replace 'path_to_icon_profile.png' with the actual path to your icon image
        profile_icon = Image.open(r"C:\Users\Dream Events\Desktop\FPJ\menu-icons\1.png")
        dashboard_icon = Image.open(r"C:\Users\Dream Events\Desktop\FPJ\menu-icons\2.png")
        workout_log_icon = Image.open(r"C:\Users\Dream Events\Desktop\FPJ\menu-icons\3.png")
        health_metrics_icon = Image.open(r"C:\Users\Dream Events\Desktop\FPJ\menu-icons\4.png")
        nutrition_icon = Image.open(r"C:\Users\Dream Events\Desktop\FPJ\menu-icons\5.png")


        # Resize the icons if needed
        icon_size = (150, 105)
        profile_icon = profile_icon.resize(icon_size, Image.LANCZOS)
        dashboard_icon = dashboard_icon.resize(icon_size, Image.LANCZOS)
        workout_log_icon = workout_log_icon.resize(icon_size, Image.LANCZOS)
        health_metrics_icon = health_metrics_icon.resize(icon_size, Image.LANCZOS)
        nutrition_icon = nutrition_icon.resize(icon_size, Image.LANCZOS)

        profile_icon = ImageTk.PhotoImage(profile_icon)
        dashboard_icon = ImageTk.PhotoImage(dashboard_icon)
        workout_log_icon = ImageTk.PhotoImage(workout_log_icon)
        health_metrics_icon = ImageTk.PhotoImage(health_metrics_icon)
        nutrition_icon = ImageTk.PhotoImage(nutrition_icon)

        profile_button = ttk.Button(parent_frame, text='', image=profile_icon, compound=tk.LEFT,
                                    command=lambda: self.profile_page(username), style='NoBorder.TButton')
        profile_button.image = profile_icon  # Keep a reference to the image
        profile_button.pack(pady=5, fill=tk.X, padx=10, ipady=10)

        dashboard_button = ttk.Button(parent_frame, text='', image=dashboard_icon, compound=tk.LEFT,
                                      command=lambda: self.dashboard_page(username), style='NoBorder.TButton')
        dashboard_button.image = dashboard_icon
        dashboard_button.pack(pady=5, fill=tk.X, padx=10, ipady=10)

        workout_log_button = ttk.Button(parent_frame, text='', image=workout_log_icon, compound=tk.LEFT,
                                        command=lambda: self.workout_log_page(username), style='NoBorder.TButton')
        workout_log_button.image = workout_log_icon
        workout_log_button.pack(pady=5, fill=tk.X, padx=10, ipady=10)

        health_metrics_button = ttk.Button(parent_frame, text='', image=health_metrics_icon, compound=tk.LEFT,
                                           command=lambda: self.health_metrics_page(username), style='NoBorder.TButton')
        health_metrics_button.image = health_metrics_icon
        health_metrics_button.pack(pady=5, fill=tk.X, padx=10, ipady=10)

        nutrition_button = ttk.Button(parent_frame, text='', image=nutrition_icon, compound=tk.LEFT,
                                      command=lambda: self.nutrition_page(username), style='NoBorder.TButton')
        nutrition_button.image = nutrition_icon
        nutrition_button.pack(pady=5, fill=tk.X, padx=10, ipady=10)

    def main_menu(self, username):
        self.clear_frame()

        sidebar_frame = tk.Frame(self.root, width=400, bg='#22668D')
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        label = ttk.Frame(self.root, padding=20)
        label.pack(side=tk.LEFT, fill=tk.Y)

        buttons_frame = tk.Frame(sidebar_frame, bg='#F0F0F0')
        buttons_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.create_buttons(sidebar_frame, username)

        sign_out_button = ttk.Button(sidebar_frame, text='Sign Out', command=self.startup_page, style='NoBorder.TButton')
        sign_out_button.pack(pady=15, fill=tk.X)

        self.custom_dashboard(username)

    def custom_dashboard(self, username):
        content_frame = tk.Frame(self.root)
        content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        profile_picture = ImageTk.PhotoImage(Image.open(r"C:\Users\Dream Events\Desktop\FPJ\headers\head.png").resize((1100, 200)))
        profile_picture_label = tk.Label(content_frame, image=profile_picture)
        profile_picture_label.image = profile_picture  # Keep a reference to the image
        profile_picture_label.pack()

        profile_picture = ImageTk.PhotoImage(Image.open(r"C:\Users\Dream Events\Desktop\FPJ\welcome.png").resize((1100, 100)))
        profile_picture_label = tk.Label(content_frame, image=profile_picture)
        profile_picture_label.image = profile_picture  # Keep a reference to the image
        profile_picture_label.pack()

        profile_picture = ImageTk.PhotoImage(Image.open(r"C:\Users\Dream Events\Desktop\FPJ\WHN.png").resize((1100, 475)))
        profile_picture_label = tk.Label(content_frame, image=profile_picture)
        profile_picture_label.image = profile_picture  # Keep a reference to the image
        profile_picture_label.pack()


    def profile_page(self, username):
        self.clear_frame()
        sidebar_frame = tk.Frame(self.root, width=400, bg='#22668D')
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        label = ttk.Frame(self.root, padding=20)
        label.pack(side=tk.LEFT, fill=tk.Y)

        buttons_frame = tk.Frame(sidebar_frame, bg='#F0F0F0')
        buttons_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.create_buttons(sidebar_frame, username)

        sign_out_button = ttk.Button(sidebar_frame, text='Sign Out', command=self.startup_page, style='NoBorder.TButton')
        sign_out_button.pack(pady=15, fill=tk.X)

        label = ttk.Frame(self.root, padding=20)
        label.pack(side=tk.LEFT, fill=tk.Y)

        back_button = ttk.Button(self.root, text='Back', command=lambda: self.main_menu(username))
        back_button.pack(side='top', anchor='nw', padx=10, pady=10)

        header_image_path = r"C:\Users\Dream Events\Desktop\FPJ\headers\profile.png"
        if os.path.isfile(header_image_path):
            header_image = ImageTk.PhotoImage(Image.open(header_image_path).resize((789, 100)))
            header_label = tk.Label(self.root, image=header_image)
            header_label.image = header_image
            header_label.pack()

        try:
            cursor = conn.cursor()
            select_profile_query = "SELECT * FROM users WHERE username = %s"
            cursor.execute(select_profile_query, (username,))
            user_data = cursor.fetchone()

            if user_data:
                profile_picture_path = user_data[5]
                if profile_picture_path and os.path.isfile(profile_picture_path):
                    profile_picture = ImageTk.PhotoImage(Image.open(profile_picture_path).resize((100, 100)))
                else:
                    profile_picture = ImageTk.PhotoImage(Image.open(r"C:\Users\Dream Events\Desktop\FPJ\placeholder.png").resize((100, 100)))

                profile_picture_label = tk.Label(self.root, image=profile_picture)
                profile_picture_label.image = profile_picture
                profile_picture_label.pack(pady=10)

                username_label = tk.Label(self.root, text=f'Username: {user_data[1]}', font=('Arial', 12))
                username_label.pack(pady=5)

                pin_label = tk.Label(self.root, text=f'4-digit PIN: {"*" * len(user_data[2])}', font=('Arial', 12))
                pin_label.pack(pady=5)

                email_label = tk.Label(self.root, text=f'Email: {user_data[3]}', font=('Arial', 12))
                email_label.pack(pady=5)

                initial_weight_label = tk.Label(self.root, text=f'Initial Weight: {user_data[4]}', font=('Arial', 12))
                initial_weight_label.pack(pady=5)

                edit_picture_button = ttk.Button(self.root, text='Edit Profile Picture', command=lambda: self.edit_profile_picture(username))
                edit_picture_button.pack(pady=10)

                edit_details_button = ttk.Button(self.root, text='Edit Profile Details', command=lambda: self.edit_profile_details(username))
                edit_details_button.pack(pady=10)
            else:
                print(f"Error: User {username} not found.")

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if 'cursor' in locals():
                cursor.close()

    def edit_profile_picture(self, username):
        self.clear_frame()
        sidebar_frame = tk.Frame(self.root, width=400, bg='#22668D')
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        label = ttk.Frame(self.root, padding=20)
        label.pack(side=tk.LEFT, fill=tk.Y)

        buttons_frame = tk.Frame(sidebar_frame, bg='#F0F0F0')
        buttons_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.create_buttons(sidebar_frame, username)

        sign_out_button = ttk.Button(sidebar_frame, text='Sign Out', command=self.startup_page, style='NoBorder.TButton')
        sign_out_button.pack(pady=15, fill=tk.X)

        back_button = ttk.Button(self.root, text='Back', command=lambda: self.profile_page(username))
        back_button.pack(side='top', anchor='nw', padx=10, pady=10)

        header_image_path = r"C:\Users\Dream Events\Desktop\FPJ\headers\profile.png"
        if os.path.isfile(header_image_path):
            header_image = ImageTk.PhotoImage(Image.open(header_image_path).resize((789, 100)))
            header_label = tk.Label(self.root, image=header_image)
            header_label.image = header_image
            header_label.pack()

        try:
            cursor = conn.cursor()
            select_profile_query = "SELECT profile_picture_path FROM users WHERE username = %s"
            cursor.execute(select_profile_query, (username,))
            result = cursor.fetchone()

            if result and result[0]:
                current_image_path = result[0]
                current_profile_picture = ImageTk.PhotoImage(Image.open(current_image_path).resize((100, 100)))
                current_picture_label = tk.Label(self.root, image=current_profile_picture)
                current_picture_label.image = current_profile_picture
                current_picture_label.pack(pady=5)
            else:
                placeholder_path = r"C:\Users\Dream Events\Desktop\FPJ\placeholder.png"
                placeholder_photo = ImageTk.PhotoImage(Image.open(placeholder_path).resize((100, 100)))
                current_picture_label = tk.Label(self.root, image=placeholder_photo)
                current_picture_label.image = placeholder_photo
                current_picture_label.pack(pady=5)

            upload_button = ttk.Button(self.root, text='Upload Picture', command=lambda: self.upload_picture(username, current_picture_label))
            upload_button.pack(pady=10)

            save_button = ttk.Button(self.root, text='Save', command=lambda: self.save_profile_picture(username))
            save_button.pack(pady=10)

            remove_button = ttk.Button(self.root, text='Remove Picture', command=lambda: self.remove_profile_picture(username, current_picture_label))
            remove_button.pack(pady=10)

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if 'cursor' in locals():
                cursor.close()

    def upload_picture(self, username, current_picture_label):
        file_path = filedialog.askopenfilename(title="Select Profile Picture", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])

        if file_path:
            _, file_extension = os.path.splitext(file_path)
            new_filename = f"{username}_profile_picture{file_extension}"
            new_file_path = os.path.join(self.uploaded_pictures_directory, new_filename)
            os.rename(file_path, new_file_path)

            new_profile_picture = ImageTk.PhotoImage(Image.open(new_file_path).resize((100, 100)))
            current_picture_label.configure(image=new_profile_picture)
            current_picture_label.image = new_profile_picture

            self.new_profile_picture_path = new_file_path

    def save_profile_picture(self, username):
        try:
            cursor = conn.cursor()

            update_query = "UPDATE users SET profile_picture_path = %s WHERE username = %s"
            cursor.execute(update_query, (self.new_profile_picture_path, username))
            conn.commit()

            print("Profile picture saved successfully!")

            self.profile_page(username)

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if 'cursor' in locals():
                cursor.close()

    def get_image_path(self, username):
        try:
            cursor = conn.cursor()
            select_profile_query = "SELECT profile_picture_path FROM users WHERE username = %s"
            cursor.execute(select_profile_query, (username,))
            result = cursor.fetchone()

            if result and result[0]:
                return result[0]

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if 'cursor' in locals():
                cursor.close()

        return None

    def remove_profile_picture(self, username, current_picture_label):
        try:
            cursor = conn.cursor()

            update_query = "UPDATE users SET profile_picture_path = NULL WHERE username = %s"
            cursor.execute(update_query, (username,))
            conn.commit()

            print("Profile picture removed successfully!")

            placeholder_path = r"C:\Users\Dream Events\Desktop\FPJ\placeholder.png"
            placeholder_photo = ImageTk.PhotoImage(Image.open(placeholder_path).resize((100, 100)))
            current_picture_label.configure(image=placeholder_photo)
            current_picture_label.image = placeholder_photo

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if 'cursor' in locals():
                cursor.close()

    def edit_profile_details(self, username):
        self.clear_frame()
        sidebar_frame = tk.Frame(self.root, width=400, bg='#22668D')
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        label = ttk.Frame(self.root, padding=20)
        label.pack(side=tk.LEFT, fill=tk.Y)

        buttons_frame = tk.Frame(sidebar_frame, bg='#F0F0F0')
        buttons_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.create_buttons(sidebar_frame, username)

        sign_out_button = ttk.Button(sidebar_frame, text='Sign Out', command=self.startup_page, style='NoBorder.TButton')
        sign_out_button.pack(pady=15, fill=tk.X)

        back_button = ttk.Button(self.root, text='Back', command=lambda: self.profile_page(username))
        back_button.pack(side='top', anchor='nw', padx=10, pady=10)

        header_image_path = r"C:\Users\Dream Events\Desktop\FPJ\headers\profile.png"
        if os.path.isfile(header_image_path):
            header_image = ImageTk.PhotoImage(Image.open(header_image_path).resize((789, 100)))
            header_label = tk.Label(self.root, image=header_image)
            header_label.image = header_image
            header_label.pack()

        try:
            cursor = conn.cursor()
            select_profile_query = "SELECT * FROM users WHERE username = %s"
            cursor.execute(select_profile_query, (username,))
            user_data = cursor.fetchone()

            if user_data:
                new_username_label = tk.Label(self.root, text='New Username:', font=('Arial', 12))
                new_username_label.pack(pady=5)

                new_username_entry = tk.Entry(self.root, font=('Arial', 12))
                new_username_entry.insert(0, user_data[1])
                new_username_entry.pack(pady=5)

                new_pin_label = tk.Label(self.root, text='New 4-digit PIN:', font=('Arial', 12))
                new_pin_label.pack(pady=5)

                new_pin_entry = tk.Entry(self.root, font=('Arial', 12), show='*')
                new_pin_entry.insert(0, user_data[2])
                new_pin_entry.pack(pady=5)

                new_email_label = tk.Label(self.root, text='New Email:', font=('Arial', 12))
                new_email_label.pack(pady=5)

                new_email_entry = tk.Entry(self.root, font=('Arial', 12))
                new_email_entry.insert(0, user_data[3])
                new_email_entry.pack(pady=5)

                save_username_button = ttk.Button(self.root, text='Save Username', command=lambda: self.save_username(username, new_username_entry.get()))
                save_username_button.pack(pady=10)

                save_pin_button = ttk.Button(self.root, text='Save PIN', command=lambda: self.save_pin(username, new_pin_entry.get()))
                save_pin_button.pack(pady=10)

                save_email_button = ttk.Button(self.root, text='Save Email', command=lambda: self.save_email(username, new_email_entry.get()))
                save_email_button.pack(pady=10)
            else:
                print(f"Error: User {username} not found.")

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if 'cursor' in locals():
                cursor.close()

    def save_username(self, old_username, new_username):
        try:
            cursor = conn.cursor()

            update_query = "UPDATE users SET username = %s WHERE username = %s"
            cursor.execute(update_query, (new_username, old_username))
            conn.commit()

            print("Username saved successfully!")

            self.profile_page(new_username)

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if 'cursor' in locals():
                cursor.close()

    def save_pin(self, username, new_pin):
        try:
            cursor = conn.cursor()

            update_query = "UPDATE users SET pin = %s WHERE username = %s"
            cursor.execute(update_query, (new_pin, username))
            conn.commit()

            print("PIN saved successfully!")

            self.profile_page(username)

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if 'cursor' in locals():
                cursor.close()

    def save_email(self, username, new_email):
        try:
            cursor = conn.cursor()

            update_query = "UPDATE users SET email = %s WHERE username = %s"
            cursor.execute(update_query, (new_email, username))
            conn.commit()

            print("Email saved successfully!")

            self.profile_page(username)

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if 'cursor' in locals():
                cursor.close()

    def dashboard_page(self, username):
        self.clear_frame()

        sidebar_frame = tk.Frame(self.root, width=400, bg='#22668D')
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        label = ttk.Frame(self.root, padding=20)
        label.pack(side=tk.LEFT, fill=tk.Y)

        buttons_frame = tk.Frame(sidebar_frame, bg='#F0F0F0')
        buttons_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.create_buttons(sidebar_frame, username)

        sign_out_button = ttk.Button(sidebar_frame, text='Sign Out', command=self.startup_page, style='NoBorder.TButton')
        sign_out_button.pack(pady=15, fill=tk.X)

        back_button = ttk.Button(self.root, text='Back', command=lambda: self.profile_page(username))
        back_button.pack(side='top', anchor='nw', padx=10, pady=10)

        header_image_path = r"C:\Users\Dream Events\Desktop\FPJ\headers\dashboard.png"
        if os.path.isfile(header_image_path):
            header_image = ImageTk.PhotoImage(Image.open(header_image_path).resize((789, 100)))
            header_label = tk.Label(self.root, image=header_image)
            header_label.image = header_image
            header_label.pack()

        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(8, 2))

        # Corrected method calls with the username parameter
        self.display_workout_logs(ax1, username)
        self.display_weight_logs(ax2, username)
        self.display_sleep_logs(ax3, username)

        # Embed the matplotlib figure in the tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        canvas.draw()


    def display_logs(self, username, log_type):
        if log_type == 'workout':
            self.display_workout_logs(username)
        elif log_type == 'weight':
            self.display_weight_logs(username)
        elif log_type == 'sleep':
            self.display_sleep_logs(username)
        else:
            print(f"Error: User {username} not found.")

    def filter_weight_logs_by_selected_month(self, username, selected_month, weight_data):
        filtered_data = [entry for entry in weight_data if entry[1] is not None and entry[1].strftime("%B") == selected_month]

        if filtered_data:
            print(f"Weight Logs for {selected_month}:")
            for entry in filtered_data:
                print(f"{entry[1].strftime('%m/%d')}: Weight - {entry[0]} kg")
        else:
            print(f"No weight data available for {selected_month}.")

    def update_sleep_graph(self, dates, sleep_durations):
        fig, ax = plt.subplots(figsize=(3, 2))
        ax.bar(dates, sleep_durations, color='purple')
        ax.set_xlabel('Date')
        ax.set_ylabel('Sleep Duration (hours)')

        self.canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.place(relx=0.72, rely=0.35)
        self.canvas.draw()

    def get_sleep_logs(self, username):
        try:
            cursor = conn.cursor()
            select_sleep_logs_query = "SELECT sleep_duration, date FROM health_metrics WHERE username = %s"
            cursor.execute(select_sleep_logs_query, (username,))
            sleep_data = cursor.fetchall()
            return sleep_data
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
        finally:
            if 'cursor' in locals():
                cursor.close()

    def get_user_workouts(self, username):
        try:
            cursor = conn.cursor()
            select_workouts_query = "SELECT exercise_type, SUM(duration) FROM workouts WHERE username = %s GROUP BY exercise_type"
            cursor.execute(select_workouts_query, (username,))
            workout_data = cursor.fetchall()
            return workout_data
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            if 'cursor' in locals():
                cursor.close()

    def average_sleep_per_week(self, username):
        try:
            cursor = conn.cursor()
            select_sleep_logs_query = "SELECT AVG(sleep_duration), WEEK(date) FROM sleep_logs WHERE username = %s GROUP BY WEEK(date)"
            cursor.execute(select_sleep_logs_query, (username,))
            average_sleep_data = cursor.fetchall()

            if average_sleep_data:
                print("Average Sleep Duration per Week:")
                for entry in average_sleep_data:
                    print(f"Week {entry[1]}: {entry[0]:.2f} hours")
            else:
                print("No sleep data available.")

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if 'cursor' in locals():
                cursor.close()

    def workout_log_page(self, username):
        self.clear_frame()
        sidebar_frame = tk.Frame(self.root, width=400, bg='#22668D')
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        label = ttk.Frame(self.root, padding=20)
        label.pack(side=tk.LEFT, fill=tk.Y)

        buttons_frame = tk.Frame(sidebar_frame, bg='#F0F0F0')
        buttons_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.create_buttons(sidebar_frame, username)

        sign_out_button = ttk.Button(sidebar_frame, text='Sign Out', command=self.startup_page, style='NoBorder.TButton')
        sign_out_button.pack(pady=15, fill=tk.X)

        back_button = ttk.Button(self.root, text='Back', command=lambda: self.main_menu(username))
        back_button.pack(side='top', anchor='nw', padx=10, pady=10)

        header_image_path = r"C:\Users\Dream Events\Desktop\FPJ\headers\workout.png"
        if os.path.isfile(header_image_path):
            header_image = ImageTk.PhotoImage(Image.open(header_image_path).resize((789, 100)))
            header_label = tk.Label(self.root, image=header_image)
            header_label.image = header_image
            header_label.pack()

        form_frame = ttk.Frame(self.root, padding=20)
        form_frame.pack(expand=True, fill='both')

        form_frame.columnconfigure(0, weight=1)

        success_label = ttk.Label(form_frame, text='', font=('Arial', 12), foreground='green')
        success_label.grid(row=16, column=0, columnspan=2, padx=10, pady=5, sticky='nsew')

        warning_label = ttk.Label(form_frame, text='', font=('Arial', 12), foreground='red')
        warning_label.grid(row=9, column=0, padx=10, pady=5, sticky='nsew')

        date_label = ttk.Label(form_frame, text='Date:', font=('Helvetica', 14))
        date_label.grid(row=2, column=0, padx=10, pady=5, sticky='nsew')

        date_entry = DateEntry(form_frame, width=15, background='darkblue', foreground='white', borderwidth=2)
        date_entry.grid(row=3, column=0, padx=10, pady=5, sticky='nsew')

        exercise_label = ttk.Label(form_frame, text='Exercise Type:', font=('Helvetica', 14))
        exercise_label.grid(row=4, column=0, padx=10, pady=5, sticky='nsew')
        exercise_types = self.get_exercise_types()

        exercise_var = tk.StringVar()
        exercise_combobox = ttk.Combobox(form_frame, textvariable=exercise_var, values=exercise_types, font=('Arial', 12), width=10)
        exercise_combobox.grid(row=5, column=0, padx=10, pady=5, sticky='nsew')

        duration_label = ttk.Label(form_frame, text='Duration (minutes):', font=('Arial', 14))
        duration_label.grid(row=6, column=0, padx=10, pady=5, sticky='nsew')

        duration_entry = ttk.Entry(form_frame, font=('Helvetica', 12), width=20)
        duration_entry.grid(row=7, column=0, padx=10, pady=5, sticky='nsew')

        submit_button = ttk.Button(form_frame, text='Submit Workout', command=lambda: self.log_workout(username, exercise_combobox.get(), duration_entry.get(), date_entry.get(), warning_label, success_label))
        submit_button.grid(row=8, column=0, padx=10, pady=(20, 10), sticky='nsew')

        clear_button = ttk.Button(self.root, text='Clear Labels', command=self.clear_workout_form)
        clear_button.pack(pady=10)

    def get_exercise_types(self):
        exercise_types = ['Running', 'Cycling', 'Weightlifting', 'Yoga', 'Swimming', 'Other']
        return exercise_types

    def log_workout(self, username, exercise, duration, date, warning_label, success_label):
        try:
            cursor = conn.cursor()

            if not exercise or not duration or not date:
                warning_label.config(text='Invalid input. Please fill in all fields.')
                return

            if not duration.isdigit():
                warning_label.config(text='Invalid duration. Please enter a numeric value.')
                return

            formatted_date = datetime.strptime(date, "%m/%d/%y").strftime("%Y-%m-%d")

            insert_workout_query = "INSERT INTO workouts (username, exercise_type, duration, date) VALUES (%s, %s, %s, %s)"
            workout_data = (username, exercise, duration, formatted_date)
            cursor.execute(insert_workout_query, workout_data)

            conn.commit()

            print("Workout logged successfully!")
            success_label.config(text='Workout logged successfully!')

            warning_label.config(text='')

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if 'cursor' in locals():
                cursor.close()

    def clear_workout_form(self):
        form_frame = self.root.winfo_children()[1].winfo_children()[2]
        for widget in form_frame.winfo_children():
            if isinstance(widget, (ttk.Entry, tk.Entry)):
                widget.delete(0, 'end')
            elif isinstance(widget, ttk.Label):
                pass

    def health_metrics_page(self, username):
        self.clear_frame()
        sidebar_frame = tk.Frame(self.root, width=400, bg='#22668D')
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        label = ttk.Frame(self.root, padding=20)
        label.pack(side=tk.LEFT, fill=tk.Y)

        buttons_frame = tk.Frame(sidebar_frame, bg='#F0F0F0')
        buttons_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.create_buttons(sidebar_frame, username)

        sign_out_button = ttk.Button(sidebar_frame, text='Sign Out', command=self.startup_page, style='NoBorder.TButton')
        sign_out_button.pack(pady=15, fill=tk.X)

        back_button = ttk.Button(self.root, text='Back', command=lambda: self.main_menu(username))
        back_button.pack(side='top', anchor='nw', padx=10, pady=10)

        header_image_path = r"C:\Users\Dream Events\Desktop\FPJ\headers\health.png"
        if os.path.isfile(header_image_path):
            header_image = ImageTk.PhotoImage(Image.open(header_image_path).resize((789, 100)))
            header_label = tk.Label(self.root, image=header_image)
            header_label.image = header_image
            header_label.pack()

        form_frame = ttk.Frame(self.root, padding=20)
        form_frame.pack(expand=True, fill='both')

        form_frame.columnconfigure(0, weight=1)

        date_label = tk.Label(form_frame, text='Date:', font=('Helvetica', 12))
        date_label.grid(row=2, column=0, padx=10, pady=5, sticky='nsew')

        date_entry = DateEntry(form_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        date_entry.grid(row=3, column=0, padx=10, pady=5, sticky='nsew')

        weight_label = tk.Label(form_frame, text='Weight (kg):', font=('Helvetica', 12))
        weight_label.grid(row=5, column=0, padx=10, pady=5, sticky='nsew')

        weight_entry = tk.Entry(form_frame, font=('Helvetica', 12))
        weight_entry.grid(row=6, column=0, padx=10, pady=5, sticky='nsew')

        activity_label = tk.Label(form_frame, text='Activity Level:', font=('Helvetica', 12))
        activity_label.grid(row=8, column=0, padx=10, pady=5, sticky='nsew')

        activity_levels = ['Sedentary', 'Lightly Active', 'Moderately Active', 'Highly Active']
        activity_var = tk.StringVar()
        activity_combobox = ttk.Combobox(form_frame, textvariable=activity_var, values=activity_levels)
        activity_combobox.grid(row=9, column=0, padx=10, pady=5, sticky='nsew')

        sleep_label = tk.Label(form_frame, text='Sleep Duration (hours):', font=('Helvetica', 12))
        sleep_label.grid(row=11, column=0, padx=10, pady=5, sticky='nsew')

        sleep_entry = tk.Entry(form_frame, font=('Helvetica', 12))
        sleep_entry.grid(row=12, column=0, padx=10, pady=5, sticky='nsew')

        date_warning = ttk.Label(form_frame, text='', foreground='red')
        date_warning.grid(row=3, column=1, padx=10, pady=5, sticky='nsew')

        success_label = ttk.Label(form_frame, text='', font=('Arial', 12), foreground='green')
        success_label.grid(row=16, column=0, columnspan=2, padx=10, pady=5, sticky='nsew')

        weight_warning = ttk.Label(form_frame, text='', foreground='red')
        weight_warning.grid(row=6, column=1, padx=10, pady=5, sticky='nsew')

        activity_warning = ttk.Label(form_frame, text='', foreground='red')
        activity_warning.grid(row=9, column=1, padx=10, pady=5, sticky='nsew')

        sleep_warning = ttk.Label(form_frame, text='', foreground='red')
        sleep_warning.grid(row=12, column=1, padx=10, pady=5, sticky='nsew')

        general_warning = ttk.Label(form_frame, text='', foreground='red')
        general_warning.grid(row=14, column=0, columnspan=2, padx=10, pady=5, sticky='nsew')

        submit_button = ttk.Button(form_frame, text='Submit Metrics', command=lambda: self.log_health_metrics(username, weight_entry.get(), date_entry.get(), activity_combobox.get(), sleep_entry.get(), weight_warning, date_warning, activity_warning, sleep_warning, general_warning, success_label))
        submit_button.grid(row=15, column=0, columnspan=2, padx=10, pady=5, sticky='nsew')

        form_frame.grid_rowconfigure(4, minsize=15)
        form_frame.grid_rowconfigure(7, minsize=15)
        form_frame.grid_rowconfigure(10, minsize=15)
        form_frame.grid_rowconfigure(13, minsize=15)

    def filter_health_logs_by_month(self, username, selected_month):
        try:
            cursor = conn.cursor()
            select_health_logs_query = "SELECT weight, date FROM health_metrics WHERE username = %s"
            cursor.execute(select_health_logs_query, (username,))
            health_data = cursor.fetchall()

            if health_data:
                filtered_data = [entry for entry in health_data if entry[1].strftime("%B") == selected_month]

                if filtered_data:
                    print(f"Heath Metrics Logs for {selected_month}:")
                    for entry in filtered_data:
                        print(f"{entry[1].strftime('%m/%d')}: Weight - {entry[0]} kg")
                else:
                    print(f"No health data available for {selected_month}.")
            else:
                print("No health data available.")

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if 'cursor' in locals():
                cursor.close()

    def log_health_metrics(self, username, weight, date, activity_level, sleep_duration, weight_warning, date_warning, activity_warning, sleep_warning, general_warning, success_label):
        try:
            if not weight or not date or not activity_level or not sleep_duration:
                general_warning.config(text='Please fill in all fields.')
                return

            if not weight.replace('.', '', 1).isdigit():
                weight_warning.config(text='Invalid weight. Please enter a numeric value.')
            else:
                weight_warning.config(text='')

            try:
                formatted_date = datetime.strptime(date, "%m/%d/%y").strftime("%Y-%m-%d")
                date_warning.config(text='')
            except ValueError:
                date_warning.config(text='Invalid date format. Please use mm/dd/yy.')

            if not activity_level:
                activity_warning.config(text='Please select an activity level.')
            else:
                activity_warning.config(text='')

            if not sleep_duration.isdigit():
                sleep_warning.config(text='Invalid sleep duration. Please enter a numeric value.')
            else:
                sleep_warning.config(text='')

            int_sleep_duration = int(sleep_duration)

            cursor = conn.cursor()

            # Insert into health_metrics table
            insert_health_metrics_query = "INSERT INTO health_metrics (username, weight, date, activity_level, sleep_duration) VALUES (%s, %s, %s, %s, %s)"
            health_metrics_data = (username, float(weight), formatted_date, activity_level, int_sleep_duration)
            cursor.execute(insert_health_metrics_query, health_metrics_data)

            # Insert into sleep_logs table
            insert_sleep_logs_query = "INSERT INTO sleep_logs (username, sleep_duration, date) VALUES (%s, %s, %s)"
            sleep_logs_data = (username, int_sleep_duration, formatted_date)
            cursor.execute(insert_sleep_logs_query, sleep_logs_data)

            conn.commit()

            print("Health Metrics and Sleep Logs logged successfully!")
            success_label.config(text='Health Metrics and Sleep Logs logged successfully!')
            general_warning.config(text='')

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if 'cursor' in locals():
                cursor.close()


    def nutrition_page(self, username):
        self.clear_frame()
        sidebar_frame = tk.Frame(self.root, width=400, bg='#22668D')
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        label = ttk.Frame(self.root, padding=20)
        label.pack(side=tk.LEFT, fill=tk.Y)

        buttons_frame = tk.Frame(sidebar_frame, bg='#F0F0F0')
        buttons_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.create_buttons(sidebar_frame, username)

        sign_out_button = ttk.Button(sidebar_frame, text='Sign Out', command=self.startup_page, style='NoBorder.TButton')
        sign_out_button.pack(pady=15, fill=tk.X)

        back_button = ttk.Button(self.root, text='Back', command=lambda: self.main_menu(username))
        back_button.pack(side='top', anchor='nw', padx=10, pady=10)

        header_image_path = r"C:\Users\Dream Events\Desktop\FPJ\headers\nutrition.png"
        if os.path.isfile(header_image_path):
            header_image = ImageTk.PhotoImage(Image.open(header_image_path).resize((789, 100)))
            header_label = tk.Label(self.root, image=header_image)
            header_label.image = header_image
            header_label.pack()

        form_frame = ttk.Frame(self.root, padding=20)
        form_frame.pack(expand=True, fill='both')

        goal_label = ttk.Label(form_frame, text='Select Weight Goal:', font=('Helvetica', 12))
        goal_label.grid(row=2, column=0, pady=5, sticky='nsew')

        goal_options = ['Losing Weight', 'Maintaining Weight', 'Gaining Weight']
        goal_var = tk.StringVar()
        goal_combobox = ttk.Combobox(form_frame, textvariable=goal_var, values=goal_options)
        goal_combobox.grid(row=2, column=1, pady=5, padx=(0, 10), sticky='nsew')

        weight_label = ttk.Label(form_frame, text='Weight (kg):', font=('Helvetica', 12))
        weight_label.grid(row=3, column=0, pady=5, sticky='nsew')

        weight_entry = ttk.Entry(form_frame, font=('Helvetica', 12))
        weight_entry.grid(row=3, column=1, pady=5, padx=(0, 10), sticky='nsew')

        height_label = ttk.Label(form_frame, text='Height (cm):', font=('Helvetica', 12))
        height_label.grid(row=4, column=0, pady=5, sticky='nsew')

        height_entry = ttk.Entry(form_frame, font=('Helvetica', 12))
        height_entry.grid(row=4, column=1, pady=5, padx=(0, 10), sticky='nsew')

        activity_label = ttk.Label(form_frame, text='Activity Level:', font=('Helvetica', 12))
        activity_label.grid(row=5, column=0, pady=5, sticky='nsew')

        activity_levels = ['Sedentary', 'Lightly Active', 'Moderately Active', 'Highly Active']
        activity_var = tk.StringVar()
        activity_combobox = ttk.Combobox(form_frame, textvariable=activity_var, values=activity_levels)
        activity_combobox.grid(row=5, column=1, pady=5, padx=(0, 10), sticky='w')

        calculate_and_get_suggestions_button = ttk.Button(
            form_frame,
            text='Calculate Calories and Get Food Suggestions',
            command=lambda: self.show_combined_results(
                weight_entry.get(),
                height_entry.get(),
                activity_combobox.get(),
                goal_combobox.get(),
                username
            )
        )
        calculate_and_get_suggestions_button.grid(row=6, column=1, pady=10, padx=10, sticky='nsew')

        form_frame.columnconfigure(0, weight=1)
        form_frame.columnconfigure(1, weight=1)

    def show_combined_results(self, weight, height, activity_level, goal, username):
        try:
            self.clear_frame()

            sidebar_frame = tk.Frame(self.root, width=400, bg='#22668D')
            sidebar_frame.grid(row=0, column=0, sticky='nsw')

            content_frame = ttk.Frame(self.root, padding=20)
            content_frame.grid(row=0, column=1, sticky='nsew')
            content_frame.columnconfigure(0, weight=1)

            self.create_buttons(sidebar_frame, username)

            sign_out_button = ttk.Button(sidebar_frame, text='Sign Out', command=self.startup_page, style='NoBorder.TButton')
            sign_out_button.pack(pady=15, fill=tk.X)

            back_button = ttk.Button(content_frame, text='Back', command=lambda: self.nutrition_page(username))
            back_button.grid(row=0, column=0, padx=10, pady=10, sticky='sw')

            weight = float(weight)
            height = float(height)

            bmi = self.calculate_bmi(weight, height)
            self.bmi = bmi

            activity_multipliers = {
                'Sedentary': 1.2,
                'Lightly Active': 1.375,
                'Moderately Active': 1.55,
                'Highly Active': 1.725
            }

            activity_multiplier = activity_multipliers.get(activity_level, 1.2)

            goal_calorie_adjustments = {
                'Losing Weight': -500,
                'Maintaining Weight': 0,
                'Gaining Weight': 500
            }

            calorie_adjustment = goal_calorie_adjustments.get(goal, 0)

            bmr = 10 * weight + 6.25 * height - 5
            tdee = bmr * activity_multiplier + calorie_adjustment
            self.bmi = bmi

            result_label = ttk.Label(content_frame, text=f'Total Daily Calories: {tdee:.2f} calories', font=('Helvetica', 18))
            result_label.grid(row=1, column=0, padx=10, pady=20, sticky='nsew')

            image_paths = {
                'Losing Weight': r'C:\Users\Dream Events\Desktop\FPJ\losing.png',
                'Maintaining Weight': r'C:\Users\Dream Events\Desktop\FPJ\maintain.png',
                'Gaining Weight': r'C:\Users\Dream Events\Desktop\FPJ\gain.png',
            }
            self.images = {goal: PhotoImage(file=image_path) for goal, image_path in image_paths.items()}

            img_label = Label(content_frame, image=self.images[goal])
            img_label.grid(row=2, column=0, padx=10, pady=20, sticky='nw')

        except ValueError:
            print("Error: Please enter valid numerical values for weight and height.")
        except Exception as e:
            print(f"Error: {e}")

    def calculate_bmi(self, weight_kg, height_cm):
        height_m = height_cm / 100
        return weight_kg / (height_m ** 2)

    def classify_bmi(bmi):
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 25:
            return "Normal weight"
        elif 25 <= bmi < 30:
            return "Overweight"
        else:
            return "Obese"

if __name__ == '__main__':
    try:
        cursor = conn.cursor()
        create_users_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50),
            pin VARCHAR(4),
            email VARCHAR(100),
            initial_weight FLOAT,
            profile_picture_path VARCHAR(255) DEFAULT NULL
            )
            """
        cursor.execute(create_users_table_query)

        create_workouts_table_query = """
        CREATE TABLE IF NOT EXISTS workouts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50),
            exercise_type VARCHAR(100),
            duration INT,
            date DATE
        )
        """
        cursor.execute(create_workouts_table_query)
        conn.commit()

        create_health_metrics_table_query = """
        CREATE TABLE IF NOT EXISTS health_metrics (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50),
            weight DECIMAL(5, 2),
            date DATE,
            activity_level VARCHAR(20),
            sleep_duration INT  # Added sleep_duration column
        )
        """
        cursor.execute(create_health_metrics_table_query)
        conn.commit()

        create_sleep_logs_table_query = """
        CREATE TABLE IF NOT EXISTS sleep_logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50),
            sleep_duration INT,
            date DATE
        )
        """
        cursor.execute(create_sleep_logs_table_query)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if 'cursor' in locals():
            cursor.close()

    root = tk.Tk()
    style = ttk.Style(root)

    sv_ttk.set_theme("dark")

    root.geometry("1200x800")

    app = FitnessApp(root)
    root.mainloop()

    conn.close()
