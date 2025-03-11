# Online Library Management System (Backend)

The **Online Library Management System** is a full-stack Python application designed to manage library operations efficiently. It provides a seamless experience for administrators, librarians, and members to handle books, users, borrowing records, and returns. The backend is built using **Django** with a structured approach for database management and API handling.

## Features
- **User Authentication & Role-based Access (Admins, Librarians, Members)**
- **CRUD Operations for Book Management**
- **Borrow & Return Book Functionality**
- **Fine Calculation for Late Returns**
- **Search & Filter Books**
- **Responsive Web Interface with Django Templates**

## Tech Stack
- **Backend:** Django (Python Full-Stack)
- **Database:** SQLite/PostgreSQL
- **Templating Engine:** Django Templates
- **Authentication:** Django User Model

## Installation & Setup
### Prerequisites:
- Python 3.8+
- PostgreSQL (if not using SQLite)
- pip & virtualenv

### Steps:
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/online-library-management.git
   cd online-library-management
   ```
2. Create a virtual environment and activate it:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Set up environment variables (`.env` file in root directory, if needed):
   ```sh
   SECRET_KEY=your_secret_key
   DATABASE_URL=your_postgres_db_url  # If using PostgreSQL
   ```
5. Run database migrations:
   ```sh
   python manage.py migrate
   ```
6. Create a superuser for admin access:
   ```sh
   python manage.py createsuperuser
   ```
7. Start the development server:
   ```sh
   python manage.py runserver
   ```
8. The backend and web interface will be available at `http://127.0.0.1:8000`



## API & Web Endpoints
| Method | Endpoint | Description |
|--------|---------|-------------|
| GET | `/` | Home page |
| GET | `/admin/` | Django Admin Panel |
| GET | `/books/` | List of books |
| POST | `/books/add/` | Add a new book (Admin only) |
| GET | `/books/:id` | Get book details |
| PUT | `/books/:id/update` | Update book information (Admin only) |
| DELETE | `/books/:id/delete` | Delete a book (Admin only) |
| POST | `/borrow/` | Borrow a book |
| POST | `/return/` | Return a borrowed book |
| GET | `/borrow/history/` | View borrowing history |


## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact
For queries or collaborations, feel free to reach out:
📧 venerablevignesh@gmail.com

