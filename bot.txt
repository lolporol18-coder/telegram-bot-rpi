#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from dotenv import load_dotenv
import os

# Загружаем переменные окружения из .env
load_dotenv()

# Получаем токен из переменной окружения
TOKEN = os.getenv("TOKEN")

# Определяем этапы разговора
PRODUCT, WAREHOUSE, CITY, FIO, AMOUNT, DELIVERY, CHANNEL, INVOICE, STATUS = range(9)

# Списки для кнопок
WAREHOUSES = ["Склад А", "Склад Б", "Склад В"]
CHANNELS = ["Авито", "Дром", "Wildberries", "Ozon"]
STATUSES = ["На складе", "В пути к покупателю"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот для учёта продаж.")
    await update.message.reply_text("Используй /add_sale, чтобы добавить продажу.")

async def add_sale(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Введите наименование товара:")
    return PRODUCT

async def get_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['product'] = update.message.text
    keyboard = [[KeyboardButton(wh)] for wh in WAREHOUSES]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text("Выберите склад:", reply_markup=reply_markup)
    return WAREHOUSE

async def get_warehouse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['warehouse'] = update.message.text
    await update.message.reply_text("Введите город покупателя:")
    return CITY

async def get_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['city'] = update.message.text
    await update.message.reply_text("Введите ФИО покупателя:")
    return FIO

async def get_fio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['fio'] = update.message.text
    await update.message.reply_text("Введите сумму товара:")
    return AMOUNT

async def get_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['amount'] = update.message.text
    await update.message.reply_text("Введите сумму доставки:")
    return DELIVERY

async def get_delivery(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['delivery'] = update.message.text
    keyboard = [[KeyboardButton(ch)] for ch in CHANNELS]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text("Выберите канал продаж:", reply_markup=reply_markup)
    return CHANNEL

async def get_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['channel'] = update.message.text
    await update.message.reply_text("Введите номер накладной:")
    return INVOICE

async def get_invoice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['invoice'] = update.message.text
    keyboard = [[KeyboardButton(st)] for st in STATUSES]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text("Выберите статус:", reply_markup=reply_markup)
    return STATUS

async def get_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['status'] = update.message.text

    # Формируем шаблон сообщения
    msg = (
        f"{context.user_data['product']}\n"
        f"из фф {context.user_data['warehouse']}\n"
        f"{context.user_data['city']}\n\n"
        f"{context.user_data['fio']} {context.user_data['amount']}р. доставка {context.user_data['delivery']}р\n"
        f"оплатил сразу то и то\n\n"
        f"{context.user_data['channel']} 2\n"
        f"$\n"
        f"{context.user_data['invoice']}"
    )

    await update.message.reply_text(msg)
    return ConversationHandler.END

def main():
    # Создаём приложение
    application = Application.builder().token(TOKEN).build()

    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))

    # Добавляем обработчик команды /add_sale
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("add_sale", add_sale)],
        states={
            PRODUCT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_product)],
            WAREHOUSE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_warehouse)],
            CITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_city)],
            FIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_fio)],
            AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_amount)],
            DELIVERY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_delivery)],
            CHANNEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_channel)],
            INVOICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_invoice)],
            STATUS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_status)],
        },
        fallbacks=[]
    )
    application.add_handler(conv_handler)

    # Запускаем бота
    print("Бот запущен...")
    application.run_polling()

if __name__ == "__main__":
    main()