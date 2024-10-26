# NexMenu

NexMenu is a web application that allows users to create, manage, and share menus effortlessly. The application provides an easy-to-use interface for adding and categorizing menu items, customizing menus, and collaborating with others.

## Features

- Create and manage your menus effortlessly
- Add and categorize menu items
- Customize your menu with ease
- Share your menu with others
- Edit your menus in real-time from an easy-to-use interface
- Access your menus from any device, anywhere
- Collaborate with others to build the perfect menu
- Feature your menus in the Catalog to reach a wider audience

## Technologies Used

### Backend:
- Python
- Django
- PostgreSQL

### Frontend:
- JavaScript
- HTML
- CSS
- Alpine.js

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/nexmenu.git
    cd nexmenu
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Apply migrations:
    ```sh
    python manage.py migrate
    ```

5. Run the development server:
    ```sh
    python manage.py runserver
    ```

6. Open your browser and navigate to `http://127.0.0.1:8000/` to see the application in action.

## Usage

- **Home Page**: Provides an introduction to NexMenu and its features.
- **Catalog**: Browse and explore menus featured by users.
- **Login/Register**: Create an account or log in to manage your menus.

## Project Structure

- `catalog/`: Contains the catalog app for searching and displaying menus in the Catalog.
- `menu/`: Contains the menu app for managing and displaying menus.
- `templates/`: Contains HTML templates for rendering the web pages.
- `urls.py`: URL routing for the application.
- `menu/views.py`and `catalog/views.py`: Contains the backend functions for handling requests and rendering templates.


## License

This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International Public License.
