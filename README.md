# Madola Restaurant

Madola Restaurant is a Django-based web application that serves as an online platform for showcasing the restaurant's offerings, managing reservations, and providing information to customers. The front end is built using Bootstrap for a responsive and modern design.

## Project Structure

```
madola_restaurant/
├── madola_restaurant/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── restaurant/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   ├── templates/
│   │   └── restaurant/
│   │       └── index.html
│   └── static/
│       └── restaurant/
│           └── css/
│               └── bootstrap.min.css
├── manage.py
└── README.md
```

## Features

- **Responsive Design**: Utilizes Bootstrap for a mobile-friendly interface.
- **Django Admin**: Easy management of restaurant data through the Django admin interface.
- **Customizable**: Easily extendable to add more features like online ordering or user accounts.

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd madola_restaurant
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```
   python manage.py migrate
   ```

5. Run the development server:
   ```
   python manage.py runserver
   ```

6. Access the application at `http://127.0.0.1:8000/`.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.