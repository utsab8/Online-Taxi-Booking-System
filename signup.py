import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
from db_connection import get_connection
import navigation

class SignupPage:
    def __init__(self, master):
        self.master = master
        self.master.title('Signup')
        self.master.geometry("800x600")
        self.master.configure(bg="#f0f4f8")
        

        # Main Container
        self.main_frame = tk.Frame(self.master, bg="#ffffff", width=900, height=700)
        self.main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.main_frame.pack_propagate(False)

        # Left side - Decorative section
        self.left_frame = tk.Frame(self.main_frame, width=450, height=700, bg="#4a90e2")
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.left_frame.pack_propagate(False)

        # Signup text
        signup_label = tk.Label(self.left_frame, text="Create Account", 
                                font=("Arial", 28, "bold"), 
                                fg="white", 
                                bg="#4a90e2")
        signup_label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        slogan_label = tk.Label(self.left_frame, 
                                text="Join our platform today!", 
                                font=("Arial", 14), 
                                fg="white", 
                                bg="#4a90e2")
        slogan_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Right side - Signup form
        self.right_frame = tk.Frame(self.main_frame, width=450, height=700, bg="white")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        self.right_frame.pack_propagate(False)

        # User Type
        user_type_label = tk.Label(self.right_frame, text="User Type", 
                                   font=("Arial", 12), 
                                   fg="#666666", 
                                   bg="white")
        user_type_label.place(x=75, y=50)

        self.user_type_var = tk.StringVar(value="Customer")
        self.user_type_dropdown = ttk.Combobox(self.right_frame, 
                                               textvariable=self.user_type_var, 
                                               values=["Customer", "Driver"], 
                                               state="readonly", 
                                               font=("Arial", 14), 
                                               width=25)
        self.user_type_dropdown.place(x=75, y=80, height=40)
        self.user_type_dropdown.bind("<<ComboboxSelected>>", self.toggle_driver_fields)

        # Full Name
        full_name_label = tk.Label(self.right_frame, text="Full Name", 
                                   font=("Arial", 12), 
                                   fg="#666666", 
                                   bg="white")
        full_name_label.place(x=75, y=130)

        self.full_name_entry = ttk.Entry(self.right_frame, 
                                         font=("Arial", 14), 
                                         width=30)
        self.full_name_entry.place(x=75, y=160, height=40)

        # Email
        email_label = tk.Label(self.right_frame, text="Email", 
                               font=("Arial", 12), 
                               fg="#666666", 
                               bg="white")
        email_label.place(x=75, y=210)

        self.email_entry = ttk.Entry(self.right_frame, 
                                     font=("Arial", 14), 
                                     width=30)
        self.email_entry.place(x=75, y=240, height=40)

        # Phone
        phone_label = tk.Label(self.right_frame, text="Phone Number", 
                               font=("Arial", 12), 
                               fg="#666666", 
                               bg="white")
        phone_label.place(x=75, y=290)

        self.phone_entry = ttk.Entry(self.right_frame, 
                                     font=("Arial", 14), 
                                     width=30)
        self.phone_entry.place(x=75, y=320, height=40)

        # Password
        password_label = tk.Label(self.right_frame, text="Password", 
                                  font=("Arial", 12), 
                                  fg="#666666", 
                                  bg="white")
        password_label.place(x=75, y=370)

        self.password_entry = ttk.Entry(self.right_frame, 
                                        show="*", 
                                        font=("Arial", 14), 
                                        width=30)
        self.password_entry.place(x=75, y=400, height=40)

        # Confirm Password
        confirm_password_label = tk.Label(self.right_frame, text="Confirm Password", 
                                          font=("Arial", 12), 
                                          fg="#666666", 
                                          bg="white")
        confirm_password_label.place(x=75, y=450)

        self.confirm_password_entry = ttk.Entry(self.right_frame, 
                                                show="*", 
                                                font=("Arial", 14), 
                                                width=30)
        self.confirm_password_entry.place(x=75, y=480, height=40)

        # Driver-specific fields
        self.license_label = tk.Label(self.right_frame, text="License Number", 
                                      font=("Arial", 12), 
                                      fg="#666666", 
                                      bg="white")
        self.license_entry = ttk.Entry(self.right_frame, 
                                       font=("Arial", 14), 
                                       width=30)

        self.car_label = tk.Label(self.right_frame, text="Car Number", 
                                  font=("Arial", 12), 
                                  fg="#666666", 
                                  bg="white")
        self.car_entry = ttk.Entry(self.right_frame, 
                                   font=("Arial", 14), 
                                   width=30)

        # Submit Button
        submit_button = tk.Button(self.right_frame, 
                                  text="Create Account", 
                                  font=("Arial", 16, "bold"), 
                                  bg="#4a90e2", 
                                  fg="white", 
                                  borderwidth=0, 
                                  activebackground="#3a80d2",
                                  command=self.validate_and_process_registration)
        submit_button.place(x=75, y=570, width=300, height=50)

        # Login Link
        login_text = tk.Label(self.right_frame, 
                              text="Already have an account? ", 
                              font=("Arial", 12), 
                              bg="white", 
                              fg="#666666")
        login_text.place(x=140, y=640)

        login_link = tk.Label(self.right_frame, 
                              text="Login", 
                              font=("Arial", 12, "underline"), 
                              bg="white", 
                              fg="#4a90e2", 
                              cursor="hand2")
        login_link.place(x=330, y=640)
        login_link.bind("<Button-1>", self.navigate_to_login)

        # Initially hide driver-specific fields
        self.toggle_driver_fields()

    def toggle_driver_fields(self, event=None):
        """Toggle visibility of driver-specific fields."""
        user_type = self.user_type_var.get()
        if user_type == "Driver":
            self.license_label.place(x=75, y=530)
            self.license_entry.place(x=75, y=560, height=40)
            self.car_label.place(x=75, y=610)
            self.car_entry.place(x=75, y=640, height=40)
        else:
            self.license_label.place_forget()
            self.license_entry.place_forget()
            self.car_label.place_forget()
            self.car_entry.place_forget()

    def register_user(self, full_name, email, phone, password, user_type, car_number=None, license_number=None):
        """
        Register a new user in the database.
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()

            # Check for duplicate email
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                messagebox.showerror("Registration Error", "Email already exists.")
                return False

            # Prepare SQL query and parameters based on user type
            if user_type == "Driver":
                query = """
                    INSERT INTO users (user_type, full_name, email, phone, password, car_number, license_number)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                params = ("Driver", full_name, email, phone, password, car_number, license_number)
            else:
                query = """
                    INSERT INTO users (user_type, full_name, email, phone, password)
                    VALUES (%s, %s, %s, %s, %s)
                """
                params = ("Customer", full_name, email, phone, password)

            cursor.execute(query, params)
            conn.commit()
            messagebox.showinfo("Success", "Registration successful!")
            return True

        except Exception as e:
            conn.rollback()
            messagebox.showerror("Registration Error", f"An error occurred: {e}")
            return False

        finally:
            cursor.close()
            conn.close()

    def navigate_to_login(self, event=None):
        """Close the signup window and navigate to the login screen."""
        self.master.destroy()
        navigation.navigate_to_login()

    def validate_and_process_registration(self):
        """Validate user inputs and attempt registration."""
        try:
            # Collect user input values
            full_name = self.full_name_entry.get().strip()
            email = self.email_entry.get().strip()
            phone = self.phone_entry.get().strip()
            password = self.password_entry.get()
            confirm_password = self.confirm_password_entry.get()
            user_type = self.user_type_var.get()

            # Collect driver-specific fields if user type is 'Driver'
            car_number = self.car_entry.get().strip() if user_type == "Driver" else None
            license_number = self.license_entry.get().strip() if user_type == "Driver" else None

            # Input validation
            errors = []
            if not full_name:
                errors.append("Full Name is required.")
            if not email:
                errors.append("Email is required.")
            if not phone.isdigit() or len(phone) < 5:
                errors.append("Phone number must be numeric and at least 5 digits.")
            if not password or len(password) < 5:
                errors.append("Password must be at least 5 characters.")
            if password != confirm_password:
                errors.append("Passwords do not match.")
            if user_type == "Driver" and (not car_number or not license_number):
                errors.append("Car number and license number are required for drivers.")

            if errors:
                messagebox.showerror("Registration Error", "\n".join(errors))
                return

            # Attempt registration
            if self.register_user(full_name, email, phone, password, user_type, car_number, license_number):
                self.navigate_to_login()

        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

def show_signup_page():
    """Display the signup page."""
    root = tk.Tk()
    SignupPage(root)
    root.mainloop()

# Run the signup page when the script is executed
if __name__ == "__main__":
    show_signup_page()