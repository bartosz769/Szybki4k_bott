import os
import json
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

GROUPS_FILE = "groups.json"
MESSAGE_FILE = "message.txt"


# ------------------- POMOCNICZE -------------------

def load_groups():
    if not os.path.exists(GROUPS_FILE):
        return []
    with open(GROUPS_FILE, "r") as f:
        return json.load(f)

def save_groups(groups):
    with open(GROUPS_FILE, "w") as f:
        json.dump(groups, f)

def load_message():
    if not os.path.exists(MESSAGE_FILE):
        return "😈😈😈"
    with open(MESSAGE_FILE, "r") as f:
        return f.read()

def save_message(text):
    with open(MESSAGE_FILE, "w") as f:
        f.write(text)


# ------------------- KOMENDY -------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot działa 😈")

async def addgroup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    groups = load_groups()

    if chat_id not in groups:
        groups.append(chat_id)
        save_groups(groups)
        await update.message.reply_text("✅ Grupa dodana.")
    else:
        await update.message.reply_text("Ta grupa już jest dodana.")

async def setmessage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Użycie: /setmessage twoja wiadomość")
        return

    new_text = " ".join(context.args)
    save_message(new_text)
    await update.message.reply_text("✅ Wiadomość zmieniona.")

async def send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    groups = load_groups()
    message = load_message()

    if not groups:
        await update.message.reply_text("Brak dodanych grup.")
        return

    for group_id in groups:
        try:
            await context.bot.send_message(chat_id=group_id, text=message)
        except Exception as e:
            print(f"Błąd wysyłania do {group_id}: {e}")

    await update.message.reply_text("📨 Wysłano do wszystkich grup.")


# ------------------- START BOTA (ważne dla Render) -------------------

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("addgroup", addgroup))
    app.add_handler(CommandHandler("setmessage", setmessage))
    app.add_handler(CommandHandler("send", send))

    print("Bot działa...")

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    # Bot działa bez kończenia programu
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
