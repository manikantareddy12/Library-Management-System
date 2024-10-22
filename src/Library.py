import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk


# Define the main application class
class LibraryManagementSystem(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Library Enclave")
        self.geometry("400x300")

        # Initialize database connection
        self.initialize_database()

        # Create GUI components
        self.Login_Frame()

    def initialize_database(self):
        self.conn = sqlite3.connect("../users.db")
        self.cursor = self.conn.cursor()

        # users table if it doesn't exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY,
                                username TEXT UNIQUE,
                                password TEXT,
                                user_type TEXT
                            )''')

        predefined_users = [
            ("admin", "admin123", "employee"),
            ("student", "student123", "student"),
        ]

        for user in predefined_users:
            username, password, user_type = user
            try:
                self.cursor.execute('''INSERT INTO users (username, password, user_type) VALUES (?, ?, ?)''',
                                    (username, password, user_type))
            except sqlite3.IntegrityError:
                pass  # Skip insertion if username already exists


        # Connect to the SQLite database
        conn = sqlite3.connect('../books.db')
        c = conn.cursor()

        # Check if the table already exists
        c.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='books'")
        if c.fetchone()[0] == 0:
            # Table doesn't exist, create it
            c.execute('''CREATE TABLE books (
                         id TEXT PRIMARY KEY,
                         title TEXT,
                         author TEXT,
                         genre TEXT,
                         availability INTEGER
                         )''')

        # Add predefined books
        global predefined_books
        predefined_books = [
            # Computer Science Books
            ('CS001', 'Introduction to Algorithms',
             'Thomas H. Cormen', 'Computer Science', 10),
            ('CS002', 'Computer Networking Approach', 'James F. Kurose',
             'Computer Science', 8),
            ('CS003', 'Operating System Concepts', 'Abraham Silberschatz',
             'Computer Science', 7),
            ('CS004', 'AI: A Modern Approach', 'Stuart Russell, Peter Norvig',
             'Computer Science', 9),
            ('CS005', 'Database System Concepts', 'Abraham Silberschatz',
             'Computer Science', 6),

            # Data Science Books
            ('DS001', 'Python for Data Analysis', 'Wes McKinney', 'Data Science', 10),
            ('DS002', 'Machine Learning with Scikit', 'Aurélien Géron',
             'Data Science', 8),
            ('DS003', 'Data Science for Business', 'Foster Provost', 'Data Science', 7),
            ('DS004', 'R for Data Science', 'Hadley Wickham', 'Data Science', 9),

            # Machine Learning Books
            ('ML001', 'Pattern Recognition ML', 'Christopher M. Bishop', 'Machine Learning', 10),
            ('ML002', 'Machine Learning Yearning', 'Andrew Ng', 'Machine Learning', 8),
            ('ML003', 'ML: A Probabilistic Perspective', 'Kevin P. Murphy', 'Machine Learning', 7),
            ('ML004', 'Deep Learning for Computer Vision', 'Rajalingappaa Shanmugamani', 'Machine Learning', 9),
            ('ML005', 'Machine Learning with Scikit', 'Aurélien Géron',
             'Machine Learning', 6),

            # Data Analytics Books
            (
                'DA001', 'Big Data Analytics: A Hands-On ', 'Arshdeep Bahga, Vijay Madisetti', 'Data Analytics',
                10),
            ('DA002', 'Practical Statistics for Data Scientists', 'Andrew Bruce, Peter Bruce', 'Data Analytics', 8),
            ('DA003', 'Data Analytics Made Accessible', 'Anil Maheshwari', 'Data Analytics', 7),
            ('DA004', 'Data Analysis Using SQL and Excel', 'Gordon S. Linoff, Daniel T. McGrath', 'Data Analytics',
             9),
            ('DA005', 'Storytelling with Data', 'Cole Nussbaumer Knaflic', 'Data Analytics', 6),

            # Business Analytics Books
            ('BA001', 'Business Analytics Decision Making',
             'S. Christian Albright', 'Business Analytics', 10),
            ('BA002', 'Predictive Analytics', 'Eric Siegel',
             'Business Analytics', 8),
            ('BA003', 'Analytics : Smarter Decisions',
             'Thomas H. Davenport', 'Business Analytics', 7),
            ('BA004', 'Data Science for Business', 'Foster Provost, Fawcett', 'Business Analytics', 9),
            ('BA005', 'Competing on Analytics', 'Thomas H. Davenport, Jeanne G. Harris',
             'Business Analytics', 6),

            # Artificial Intelligence Books
            ('AI001', 'AI: A Modern Approach', 'Stuart Russell',
             'Artificial Intelligence', 10),
            ('AI002', 'Deep Learning', ' Aaron Courville', 'Artificial Intelligence',
             8),
            ('AI003', 'Foundations of Computational Agents',
             'Alan K. Mackworth', 'Artificial Intelligence', 7),
            ('AI004', 'Reinforcement Learning', 'Richard S. Sutton',
             'Artificial Intelligence', 9),
            ('AI005', 'Practical AI Programming in Java', 'Mark Watson',
             'Artificial Intelligence', 6),

            # Cybersecurity Books
            ('CSY001', 'Hacking: The Art of Exploitation', 'Jon Erickson', 'Cybersecurity', 10),
            ('CSY002', 'The Web Application Hacker', 'Dafydd Stuttard, Marcus Pinto', 'Cybersecurity',
             8),
            ('CSY003', 'Network Security Essentials', 'William Stallings', 'Cybersecurity', 7),
            ('CSY004', 'CISSP All-in-One Exam Guide', 'Shon Harris, Fernando Maymi', 'Cybersecurity', 9),
            ('CSY005', 'Practical Malware Analysis', 'Michael Sikorski, Andrew Honig', 'Cybersecurity', 6),

            # Arts & Science Books
            ('AS001', 'Sapiens: A Brief History', 'Yuval Noah Harari', 'Arts & Science', 10),
            ('AS002', 'Thinking, Fast and Slow', 'Daniel Kahneman', 'Arts & Science', 8),
            ('AS003', 'Power of Habit: Life & Business', 'Charles Duhigg',
             'Arts & Science', 7),
            ('AS004', 'Freakonomics: A Rogue Economist',
             'Steven D. Levitt, Stephen J. Dubner', 'Arts & Science', 9),
        ]

        c.executemany('INSERT OR IGNORE INTO books VALUES (?, ?, ?, ?, ?)', predefined_books)

        # Save changes and close the connection
        conn.commit()
        conn.close()

    def get_books_by_genre(self, genre):
        conn = sqlite3.connect('../books.db')
        c = conn.cursor()
        c.execute('SELECT * FROM books WHERE genre = ?', (genre,))
        books = c.fetchall()
        conn.close()
        return books

    def show_books_by_genre(self, genre):
        # Clear existing books
        for item in self.books_tree.get_children():
            self.books_tree.delete(item)

        # Fetch books by genre from the predefined books list
        # books_by_genre = [book for book in predefined_books if book[3] == genre]
        books_by_genre = self.get_books_by_genre(genre)

        # Insert books into the treeview
        for book in books_by_genre:
            self.books_tree.insert("", "end", values=(book[0], book[1], book[2], book[4]),
                                   tags=("Book ID", "Title", "Author", "Availability"))
    def Login_Frame(self):
        # Load the background image
        image = Image.open("../images/library.png")
        image = image.resize((self.winfo_screenwidth(), self.winfo_screenheight()))
        photo = ImageTk.PhotoImage(image)

        # Create a label to display the background image
        self.background_label = tk.Label(self, image=photo)
        self.background_label.image = photo
        self.background_label.grid(row=0, column=0, sticky="nsew")
        self.update_idletasks()

        # Create a frame to hold widgets
        # content_frame = tk.Frame(self.background_label)
        content_frame = tk.Frame(self.background_label, width=500, height=400)

        content_frame.grid(row=0, column=1, sticky="nsew")
        content_frame.grid_columnconfigure(0, weight=2)

        # Place the frame in the center
        content_frame.place(relx=0.75, rely=0.45, anchor='center')

        # Padding within the content frame
        content_frame.grid_rowconfigure(0, pad=80)
        content_frame.grid_rowconfigure(2, pad=50)
        content_frame.grid_columnconfigure(0, pad=60)

        # Create the "Library Enclave" heading label
        self.heading_label = tk.Label(content_frame, text="Library Enclave",
                                      font=("Helvetica", 24, "bold"), fg="#FFFFFF", bg="#398333")
        self.heading_label.grid(row=0, column=0, sticky="ew", pady=15)

        # Create the username label and entry
        self.username_label = tk.Label(content_frame, text="Username:", font=("Helvetica", 12), fg="#333333")
        self.username_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.username_entry = tk.Entry(content_frame, font=("Helvetica", 12), bg="#FFFFFF", fg="#333333", bd=1,
                                       relief=tk.SOLID)
        self.username_entry.grid(row=1, column=1, sticky="w")

        # Create the password label and entry
        self.password_label = tk.Label(content_frame, text="Password:", font=("Helvetica", 12), fg="#333333")
        self.password_label.grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.password_entry = tk.Entry(content_frame, show="*", font=("Helvetica", 12), bg="#FFFFFF", fg="#333333",
                                       bd=1, relief=tk.SOLID)
        self.password_entry.grid(row=2, column=1, sticky="w")

        # Create the user type label and radio buttons
        self.user_type_label = tk.Label(content_frame, text="User Type:", font=("Helvetica", 12), fg="#333333")
        self.user_type_label.grid(row=3, column=0, sticky="e")
        self.user_type_var = tk.StringVar(value="employee")
        self.employee_radio = tk.Radiobutton(content_frame, text="Employee", variable=self.user_type_var,
                                             value="employee", font=("Helvetica", 10), fg="#333333",
                                             activeforeground="#333333", bg="#FFFFFF")
        self.employee_radio.grid(row=3, column=1, sticky="ew")
        self.student_radio = tk.Radiobutton(content_frame, text="Student", variable=self.user_type_var, value="student",
                                            font=("Helvetica", 10), fg="#333333", activeforeground="#333333",
                                            bg="#FFFFFF")
        self.student_radio.grid(row=3, column=2, sticky="ew")

        # Create the login and signup buttons
        self.login_button = tk.Button(content_frame, text="Login", font=("Helvetica", 12), bg="#333333", fg="#FFFFFF",
                                      bd=0, relief=tk.FLAT, command=self.login)
        self.login_button.grid(row=4, column=0, columnspan=2, sticky="ew")
        self.signup_button = tk.Button(content_frame, text="Sign Up", font=("Helvetica", 12), bg="#333333",
                                       fg="#FFFFFF", bd=0, relief=tk.FLAT, command=self.signup)
        self.signup_button.grid(row=4, column=2, sticky="ew")



    def students_Frame(self, user):
        # Load the background image
        image = Image.open("../images/library3.png")
        image = image.resize((self.winfo_screenwidth(), self.winfo_screenheight()))
        photo = ImageTk.PhotoImage(image)

        # Create a label to display the background image
        self.background_label = tk.Label(self, image=photo)
        self.background_label.image = photo
        self.background_label.grid(row=0, column=0, sticky="nsew")

        # Create the heading label
        heading_label = tk.Label(self, text="  Library Enclave Books  ", font=("Helvetica", 24), bg="lightblue")
        heading_label.place(relx=0.5, rely=0.25, anchor="n")

        # Create the main content frame
        content_frame = tk.Frame(self, bg="lightblue", padx=10, pady=10)
        content_frame.place(relx=0.5, rely=0.5, anchor="center")



        # Create the genre frame on the left with a specific width
        genre_frame = tk.Frame(content_frame, bg="lightgray", width=200, padx=10, pady=10)
        genre_frame.grid(row=0, column=0, sticky="ns")

        # Create the genre frame on the left
        genre_frame = tk.Frame(content_frame, bg="lightgray", padx=10, pady=10)
        genre_frame.grid(row=0, column=0, sticky="e")

        # Create the subheading label
        subheading_label = tk.Label(genre_frame, text="Book Search", font=("Verdana", 16), bg="lightgray")
        subheading_label.grid(row=0, column=0, columnspan=2, padx=4, pady=5)

        # Define the new list of genres
        genres = [
            "Computer Science",
            "Data Science",
            "Machine Learning",
            "Data Analytics",
            "Business Analytics",
            "Artificial Intelligence",
            "Cybersecurity",
            "Arts & Science"
        ]
        # Create genre buttons
        for i, genre in enumerate(genres):
            btn = tk.Button(genre_frame, text=genre, command=lambda g=genre: self.show_books_by_genre(g))

            btn.grid(row=i+1, column=0, sticky="ew", padx=5, pady=5)

        # Create a spacer frame between genre frame and books frame
        spacer_frame = tk.Frame(content_frame, bg="white", width=10)
        spacer_frame.grid(row=0, column=1)

        # Create the books frame on the right
        books_frame = tk.Frame(content_frame, bg="lightblue", padx=5, pady=5)
        books_frame.grid(row=0, column=2, sticky="e")

        # Create a new style for the headings
        style = ttk.Style()
        style.theme_use("clam")  # Choose the theme you prefer

        # Configure the style for the headings
        style.configure("Treeview.Heading", foreground="black", background="#bdde86")  # Adjust colors as needed

        # Create a treeview to display books
        self.books_tree = ttk.Treeview(books_frame, columns=("Book ID", "Title", "Author", "Availability"))
        self.books_tree.heading("#0", text="")
        self.books_tree.heading("#1", text="Book ID")
        self.books_tree.heading("#2", text="Title")
        self.books_tree.heading("#3", text="Author")
        # self.books_tree.heading("#4", text="Genre")
        self.books_tree.heading("#4", text="Availability")
        self.books_tree.grid(row=2, column=2, sticky="e")

        # Create logout button
        logout_button = tk.Button(content_frame, text="Logout", command=self.logout)
        logout_button.grid(row=1, column=5, sticky="se")

        # Adjust column weights for proper resizing
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=2)

    def employee_Frame(self, username):
        # Load the background image
        image = Image.open("../images/library2.png")
        image = image.resize((self.winfo_screenwidth(), self.winfo_screenheight()))
        photo = ImageTk.PhotoImage(image)

        # Create a label to display the background image
        self.background_label = tk.Label(self, image=photo)
        self.background_label.image = photo
        self.background_label.grid(row=0, column=0, sticky="nsew")

        # Create the main content frame
        content_frame = tk.Frame(self, bg="lightblue", padx=10, pady=10)
        content_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Create the frame on the left with a specific width
        self.employee_frame = tk.Frame(content_frame, bg="lightgray", width=200, padx=10, pady=10)
        self.employee_frame.grid(row=0, column=0, sticky="ew")

        # Create the frame on the left
        options_frame = tk.Frame(content_frame, bg="lightgray", padx=10, pady=10)
        options_frame.grid(row=0, column=0, sticky="ew")

        # Create the subheading label
        subheading_label = tk.Label(self.employee_frame, text="                   Library Enclave   ",
                                      font=("Helvetica", 24, "bold"), fg="#FFFFFF", bg="#398333")
        subheading_label.grid(row=0, column=8, columnspan=2, padx=4, pady=5)
        # Create the subheading label
        subheading_label = tk.Label(self.employee_frame, text=f'Welcome {username}!', font=("Verdana", 15), bg="lightgray")
        subheading_label.grid(row=2, column=6, columnspan=2, padx=4, pady=5)
        # Create buttons for each operation
        add_book_button = tk.Button(self.employee_frame, text="Add Book", bg="#398333", command=lambda: self.perform_book_operations("Add Book"))
        add_book_button.grid(row=4, column=0, padx=5, pady=5, sticky="ew")

        update_book_button = tk.Button(self.employee_frame, text="Update Book", bg="#398333", command=lambda: self.perform_book_operations("Update Book"))
        update_book_button.grid(row=5, column=0, padx=5, pady=5, sticky="ew")

        delete_book_button = tk.Button(self.employee_frame, text="Delete Book", bg="#398333", command=lambda: self.perform_book_operations("Delete Book"))
        delete_book_button.grid(row=6, column=0, padx=5, pady=5, sticky="ew")

        issue_book_button = tk.Button(self.employee_frame, text="Issue Book", bg="#398333", command=lambda: self.perform_book_operations("Issue Book"))
        issue_book_button.grid(row=7, column=0, padx=5, pady=5, sticky="ew")

        return_book_button = tk.Button(self.employee_frame, text="Return Book", bg="#398333", command=lambda: self.perform_book_operations("Return Book"))
        return_book_button.grid(row=8, column=0, padx=5, pady=5, sticky="ew")

        # Create a frame for displaying operation results
        self.operation_frame = tk.Frame(self.employee_frame, bg="white", padx=10, pady=10)
        self.operation_frame.grid(row=7, column=7, rowspan=5, padx=10, pady=10, sticky="se")

        # Create logout button
        logout_button = tk.Button(self.employee_frame, text="Logout", bg="#398333", command=self.logout)
        logout_button.grid(row=11, column=15, sticky="se")

    # Function to display label and entry fields for book ID and username
    def perform_book_operations(self, operation):
        # Clear any existing widgets in the operation frame
        for widget in self.operation_frame.winfo_children():
            widget.destroy()

        # Add labels and entry fields based on the operation
        if operation == "Add Book":
            labels = ["Book ID:", "Title:", "Author:", "Genre:", "Availability:"]
        elif operation == "Update Book":
            labels = ["Enter Book ID to Update:", "New Availability:"]
        elif operation == "Delete Book":
            labels = ["Enter Book ID to Delete:"]
        elif operation == "Issue Book":
            labels = ["Enter Book ID to Issue:"]
        elif operation == "Return Book":
            labels = ["Enter Book ID to Return:"]

        # Create labels and entry fields
        entry_fields = []
        for i, label_text in enumerate(labels):
            label = tk.Label(self.operation_frame, text=label_text, bg="white")
            label.grid(row=i, column=0, padx=5, pady=5, sticky="w")

            entry = tk.Entry(self.operation_frame)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
            entry_fields.append(entry)

        # Add a submit button
        submit_button = tk.Button(self.operation_frame, text="Submit",
                                  command=lambda: self.submit_operation(operation,
                                                                        *[entry.get() for entry in entry_fields]))

        submit_button.grid(row=i + 1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

    # Function to handle submit button click for each operation
    def submit_operation(self, operation, *args):
        if operation == "Delete Book":
            self.delete_book(*args)
        elif operation == "Add Book":
            book_id, title, author, genre, availability = args
            self.add_book(book_id, title, author, genre, availability)
        elif operation == "Update Book":
            book_id, new_availability = args
            self.update_book(book_id, new_availability)
        elif operation == "Issue Book":
            self.issue_book(*args)
        elif operation == "Return Book":
            self.return_book(*args)

    # Function to handle logout
    def logout(self):
        # Show the main login frame
        self.Login_Frame()



    def login(self):
        # Get the username, password, and user type from the entry fields
        username = self.username_entry.get()
        password = self.password_entry.get()
        user_type = self.user_type_var.get()

        # Check if username and password are not empty
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
            return

        # Check the database for the entered credentials
        self.cursor.execute('''SELECT * FROM users WHERE username=? AND password=? AND user_type=?''',
                            (username, password, user_type))
        user = self.cursor.fetchone()

        # If user exists, show a welcome message and proceed
        if user:
            if user_type == "student":
                # messagebox.showinfo("Login", f"Welcome, {username}!")
                self.students_Frame(username)
            elif user_type == "employee":
                self.employee_Frame(username)

        else:
            messagebox.showerror("Error", "Invalid username or password.")


    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user_type = self.user_type_var.get()

        self.cursor.execute('''SELECT * FROM users WHERE username=?''', (username,))
        existing_user = self.cursor.fetchone()

        if existing_user:
            messagebox.showerror("Error", "Username already exists.")
        else:
            self.cursor.execute('''INSERT INTO users (username, password, user_type) VALUES (?, ?, ?)''',
                                (username, password, user_type))
            self.conn.commit()
            messagebox.showinfo("Success", "User created successfully.")

    # Function to add a book to the database
    def add_book(self, book_id, title, author, genre, availability):
        return_message_label = tk.Label(self.operation_frame, bg="white")
        return_message_label.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        try:
            conn = sqlite3.connect('../books.db')
            c = conn.cursor()
            c.execute('INSERT INTO books VALUES (?, ?, ?, ?, ?)', (book_id, title, author, genre, availability))
            conn.commit()
            conn.close()
            message=f"Book added successfully: {title}"
            self.update_return_message(return_message_label, message)
        except sqlite3.Error as e:
            message=f"Error adding book: {e}"
            self.update_return_message(return_message_label, message)

    # Function to Update a book to the database
    def update_book(self, book_id, new_availability):
        return_message_label = tk.Label(self.operation_frame, bg="white")
        return_message_label.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        try:
            conn = sqlite3.connect('../books.db')
            c = conn.cursor()
            c.execute('UPDATE books SET availability = ? WHERE id = ?', (new_availability, book_id))
            conn.commit()
            conn.close()

            message = f"Book availability updated successfully: {book_id}"
            self.update_return_message(return_message_label, message)
        except sqlite3.Error as e:
            message=f"Error updating book availability: {e}"
            self.update_return_message(return_message_label, message)

    # Function to delete a book from the database
    def delete_book(self, book_id):
        conn = sqlite3.connect('../books.db')
        c = conn.cursor()
        c.execute('DELETE FROM books WHERE id = ?', (book_id,))
        conn.commit()
        conn.close()
        return_message_label = tk.Label(self.operation_frame, bg="white")
        return_message_label.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        message = f"Book with ID {book_id} Deleted successfully"
        self.update_return_message(return_message_label, message)

    # Function to issue a book (decrease availability) in the database
    def issue_book(self, book_id):
        conn = sqlite3.connect('../books.db')
        c = conn.cursor()
        c.execute('UPDATE books SET availability = availability - 1 WHERE id = ?', (book_id,))
        conn.commit()
        conn.close()
        return_message_label = tk.Label(self.operation_frame, bg="white")
        return_message_label.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        message = f"Book with ID {book_id} Issued successfully"
        self.update_return_message(return_message_label, message)

    # Function to return a book (increase availability) in the database
    def return_book(self, book_id):
        conn = sqlite3.connect('../books.db')
        c = conn.cursor()
        c.execute('UPDATE books SET availability = availability + 1 WHERE id = ?', (book_id,))
        conn.commit()
        conn.close()
        return_message_label = tk.Label(self.operation_frame, bg="white")
        return_message_label.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        message = f"Book with ID {book_id} returned successfully"
        self.update_return_message(return_message_label, message)


    def update_return_message(self, label, message):
        label.config(text=message, fg="red")  # Set text color to red
        label.grid(row=10, column=0, columnspan=5, padx=10, pady=10, sticky="e")  # Position on the extreme right side


# Main function to start the application
def main():
    app = LibraryManagementSystem()
    app.mainloop()

if __name__ == "__main__":
    main()
