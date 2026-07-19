# Telegram Task Bot

This is a Telegram bot built to manage tasks directly from the chat.

The bot supports multiple users, using a SQLite database to make sure each person can only access and manage their own list, kept fully isolated from everyone else's.

## Commands

| Command | What it does |
|---|---|
| `/start` | Welcome message |
| `/add <task>` | Adds a new task |
| `/list` | Lists pending tasks |
| `/done <id>` | Marks a task as completed |
| `/remove <id>` | Removes a task |
| `/help` | Shows the available commands |

## How to run

1. Create a bot with [@BotFather](https://t.me/BotFather) on Telegram and
   copy the token it gives you.

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and paste your token in there:
   ```bash
   cp .env.example .env
   ```

4. Run:
   ```bash
   python src/bot.py
   ```

5. Open a chat with the bot on Telegram and send `/start`.

## Structure

```
telegram-bot-python/
├── src/
│   ├── bot.py          # commands and integration with the Telegram API
│   └── database.py     # everything related to the database (SQLite)
├── .env.example
├── .gitignore
└── requirements.txt
```

## Tech stack

- **python-telegram-bot** to talk to the Telegram API
- **SQLite** to store the tasks (no external database server needed)
- **python-dotenv** to keep the token out of the source code

## Why the token is kept in a `.env` file

A bot token is like a password — anyone who gets it can control the bot.
That's why it lives in an environment variable, and the `.env` file is
listed in `.gitignore`, so it never accidentally ends up on GitHub.

## Next ideas

- Scheduled reminders (the bot notifies you at a set time)
- Task priority levels
- Editing an existing task, instead of having to delete and re-add it
