import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import pymysql
from db_connection import get_connection

# Set the default color theme
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

class DriverDashboard:
    def __init__(self):
        # Create the main window
        self.root = ctk.CTk()
        self.root.title("RideSync - Driver Dashboard")
        self.root.geometry("1100x700")
        
        # Configure grid layout
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar_frame = ctk.CTkFrame(self.root, width=240, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        # Sidebar logo
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="RideSync Driver", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Sidebar buttons
        self.rides_button = ctk.CTkButton(
            self.sidebar_frame, 
            text="Available Rides", 
            command=self.show_rides_view
        )
        self.rides_button.grid(row=1, column=0, padx=20, pady=10)

        self.history_button = ctk.CTkButton(
            self.sidebar_frame, 
            text="Ride History", 
            command=self.show_history_view
        )
        self.history_button.grid(row=2, column=0, padx=20, pady=10)

        # Main content frame
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.grid(row=0, column=1, columnspan=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        # Create rides view
        self.create_rides_view()
        
        # Add action buttons
        self.action_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.action_frame.grid(row=1, column=1, columnspan=3, padx=(20, 20), pady=(0, 20), sticky="ew")

        # Ride action buttons
        self.accept_button = ctk.CTkButton(
            self.action_frame, 
            text="Accept Ride", 
            command=self.accept_ride,
            fg_color="green",
            hover_color="darkgreen"
        )
        self.accept_button.pack(side="left", padx=10, expand=True, fill="x")

        self.reject_button = ctk.CTkButton(
            self.action_frame, 
            text="Reject Ride", 
            command=self.cancel_ride,
            fg_color="red",
            hover_color="darkred"
        )
        self.reject_button.pack(side="left", padx=10, expand=True, fill="x")

    def open_driver_dashboard(self):
        """Method to open and start the driver dashboard"""
        self.root.mainloop()

    def create_rides_view(self):
        """Create the rides treeview"""
        # Destroy any existing widgets in main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Rides label
        self.rides_label = ctk.CTkLabel(
            self.main_frame, 
            text="Available Rides", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.rides_label.grid(row=0, column=0, padx=20, pady=(10, 10), sticky="w")

        # Create treeview with scrollbar
        self.tree_frame = ctk.CTkFrame(self.main_frame)
        self.tree_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.tree_frame.grid_columnconfigure(0, weight=1)
        self.tree_frame.grid_rowconfigure(0, weight=1)

        # Treeview
        columns = ("ID", "Pickup", "Drop", "Date", "Time", "Fare", "Status")
        self.tree = tk.ttk.Treeview(
            self.tree_frame, 
            columns=columns, 
            show="headings", 
            selectmode="browse"
        )

        # Configure columns
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")

        # Scrollbar
        self.tree_scrollbar = ctk.CTkScrollbar(
            self.tree_frame, 
            orientation="vertical", 
            command=self.tree.yview
        )
        self.tree.configure(yscroll=self.tree_scrollbar.set)

        # Place treeview and scrollbar
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.tree_scrollbar.grid(row=0, column=1, sticky="ns")

        # Fetch rides
        self.fetch_rides()

    def fetch_rides(self):
        """Fetch the rides data to display in the Treeview."""
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT r.id, r.current_location, r.target_location, r.travel_date, r.booking_time, r.fare, r.booking_status
                FROM rides r
                WHERE r.booking_status = 'Scheduled'
            """)
            rides = cursor.fetchall()

            # Clear the previous data in the tree
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Add ride data to the Treeview
            for row in rides:
                self.tree.insert("", tk.END, values=row)

            conn.commit()

        except pymysql.MySQLError as e:
            messagebox.showerror("Database Error", f"An error occurred while fetching ride data: {e}")
        finally:
            cursor.close()
            conn.close()

    def show_rides_view(self):
        """Show the available rides view"""
        self.create_rides_view()

    def show_history_view(self):
        """Show the ride history view"""
        # Destroy any existing widgets in main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # History label
        self.history_label = ctk.CTkLabel(
            self.main_frame, 
            text="Ride History", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.history_label.grid(row=0, column=0, padx=20, pady=(10, 10), sticky="w")

        # Create treeview with scrollbar
        self.history_frame = ctk.CTkFrame(self.main_frame)
        self.history_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.history_frame.grid_columnconfigure(0, weight=1)
        self.history_frame.grid_rowconfigure(0, weight=1)

        # Treeview
        columns = ("ID", "Pickup", "Drop", "Date", "Time", "Fare", "Status")
        self.history_tree = tk.ttk.Treeview(
            self.history_frame, 
            columns=columns, 
            show="headings", 
            selectmode="browse"
        )

        # Configure columns
        for col in columns:
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=100, anchor="center")

        # Scrollbar
        self.history_scrollbar = ctk.CTkScrollbar(
            self.history_frame, 
            orientation="vertical", 
            command=self.history_tree.yview
        )
        self.history_tree.configure(yscroll=self.history_scrollbar.set)

        # Place treeview and scrollbar
        self.history_tree.grid(row=0, column=0, sticky="nsew")
        self.history_scrollbar.grid(row=0, column=1, sticky="ns")

        # Fetch history
        self.fetch_history()

    def fetch_history(self):
        """Fetch the ride history data to display in the Treeview."""
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT r.id, r.current_location, r.target_location, r.travel_date, r.booking_time, r.fare, r.booking_status
                FROM rides r
                WHERE r.booking_status IN ('Started', 'Rejected')
            """)
            rides = cursor.fetchall()

            # Clear the previous data in the tree
            for item in self.history_tree.get_children():
                self.history_tree.delete(item)

            # Add ride history data to the Treeview
            for row in rides:
                self.history_tree.insert("", tk.END, values=row)

            conn.commit()

        except pymysql.MySQLError as e:
            messagebox.showerror("Database Error", f"An error occurred while fetching ride history: {e}")
        finally:
            cursor.close()
            conn.close()

    def accept_ride(self):
        """Accept the selected ride by updating its status to 'Started'."""
        selected_item = self.tree.selection()
        if selected_item:
            ride_id = self.tree.item(selected_item)["values"][0]
            try:
                conn = get_connection()
                cursor = conn.cursor()

                # Update ride status to "Started"
                cursor.execute("""
                    UPDATE rides
                    SET booking_status = 'Started'
                    WHERE id = %s
                """, (ride_id,))

                conn.commit()
                
                # Show success message
                messagebox.showinfo("Ride Accepted", "You have successfully accepted the ride.")

                # Refresh the ride list after acceptance
                self.fetch_rides()

            except pymysql.MySQLError as e:
                messagebox.showerror("Database Error", f"An error occurred while accepting the ride: {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            messagebox.showwarning("No Ride Selected", "Please select a ride to accept.")

    def cancel_ride(self):
        """Cancel the selected ride by updating its status to 'Rejected'."""
        selected_item = self.tree.selection()
        if selected_item:
            ride_id = self.tree.item(selected_item)["values"][0]
            try:
                conn = get_connection()
                cursor = conn.cursor()

                # Update ride status to "Rejected"
                cursor.execute("""
                    UPDATE rides
                    SET booking_status = 'Rejected'
                    WHERE id = %s
                """, (ride_id,))

                conn.commit()
                messagebox.showinfo("Ride Rejected", "You have successfully rejected the ride.")

                # Refresh the ride list after rejection
                self.fetch_rides()

            except pymysql.MySQLError as e:
                messagebox.showerror("Database Error", f"An error occurred while rejecting the ride: {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            messagebox.showwarning("No Ride Selected", "Please select a ride to reject.")

if __name__ == "__main__":
    app = DriverDashboard()
    app.open_driver_dashboard()
