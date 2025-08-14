import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os
import uuid
from datetime import datetime
from PIL import Image, ImageTk # Requires Pillow: pip install Pillow

# --- OOP Concept: Encapsulation ---
# Each class below encapsulates its data (attributes) and methods that operate on that data.
# This means the internal state of an object is managed by its own methods,
# providing a clear interface for interaction.

class User:
    """
    Represents a user (office staff) with a username and password.
    Encapsulates user data and provides methods for conversion to/from dictionary.
    """
    def __init__(self, username, password):
        self._username = username # Encapsulated attribute
        self._password = password # Encapsulated attribute (should be hashed in real apps)

    # Properties to allow controlled access to attributes (a form of encapsulation)
    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    def to_dict(self):
        """Converts User object to a dictionary for CSV writing."""
        return {"username": self._username, "password": self._password}

    @staticmethod
    def from_dict(data):
        """Creates a User object from a dictionary (e.g., from CSV reading)."""
        return User(data["username"], data["password"])

class Vehicle:
    """
    Represents a vehicle available for rent.
    Encapsulates vehicle details and availability status.
    """
    def __init__(self, vehicle_id, vehicle_type, make, model, year, daily_rate, image_path, is_available=True):
        self._vehicle_id = vehicle_id
        self._type = vehicle_type
        self._make = make
        self._model = model
        self._year = year
        self._daily_rate = float(daily_rate)
        self._image_path = image_path
        self._is_available = is_available # Boolean status

    # Properties for controlled access
    @property
    def vehicle_id(self):
        return self._vehicle_id

    @property
    def type(self):
        return self._type

    @property
    def make(self):
        return self._make

    @property
    def model(self):
        return self._model

    @property
    def year(self):
        return self._year

    @property
    def daily_rate(self):
        return self._daily_rate

    @property
    def image_path(self):
        return self._image_path
    
    @property
    def is_available(self):
        return self._is_available

    @is_available.setter # Setter for 'is_available' to allow modification
    def is_available(self, value):
        if isinstance(value, bool):
            self._is_available = value
        else:
            raise ValueError("is_available must be a boolean.")

    def to_dict(self):
        """Converts Vehicle object to a dictionary for CSV writing."""
        return {
            "vehicle_id": self._vehicle_id,
            "type": self._type,
            "make": self._make,
            "model": self._model,
            "year": self._year,
            "daily_rate": self._daily_rate,
            "image_path": self._image_path,
            "is_available": self._is_available # Store boolean as string for CSV
        }

    @staticmethod
    def from_dict(data):
        """Creates a Vehicle object from a dictionary (e.g., from CSV reading)."""
        return Vehicle(
            data["vehicle_id"],
            data["type"],
            data["make"],
            data["model"],
            int(data["year"]), # Convert year to int
            float(data["daily_rate"]),
            data["image_path"],
            data["is_available"] == 'True' # Convert string back to boolean
        )

class Rental:
    """
    Represents a rental transaction.
    Encapsulates rental details, customer information, and rental status.
    """
    def __init__(self, rental_id, vehicle_id, customer_id, customer_name, customer_address, 
                 customer_tel, rent_date, proposed_return_date, actual_return_date="N/A", status="Rented"):
        self._rental_id = rental_id
        self._vehicle_id = vehicle_id
        self._customer_id = customer_id
        self._customer_name = customer_name
        self._customer_address = customer_address
        self._customer_tel = customer_tel
        self._rent_date = rent_date
        self._proposed_return_date = proposed_return_date
        self._actual_return_date = actual_return_date
        self._status = status

    # Properties for controlled access
    @property
    def rental_id(self): return self._rental_id
    @property
    def vehicle_id(self): return self._vehicle_id
    @property
    def customer_id(self): return self._customer_id
    @customer_id.setter
    def customer_id(self, value): self._customer_id = value
    @property
    def customer_name(self): return self._customer_name
    @customer_name.setter
    def customer_name(self, value): self._customer_name = value
    @property
    def customer_address(self): return self._customer_address
    @customer_address.setter
    def customer_address(self, value): self._customer_address = value
    @property
    def customer_tel(self): return self._customer_tel
    @customer_tel.setter
    def customer_tel(self, value): self._customer_tel = value
    @property
    def rent_date(self): return self._rent_date
    @rent_date.setter
    def rent_date(self, value): self._rent_date = value
    @property
    def proposed_return_date(self): return self._proposed_return_date
    @proposed_return_date.setter
    def proposed_return_date(self, value): self._proposed_return_date = value
    @property
    def actual_return_date(self): return self._actual_return_date
    @actual_return_date.setter
    def actual_return_date(self, value): self._actual_return_date = value
    @property
    def status(self): return self._status
    @status.setter
    def status(self, value): self._status = value

    def to_dict(self):
        """Converts Rental object to a dictionary for CSV writing."""
        return {
            "rental_id": self._rental_id,
            "vehicle_id": self._vehicle_id,
            "customer_id": self._customer_id,
            "customer_name": self._customer_name,
            "customer_address": self._customer_address,
            "customer_tel": self._customer_tel,
            "rent_date": self._rent_date,
            "proposed_return_date": self._proposed_return_date,
            "actual_return_date": self._actual_return_date,
            "status": self._status
        }

    @staticmethod
    def from_dict(data):
        """Creates a Rental object from a dictionary (e.g., from CSV reading)."""
        return Rental(
            data["rental_id"],
            data["vehicle_id"],
            data["customer_id"],
            data["customer_name"],
            data["customer_address"],
            data["customer_tel"],
            data["rent_date"],
            data["proposed_return_date"],
            data.get("actual_return_date", "N/A"),
            data.get("status", "Rented")
        )

