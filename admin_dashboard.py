# Import necessary modules for creating the Tkinter GUI and handling MySQL connections
import tkinter as tk
from tkinter import ttk, messagebox  # Import for displaying messages and creating the tree view
import pymysql  # MySQL client for database connection
from db_connection import get_connection  # Custom function to get the database connection
import customtkinter as ctk  # Modern Tkinter alternative for enhanced design

# Set the appearance mode and color theme
ctk.set_appearance_mode("light")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

def open_admin_dashboard():
    """
    Function to open the admin dashboard window with an enhanced design, 
    display ride data, and provide options to refresh the list of rides and assign a driver.
    """
    # Create the main window for the dashboard using customtkinter
    root = ctk.CTk()
    root.title("Admin Dashboard - Ride Management")
    root.geometry("1000x600")  # Increased window size for better readability

    # Configure the grid layout
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)

    # Create a stylish header frame
    header_frame = ctk.CTkFrame(root, corner_radius=10, fg_color="#2C3E50")
    header_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

    # Stylish header label
    header_label = ctk.CTkLabel(
        header_frame, 
        text="Ride Management Dashboard", 
        font=("Arial", 24, "bold"),
        text_color="white"
    )
    header_label.pack(pady=15, padx=20)

    # Create the Treeview widget with a more modern look
    columns = ("ID", "Pickup", "Drop", "Date", "Time", "Fare", "Status")
    tree_frame = ctk.CTkFrame(root, corner_radius=10)
    tree_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

    # Scrollbar for the Treeview
    tree_scroll = ctk.CTkScrollbar(tree_frame)
    tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    # Create Treeview with custom styling
    tree = ttk.Treeview(
        tree_frame, 
        columns=columns, 
        show="headings", 
        height=15,
        yscrollcommand=tree_scroll.set
    )
    tree_scroll.configure(command=tree.yview)

    # Define the column headings and their respective styles
    style = ttk.Style()
    style.theme_use('default')
    style.configure(
        "Treeview", 
        background="#D3D3D3",
        foreground="black",
        rowheight=25,
        fieldbackground="#D3D3D3"
    )
    style.map(
        "Treeview", 
        background=[('selected', "#347083")]
    )

    for col in columns:
        tree.heading(col, text=col, anchor="center")
        tree.column(col, width=120, anchor="center")

    tree.pack(expand=True, fill="both", padx=10, pady=10)

    # Fetch ride data from the database where the booking status is 'Scheduled'
    def refresh_rides():
        """
        Refreshes the list of rides displayed in the Treeview.
        """
        # Clear existing data from the Treeview
        for row in tree.get_children():
            tree.delete(row)

        try:
            # Establish a connection to the database
            conn = get_connection()
            cursor = conn.cursor()

            # Execute SQL query to get rides that are in 'Scheduled' status
            cursor.execute("""
                SELECT r.id, r.current_location, r.target_location, r.travel_date, r.booking_time, r.fare, r.booking_status
                FROM rides r
                WHERE r.booking_status = 'Scheduled'
            """)
            rides = cursor.fetchall()  # Fetch all results of the query

            # Add the fetched data to the Treeview widget with alternating row colors
            for i, row in enumerate(rides):
                tags = ('oddrow',) if i % 2 == 0 else ('evenrow',)
                tree.insert("", tk.END, values=row, tags=tags)

            # Configure alternating row colors
            tree.tag_configure('oddrow', background='#FFFFFF')
            tree.tag_configure('evenrow', background='#E0E0E0')

        except pymysql.MySQLError as e:
            # If an error occurs while fetching data, show an error message
            messagebox.showerror("Database Error", f"An error occurred while fetching ride data: {e}")
        finally:
            # Close the cursor and connection to free resources
            cursor.close()
            conn.close()

    # Initial fetch of ride data
    refresh_rides()

    # Create a frame to hold the action buttons with modern styling
    button_frame = ctk.CTkFrame(root, corner_radius=10, fg_color="transparent")
    button_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

    # Refresh Rides button with modern design
    refresh_button = ctk.CTkButton(
        button_frame, 
        text="Refresh Rides", 
        command=refresh_rides,
        fg_color="#2C3E50",
        hover_color="#34495E",
        text_color="white"
    )
    refresh_button.pack(side=tk.LEFT, padx=10)

    # Assign Driver button with modern design
    assign_button = ctk.CTkButton(
        button_frame, 
        text="Assign Driver", 
        command=lambda: assign_driver_action(1),  # Example ride_id 1
        fg_color="#27AE60",
        hover_color="#2ECC71",
        text_color="white"
    )
    assign_button.pack(side=tk.LEFT, padx=10)

    # Start the Tkinter event loop to keep the window running
    root.mainloop()

def assign_driver_action(ride_id):
    """
    Function to assign a driver to a ride and update its status to 'Scheduled'.
    The function will run an SQL query to update the booking status of the selected ride.
    """
    try:
        # Establish a connection to the database
        conn = get_connection()
        cursor = conn.cursor()

        # Execute SQL query to update the booking status of the ride to 'Scheduled'
        cursor.execute("""
            UPDATE rides
            SET booking_status = 'Scheduled'
            WHERE id = %s
        """, (ride_id,))  # Use the provided ride_id to select the correct ride

        conn.commit()  # Commit the transaction to update the database

        # Show a success message to the user
        messagebox.showinfo("Driver Assigned", "Ride has been successfully assigned.")

    except pymysql.MySQLError as e:
        # If an error occurs while assigning the driver, show an error message
        messagebox.showerror("Database Error", f"An error occurred while assigning the driver: {e}")
    finally:
        # Close the cursor and connection to free resources
        cursor.close()
        conn.close()

if __name__ == "__main__":
    # Start the admin dashboard when the script is run
    open_admin_dashboard()