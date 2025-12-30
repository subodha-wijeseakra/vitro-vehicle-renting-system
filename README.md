# 🚗 Vitro Vehicle Rental System

> **A comprehensive Vehicle Rental Management Application built with Python and Tkinter.**  
> *Created for the Object Oriented Programming (OOP) University Module.*

---

## 📖 About The Project

This project is a desktop-based application designed to streamline the operations of a vehicle rental agency. It allows office staff to manage a fleet of vehicles, handle customer rentals, and track availability in real-time.

The core objective of this project was to demonstrate robust **Object-Oriented Programming (OOP)** principles in a practical, real-world scenario. The application features a responsive graphical user interface (GUI) built with **Tkinter** and uses a persistent CSV-based database system.

---

## ✨ Key Features

### 🔐 User Access Control
- **Secure Authentication**: Staff login and registration system.
- **Data Encapsulation**: User credentials and sessions are securely managed within the application structure.

### 🚙 Fleet Management
- **Visual Grid Display**: Vehicles are displayed in a responsive grid layout with images and status indicators.
- **Smart Filtering**: Filter vehicles by **Type** (e.g., Car, Van, SUV) or **Price** (Low-to-High / High-to-Low).
- **Instant Search**: Real-time search functionality to find vehicles by Make, Model, or Type.
- **Availability Tracking**: Visual cues indicate if a vehicle is "Available" (Green) or "Rented" (Red).

### 📝 Rental Operations
- **Streamlined Booking**: Intuitive workflows for renting out vehicles to customers.
- **Customer Database**: Stores customer details (Name, Address, Tel) associated with each rental.
- **Rental History**: Tracks rent dates, proposed return dates, and actual returns.

---

## 🏗️ OOP Principles Implemented

This project is architected around four fundamental OOP concepts:

1.  **Encapsulation**:
    *   Classes like `User`, `Vehicle`, and `Rental` bundler data (attributes) and behavior (methods) together.
    *   Access to internal state is controlled using properties and private attributes (e.g., `self._username`).

2.  **Abstraction**:
    *   The `DatabaseManager` class hides the complexity of CSV file handling. The main application pushes and pulls data without knowing the underlying storage details.

3.  **Inheritance**:
    *   The main application class, `VehicleRentalApp`, inherits from `tk.Tk`, gaining all the properties of a standard GUI window while extending it with custom rental logic.

4.  **Polymorphism**:
    *   The display logic implicitly treats all vehicle objects uniformly, whether they are different types or filtered results, allowing for flexible and reusable code components.

---

## 🛠️ Technical Stack

-   **Language**: Python 3.x
-   **GUI Framework**: Tkinter (Standard Python GUI)
-   **Image Processing**: Pillow (PIL Fork)
-   **Data Storage**: CSV (Comma Separated Values) text files

---

## 🚀 Getting Started

### Prerequisites

Ensure you have Python installed. You also need the `Pillow` library for handling images.

```bash
pip install Pillow
```

### Installation

1.  **Clone or Download** the repository to your local machine.
2.  **Navigate** to the project directory.

### Running the Application

Execute the main script:

```bash
python main.py
```

> **Note**: On the first run, the application will automatically create an `images` folder and generate necessary CSV files (`users.csv`, `vehicles.csv`, `rentals.csv`). It may ask you to restart to populate the images folder with real vehicle photos.

### Image Setup
The application looks for images in the `images/` directory. If missing, it uses a placeholder. For the best experience, add `.jpg` images matching the vehicle definitions (e.g., `toyota_corolla.jpg`).

---

## 📂 Project Structure

-   `main.py`: The entry point and core source code containing all classes and logic.
-   `users.csv`: Stores staff login credentials.
-   `vehicles.csv`: Database of all vehicles in the fleet.
-   `rentals.csv`: Records of all current and past rental transactions.
-   `images/`: Directory for vehicle thumbnails.

---

## 🛡️ License

This project was created for educational purposes.
