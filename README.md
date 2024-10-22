
# Library Management System

This project is a **Library Management System** built using **Python**, **Tkinter** for the GUI, and **SQLite** for the database. It provides a user-friendly interface for managing books, users, and transactions within a library. The system is designed to help librarians and library users streamline book borrowing, returning, and managing library resources.

## Features
- **Book Management**: Add, view, update, and delete books in the library.
- **User Management**: Manage library users (students, employees).
- **Borrowing and Returning**: Track book borrowing and returning transactions.
- **Login System**: Separate login for users and administrators.
- **Search Functionality**: Search for books by title, author, genre, and availability.

## Technologies Used
- **Python**: Core programming language for the application.
- **Tkinter**: Python library for creating graphical user interfaces (GUIs).
- **SQLite**: Lightweight relational database for managing the library’s data.

## Project Structure
```
Library-Management-System/
├── src/
│   └── Library.py           # Main Python script for the library system
├── docs/
│   ├── Library Management System Project with Tkinter and SQLite.pptx  # Presentation
│   ├── LIBRARY MANAGEMENT SYSTEM USING TKINTER AND SQLITE.docx         # Documentation
│   └── README.md            # Project overview and setup instructions
├── .gitignore               # Git ignore file for Python
```

## Requirements
To run this project, you need to have the following installed:
- Python 3.x
- Tkinter (Comes pre-installed with Python)
- SQLite (Comes pre-installed with Python)

## Setup Instructions
1. **Clone the repository:**
   ```bash
   git clone https://github.com/manikantareddy12/Library-Management-System.git
   ```
   
2. **Navigate to the project directory:**
   ```bash
   cd Library-Management-System/src
   ```

3. **Run the Python script:**
   ```bash
   python Library.py
   ```

## Database
The system uses **SQLite** for database management. The following tables are used:
- **users.db**: Manages user data including `username`, `password`, and `user_type` (student or employee).
- **books.db**: Contains information about the books, including `book_id`, `title`, `author`, `genre`, and `availability`.

## Future Enhancements
- Add advanced search options like filters for publication year and user reviews.
- Implement analytics features for insights into borrowing patterns.
- Integrate email notifications for overdue books.
- Expand the user interface for compatibility with mobile devices.

## Limitations
- The system currently supports desktop use only and does not have real-time synchronization for multiple users accessing it simultaneously.

## Contributing
If you would like to contribute to this project, feel free to submit a pull request or raise an issue for discussion.


## Author
**ManikantaReddy Annem**
