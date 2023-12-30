"""
This module contains a Telegram bot for task management.
The bot allows users to create, update, delete, and list tasks.
Each task is associated with the user who created it,
and users can only manage their own tasks.
"""

import os
import sys
import time

import django
import telebot
from telebot import types

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskmaster.settings')
django.setup()
from django.contrib.auth.models import User

from tasks.models import Task

API_REQUEST_DELAY = 1
MAX_TITLE_LENGTH = 200

TOKEN = os.getenv('TELEGRAM_TOKEN')
if not TOKEN:
    print('Error: Telegram token not found.'
          ' Please set the TELEGRAM_TOKEN environment variable.')
    sys.exit(1)
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    """
    Handle the /start command.
    Create a new user if the user does not exist, and send a welcome message.
    """
    user_id = message.from_user.id
    user, created = User.objects.get_or_create(username=str(user_id))
    if created:
        bot.reply_to(
            message,
            'Hello! I am your Task Manager bot.'
            ' You can start by creating a new task with /create_task command.')
    else:
        bot.reply_to(message,
                     'Welcome back! You can continue managing your tasks.')
    time.sleep(API_REQUEST_DELAY)


@bot.message_handler(commands=['create_task'])
def create_task(message):
    """
    Handle the /create_task command.
    Ask the user to enter the title and description of the new task.
    """
    markup = types.ForceReply(selective=False)
    bot.send_message(
        message.chat.id,
        'Enter the title of the new task'
        ' and the task description separated by a space:',
        reply_markup=markup)
    time.sleep(API_REQUEST_DELAY)


@bot.message_handler(
    func=lambda message: message.reply_to_message is not None and
    message.reply_to_message.text ==
    'Enter the title of the new task'
    ' and the task description separated by a space:')
def save_new_task(message):
    """
    Handle the reply to the /create_task command.
    Create a new task with the title and description provided by the user.
    """
    user_id = message.from_user.id
    user, created = User.objects.get_or_create(username=str(user_id))
    split_message = message.text.split(maxsplit=1)
    if len(split_message) == 2:
        task_title, task_description = split_message
        if len(task_title) > MAX_TITLE_LENGTH:
            bot.reply_to(message, 'The task title is too long.')
            return
        Task.objects.create(title=task_title, description=task_description,
                            author=user)
        bot.reply_to(message, 'Task created.')
    else:
        bot.reply_to(
            message,
            'You did not specify the task title and task description.')
    time.sleep(API_REQUEST_DELAY)


@bot.message_handler(commands=['update_task'])
def update_task(message):
    """
    Handle the /update_task command.
    Ask the user to enter the title of the task to update
    and the new task text.
    """
    markup = types.ForceReply(selective=False)
    bot.send_message(
        message.chat.id,
        ('Enter the title of the task to update'
         ' and the new task text separated by a space:'),
        reply_markup=markup)
    time.sleep(API_REQUEST_DELAY)


@bot.message_handler(
    func=lambda message: message.reply_to_message is not None and
    message.reply_to_message.text ==
    ('Enter the title of the task to update'
     ' and the new task text separated by a space:'))
def modify_task(message):
    """
    Handle the reply to the /update_task command.
    Update the task with the new text provided by the user.
    """
    user_id = message.from_user.id
    user, created = User.objects.get_or_create(username=str(user_id))
    split_message = message.text.split(maxsplit=1)
    if len(split_message) == 2:
        task_title, new_task_text = split_message
        try:
            task = Task.objects.get(title=task_title, author=user)
            task.text = new_task_text
            task.save()
            bot.reply_to(message, 'Task updated.')
        except Task.DoesNotExist:
            bot.reply_to(message, 'Task not found.')
    else:
        bot.reply_to(message,
                     'You did not specify the task title and new task text.')
    time.sleep(API_REQUEST_DELAY)


@bot.message_handler(commands=['delete_task'])
def delete_task(message):
    """
    Handle the /delete_task command.
    Ask the user to enter the title of the task to delete.
    """
    markup = types.ForceReply(selective=False)
    bot.send_message(message.chat.id, 'Enter the title of the task to delete:',
                     reply_markup=markup)
    time.sleep(API_REQUEST_DELAY)


@bot.message_handler(
    func=lambda message: message.reply_to_message is not None and
    message.reply_to_message.text == 'Enter the title of the task to delete:')
def confirm_task_deletion(message):
    """
    Handle the reply to the /delete_task command.
    Ask the user to confirm the deletion of the task.
    """
    user_id = message.from_user.id
    user, created = User.objects.get_or_create(username=str(user_id))
    task_title = message.text.strip()
    try:
        Task.objects.get(title=task_title, author=user)
        markup = types.ForceReply(selective=False)
        bot.send_message(
            message.chat.id,
            (f'Are you sure you want to delete the task "{task_title}"?'
             f' Reply with Yes or No.'),
            reply_markup=markup)
    except Task.DoesNotExist:
        bot.reply_to(message, 'Task not found.')
    time.sleep(API_REQUEST_DELAY)


@bot.message_handler(
    func=lambda message: message.reply_to_message is not None and
    message.reply_to_message.text.startswith(
        'Are you sure you want to delete the task'))
def remove_task(message):
    """
    Handle the reply to the task deletion confirmation.
    Delete the task if the user confirmed the deletion.
    """
    if message.text.lower() == 'yes':
        user_id = message.from_user.id
        user, created = User.objects.get_or_create(username=str(user_id))
        task_title = message.reply_to_message.text.replace(
            'Are you sure you want to delete the task "', '').replace(
                '"? Reply with Yes or No.', '').strip()
        try:
            task = Task.objects.get(title=task_title, author=user)
            task.delete()
            bot.reply_to(message, 'Task deleted.')
        except Task.DoesNotExist:
            bot.reply_to(message, 'Task not found.')
    elif message.text.lower() == 'no':
        bot.reply_to(message, 'Task deletion cancelled.')
    else:
        bot.reply_to(message, 'Invalid response. Please reply with Yes or No.')
    time.sleep(API_REQUEST_DELAY)


@bot.message_handler(commands=['list_tasks'])
def list_tasks(message):
    """
    Handle the /list_tasks command.
    Send a list of the user's tasks.
    """
    user_id = message.from_user.id
    user = User.objects.get(username=str(user_id))
    tasks = Task.objects.filter(author=user).order_by('-created_at')
    if tasks.exists():
        response = '\n'.join([f'{task.title}' for task in tasks])
        bot.reply_to(message, response)
    else:
        bot.reply_to(message, 'No tasks.')
    time.sleep(API_REQUEST_DELAY)


bot.polling()
