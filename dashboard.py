from tkinter import *  # Importing all widgets from Tkinter for GUI development
from tkinter import messagebox, ttk  # For showing message boxes and using Treeview
from tkcalendar import DateEntry  # For selecting dates using a calendar widget
import random  # For generating random fare values
import pymysql  # For connecting to the MySQL database
from datetime import datetime  # For working with date and time
from db_connection import get_connection  # Custom method for database connection

class RideHistoryWindow:
    def __init__(self, parent):
        """
        Initializes the RideHistoryWindow with an enhanced design.
        parent: The main window from which this window is opened.
        """
        self.window = Toplevel(parent)
        self.window.title('Ride History')
        self.window.geometry('1000x600')
        self.window.configure(bg="#1E1E2C")

        # Custom title frame
        title_frame = Frame(self.window, bg="#2C2C3E", height=80)
        title_frame.pack(fill=X)
        title_frame.pack_propagate(False)

        Label(
            title_frame,
            text='Ride History',
            font=('Segoe UI', 24, 'bold'),
            bg="#2C2C3E",
            fg="white"
        ).pack(pady=20, padx=20, anchor='w')

        # Treeview with custom style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Custom.Treeview", 
            background="#1E1E2C", 
            foreground="white", 
            fieldbackground="#1E1E2C",
            font=('Segoe UI', 10)
        )
        style.configure("Custom.Treeview.Heading", 
            background="#2C2C3E", 
            foreground="white", 
            font=('Segoe UI', 12, 'bold')
        )
        style.map('Custom.Treeview', 
            background=[('selected', '#3498DB')],
            foreground=[('selected', 'white')]
        )

        self.ride_list = ttk.Treeview(
            self.window,
            columns=('Date', 'From', 'To', 'Fare', 'Status'),
            show='headings',
            style="Custom.Treeview"
        )

        # Configure column headings
        self.ride_list.heading('Date', text='Date')
        self.ride_list.heading('From', text='From')
        self.ride_list.heading('To', text='To')
        self.ride_list.heading('Fare', text='Fare')
        self.ride_list.heading('Status', text='Status')

        self.ride_list.column('Date', width=150, anchor='center')
        self.ride_list.column('From', width=200, anchor='center')
        self.ride_list.column('To', width=200, anchor='center')
        self.ride_list.column('Fare', width=100, anchor='center')
        self.ride_list.column('Status', width=100, anchor='center')

        self.ride_list.pack(padx=20, pady=10, fill=BOTH, expand=True)

        # Enhanced button design
        btn_frame = Frame(self.window, bg="#1E1E2C")
        btn_frame.pack(pady=10)

        cancel_btn = Button(
            btn_frame, 
            text="Cancel Ride", 
            command=self.cancel_ride,
            bg="#E74C3C",
            fg="white",
            font=('Segoe UI', 12, 'bold'),
            padx=20,
            pady=10,
            relief=FLAT
        )
        cancel_btn.pack()

        self.load_history()  # Load ride history data into the Treeview

    def load_history(self):
        """Fetches ride history from the database and populates the Treeview widget."""
        try:
            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT travel_date, current_location, target_location, fare, booking_status
                FROM rides
                ORDER BY travel_date DESC
                LIMIT 20
            """)
            rides = cursor.fetchall()

            for item in self.ride_list.get_children():
                self.ride_list.delete(item)

            for ride in rides:
                self.ride_list.insert('', 'end', values=ride)

        except pymysql.MySQLError as error:
            messagebox.showerror("Database Error", f"Could not fetch ride history: {error}")
        finally:
            cursor.close()
            connection.close()

    def cancel_ride(self):
        """Cancels the selected ride by updating its status in the database."""
        selected_item = self.ride_list.focus()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a ride to cancel.")
            return

        ride_values = self.ride_list.item(selected_item)['values']
        travel_date, current_location, target_location = ride_values[0], ride_values[1], ride_values[2]

        try:
            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE rides
                SET booking_status = 'Cancelled'
                WHERE travel_date = %s AND current_location = %s AND target_location = %s
            """, (travel_date, current_location, target_location))
            connection.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo("Ride Cancelled", "The selected ride has been cancelled.")
                self.load_history()  # Refresh ride history
            else:
                messagebox.showwarning("Cancellation Failed", "Unable to cancel the selected ride.")

        except pymysql.MySQLError as error:
            messagebox.showerror("Database Error", f"An error occurred while canceling the ride: {error}")
        finally:
            cursor.close()
            connection.close()

