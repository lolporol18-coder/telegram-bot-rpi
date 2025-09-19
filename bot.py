#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Замени 'YOUR_TOKEN_HERE' на токен от @BotFather

import os
TOKEN = os.getenv("TELEGRAM_TOKEN")
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я твой бот на Raspberry Pi 😊")

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    print("Бот запущен...")
    application.run_polling()

if __name__ == "__main__":
    main()