import json
import schedule
import time
import requests
import random
import argparse
from datetime import datetime, timedelta
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

DISCORD_WEBHOOK_URL = 'discordwebhookhere'

# Define your Telegram bot token here
TELEGRAM_BOT_TOKEN = 'Telegram bot token here'

# Define your Telegram chat ID here
TELEGRAM_CHAT_ID = 'Telegram chat ID here'

# Load your class data from a JSON file (update the file path)
def load_class_data():
    with open('class_data.json', 'r') as file:  # Update the file path here
        return json.load(file)['classes']

# Initialize the class data
class_data = load_class_data()

# Initialize the Discord webhook client
def get_discord_webhook():
    return requests.post(DISCORD_WEBHOOK_URL)

# Initialize the Telegram bot
def get_telegram_bot():
    return requests.get(f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getMe')

# Function to send class details to Discord
def send_class_details_discord(class_name, teacher, time_range, date, location, week_duration):
    emoji = emoji_dict.get(class_name, "")  # Get the emoji for the class if available
    message = f"{emoji} Class: {class_name}\n"
    message += f"{param_emojis['Teacher']} Teacher: {teacher}\n"
    message += f"{param_emojis['Time']} Time: {time_range}\n"
    message += f"{param_emojis['Date']} Date: {date}\n"
    message += f"{param_emojis['Location']} Location: {location}\n"
    message += f"{param_emojis['Duration']} Duration: {week_duration}."

    print(f"Sending Discord message:\n{message}")  # Add this line for debugging
    webhook = get_discord_webhook()
    data = {"content": message}
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    response.raise_for_status()

    # Send random metaphorical message
    send_random_metaphorical_message_discord()

# Function to send class details to Telegram
def send_class_details_telegram(class_name, teacher, time_range, date, location, week_duration):
    emoji = emoji_dict.get(class_name, "")  # Get the emoji for the class if available
    message = f"{emoji} Class: {class_name}\n"
    message += f"{param_emojis['Teacher']} Teacher: {teacher}\n"
    message += f"{param_emojis['Time']} Time: {time_range}\n"
    message += f"{param_emojis['Date']} Date: {date}\n"
    message += f"{param_emojis['Location']} Location: {location}\n"
    message += f"{param_emojis['Duration']} Duration: {week_duration}."

    print(f"Sending Telegram message:\n{message}")  # Add this line for debugging
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    data = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message
    }
    response = requests.post(url, data=data)
    response.raise_for_status()

    # Send random metaphorical message
    send_random_metaphorical_message_telegram()
parser = argparse.ArgumentParser(description='Send class details and reminders to Discord or Telegram.')
parser.add_argument('--taskname', help='Task name (e.g., assignment, presentation, meeting)')
parser.add_argument('--repeat', action='store_true', help='Repeat the reminder daily')
parser.add_argument('-v', '--notification', choices=['discord', 'telegram'], default='discord', help='Notification platform (default: discord)')
args = parser.parse_args()
# Function to send random metaphorical message to Discord
def send_random_metaphorical_message_discord():
    metaphorical_messages = [
        "Embrace the challenges in today's class. They are stepping stones to success! 💪",
        "Learning is a journey. Enjoy every step of it. 🚀",
        "Stay curious and keep learning. Knowledge knows no bounds! 🧠",
    ]
    random_message = random.choice(metaphorical_messages)
    data = {"content": random_message}
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    response.raise_for_status()

# Function to send random metaphorical message to Telegram
def send_random_metaphorical_message_telegram():
    metaphorical_messages = [
        "Embrace the challenges in today's class. They are stepping stones to success! 💪",
        "Learning is a journey. Enjoy every step of it. 🚀",
        "Stay curious and keep learning. Knowledge knows no bounds! 🧠",
    ]
    random_message = random.choice(metaphorical_messages)
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    data = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': random_message
    }
    response = requests.post(url, data=data)
    response.raise_for_status()

# Function to send the schedule for the next day at 11:59 PM
def send_schedule_for_next_day():
    # Get the current date and time
    now = datetime.now()
    current_day = now.strftime("%A")
    current_time = now.strftime("%H:%M")

    # Calculate the next day's date
    next_day_date = now + timedelta(days=1)
    formatted_next_day_date = next_day_date.strftime("%A")

    # Get all classes that match the next day's date from the JSON file
    matching_classes = [class_info for class_info in class_data if class_info["Day"] == formatted_next_day_date]

    for class_info in matching_classes:
        class_name = class_info["classname"]
        teacher = class_info["teacher"]
        time_range = class_info["time"]
        location = class_info.get("location", "")
        week_duration = class_info["week_duration"]

        # Extract start and end times from the time_range
        start_time_str, end_time_str = map(str.strip, time_range.split('-'))

        # Convert start and end times to datetime objects
        start_time = datetime.strptime(start_time_str, "%I.%M%p").strftime("%H:%M")
        end_time = datetime.strptime(end_time_str, "%I.%M%p").strftime("%H:%M")

        # Check if the class is scheduled for the next day and the current time is 20 minutes before the class
        class_start_time = datetime.strptime(start_time, "%H:%M")
        notification_time = class_start_time - timedelta(minutes=20)
        formatted_notification_time = notification_time.strftime("%H:%M")

        if current_day == formatted_next_day_date and current_time == formatted_notification_time:
            # Send the schedule message to both Discord and Telegram
            send_class_details_discord(class_name, teacher, f"{start_time}-{end_time}", formatted_next_day_date, location, week_duration)
            send_class_details_telegram(class_name, teacher, f"{start_time}-{end_time}", formatted_next_day_date, location, week_duration)