class RideDashboard:
    def __init__(self, user_id):
        """
        Initializes the RideDashboard with an enhanced design.
        user_id: The user ID for the current session.
        """
        self.user_id = user_id
        self.root = Tk()
        self.root.title('Ride Booking Dashboard')
        self.root.geometry("1400x900")
        self.root.configure(bg="#1E1E2C")

        # Custom styling
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure custom styles
        self.style.configure("TLabel", 
            background="#1E1E2C", 
            foreground="white", 
            font=('Segoe UI', 12)
        )
        self.style.configure("TEntry", 
            background="#2C2C3E", 
            foreground="white", 
            font=('Segoe UI', 12)
        )
        self.style.configure("TButton", 
            background="#3498DB", 
            foreground="white", 
            font=('Segoe UI', 12, 'bold')
        )

        self.create_dashboard()

    def create_dashboard(self):
        """Creates the layout for the dashboard with an enhanced design."""
        # Main frame with dark background
        main_frame = Frame(self.root, bg="#1E1E2C")
        main_frame.pack(padx=20, pady=20, fill=BOTH, expand=True)

        # Custom title frame
        title_frame = Frame(main_frame, bg="#2C2C3E", height=100)
        title_frame.pack(fill=X)
        title_frame.pack_propagate(False)

        Label(
            title_frame,
            text='Book Your Ride',
            font=('Segoe UI', 28, 'bold'),
            bg="#2C2C3E",
            fg="white"
        ).pack(pady=25, padx=20, anchor='w')

        # Input frame with improved design
        input_frame = Frame(main_frame, bg="#1E1E2C")
        input_frame.pack(padx=50, pady=20)

        # Input fields with enhanced styling
        input_configs = {
            'width': 50, 
            'font': ('Segoe UI', 12), 
            'bg': "#2C2C3E", 
            'fg': "white", 
            'insertbackground': 'white',
            'relief': FLAT,
            'highlightthickness': 1,
            'highlightcolor': '#3498DB',
            'highlightbackground': "#2C2C3E"
        }

        # Labels and Entries
        location_label = ttk.Label(input_frame, text="Current Location")
        location_label.pack(anchor='w', pady=(0, 5))
        self.current_location = Entry(input_frame, **input_configs)
        self.current_location.pack(pady=(0, 15))

        dest_label = ttk.Label(input_frame, text="Destination")
        dest_label.pack(anchor='w', pady=(0, 5))
        self.target_location = Entry(input_frame, **input_configs)
        self.target_location.pack(pady=(0, 15))

        date_label = ttk.Label(input_frame, text="Travel Date")
        date_label.pack(anchor='w', pady=(0, 5))
        self.travel_date = DateEntry(input_frame, width=20, date_pattern='yyyy-mm-dd', 
            background='#3498DB', foreground='white', 
            headersbackground='#2C2C3E', normalbackground='#1E1E2C', 
            weekendbackground='#2980B9', othermonthbackground='#34495E')
        self.travel_date.pack(pady=(0, 15))

        time_label = ttk.Label(input_frame, text="Booking Time")
        time_label.pack(anchor='w', pady=(0, 5))
        self.booking_time = Entry(input_frame, **input_configs)
        self.booking_time.pack(pady=(0, 15))

        # Fare display with enhanced styling
        self.fare_var = StringVar(value="Fare: RS0.00")
        fare_label = Label(
            input_frame,
            textvariable=self.fare_var,
            font=('Segoe UI', 16, 'bold'),
            bg="#1E1E2C",
            fg="#2ECC71"
        )
        fare_label.pack(pady=(10, 15))

        # Button frame with modern design
        btn_frame = Frame(input_frame, bg="#1E1E2C")
        btn_frame.pack(fill=X, pady=10)

        button_configs = {
            'font': ('Segoe UI', 12, 'bold'),
            'relief': FLAT,
            'padx': 20,
            'pady': 10
        }

        fare_btn = Button(
            btn_frame, 
            text="Generate Fare", 
            command=self.auto_generate_fare,
            bg="#3498DB", 
            fg="white",
            **button_configs
        )
        fare_btn.pack(side=LEFT, padx=5, expand=True)

        book_btn = Button(
            btn_frame, 
            text="Book Ride", 
            command=self.find_drive_action,
            bg="#2ECC71", 
            fg="white",
            **button_configs
        )
        book_btn.pack(side=LEFT, padx=5, expand=True)

        history_btn = Button(
            btn_frame, 
            text="Ride History", 
            command=self.open_history_window,
            bg="#F39C12", 
            fg="white",
            **button_configs
        )
        history_btn.pack(side=LEFT, padx=5, expand=True)

        logout_btn = Button(
            btn_frame, 
            text="Logout", 
            command=self.logout_action,
            bg="#E74C3C", 
            fg="white",
            **button_configs
        )
        logout_btn.pack(side=LEFT, padx=5, expand=True)

    def open_history_window(self):
        """Opens the RideHistoryWindow."""
        RideHistoryWindow(self.root)

    def auto_generate_fare(self):
        """Generates a random fare between 100 and 500."""
        fare = round(random.uniform(100, 500), 2)
        self.fare_var.set(f"Fare: RS{fare}")
        return fare

    def find_drive_action(self):
        """Saves the ride booking information into the database."""
        current_location = self.current_location.get()
        target_location = self.target_location.get()
        travel_date = self.travel_date.get()
        booking_time = self.booking_time.get()
        fare = self.auto_generate_fare()

        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO rides 
                (current_location, target_location, travel_date, booking_time, fare, booking_status)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (current_location, target_location, travel_date, booking_time, fare, 'Scheduled')
            )
            connection.commit()
            messagebox.showinfo("Ride Booked", "Your ride has been successfully booked!")
        except pymysql.MySQLError as error:
            messagebox.showerror("Database Error", f"An error occurred while booking your ride: {error}")
        finally:
            cursor.close()
            connection.close()

    def logout_action(self):
        """Closes the application window."""
        self.root.destroy()

    def run(self):
        """Starts the Tkinter event loop."""
        self.root.mainloop()

def open_dashboard(user_id):
    """
    Starts the ride dashboard for a given user.
    """
    dashboard = RideDashboard(user_id)
    dashboard.run()