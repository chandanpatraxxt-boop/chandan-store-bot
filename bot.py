import logging
import base64
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, CallbackQueryHandler, filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = "8950227047:AAGKQ7D9Jx4cmWrYAWNPYA0IEHrAdErH0lA"
RAZORPAY_KEY_ID = "rzp_test_Tju8CLPgkcpwhb"
RAZORPAY_KEY_SECRET = "mGgetXe4fJ3nbAE4p5fBXLvwBc"

user_balances = {}
user_orders = {}
verified_users = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id not in verified_users:
        verify_text = (
            "┏ 🔒 **VERIFICATION REQUIRED** ┓\n"
            "┗━━━━━━━━━━━━━━━━━━━━━━┛\n\n"
            "To start shopping, please verify your phone number.\n\n"
            "🟩 **Why we need this:**\n"
            "• Secure your purchases\n"
            "• Deliver keys to you\n"
            "• Protect your account\n\n"
            "👇 Click the button below to share your phone number:"
        )
        contact_keyboard = [[KeyboardButton("📱 Share Phone Number", request_contact=True)]]
        reply_markup = ReplyKeyboardMarkup(contact_keyboard, resize_keyboard=True, one_time_keyboard=True)
        await update.message.reply_text(verify_text, reply_markup=reply_markup, parse_mode="Markdown")
        return

    welcome_text = (
        "┏ 🌟 **CHANDAN PREMIUM STORE** 🌟 ┓\n"
        "┗━━━━━━━━━━━━━━━━━━━━━━┛\n\n"
        "Welcome to the ultimate digital store! Choose an option below:"
    )
    keyboard = [
        [InlineKeyboardButton("🛒 Buy Products", callback_data="buy_products")],
        [InlineKeyboardButton("💰 Add Money", callback_data="add_money")],
        [InlineKeyboardButton("👤 My Profile", callback_data="my_profile")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    contact = update.message.contact
    if contact and contact.user_id == user.id:
        verified_users.add(user.id)
        await update.message.reply_text("✅ Phone number verified successfully!", reply_markup=None)
        await start(update, context)
    else:
        await update.message.reply_text("❌ Please share your own contact using the button provided.")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == "add_money":
        await query.message.reply_text("Please enter the amount you want to add (e.g., 100):")
        context.user_data['waiting_for_amount'] = True

    elif query.data == "buy_products":
        keyboard = [
            [InlineKeyboardButton("Netflix - Rs. 150", callback_data="buy_netflix")],
            [InlineKeyboardButton("Spotify - Rs. 99", callback_data="buy_spotify")],
            [InlineKeyboardButton("🔙 Back", callback_data="main_menu")]
        ]
        await query.message.edit_text("Select a product to buy:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "my_profile":
        balance = user_balances.get(user_id, 0)
        profile_text = (
            f"👤 **User Profile**\n\n"
            f"🆔 ID: `{user_id}`\n"
            f"💰 Balance: Rs. {balance}\n"
            f"✅ Status: Verified"
        )
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="main_menu")]]
        await query.message.edit_text(profile_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif query.data == "main_menu":
        welcome_text = "Welcome back to the main menu!"
        keyboard = [
            [InlineKeyboardButton("🛒 Buy Products", callback_data="buy_products")],
            [InlineKeyboardButton("💰 Add Money", callback_data="add_money")],
            [InlineKeyboardButton("👤 My Profile", callback_data="my_profile")]
        ]
        await query.message.edit_text(welcome_text, reply_markup=InlineKeyboardMarkup(keyboard))

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if context.user_data.get('waiting_for_amount'):
        try:
            amount = int(update.message.text)
            if amount <= 0:
                raise ValueError()
            context.user_data['waiting_for_amount'] = False
            
            # Razorpay QR Code API Integration
            url = "https://api.razorpay.com/v1/qr_codes"
            auth = base64.b64encode(f"{RAZORPAY_KEY_ID}:{RAZORPAY_KEY_SECRET}".encode()).decode()
            headers = {
                "Authorization": f"Basic {auth}",
                "Content-Type": "application/json"
            }
            payload = {
                "type": "upi_qr",
                "name": f"Add Money {user_id}",
                "usage": "single_use",
                "fixed_amount": True,
                "payment_amount": amount * 100,
                "description": f"Wallet topup for {user_id}"
            }
            
            response = requests.post(url, json=payload, headers=headers)
            data = response.json()
            
            if response.status_code == 200 and 'image_url' in data:
                qr_url = data['image_url']
                await update.message.reply_photo(photo=qr_url, caption=f"scan this QR to pay Rs. {amount}. It is single-use.")
            else:
                await update.message.reply_text("⚠️ Error generating QR code from Razorpay. Please try again later.")
        except ValueError:
            await update.message.reply_text("❌ Please enter a valid number for the amount.")

def main():
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.CONTACT, contact_handler))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    
    application.run_polling()

if __name__ == '__main__':
    main()
