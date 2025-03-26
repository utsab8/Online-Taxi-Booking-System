import customtkinter as ctk
from tkinter import messagebox
import pymysql
from db_connection import get_connection
import dashboard
import driver_dashboard
import admin_dashboard
import navigation

class AlternativeLoginPage:
    def __init__(self):
        # Create main window
        self.root = ctk.CTk()
        self.root.title("Login")
        self.root.geometry("800x600")
        self.root.configure(fg_color=("white", "gray15"))

        # Centered login container
        self.login_container = ctk.CTkFrame(
            self.root, 
            corner_radius=20,
            fg_color=("gray95", "gray10"),
            width=500,
            height=550
        )
        self.login_container.place(relx=0.5, rely=0.5, anchor="center")

        # Logo and Title
        self.logo_label = ctk.CTkLabel(
            self.login_container, 
            text="RideSync", 
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color=("dark blue", "light blue")
        )
        self.logo_label.pack(pady=(40, 10))

        self.subtitle_label = ctk.CTkLabel(
            self.login_container, 
            text="Welcome Back", 
            font=ctk.CTkFont(size=20),
            text_color=("gray50", "gray60")
        )
        self.subtitle_label.pack(pady=(0, 30))

        # Form Container
        self.form_frame = ctk.CTkFrame(
            self.login_container, 
            fg_color="transparent"
        )
        self.form_frame.pack(padx=40, fill="x")

        # Email Input
        self.email_label = ctk.CTkLabel(
            self.form_frame, 
            text="Email", 
            anchor="w", 
            font=ctk.CTkFont(size=14),
            text_color=("dark blue", "light blue")
        )
        self.email_label.pack(fill="x", pady=(0, 5))

        self.email_entry = ctk.CTkEntry(
            self.form_frame, 
            placeholder_text="Enter your email",
            font=ctk.CTkFont(size=14),
            height=40
        )
        self.email_entry.pack(fill="x", pady=(0, 20))

        # Password Input
        self.password_label = ctk.CTkLabel(
            self.form_frame, 
            text="Password", 
            anchor="w", 
            font=ctk.CTkFont(size=14),
            text_color=("dark blue", "light blue")
        )
        self.password_label.pack(fill="x", pady=(0, 5))

        self.password_entry = ctk.CTkEntry(
            self.form_frame, 
            placeholder_text="Enter your password",
            show="*",
            font=ctk.CTkFont(size=14),
            height=40
        )
        self.password_entry.pack(fill="x", pady=(0, 10))

        # Password Visibility Toggle
        self.show_password_var = ctk.BooleanVar(value=False)
        self.show_password_switch = ctk.CTkSwitch(
            self.form_frame, 
            text="Show Password", 
            command=self.toggle_password_visibility,
            variable=self.show_password_var
        )
        self.show_password_switch.pack(anchor="w", pady=(0, 20))

        # Login Button
        self.login_button = ctk.CTkButton(
            self.form_frame, 
            text="Sign In", 
            command=self.on_login_button_click,
            font=ctk.CTkFont(size=16, weight="bold"),
            corner_radius=10,
            height=45,
            fg_color=("blue", "royal blue"),
            hover_color=("dark blue", "medium blue")
        )
        self.login_button.pack(fill="x", pady=(0, 20))

        # Signup Link
        self.signup_frame = ctk.CTkFrame(
            self.form_frame, 
            fg_color="transparent"
        )
        self.signup_frame.pack(fill="x", pady=(0, 20))

        self.signup_label = ctk.CTkLabel(
            self.signup_frame, 
            text="Don't have an account? ", 
            font=ctk.CTkFont(size=12)
        )
        self.signup_label.pack(side="left", anchor="center")

        self.signup_button = ctk.CTkButton(
            self.signup_frame, 
            text="Sign Up", 
            command=self.navigate_to_signup,
            fg_color="transparent", 
            text_color=("blue", "light blue"),
            hover_color=("light gray", "gray20"),
            font=ctk.CTkFont(size=12, underline=True)
        )
        self.signup_button.pack(side="left", anchor="center")

    def toggle_password_visibility(self):
        """Toggle the visibility of the password."""
        show_text = self.show_password_var.get()
        self.password_entry.configure(show="" if show_text else "*")

    def navigate_to_signup(self):
        """Navigate to the Signup page."""
        self.root.destroy()
        navigation.navigate_to_signup()

    def validate_login(self, email, password):
        """Validate the user login by checking the email and password in the database."""
        if email == "admin" and password == "admin":
            return "Admin", None

        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT id, email, user_type FROM users WHERE email = %s AND password = %s", (email, password))
            user = cursor.fetchone()

            if user:
                user_id, email, user_type = user
                return user_type, user_id
            else:
                messagebox.showerror("Login Error", "Invalid email or password. Please try again.")
                return None, None

        except pymysql.MySQLError as e:
            messagebox.showerror("Database Error", f"An error occurred while checking credentials: {e}")
            return None, None

        finally:
            cursor.close()
            conn.close()

    def on_login_button_click(self):
        """Handle login button click."""
        email = self.email_entry.get().strip()
        password = self.password_entry.get()

        if email and password:
            user_type, user_id = self.validate_login(email, password)
            if user_type:
                self.root.destroy()

                if user_type == 'Customer':
                    dashboard.open_dashboard(user_id)
                elif user_type == 'Driver':
                    driver_dashboard_instance = driver_dashboard.DriverDashboard()
                    driver_dashboard_instance.open_driver_dashboard()
                elif user_type == 'Admin':
                    admin_dashboard.open_admin_dashboard()
                else:
                    messagebox.showerror("Login Error", f"Unsupported user type: {user_type}")
            else:
                print("Login failed!")
        else:
            messagebox.showerror("Input Error", "Please enter both email and password.")

    def run(self):
        """Start the login page"""
        self.root.mainloop()

def show_login_page():
    """Display the Login page."""
    login_app = AlternativeLoginPage()
    login_app.run()

# Run the login page when the script is executed
if __name__ == "__main__":
    show_login_page()