# --- OOP Concept: Abstraction ---
# The DatabaseManager class abstracts away the complexities of file I/O operations (CSV reading/writing).
# Users of this class don't need to know how data is stored or retrieved; they just call methods like
# 'get_users()', 'add_vehicle()', etc. This hides the intricate details of CSV handling.
class DatabaseManager:
    """
    Manages all interactions with CSV files for users, vehicles, and rentals.
    Abstracts file I/O operations.
    """
    def __init__(self, users_csv='users.csv', vehicles_csv='vehicles.csv', rentals_csv='rentals.csv'):
        self.users_csv = users_csv
        self.vehicles_csv = vehicles_csv
        self.rentals_csv = rentals_csv
        self._create_csv_if_not_exists()

    def _create_csv_if_not_exists(self):
        """Ensures CSV files exist and creates them with headers if not.
           Initializes vehicles.csv with some available vehicles if new.
        """
        # --- Encapsulation: _method indicates it's an internal helper method ---
        
        # Create users.csv
        if not os.path.exists(self.users_csv):
            with open(self.users_csv, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=["username", "password"])
                writer.writeheader()

        if not os.path.exists(self.vehicles_csv):
            with open(self.vehicles_csv, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=[
                    "vehicle_id", "type", "make", "model", "year", 
                    "daily_rate", "image_path", "is_available"
                ])
                writer.writeheader()
                

        # Create rentals.csv
        if not os.path.exists(self.rentals_csv):
            with open(self.rentals_csv, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=[
                    "rental_id", "vehicle_id", "customer_id", "customer_name", 
                    "customer_address", "customer_tel", "rent_date", 
                    "proposed_return_date", "actual_return_date", "status"
                ])
                writer.writeheader()

    def get_users(self):
        """Retrieves all users from users.csv."""
        users = []
        try:
            with open(self.users_csv, 'r', newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    users.append(User.from_dict(row))
        except FileNotFoundError:
            pass
        return users

    def add_user(self, user):
        """Adds a new user to users.csv."""
        users = self.get_users()
        if any(u.username == user.username for u in users):
            return False # Username already exists
        
        users.append(user)
        self._write_users_to_csv(users)
        return True

    def _write_users_to_csv(self, users):
        """Internal helper to write all users to users.csv."""
        with open(self.users_csv, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["username", "password"])
            writer.writeheader()
            for user in users:
                writer.writerow(user.to_dict())

    def get_vehicles(self):
        """Retrieves all vehicles from vehicles.csv."""
        vehicles = []
        try:
            with open(self.vehicles_csv, 'r', newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    vehicles.append(Vehicle.from_dict(row))
        except FileNotFoundError:
            pass
        return vehicles

    def add_vehicle(self, vehicle):
        """Adds a new vehicle to vehicles.csv."""
        vehicles = self.get_vehicles()
        vehicles.append(vehicle)
        self._write_vehicles_to_csv(vehicles)

    def update_vehicle(self, updated_vehicle):
        """Updates an existing vehicle's data in vehicles.csv."""
        vehicles = self.get_vehicles()
        for i, vehicle in enumerate(vehicles):
            if vehicle.vehicle_id == updated_vehicle.vehicle_id:
                vehicles[i] = updated_vehicle
                break
        self._write_vehicles_to_csv(vehicles)

    def _write_vehicles_to_csv(self, vehicles):
        """Internal helper to write all vehicles to vehicles.csv."""
        with open(self.vehicles_csv, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                "vehicle_id", "type", "make", "model", "year", 
                "daily_rate", "image_path", "is_available"
            ])
            writer.writeheader()
            for vehicle in vehicles:
                writer.writerow(vehicle.to_dict())

    def get_rentals(self):
        """Retrieves all rentals from rentals.csv."""
        rentals = []
        try:
            with open(self.rentals_csv, 'r', newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    rentals.append(Rental.from_dict(row))
        except FileNotFoundError:
            pass
        return rentals

    def add_rental(self, rental):
        """Adds a new rental record to rentals.csv."""
        rentals = self.get_rentals()
        rentals.append(rental)
        self._write_rentals_to_csv(rentals)

    def update_rental(self, updated_rental):
        """Updates an existing rental record in rentals.csv."""
        rentals = self.get_rentals()
        for i, rental in enumerate(rentals):
            if rental.rental_id == updated_rental.rental_id:
                rentals[i] = updated_rental
                break
        self._write_rentals_to_csv(rentals)

    def _write_rentals_to_csv(self, rentals):
        """Internal helper to write all rentals to rentals.csv."""
        with open(self.rentals_csv, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                "rental_id", "vehicle_id", "customer_id", "customer_name", 
                "customer_address", "customer_tel", "rent_date", 
                "proposed_return_date", "actual_return_date", "status"
            ])
            writer.writeheader()
            for rental in rentals:
                writer.writerow(rental.to_dict())

# --- OOP Concept: Inheritance ---
# The VehicleRentalApp class inherits from tk.Tk, gaining all the functionalities
# of a Tkinter root window. This is a clear example of inheritance, where
# VehicleRentalApp is a specialized type of Tkinter window.
class VehicleRentalApp(tk.Tk):
    """
    Main application class for the Vehicle Rental System.
    Handles GUI creation, user interaction, and orchestrates data management.
    """
    def __init__(self):
        super().__init__() # Calls the constructor of the parent class (tk.Tk)
        self.title("Vehicle Rental System")
        self.geometry("1400x850") # Increased default window size for 6 columns
        self.resizable(True, True) # Make window resizable

        # Configure styling
        self.style = ttk.Style(self)
        self.style.theme_use('clam') # 'clam' or 'alt' or 'default'
        
        # Define neutral color palette (black, dark grey, light grey)
        primary_dark = "#2C3E50" # Dark slate gray (almost black)
        secondary_dark = "#34495E" # Darker gray
        light_gray = "#ECF0F1" # Very light grey
        text_color = "#333333" # Standard dark text

        self.style.configure('TFrame', background=light_gray)
        self.style.configure('TLabel', background=light_gray, font=("Arial", 12), foreground=text_color)
        self.style.configure('TButton', font=("Arial", 11, "bold"), # Slightly smaller font for 6 buttons
                             background=primary_dark, foreground='white',
                             relief='flat', padding=8) # Smaller padding for 6 buttons
        self.style.map('TButton', background=[('active', secondary_dark)])
        self.style.configure('TEntry', font=("Arial", 12), padding=5, fieldbackground="white", foreground=text_color)
        self.style.configure('Treeview.Heading', font=("Arial", 12, "bold"), background=secondary_dark, foreground="white")
        self.style.configure('Treeview', font=("Arial", 11), background="white", foreground=text_color, fieldbackground="white")
        self.style.map('Treeview', background=[('selected', primary_dark)]) # Selected row background
        self.style.configure('TLabelframe.Label', font=("Arial", 14, "bold"), foreground=secondary_dark)


        self.db_manager = DatabaseManager()
        self.current_user = None

        self._create_image_folder() # Ensure images folder exists

        self.show_login_screen()

    def _create_image_folder(self):
        """Helper to create the 'images' folder and instruct user for image placement."""
        if not os.path.exists("images"):
            os.makedirs("images")
            messagebox.showinfo("Image Folder Created", 
                                "The 'images' folder has been created. Please download sample images into this folder:\n\n"
                                "1. toyota_corolla.jpg: https://www.carpixel.net/site-images/uploads/2023/10/toyota-corolla-2024-1080p.jpg\n"
                                "2. honda_odyssey.jpg: https://www.carpixel.net/site-images/uploads/2023/10/honda-civic-type-r-2023-1080p.jpg (Use this placeholder for a van)\n"
                                "3. harley_davidson.jpg: https://www.carpixel.net/site-images/uploads/2022/10/ford-f150-lightning-platinum-2023-1080p.jpg (Use this placeholder for a bike)\n"
                                "4. mercedes_c_class.jpg: https://www.carpixel.net/site-images/uploads/2022/10/mercedes-benz-c-class-sedan-2023-1080p.jpg\n"
                                "5. bmw_x5.jpg: https://www.carpixel.net/site-images/uploads/2022/10/bmw-x5-xdrive40i-2023-1080p.jpg\n"
                                "6. tesla_model_3.jpg: https://www.carpixel.net/site-images/uploads/2022/08/tesla-model-3-2023-1080p.jpg\n"
                                "7. ford_mustang.jpg: https://www.carpixel.net/site-images/uploads/2023/12/ford-mustang-dark-horse-2024-1080p.jpg\n"
                                "8. chevrolet_silverado.jpg: https://www.carpixel.net/site-images/uploads/2022/08/chevrolet-silverado-zr2-2022-1080p.jpg\n"
                                "9. mercedes_sprinter.jpg: https://www.carpixel.net/site-images/uploads/2020/09/mercedes-benz-sprinter-2018-1080p.jpg\n"
                                "10. audi_q7.jpg: https://www.carpixel.net/site-images/uploads/2022/10/audi-q7-55-tfsi-2023-1080p.jpg\n\n"
                                "Also, create a simple 'placeholder.png' image for missing vehicle images."
                                "\n\nThen restart the application after placing all images."
                                )
            self.destroy() # Close the app so user can put images
        
        # Create a basic placeholder image if it doesn't exist
        if not os.path.exists("images/placeholder.png"):
            try:
                img = Image.new('RGB', (120, 90), color = (200, 200, 200)) # Grey placeholder for new size
                img.save('images/placeholder.png')
            except Exception as e:
                print(f"Could not create placeholder image: {e}. Please ensure Pillow is installed.")


    def clear_screen(self):
        """Removes all widgets from the current screen."""
        for widget in self.winfo_children():
            widget.destroy()

    def show_login_screen(self):
        """Displays the user login form."""
        self.clear_screen()
        self.title("Login - Vehicle Rental System")

        login_frame = ttk.Frame(self, padding="50")
        login_frame.pack(expand=True, fill="both")

        ttk.Label(login_frame, text="Staff Login", font=("Arial", 30, "bold"), foreground="#2C3E50").pack(pady=40)

        username_label = ttk.Label(login_frame, text="Username:")
        username_label.pack(pady=10)
        self.username_entry = ttk.Entry(login_frame, width=40, font=("Arial", 14))
        self.username_entry.pack(pady=5)
        self.username_entry.focus_set() # Focus on username input

        password_label = ttk.Label(login_frame, text="Password:")
        password_label.pack(pady=10)
        self.password_entry = ttk.Entry(login_frame, width=40, show="*", font=("Arial", 14))
        self.password_entry.pack(pady=5)

        login_button = ttk.Button(login_frame, text="Login", command=self.login)
        login_button.pack(pady=20)

        # Keyboard binds for login
        self.username_entry.bind("<Return>", lambda event: self.password_entry.focus_set())
        self.password_entry.bind("<Return>", lambda event: self.login())
        # Global key bindings are applied to the root window (self)
        self.bind("<Right>", lambda event: self._tab_focus(self.focus_get(), forward=True))
        self.bind("<Left>", lambda event: self._tab_focus(self.focus_get(), forward=False))


        register_link = ttk.Label(login_frame, text="Don't have an account? Register here.", 
                                  foreground="#2C3E50", cursor="hand2", font=("Arial", 12, "underline"))
        register_link.pack(pady=15)
        register_link.bind("<Button-1>", lambda e: self.show_registration_screen())
        # Make register link also respond to keyboard if focused
        register_link.bind("<Return>", lambda e: self.show_registration_screen())
        register_link.bind("<space>", lambda e: self.show_registration_screen())


    def _tab_focus(self, current_widget, forward=True):
        """Helper to shift focus among entry widgets in login/registration screens."""
        widgets = []
        # Add login screen widgets if they exist
        if hasattr(self, 'username_entry') and self.username_entry.winfo_exists():
            widgets.extend([self.username_entry, self.password_entry])
        # Add registration screen widgets if they exist
        elif hasattr(self, 'reg_username_entry') and self.reg_username_entry.winfo_exists():
            widgets.extend([self.reg_username_entry, self.reg_password_entry])

        if not widgets: # No relevant entry widgets found
            return

        try:
            current_index = widgets.index(current_widget)
            if forward:
                next_index = (current_index + 1) % len(widgets)
            else:
                next_index = (current_index - 1 + len(widgets)) % len(widgets)
            widgets[next_index].focus_set()
        except ValueError:
            # Current widget not in list (e.g., a button or link), try to set focus to first/last entry
            if forward:
                widgets[0].focus_set()
            else:
                widgets[-1].focus_set()

    def login(self):
        """Authenticates user credentials."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        users = self.db_manager.get_users()
        for user in users:
            if user.username == username and user.password == password: # In a real app, verify hashed passwords
                self.current_user = user
                messagebox.showinfo("Success", f"Welcome, {username}!", parent=self)
                self.show_main_app_screen()
                return
        messagebox.showerror("Login Failed", "Invalid username or password.", parent=self)

    def show_registration_screen(self):
        """Displays the user registration form."""
        self.clear_screen()
        self.title("Register - Vehicle Rental System")

        reg_frame = ttk.Frame(self, padding="50")
        reg_frame.pack(expand=True, fill="both")

        ttk.Label(reg_frame, text="Register New Account", font=("Arial", 26, "bold"), foreground="#2C3E50").pack(pady=40)

        username_label = ttk.Label(reg_frame, text="Username:")
        username_label.pack(pady=10)
        self.reg_username_entry = ttk.Entry(reg_frame, width=40, font=("Arial", 14))
        self.reg_username_entry.pack(pady=5)
        self.reg_username_entry.focus_set()

        password_label = ttk.Label(reg_frame, text="Password:")
        password_label.pack(pady=10)
        self.reg_password_entry = ttk.Entry(reg_frame, width=40, show="*", font=("Arial", 14))
        self.reg_password_entry.pack(pady=5)

        register_button = ttk.Button(reg_frame, text="Register", command=self.register_user)
        register_button.pack(pady=20)
        
        # Keyboard binds for registration
        self.reg_username_entry.bind("<Return>", lambda event: self.reg_password_entry.focus_set())
        self.reg_password_entry.bind("<Return>", lambda event: self.register_user())
        # Global key bindings are applied to the root window (self)
        self.bind("<Right>", lambda event: self._tab_focus(self.focus_get(), forward=True))
        self.bind("<Left>", lambda event: self._tab_focus(self.focus_get(), forward=False))

        back_to_login_link = ttk.Label(reg_frame, text="Back to Login", 
                                       foreground="#2C3E50", cursor="hand2", font=("Arial", 12, "underline"))
        back_to_login_link.pack(pady=15)
        back_to_login_link.bind("<Button-1>", lambda e: self.show_login_screen())
        back_to_login_link.bind("<Return>", lambda e: self.show_login_screen())
        back_to_login_link.bind("<space>", lambda e: self.show_login_screen())


    def register_user(self):
        """Registers a new user account."""
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Username and Password cannot be empty.", parent=self)
            return

        new_user = User(username, password)
        if self.db_manager.add_user(new_user):
            messagebox.showinfo("Success", "Account created successfully! Please login.", parent=self)
            self.show_login_screen()
        else:
            messagebox.showerror("Error", "Username already exists. Please choose a different one.", parent=self)

    def show_main_app_screen(self):
        """Displays the main vehicle listing and management screen."""
        self.clear_screen()
        self.title("Available Vehicles - Vehicle Rental System")

        # Top Bar for Search and Filter
        top_frame = ttk.Frame(self, padding="15")
        top_frame.pack(fill="x", pady=(0, 10))

        # Search
        self.search_entry = ttk.Entry(top_frame, width=40, font=("Arial", 12))
        self.search_entry.pack(side="left", padx=10, ipady=4)
        search_button = ttk.Button(top_frame, text="Search", command=self.perform_search)
        search_button.pack(side="left", padx=5)

        # Filters
        ttk.Label(top_frame, text="Filter by:").pack(side="left", padx=(30, 10))
        
        self.filter_type_var = tk.StringVar(self)
        self.filter_type_var.set("All Types")
        vehicle_types = ["All Types"] + sorted(list(set(v.type for v in self.db_manager.get_vehicles())))
        self.filter_type_menu = ttk.OptionMenu(top_frame, self.filter_type_var, "All Types", *vehicle_types, command=self.apply_filters)
        self.filter_type_menu.pack(side="left", padx=5, ipady=4)
        self.filter_type_menu.config(width=15)

        self.filter_fee_var = tk.StringVar(self)
        self.filter_fee_var.set("No Sort")
        self.filter_fee_menu = ttk.OptionMenu(top_frame, self.filter_fee_var, "No Sort", "Fee Low to High", "Fee High to Low", command=self.apply_filters)
        self.filter_fee_menu.pack(side="left", padx=5, ipady=4)
        self.filter_fee_menu.config(width=15)


        # History button
        history_button = ttk.Button(top_frame, text="Rental History", command=self.show_rental_history)
        history_button.pack(side="right", padx=10)

        # Main content area for vehicles
        self.vehicle_display_frame = ttk.Frame(self, padding="15")
        self.vehicle_display_frame.pack(expand=True, fill="both")
        
        self.canvas = tk.Canvas(self.vehicle_display_frame, bg=self.style.lookup('TFrame', 'background'))
        self.scrollbar = ttk.Scrollbar(self.vehicle_display_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas, style='TFrame') # Apply frame style

        # --- Responsive grid setup for scrollable_frame ---
        self.max_cols = 6 # Define max columns here for easier reference

        # Configure columns of the scrollable_frame to expand proportionally
        for i in range(self.max_cols):
            self.scrollable_frame.grid_columnconfigure(i, weight=1)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        # --- FIX: Mouse scrolling for Canvas ---
        # Bind mouse wheel events to the canvas for scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mouse_wheel) # Windows/macOS
        self.canvas.bind_all("<Button-4>", self._on_mouse_wheel)   # Linux scroll up
        self.canvas.bind_all("<Button-5>", self._on_mouse_wheel)   # Linux scroll down


        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.load_and_display_vehicles()

    def _on_mouse_wheel(self, event):
        """Handles mouse wheel scrolling for the canvas."""
        if event.num == 5 or event.delta == -120:  # Scroll down
            self.canvas.yview_scroll(1, "unit")
        elif event.num == 4 or event.delta == 120:  # Scroll up
            self.canvas.yview_scroll(-1, "unit")


    # --- OOP Concept: Polymorphism (Implicit) ---
    # The `display_vehicles_grid` method, and methods like `perform_search` and `apply_filters`
    # implicitly demonstrate polymorphism. They all operate on lists of `Vehicle` objects,
    # regardless of how those lists were generated (e.g., from search, or filtered list).
    # Each `Vehicle` object, despite potentially being different types of vehicles (Car, Van, etc.),
    # responds to the same properties (make, model, daily_rate) and methods defined in the `Vehicle` class.
    # If we had subclasses like `Car` and `Van` with overridden methods, it would be a more explicit example.

    def perform_search(self):
        """Performs a search based on user input and refreshes vehicle display."""
        search_term = self.search_entry.get().lower()
        all_vehicles = self.db_manager.get_vehicles()
        
        filtered_vehicles = [
            v for v in all_vehicles 
            if search_term in v.make.lower() or 
               search_term in v.model.lower() or 
               search_term in v.type.lower()
        ]
        self.display_vehicles_grid(filtered_vehicles)

    def apply_filters(self, *args):
        """Applies type and sorting filters to the vehicle list."""
        search_term = self.search_entry.get().lower()
        all_vehicles = self.db_manager.get_vehicles()

        # Apply search first
        filtered_vehicles = [
            v for v in all_vehicles 
            if search_term in v.make.lower() or 
               search_term in v.model.lower() or 
               search_term in v.type.lower()
        ]

        # Apply type filter
        selected_type = self.filter_type_var.get()
        if selected_type != "All Types":
            filtered_vehicles = [v for v in filtered_vehicles if v.type == selected_type]

        # Apply fee sort
        selected_sort = self.filter_fee_var.get()
        if selected_sort == "Fee Low to High":
            filtered_vehicles.sort(key=lambda v: v.daily_rate)
        elif selected_sort == "Fee High to Low":
            filtered_vehicles.sort(key=lambda v: v.daily_rate, reverse=True)
        
        self.display_vehicles_grid(filtered_vehicles)


    def load_and_display_vehicles(self):
        """Loads all vehicles and initiates their display in the grid."""
        vehicles = self.db_manager.get_vehicles()
        self.display_vehicles_grid(vehicles)

    def display_vehicles_grid(self, vehicles):
        """
        Displays a list of vehicles in a grid layout.
        Maximum 6 vehicles per row. Columns expand responsively.
        """
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        row_num = 0
        col_num = 0
        # max_cols is already defined in __init__ and used for grid_columnconfigure

        self.photo_images = [] # Keep a reference to PhotoImage objects to prevent garbage collection

        for vehicle in vehicles:
            # Removed explicit width from tile_frame to let grid weights control it
            tile_frame = ttk.Frame(self.scrollable_frame, borderwidth=2, relief="solid", padding="8", style='TFrame') # Reduced padding slightly
            # sticky="nsew" makes the tile expand to fill its grid cell
            tile_frame.grid(row=row_num, column=col_num, padx=8, pady=8, sticky="nsew") # Reduced padding
            
            # Load and resize image
            try:
                img_path = vehicle.image_path
                if not os.path.exists(img_path):
                    img_path = "images/placeholder.png" # Fallback to placeholder

                original_image = Image.open(img_path)
                # Smaller image size for 6 columns
                resized_image = original_image.resize((120, 90), Image.Resampling.LANCZOS) # Adjusted size
                img = ImageTk.PhotoImage(resized_image)
                
                self.photo_images.append(img) # Store reference
                image_label = ttk.Label(tile_frame, image=img, style='TLabel')
                image_label.pack(pady=4) # Reduced padding
            except Exception as e:
                print(f"Error loading image for {vehicle.make} {vehicle.model}: {e}")
                image_label = ttk.Label(tile_frame, text="Image Error", font=("Arial", 9), width=12, height=6, relief="solid", background="lightgrey")
                image_label.pack(pady=4)


            ttk.Label(tile_frame, text=f"{vehicle.make} {vehicle.model}", # Removed year from main title
                      font=("Arial", 11, "bold"), foreground="#333333").pack(pady=(1,0)) # Dark text
            ttk.Label(tile_frame, text=f"({vehicle.year}) - {vehicle.type}", font=("Arial", 9)).pack(pady=0)
            ttk.Label(tile_frame, text=f"Daily Rate: Rs{vehicle.daily_rate:.2f}", 
                      font=("Arial", 10, "italic"), foreground="#333333").pack(pady=2) # Dark text for price

            # Availability status
            availability_text = "Available" if vehicle.is_available else "Rented"
            availability_color = "green" if vehicle.is_available else "#8B0000" # Dark Red for rented
            status_label = ttk.Label(tile_frame, text=f"Status: {availability_text}", 
                                     foreground=availability_color, font=("Arial", 9, "bold"))
            status_label.pack(pady=3)

            # --- Combined "Check and Update" button ---
            button_frame = ttk.Frame(tile_frame, style='TFrame')
            button_frame.pack(pady=4)

            # Always show "Check and Update"
            check_update_button = ttk.Button(button_frame, text="Check and Update", command=lambda v=vehicle: self.show_vehicle_details_for_update(v))
            check_update_button.pack(side="left", padx=3, ipadx=3, ipady=2) # Reduced padding

            # "Rent" button logic remains
            rent_button = ttk.Button(button_frame, text="Rent", command=lambda v=vehicle: self.show_rent_popup(v))
            rent_button.pack(side="left", padx=3, ipadx=3, ipady=2)
            
            if vehicle.is_available:
                rent_button["state"] = "normal" 
            else:
                rent_button["state"] = "disabled" 

            col_num += 1
            if col_num >= self.max_cols: # Use self.max_cols
                col_num = 0
                row_num += 1
        
        self.scrollable_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def show_vehicle_details_for_update(self, vehicle):
        """
        Displays a popup window with full vehicle details and allows updating its availability.
        """
        detail_window = tk.Toplevel(self)
        detail_window.title(f"Vehicle Details: {vehicle.make} {vehicle.model}")
        detail_window.geometry("450x450")
        detail_window.transient(self)
        detail_window.grab_set()

        form_frame = ttk.Frame(detail_window, padding="20")
        form_frame.pack(expand=True, fill="both")

        ttk.Label(form_frame, text=f"{vehicle.make} {vehicle.model} ({vehicle.year})", 
                  font=("Arial", 18, "bold"), foreground="#333333").pack(pady=15)

        ttk.Label(form_frame, text=f"Vehicle ID: {vehicle.vehicle_id}", font=("Arial", 12)).pack(pady=2, anchor="w")
        ttk.Label(form_frame, text=f"Type: {vehicle.type}", font=("Arial", 12)).pack(pady=2, anchor="w")
        ttk.Label(form_frame, text=f"Daily Rate: Rs{vehicle.daily_rate:.2f}", font=("Arial", 12)).pack(pady=2, anchor="w")
        
        # Current status
        current_status_text = "Available" if vehicle.is_available else "Rented"
        current_status_color = "green" if vehicle.is_available else "#8B0000"
        ttk.Label(form_frame, text=f"Current Status: {current_status_text}", 
                  font=("Arial", 12, "bold"), foreground=current_status_color).pack(pady=10, anchor="w")

        # Option to change status
        ttk.Label(form_frame, text="Update Status:", font=("Arial", 12, "bold")).pack(pady=(15, 5), anchor="w")
        
        status_var = tk.StringVar(detail_window)
        status_options = ["Available", "Rented"]
        status_var.set("Available" if vehicle.is_available else "Rented") # Set initial value
        
        status_menu = ttk.OptionMenu(form_frame, status_var, status_var.get(), *status_options)
        status_menu.pack(pady=5, anchor="w", ipadx=10, ipady=3)

        def update_vehicle_status():
            new_status_str = status_var.get()
            new_is_available = (new_status_str == "Available")

            if new_is_available == vehicle.is_available:
                messagebox.showinfo("No Change", "Vehicle status is already set to this value.", parent=detail_window)
                return

            # Before changing to Available, check if there are "Rented" records for this vehicle
            if new_is_available: # Trying to make it available
                active_rentals = [
                    r for r in self.db_manager.get_rentals()
                    if r.vehicle_id == vehicle.vehicle_id and r.status == "Rented"
                ]
                if active_rentals:
                    confirm = messagebox.askyesno(
                        "Confirm Return",
                        f"There are active rental records for {vehicle.make} {vehicle.model}. "
                        "Are you sure the customer has returned the vehicle? "
                        "Please update the rental record(s) in 'Rental History' too.",
                        parent=detail_window
                    )
                    if not confirm:
                        return # User cancelled the return

            vehicle.is_available = new_is_available
            self.db_manager.update_vehicle(vehicle)
            messagebox.showinfo("Status Updated", 
                                f"{vehicle.make} {vehicle.model} is now {new_status_str}.", 
                                parent=detail_window)
            detail_window.destroy()
            self.show_main_app_screen() # Refresh main screen to reflect change

        update_button = ttk.Button(form_frame, text="Apply Status Change", command=update_vehicle_status)
        update_button.pack(pady=20, ipadx=15, ipady=8)

        detail_window.protocol("WM_DELETE_WINDOW", lambda: detail_window.destroy())


    def check_availability(self, vehicle):
        # This function is now superseded by show_vehicle_details_for_update,
        # but kept for potential future separate 'check' functionality if needed.
        """Displays a message indicating a vehicle's availability."""
        if vehicle.is_available:
            messagebox.showinfo("Availability", f"{vehicle.make} {vehicle.model} is currently available for rent.", parent=self)
        else:
            messagebox.showinfo("Availability", f"{vehicle.make} {vehicle.model} is currently rented.", parent=self)

    def show_rent_popup(self, vehicle):
        """Displays a popup window for entering customer and rental details."""
        if not vehicle.is_available:
            messagebox.showwarning("Cannot Rent", f"{vehicle.make} {vehicle.model} is currently not available.", parent=self)
            return

        popup = tk.Toplevel(self)
        popup.title(f"Rent {vehicle.make} {vehicle.model}")
        popup.geometry("550x1000") # Increased popup size
        popup.transient(self)
        popup.grab_set()

        form_frame = ttk.Frame(popup, padding="25")
        form_frame.pack(expand=True, fill="both")

        ttk.Label(form_frame, text=f"Rent Details for {vehicle.make} {vehicle.model}", 
                  font=("Arial", 18, "bold"), foreground="#333333").pack(pady=20)
   
        # Add this line to show the daily fee
        ttk.Label(form_frame, text=f"Daily Rate: Rs{vehicle.daily_rate:.2f}", 
                  font=("Arial", 14, "italic"), foreground="#333333").pack(pady=(0, 10))
# ...existing code...

        # Helper to create label and entry pairs
        def create_input_field(parent, label_text, default_value="", password_char=None):
            ttk.Label(parent, text=label_text, font=("Arial", 12)).pack(pady=(10,2), anchor="w")
            entry = ttk.Entry(parent, width=50, font=("Arial", 14), show=password_char)
            entry.insert(0, default_value)
            entry.pack(pady=5, ipady=3, anchor="w")
            return entry

        customer_id_entry = create_input_field(form_frame, "Customer ID:")
        customer_name_entry = create_input_field(form_frame, "Customer Name:")
        customer_address_entry = create_input_field(form_frame, "Customer Address:")
        customer_tel_entry = create_input_field(form_frame, "Customer Tel Number:")
        
        # Use current date from context
        current_date_colombo = datetime.now().strftime("%Y-%m-%d")
        rent_date_entry = create_input_field(form_frame, "Rent Date (YYYY-MM-DD):", 
                                             default_value=current_date_colombo)
        return_date_entry = create_input_field(form_frame, "Proposed Return Date (YYYY-MM-DD):")

        # Label to show total fee (calculated from dates)
        total_fee_var = tk.StringVar()
        total_fee_label = ttk.Label(form_frame, textvariable=total_fee_var, font=("Arial", 16, "bold"), foreground="#2C3E50")
        total_fee_label.pack(pady=(20, 10))

        def update_total_fee(*args):
            try:
                rent_date = rent_date_entry.get().strip()
                return_date = return_date_entry.get().strip()
                rent_dt = datetime.strptime(rent_date, "%Y-%m-%d")
                return_dt = datetime.strptime(return_date, "%Y-%m-%d")
                days = (return_dt - rent_dt).days
                if days < 1:
                    days = 1
                total = days * vehicle.daily_rate
                total_fee_var.set(f"Total Fee for {days} day(s): Rs{total:.2f}")
            except Exception:
                total_fee_var.set("Total Fee: Rs0.00")

        rent_date_entry.bind("<KeyRelease>", update_total_fee)
        return_date_entry.bind("<KeyRelease>", update_total_fee)
        update_total_fee()

        # Set initial focus and bind Tab/Shift+Tab for navigation in popup
        customer_id_entry.focus_set()
        
        entries = [customer_id_entry, customer_name_entry, customer_address_entry, 
                   customer_tel_entry, rent_date_entry, return_date_entry]
        for i, entry in enumerate(entries):
            if i < len(entries) - 1:
                entry.bind("<Return>", lambda event, next_entry=entries[i+1]: next_entry.focus_set())
            else: # Last entry
                entry.bind("<Return>", lambda event: confirm_rental())
# ...existing code...
            
        # Global binds for popup (ensure they don't interfere with main app)
        popup.bind("<Right>", lambda event: self._tab_focus_popup(entries, popup.focus_get(), forward=True))
        popup.bind("<Left>", lambda event: self._tab_focus_popup(entries, popup.focus_get(), forward=False))


        def _tab_focus_popup(entry_list, current_widget_in_popup, forward=True):
            try:
                current_index = entry_list.index(current_widget_in_popup)
                if forward:
                    next_index = (current_index + 1) % len(entry_list)
                else:
                    next_index = (current_index - 1 + len(entry_list)) % len(entry_list)
                entry_list[next_index].focus_set()
            except ValueError:
                if forward:
                    entry_list[0].focus_set()
                else:
                    entry_list[-1].focus_set()


        def confirm_rental():
            c_id = customer_id_entry.get().strip()
            c_name = customer_name_entry.get().strip()
            c_address = customer_address_entry.get().strip()
            c_tel = customer_tel_entry.get().strip()
            r_date = rent_date_entry.get().strip()
            p_return_date = return_date_entry.get().strip()

            if not all([c_id, c_name, c_address, c_tel, r_date, p_return_date]):
                messagebox.showerror("Input Error", "All fields are required!", parent=popup)
                return
            
            try:
                datetime.strptime(r_date, "%Y-%m-%d")
                datetime.strptime(p_return_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Date Format Error", "Please use YYYY-MM-DD format for dates (e.g., 2025-07-26).", parent=popup)
                return

            rental_id = str(uuid.uuid4())
            new_rental = Rental(rental_id, vehicle.vehicle_id, c_id, c_name, c_address, 
                                c_tel, r_date, p_return_date)
            
            self.db_manager.add_rental(new_rental)
            
            # Update vehicle availability
            vehicle.is_available = False
            self.db_manager.update_vehicle(vehicle)
            
            messagebox.showinfo("Rental Confirmed", "Vehicle rented successfully!", parent=popup)
            popup.destroy()
            self.show_main_app_screen() # Refresh the main screen to reflect availability change
            
            # Not showing the confirmation window right after renting, as requested this is for updates.
            # self.show_rental_details_for_update(new_rental.rental_id) 

        confirm_button = ttk.Button(form_frame, text="Confirm Rental", command=confirm_rental)
        confirm_button.pack(pady=20, ipadx=15, ipady=8)

        popup.protocol("WM_DELETE_WINDOW", lambda: popup.destroy())


    def show_rental_details_for_update(self, rental_id):
        """
        Displays a window to view/update rental details based on rental_id.
        This is called from rental history double-click or after a new rental.
        """
        all_rentals = self.db_manager.get_rentals()
        rental = next((r for r in all_rentals if r.rental_id == rental_id), None)

        if not rental:
            messagebox.showerror("Error", "Rental record not found.", parent=self)
            return

        all_vehicles = self.db_manager.get_vehicles()
        vehicle = next((v for v in all_vehicles if v.vehicle_id == rental.vehicle_id), None)

        if not vehicle:
            messagebox.showerror("Error", "Associated vehicle not found for this rental.", parent=self)
            return

        confirm_window = tk.Toplevel(self)
        confirm_window.title(f"Rental Details: {rental.rental_id}")
        confirm_window.geometry("600x800") # Increased size
        confirm_window.transient(self)
        confirm_window.grab_set()

        ttk.Label(confirm_window, text="Rental Details", font=("Arial", 20, "bold"), foreground="#333333").pack(pady=20)

        details_frame = ttk.LabelFrame(confirm_window, text="Rental Information", padding="20")
        details_frame.pack(padx=30, pady=10, fill="x", expand=True)

        self.rental_update_entries = {} # Store references to entry widgets for update

        # Define labels and their corresponding attributes in the Rental object
        labels_map = {
            "Rental ID:": rental.rental_id,
            "Vehicle:": f"{vehicle.make} {vehicle.model} (ID: {vehicle.vehicle_id})",
            "Customer ID:": rental.customer_id,
            "Customer Name:": rental.customer_name,
            "Customer Address:": rental.customer_address,
            "Customer Tel:": rental.customer_tel,
            "Rent Date (YYYY-MM-DD):": rental.rent_date,
            "Proposed Return Date (YYYY-MM-DD):": rental.proposed_return_date,
            "Actual Return Date (YYYY-MM-DD/N/A):": rental.actual_return_date,
            "Status:": rental.status
        }

        row_idx = 0
        for label_text, value in labels_map.items():
            ttk.Label(details_frame, text=label_text, font=("Arial", 11, "bold")).grid(row=row_idx, column=0, sticky="w", pady=5, padx=10)
            
            if label_text == "Status:":
                status_options = ["Rented", "Returned"]
                status_var = tk.StringVar(confirm_window)
                status_var.set(value)
                entry = ttk.OptionMenu(details_frame, status_var, status_var.get(), *status_options)
                entry.grid(row=row_idx, column=1, sticky="ew", pady=5, padx=10)
                self.rental_update_entries[label_text] = status_var # Store the StringVar for OptionMenu
            else:
                entry = ttk.Entry(details_frame, width=40, font=("Arial", 12))
                entry.insert(0, str(value))
                entry.grid(row=row_idx, column=1, sticky="ew", pady=5, padx=10)
                self.rental_update_entries[label_text] = entry # Store the Entry widget

            if label_text in ["Rental ID:", "Vehicle:"]:
                entry.config(state="readonly")
            row_idx += 1

        details_frame.grid_columnconfigure(1, weight=1) # Make entry column expand

        def save_rental_updates():
            try:
                # Update rental object from entries
                rental.customer_id = self.rental_update_entries["Customer ID:"].get().strip()
                rental.customer_name = self.rental_update_entries["Customer Name:"].get().strip()
                rental.customer_address = self.rental_update_entries["Customer Address:"].get().strip()
                rental.customer_tel = self.rental_update_entries["Customer Tel:"].get().strip()
                
                rent_d = self.rental_update_entries["Rent Date (YYYY-MM-DD):"].get().strip()
                prop_ret_d = self.rental_update_entries["Proposed Return Date (YYYY-MM-DD):"].get().strip()
                actual_ret_d = self.rental_update_entries["Actual Return Date (YYYY-MM-DD/N/A):"].get().strip()
                new_status = self.rental_update_entries["Status:"].get() # Get from StringVar for OptionMenu

                # Date validation
                datetime.strptime(rent_d, "%Y-%m-%d")
                datetime.strptime(prop_ret_d, "%Y-%m-%d")
                if actual_ret_d.upper() != "N/A" and actual_ret_d != "": # Allow empty or N/A
                    datetime.strptime(actual_ret_d, "%Y-%m-%d")

                # Check if status change means vehicle availability change
                original_status = rental.status
                rental.rent_date = rent_d
                rental.proposed_return_date = prop_ret_d
                rental.actual_return_date = actual_ret_d
                rental.status = new_status
                
                self.db_manager.update_rental(rental)

                # Update vehicle availability based on rental status
                if original_status == "Rented" and new_status == "Returned":
                    # If rental was 'Rented' and is now 'Returned', make vehicle available
                    vehicle.is_available = True
                    self.db_manager.update_vehicle(vehicle)
                    messagebox.showinfo("Vehicle Returned", f"Vehicle {vehicle.make} {vehicle.model} is now marked as Available.", parent=confirm_window)
                elif original_status == "Returned" and new_status == "Rented":
                    # If rental was 'Returned' and is now 'Rented' (shouldn't happen for the same rental, but for consistency)
                    vehicle.is_available = False
                    self.db_manager.update_vehicle(vehicle)
                    messagebox.showinfo("Vehicle Rented Again", f"Vehicle {vehicle.make} {vehicle.model} is now marked as Rented.", parent=confirm_window)
                
                messagebox.showinfo("Update Successful", "Rental record updated successfully!", parent=confirm_window)
                confirm_window.destroy()
                self.load_rental_history_data() # Refresh history table
                self.show_main_app_screen() # Refresh main vehicle grid

            except ValueError:
                messagebox.showerror("Date Format Error", "Please use YYYY-MM-DD format for dates, or 'N/A' for Actual Return Date.", parent=confirm_window)
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred during update: {e}", parent=confirm_window)

        button_frame = ttk.Frame(confirm_window, style='TFrame')
        button_frame.pack(pady=20)

        save_button = ttk.Button(button_frame, text="Save Updates", command=save_rental_updates)
        save_button.pack(padx=15, ipadx=15, ipady=8)

        confirm_window.protocol("WM_DELETE_WINDOW", lambda: confirm_window.destroy())


    def show_rental_history(self):
        """Displays a tabular view of all rental history."""
        history_window = tk.Toplevel(self)
        history_window.title("Rental History")
        history_window.geometry("1000x600") # Increased size
        history_window.transient(self)
        history_window.grab_set()

        ttk.Label(history_window, text="Rental History", font=("Arial", 24, "bold"), foreground="#333333").pack(pady=25)

        tree_frame = ttk.Frame(history_window, padding="15")
        tree_frame.pack(pady=10, padx=20, fill="both", expand=True)

        tree_scroll_y = ttk.Scrollbar(tree_frame)
        tree_scroll_y.pack(side="right", fill="y")
        
        tree_scroll_x = ttk.Scrollbar(tree_frame, orient="horizontal")
        tree_scroll_x.pack(side="bottom", fill="x")

        columns = ("Rental ID", "Vehicle", "Customer Name", "Rent Date", "Proposed Return", "Actual Return", "Status")
        self.history_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", 
                                         yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set,
                                         selectmode="browse") # Allow single row selection
        
        tree_scroll_y.config(command=self.history_tree.yview)
        tree_scroll_x.config(command=self.history_tree.xview)

        for col in columns:
            self.history_tree.heading(col, text=col, anchor="w")
            self.history_tree.column(col, width=150, minwidth=100) # Adjust width

        self.history_tree.pack(fill="both", expand=True)

        # Bind double-click to view/edit rental details
        self.history_tree.bind("<Double-1>", self.on_history_item_double_click)

        self.load_rental_history_data()

        history_window.protocol("WM_DELETE_WINDOW", lambda: history_window.destroy())

    def load_rental_history_data(self):
        """Loads and displays rental data into the history Treeview."""
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)

        rentals = self.db_manager.get_rentals()
        vehicles = {v.vehicle_id: v for v in self.db_manager.get_vehicles()}

        for rental in rentals:
            vehicle_info = vehicles.get(rental.vehicle_id, None)
            vehicle_name = f"{vehicle_info.make} {vehicle_info.model}" if vehicle_info else "Unknown Vehicle"
            
            # Use item ID to store the actual rental object for easy retrieval
            self.history_tree.insert("", "end", iid=rental.rental_id, values=(
                rental.rental_id,
                vehicle_name,
                rental.customer_name,
                rental.rent_date,
                rental.proposed_return_date,
                rental.actual_return_date,
                rental.status
            ))


    def on_history_item_double_click(self, event):
        """Handles double-click on a history item to show its details for update."""
        selected_item = self.history_tree.selection()
        if selected_item:
            rental_id = selected_item[0] # The iid is the rental_id
            self.show_rental_details_for_update(rental_id)


if __name__ == "__main__":
    # Ensure the 'images' directory exists first
    if not os.path.exists("images"):
        os.makedirs("images")
    
    # Placeholder for a missing image. A small grey rectangle.
    # This will be created if Pillow is installed and the file doesn't exist.
    if not os.path.exists("images/placeholder.png"):
        try:
            from PIL import Image
            # Adjusted placeholder image size to match new tile image size
            img = Image.new('RGB', (120, 90), color = (200, 200, 200)) 
            img.save('images/placeholder.png')
        except ImportError:
            print("Pillow library not found. Cannot create placeholder image. Please install it (`pip install Pillow`) or create 'images/placeholder.png' manually.")

    app = VehicleRentalApp()
    app.mainloop()