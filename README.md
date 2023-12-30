# Task Manager

Task Manager is a task management service using a Telegram bot written in Python. It allows users to create, view, update, and delete tasks directly in the Telegram chat, providing a simple and efficient way to track their tasks throughout the day.

## Installation

Follow these steps to install and setup the Task Manager:

Clone the repository:
```
git clone <https or SSH URL>
```

Navigate to the project folder:
```
cd taskmaster
```

Create and activate a virtual environment:
```
python3.11 -m venv venv
source venv/bin/activate
```

Upgrade pip:
```
python -m pip install --upgrade pip
```

Install dependencies:
```
pip install -r requirements.txt
```

Run migrations:
```
python manage.py migrate
```

Run the server:
```
python manage.py runserver
```

Run the TelegramBot:
```
python bot.py
```

## Usage

### Web Application

After running the server, you can interact with the web application. Here are some of the functionalities provided:

- Viewing a list of all tasks: Navigate to the home page (`/`).
- Creating a new task: Navigate to `/create/`.
- Updating a task: Navigate to `/update/<int:pk>/`, where `pk` is the id of the task.
- Deleting a task: Navigate to `/delete/<int:pk>/`, where `pk` is the id of the task.
- User registration: Navigate to `/register/`.
- User login: Navigate to `/login/`. After successful login, you will be redirected to the task list.
- Viewing a user profile: Navigate to `/user/<str:username>/`, where `username` is the username of the user.
- Updating a user profile: Navigate to `/user/<str:username>/update/`, where `username` is the username of the user.
- User logout: Navigate to `/logout/`. After successful logout, you will be redirected to the task list.
- Changing a user password: Navigate to `/password_change/`.
- Confirmation of password change: Navigate to `/password_change/done/`.

### Telegram Bot

The bot's name is `@TaskManagerForYouBot`. You can search for this name in the Telegram app to find and start interacting with the bot.

After running the bot, you can interact with it in the Telegram chat. Here are some of the commands you can use:

- `/start`: Start interacting with the bot.
- `/create_task`: Create a new task.
- `/update_task`: Update a task.
- `/delete_task`: Delete a task.
- `/list_tasks`: View all your tasks.

To start using the bot, you need to set the `TELEGRAM_TOKEN` environment variable to your bot token, which you can get from the BotFather in Telegram. After that, you can run the bot and start interacting with it in the Telegram chat.

### API Documentation

After starting the project, navigate to http://127.0.0.1:8000/redoc/. The documentation describes how your API should work. The documentation is presented in Redoc format.