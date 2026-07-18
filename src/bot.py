"""
Bot de gerenciamento de tarefas para Telegram.

Comandos disponiveis:
  /start          - mensagem de boas-vindas
  /add <tarefa>   - adiciona uma nova tarefa
  /list           - lista as tarefas pendentes
  /done <id>      - marca uma tarefa como concluida
  /remove <id>    - remove uma tarefa
  /help           - mostra a lista de comandos

Uso: preencha o BOT_TOKEN no arquivo .env e rode "python src/bot.py"
"""

import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

import database

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Ola! Eu sou seu bot de tarefas. 📝\n\n"
        "Use /add <tarefa> para adicionar algo a fazer, "
        "/list para ver suas tarefas, e /help para ver todos os comandos."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Comandos disponiveis:\n\n"
        "/add <tarefa> - adiciona uma nova tarefa\n"
        "/list - lista suas tarefas pendentes\n"
        "/done <id> - marca uma tarefa como concluida\n"
        "/remove <id> - remove uma tarefa\n"
        "/help - mostra esta mensagem"
    )


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Uso correto: /add <descricao da tarefa>")
        return

    description = " ".join(context.args)
    user_id = update.effective_user.id
    task_id = database.add_task(user_id, description)

    await update.message.reply_text(f"✅ Tarefa #{task_id} adicionada: {description}")


async def list_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    tasks = database.list_tasks(user_id)

    if not tasks:
        await update.message.reply_text("Voce nao tem tarefas pendentes. 🎉")
        return

    lines = [f"#{task['id']} - {task['description']}" for task in tasks]
    await update.message.reply_text("Suas tarefas pendentes:\n\n" + "\n".join(lines))


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text("Uso correto: /done <id da tarefa>")
        return

    task_id = int(context.args[0])
    user_id = update.effective_user.id

    if database.mark_done(user_id, task_id):
        await update.message.reply_text(f"✅ Tarefa #{task_id} marcada como concluida!")
    else:
        await update.message.reply_text(f"Tarefa #{task_id} nao encontrada.")


async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text("Uso correto: /remove <id da tarefa>")
        return

    task_id = int(context.args[0])
    user_id = update.effective_user.id

    if database.remove_task(user_id, task_id):
        await update.message.reply_text(f"🗑️ Tarefa #{task_id} removida.")
    else:
        await update.message.reply_text(f"Tarefa #{task_id} nao encontrada.")


def main() -> None:
    if not BOT_TOKEN:
        raise RuntimeError(
            "BOT_TOKEN nao encontrado. Copie .env.example para .env e "
            "preencha com o token gerado pelo @BotFather."
        )

    database.init_db()

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("list", list_tasks))
    app.add_handler(CommandHandler("done", done))
    app.add_handler(CommandHandler("remove", remove))

    logger.info("Bot iniciado. Pressione Ctrl+C para parar.")
    app.run_polling()


if __name__ == "__main__":
    main()
