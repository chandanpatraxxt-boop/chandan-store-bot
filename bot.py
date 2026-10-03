import logging
import base64
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Tomar notun Telegram Bot Token
TOKEN = "8950227047:AAG1GFJNsSg8_vhodMpHXUkdc9APCOmnyOg"

# Razorpay API Keys
RAZORPAY_KEY_ID = "rzp_test_TjU6CLPgkcpwhb"
RAZORPAY_KEY_SECRET = "mGxoE4fJ3nbAE4p5fBXLvwBq"

user_balances = {}
user_orders = {}
user_phones = {}

SECRET_GROUP_LINK = "https://t.me/+YourSecretGroupInviteLink"

DUMMY_KEYS = {
    "DRIPCLIENT FF ROOT ANDROID": "DRIPCLIENT-KEY-123",
    "HEX BLADE FF ROOT ANDROID": "HEXBLADE-KEY-456",
    "RAPID CORE FF ROOT ANDROID": "RAPID-CORE-XYZ123-ABC789",
    "SX2 TEAM CHEATS FF ROOT": "SX2TEAM-KEY-789",
    "NONROOT PANEL VIP": "NONROOT-VIP-999888-XYZ",
    "IOS IPA MOD VIP": "IOS-MOD-VIP-777666-ABC"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id not in user_phones:
        phone_keyboard = [[KeyboardButton("📱 Share Phone Number & Verify", request_contact=True)]]
        reply_markup = ReplyKeyboardMarkup(phone_keyboard, resize_keyboard=True, one_time_keyboard=True)
        await update.message.reply_text(
            "⚠️ **Phone Verification Required!**\n\nBot ko use karne ke liye pehle apna phone number verify karein:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        return

    if user_id not in user_balances:
        user_balances[user_id] = 0.0
    balance = user_balances[user_id]
    
    welcome_text = (
        "┏ 🤖 **CHANDAN x STORE** ⚡\n"
        "┣ 🚨 How to use : View Tutorial And Learn How To Use This Bot\n"
        "┣ 👑 Upgrade To Reseller : Become a reseller and get discount keys at low prices\n"
        "┣ ✈️ Support : Contact Support For Any Help Or Problems\n"
        "┣ 🎁 Lucky / Daily Gift : Free Daily Spin & Win Random Balance Every 24 Hours\n"
        "┗ 🍎 Language : Change Bot Language Interface\n\n"
        f"🟩 Your Balance: 💰 ₹{balance:.2f} ❞\n\n"
        "👇 Select an option from the menu below:"
    )
    keyboard = [
        [InlineKeyboardButton("🛒 Shop / Store Product", callback_data="shop")],
        [InlineKeyboardButton("🔄 Check Update", callback_data="update"), InlineKeyboardButton("💳 Add Balance", callback_data="add_balance")],
        [InlineKeyboardButton("📜 My Profile + Key History", callback_data="profile")],
        [InlineKeyboardButton("🔗 Referral", callback_data="referral"), InlineKeyboardButton("❓ How To Use", callback_data="how_to_use")],
        [InlineKeyboardButton("👑 Upgrade To Reseller", callback_data="reseller")],
        [InlineKeyboardButton("🛠 Support", callback_data="support"), InlineKeyboardButton("🎁 Lucky", callback_data="lucky")],
        [InlineKeyboardButton("🍎 Language", callback_data="language")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        query = update.callback_query
        await query.answer()
        try:
            await query.message.delete()
        except:
            pass
        await context.bot.send_message(chat_id=user_id, text=welcome_text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await update.message.reply_text(text=welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    user_id = update.effective_user.id

    if user_id not in user_phones:
        await query.answer("Please verify your phone number first using /start", show_alert=True)
        return

    if data == "shop":
        shop_text = "┏ 🛒 **PRODUCT STORE – SHOP** ❞\n┗ \n\n⚙️️ Select your device type:"
        shop_keyboard = [
            [InlineKeyboardButton("🔑 ROOT", callback_data="cat_root")],
            [InlineKeyboardButton("🔑 NONROOT", callback_data="cat_nonroot")],
            [InlineKeyboardButton("🎁 IOS", callback_data="cat_ios")],
            [InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")]
        ]
        await query.answer()
        await query.edit_message_text(text=shop_text, reply_markup=InlineKeyboardMarkup(shop_keyboard), parse_mode="Markdown")

    elif data == "cat_root":
        root_text = "┏ 🛒 **PRODUCT STORE – ROOT** ❞\n┗ \n\n👑 Choose a product:"
        root_keyboard = [
            [InlineKeyboardButton("🔑 DRIPCLIENT FF ROOT ANDROID", callback_data="prod_DRIPCLIENT_FF_ROOT_ANDROID")],
            [InlineKeyboardButton("🔑 RAPID CORE FF ROOT ANDROID", callback_data="prod_RAPID_CORE_FF_ROOT_ANDROID")],
            [InlineKeyboardButton("⬅️ Back", callback_data="shop")]
        ]
        await query.answer()
        await query.edit_message_text(text=root_text, reply_markup=InlineKeyboardMarkup(root_keyboard), parse_mode="Markdown")

    elif data == "cat_nonroot":
        nr_text = "┏ 🛒 **PRODUCT STORE – NONROOT** ❞\n┗ \n\n👑 Choose a product:"
        nr_keyboard = [
            [InlineKeyboardButton("🔑 NONROOT PANEL VIP", callback_data="prod_NONROOT_PANEL_VIP")],
            [InlineKeyboardButton("⬅️ Back", callback_data="shop")]
        ]
        await query.answer()
        await query.edit_message_text(text=nr_text, reply_markup=InlineKeyboardMarkup(nr_keyboard), parse_mode="Markdown")

    elif data == "cat_ios":
        ios_text = "┏ 🛒 **PRODUCT STORE – IOS** ❞\n┗ \n\n👑 Choose a product:"
        ios_keyboard = [
            [InlineKeyboardButton("🎁 IOS IPA MOD VIP", callback_data="prod_IOS_IPA_MOD_VIP")],
            [InlineKeyboardButton("⬅️ Back", callback_data="shop")]
        ]
        await query.answer()
        await query.edit_message_text(text=ios_text, reply_markup=InlineKeyboardMarkup(ios_keyboard), parse_mode="Markdown")

    elif data.startswith("prod_"):
        prod_name = data.replace("prod_", "").replace("_", " ").upper()
        user_orders[user_id] = {"product": prod_name}
        plan_text = f"┏ 🛒 **{prod_name}** ❞\n┗ \n\n👑 Choose a plan:\n\n• 1 Day - 💰 ₹40.00"
        plan_keyboard = [
            [InlineKeyboardButton("🛒 1 Day - ₹40.00", callback_data="plan_1")],
            [InlineKeyboardButton("⬅️ Back", callback_data="cat_root")]
        ]
        await query.answer()
        await query.edit_message_text(text=plan_text, reply_markup=InlineKeyboardMarkup(plan_keyboard), parse_mode="Markdown")

    elif data.startswith("plan_"):
        plan_name, price = "1 Day", 40.0
        user_orders[user_id]["plan"] = plan_name
        user_orders[user_id]["price"] = price

        prod = user_orders[user_id]["product"]
        summary_text = (
            "┏ 🛒 **ORDER SUMMARY** ❞\n┗ \n\n"
            f"🔑 **Product:** {prod}\n"
            f"⚙️ **Plan:** {plan_name}\n"
            f"💰 **Price:** ₹{price:.2f}\n\n"
            f"🟩 **Final Total: ₹{price:.2f}** ❞"
        )
        summary_kb = [
            [InlineKeyboardButton("✅ Confirm & Pay Online", callback_data="create_payment_link")],
            [InlineKeyboardButton("⬅️ Back to Plans", callback_data="shop")]
        ]
        await query.answer()
        await query.edit_message_text(text=summary_text, reply_markup=InlineKeyboardMarkup(summary_kb), parse_mode="Markdown")

    elif data == "create_payment_link":
        order = user_orders.get(user_id, {"price": 40.0, "product": "RAPID CORE FF ROOT ANDROID"})
        price = order.get("price", 40.0)
        prod_name = order.get("product", "RAPID CORE FF ROOT ANDROID")

        url = "https://api.razorpay.com/v1/payment_links"
        auth = base64.b64encode(f"{RAZORPAY_KEY_ID}:{RAZORPAY_KEY_SECRET}".encode()).decode()
        headers = {
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/json"
        }
        payload = {
            "amount": int(price * 100),
            "currency": "INR",
            "description": f"Purchase {prod_name}",
            "customer": {
                "name": f"User {user_id}",
                "contact": user_phones.get(user_id, "9999999999")
            },
            "notify": {"sms": False, "email": False},
            "reminder_enable": False,
            "callback_url": "https://t.me/"
        }

        response = requests.post(url, json=payload, headers=headers)
        res_data = response.json()

        if response.status_code == 200 and 'short_url' in res_data:
            payment_link = res_data['short_url']
            pl_id = res_data['id']
            user_orders[user_id]["pl_id"] = pl_id

            msg_text = (
                "┏ 💳 **RAZORPAY PAYMENT LINK** ❞\n┗ \n\n"
                f"Amount: **₹{price:.2f}**\n\n"
                "Nicher button-e click kore 5 minute er modhe payment complete korun:\n\n"
                "🟩 Payment korar por **'✅ Verify Payment'** button-e click korun."
            )
            pay_kb = [
                [InlineKeyboardButton("🌐 Pay Now via Razorpay", url=payment_link)],
                [InlineKeyboardButton("✅ Verify Payment", callback_data="verify_auto_payment")],
                [InlineKeyboardButton("❌ Cancel", callback_data="shop")]
            ]
            await query.answer()
            await query.edit_message_text(text=msg_text, reply_markup=InlineKeyboardMarkup(pay_kb), parse_mode="Markdown")
        else:
            await query.answer("⚠️ Error generating payment link. Check API keys.", show_alert=True)

    elif data == "verify_auto_payment":
        order_info = user_orders.get(user_id, {})
        pl_id = order_info.get("pl_id")
        prod_name = order_info.get("product", "RAPID CORE FF ROOT ANDROID")

        if not pl_id:
            await query.answer("⚠️ No active payment found. Please create an order first.", show_alert=True)
            return

        url = f"https://api.razorpay.com/v1/payment_links/{pl_id}"
        auth = base64.b64encode(f"{RAZORPAY_KEY_ID}:{RAZORPAY_KEY_SECRET}".encode()).decode()
        headers = {"Authorization": f"Basic {auth}"}

        response = requests.get(url, headers=headers)
        res_data = response.json()

        if response.status_code == 200:
            status = res_data.get("status")
            if status == "paid":
                key = DUMMY_KEYS.get(prod_name, "DEFAULT-KEY-12345")
                success_text = (
                    "✅ **Payment Verified Successfully!** 🎉\n\n"
                    f"📦 **Product:** {prod_name}\n"
                    f"🔑 **Your Product Key:** `{key}`\n\n"
                    f"✈️ **Join Secret Group:** [Click Here to Join]({SECRET_GROUP_LINK})"
                )
                await query.answer("Payment Verified!", show_alert=True)
                await query.edit_message_text(text=success_text, parse_mode="Markdown")
                return

        await query.answer("⚠️ Payment not received yet! Please complete payment first.", show_alert=True)

    elif data == "back_to_main":
        await start(update, context)
    else:
        await query.answer("Option under setup.", show_alert=True)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if update.message and update.message.contact:
        phone_number = update.message.contact.phone_number
        user_phones[user_id] = phone_number
        await update.message.reply_text(
            f"✅ **Phone Number Verified Successfully!**\nNumber: `{phone_number}`",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode="Markdown"
        )
        await start(update, context)

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.CONTACT, handle_message))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
