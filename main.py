import tkinter as tk
import navigation
import login
import signup

# Main application setup
root = tk.Tk()
root.geometry("800x600")
root.title("Login/Signup Page")

# Start with the Signup page
navigation.navigate_to_signup(root, signup.show_signup_page)

root.mainloop()