# Schedule sending the schedule for the next day at 11:59 PM
schedule.every().day.at("23:59").do(send_schedule_for_next_day)

# Define your emoji dictionary
emoji_dict = {
    "💻 Operating System Principle": "🖥️",
    "📝 Principles of Computer Composition": "📚",
    "🌐 Web application development basics": "🌐",
    # Add more class names and corresponding emojis as needed
}


args = parser.parse_args() 
# Define your parameter emojis dictionary
param_emojis = {
    "Teacher": "👨‍🏫",
    "Time": "⏰",
    "Date": "📅",
    "Location": "📍",
    "Duration": "⏳",
}

# Function to update class data when the JSON file changes
class FileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path == 'class_data.json':  # Update the file path here
            print("Class data file modified, updating...")
            global class_data
            class_data = load_class_data()

# Watch for changes to the class data file
observer = Observer()
observer.schedule(FileChangeHandler(), path='.', recursive=False)
observer.start()


# Get the current day
current_day = datetime.now().strftime("%A")

# Start scheduling tasks
for class_info in class_data:
    class_name = class_info["classname"]
    teacher = class_info["teacher"]
    time_range = class_info["time"]
    day = class_info["Day"]
    location = class_info.get("location", "")
    week_duration = class_info["week_duration"]

    # Extract the start and end times from the time_range
    start_time_str, end_time_str = map(str.strip, time_range.split('-'))

    # Handle 'am' and 'pm' indications
    start_time_str = start_time_str.replace('am', ' AM').replace('pm', ' PM')
    end_time_str = end_time_str.replace('am', ' AM').replace('pm', ' PM')

    # Use 24-hour format and parse the time
    start_time = datetime.strptime(start_time_str, "%I.%M %p").strftime("%H:%M")
    end_time = datetime.strptime(end_time_str, "%I.%M %p").strftime("%H:%M")

    # Calculate the notification time as 20 minutes before the start time
    class_start_time = datetime.strptime(start_time, "%H:%M")
    notification_time = class_start_time - timedelta(minutes=20)
    formatted_notification_time = notification_time.strftime("%H:%M")

    # Check if the class is scheduled for the current day
    if day == current_day:
        # Schedule class notification based on the notification platform
        if args.notification == 'discord':
            schedule.every().day.at(formatted_notification_time).do(send_class_details_discord, class_name, teacher, f"{start_time}-{end_time}", day, location, week_duration).tag(class_name)
        elif args.notification == 'telegram':
            schedule.every().day.at(formatted_notification_time).do(send_class_details_telegram, class_name, teacher, f"{start_time}-{end_time}", day, location, week_duration).tag(class_name)


# Schedule the custom task with specified time
if args.taskname:
    if args.notification == 'discord':
        send_class_details_discord(args.taskname, '', '', '', '', '')
    elif args.notification == 'telegram':
        send_class_details_telegram(args.taskname, '', '', '', '', '')

QUOTES_API_URL = 'https://favqs.com/api/qotd'

# Function to fetch a random motivational quote from the favqs.com API
def fetch_motivational_quote():
    try:
        response = requests.get(QUOTES_API_URL)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        if data and 'quote' in data and 'author' in data['quote']:
            quote = data['quote']['body']
            author = data['quote']['author']
            return f'"{quote}" - {author}'
    except requests.exceptions.RequestException as e:
        print(f"RequestException: {e}")
    except (ValueError, KeyError) as e:
        print(f"Error parsing API response: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return None

# Function to send a random motivational quote to both Discord and Telegram
def send_motivational_quote():
    quote = fetch_motivational_quote()
    if quote:
        message = f"🚀 Motivational Quote:\n{quote}"
        webhook = get_discord_webhook()
        data = {"content": message}
        response = requests.post(DISCORD_WEBHOOK_URL, json=data)
        response.raise_for_status()

        url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
        data = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': message
        }
        response = requests.post(url, data=data)
        response.raise_for_status()

# Schedule sending motivational quotes every 2/3 hours
schedule.every(6).to(7).hours.do(send_motivational_quote)



while True:
    schedule.run_pending()
    time.sleep(1)
