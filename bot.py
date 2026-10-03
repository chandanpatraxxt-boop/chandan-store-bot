import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
TOKEN = "8950227047:AAGcs_cSrkHG52lIqWZN-OgXUUQ_n8nJlnQ"

user_balances = {}
user_orders = {}
waiting_for_utr = set()

# Tomar asol UPI ID diye QR Code link set kora holo
YOUR_UPI_ID = "cn736000@oksbi"
YOUR_STORE_NAME = "ChandanStore"
QR_IMAGE_URL = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=upi://pay?pa={YOUR_UPI_ID}&pn={YOUR_STORE_NAME}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
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

    if data == "shop":
        shop_text = "┏ 🛒 **PRODUCT STORE – SHOP** ❞\n┗ \n\n⚙️ Select your device type:"
        shop_keyboard = [
            [InlineKeyboardButton("🔑 NONROOT", callback_data="cat_nonroot")],
            [InlineKeyboardButton("🎁 IOS", callback_data="cat_ios")],
            [InlineKeyboardButton("🔑 ROOT", callback_data="cat_root")],
            [InlineKeyboardButton("🔑 GUILD GLORY BOT", callback_data="item_guild")],
            [InlineKeyboardButton("🔑 8 BALL POOL NONROOT+ROOT", callback_data="item_8ball")],
            [InlineKeyboardButton("🎁 ROOT+NONROOT+IOS IPHONE", callback_data="item_all")],
            [InlineKeyboardButton("🔑 CARROM POOL", callback_data="item_carrom")],
            [InlineKeyboardButton("💻 PC", callback_data="item_pc")],
            [InlineKeyboardButton("🔑 CS RANK PAID PUSH", callback_data="item_cs")],
            [InlineKeyboardButton("🔑 CALL BOMBER", callback_data="item_bomber")],
            [InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")]
        ]
        await query.answer()
        await query.edit_message_text(text=shop_text, reply_markup=InlineKeyboardMarkup(shop_keyboard), parse_mode="Markdown")

    elif data == "cat_root":
        root_text = "┏ 🛒 **PRODUCT STORE – ROOT** ❞\n┗ \n\n👑 Choose a product:"
        root_keyboard = [
            [InlineKeyboardButton("🔑 DRIPCLIENT FF ROOT ANDROID", callback_data="prod_dripclient")],
            [InlineKeyboardButton("🔑 HEX BLADE FF ROOT ANDROID", callback_data="prod_hexblade")],
            [InlineKeyboardButton("🔑 RAPID CORE FF ROOT ANDROID", callback_data="prod_rapidcore")],
            [InlineKeyboardButton("🔑 Sx2 Team CHEATS FF ROOT", callback_data="prod_sx2")],
            [InlineKeyboardButton("⬅️ Back", callback_data="shop")]
        ]
        await query.answer()
        await query.edit_message_text(text=root_text, reply_markup=InlineKeyboardMarkup(root_keyboard), parse_mode="Markdown")

    elif data == "cat_nonroot":
        nr_text = "┏ 🛒 **PRODUCT STORE – NONROOT** ❞\n┗ \n\n👑 Choose a product:"
        nr_keyboard = [
            [InlineKeyboardButton("🔑 NONROOT PANEL VIP", callback_data="prod_nr_vip")],
            [InlineKeyboardButton("⬅️ Back", callback_data="shop")]
        ]
        await query.answer()
        await query.edit_message_text(text=nr_text, reply_markup=InlineKeyboardMarkup(nr_keyboard), parse_mode="Markdown")

    elif data == "cat_ios":
        ios_text = "┏ 🛒 **PRODUCT STORE – IOS** ❞\n┗ \n\n👑 Choose a product:"
        ios_keyboard = [
            [InlineKeyboardButton("🎁 IOS IPA MOD VIP", callback_data="prod_ios_vip")],
            [InlineKeyboardButton("⬅️ Back", callback_data="shop")]
        ]
        await query.answer()
        await query.edit_message_text(text=ios_text, reply_markup=InlineKeyboardMarkup(ios_keyboard), parse_mode="Markdown")

    elif data.startswith("prod_"):
        prod_name = data.replace("prod_", "").replace("_", " ").upper()
        user_orders[user_id] = {"product": prod_name}
        plan_text = f"┏ 🛒 **{prod_name}** ❞\n┗ \n\n👑 Choose a plan:\n\n• 1 Day - 💰 ₹40.00\n• 7 Days - 💰 ₹160.00\n• 14 Days - 💰 ₹240.00\n• 30 Days - 💰 ₹360.00"
        plan_keyboard = [
            [InlineKeyboardButton("🛒 1 Day - ₹40.00", callback_data="plan_1")],
            [InlineKeyboardButton("🛒 7 Days - ₹160.00", callback_data="plan_7")],
            [InlineKeyboardButton("🛒 14 Days - ₹240.00", callback_data="plan_14")],
            [InlineKeyboardButton("🛒 30 Days - ₹360.00", callback_data="plan_30")],
            [InlineKeyboardButton("⬅️ Back", callback_data="cat_root")]
        ]
        await query.answer()
        await query.edit_message_text(text=plan_text, reply_markup=InlineKeyboardMarkup(plan_keyboard), parse_mode="Markdown")

    elif data.startswith("plan_"):
        days_map = {"1": ("1 Day", 40.0), "7": ("7 Days", 160.0), "14": ("14 Days", 240.0), "30": ("30 Days", 360.0)}
        day_key = data.replace("plan_", "")
        plan_name, price = days_map.get(day_key, ("1 Day", 40.0))
        
        if user_id not in user_orders:
            user_orders[user_id] = {"product": "RAPID CORE FF ROOT ANDROID"}
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
            [InlineKeyboardButton("✅ Confirm & Pay", callback_data="confirm_pay")],
            [InlineKeyboardButton("⬅️ Back to Plans", callback_data="prod_rapidcore")]
        ]
        await query.answer()
        await query.edit_message_text(text=summary_text, reply_markup=InlineKeyboardMarkup(summary_kb), parse_mode="Markdown")

    elif data == "confirm_pay":
        order = user_orders.get(user_id, {"price": 40.0})
        price = order.get("price", 40.0)
        
        qr_caption = (
            "┏ 💳 **UPI PAYMENT QR** ❞\n┗ \n\n"
            f"Scan & pay exactly **₹{price:.2f}** via UPI.\n\n"
            "🟩 Pay karne ke baad 'VERIFY PAYMENT' button dabayein.\n"
            "🟩 This QR expires in 5 minutes."
        )
        pay_kb = [
            [InlineKeyboardButton("✅ VERIFY PAYMENT", callback_data="verify_payment")],
            [InlineKeyboardButton("❌ Cancel Payment", callback_data="shop")]
        ]
        await query.answer()
        try:
            await query.message.delete()
        except:
            pass
        await context.bot.send_photo(chat_id=user_id, photo=QR_IMAGE_URL, caption=qr_caption, reply_markup=InlineKeyboardMarkup(pay_kb), parse_mode="Markdown")

    elif data == "verify_payment":
        waiting_for_utr.add(user_id)
        ver_text = (
            "┏ 🟢 **Verification Active** ❞\n┗ \n\n"
            "Kripya apne payment ka **12-digit UTR Number / UPI Ref No.** yahan send karein.\n\n"
            "Send /cancel to stop."
        )
        await query.answer()
        await query.message.reply_text(text=ver_text, parse_mode="Markdown")

    elif data == "update":
        await query.answer("Checking for updates... Bot is up to date!", show_alert=True)
    elif data == "add_balance":
        bal_text = "💳 **Add Balance:**\n\nContact admin to add balance to your account.\nAdmin UPI: `cn736000@oksbi`"
        back_kb = [[InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")]]
        await query.answer()
        await query.edit_message_text(text=bal_text, reply_markup=InlineKeyboardMarkup(back_kb), parse_mode="Markdown")
    elif data == "profile":
        balance = user_balances.get(user_id, 0.0)
        profile_text = f"👤 **My Profile:**\n\n🆔 User ID: `{user_id}`\n💰 Balance: ₹{balance:.2f}\n📜 Key History: No purchased keys yet."
        back_kb = [[InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")]]
        await query.answer()
        await query.edit_message_text(text=profile_text, reply_markup=InlineKeyboardMarkup(back_kb), parse_mode="Markdown")
    elif data == "referral":
        bot_username = context.bot.username
        ref_link = f"https://t.me/{bot_username}?start={user_id}"
        ref_text = f"🔗 **Referral Program:**\n\nInvite your friends and earn bonus!\n\nYour Invite Link:\n`{ref_link}`"
        back_kb = [[InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")]]
        await query.answer()
        await query.edit_message_text(text=ref_text, reply_markup=InlineKeyboardMarkup(back_kb), parse_mode="Markdown")
    elif data == "how_to_use":
        tutorial_text = "❓ **How To Use:**\n\n1. Select Shop / Store Product.\n2. Choose your device & game type.\n3. Complete payment & get your key instantly."
        back_kb = [[InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")]]
        await query.answer()
        await query.edit_message_text(text=tutorial_text, reply_markup=InlineKeyboardMarkup(back_kb), parse_mode="Markdown")
    elif data == "reseller":
        reseller_text = "👑 **Upgrade To Reseller:**\n\nBecome a reseller to get discount keys at professional prices."
        back_kb = [[InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")]]
        await query.answer()
        await query.edit_message_text(text=reseller_text, reply_markup=InlineKeyboardMarkup(back_kb), parse_mode="Markdown")
    elif data == "support":
        support_text = "🛠 **Support:**\n\nFor any help, contact admin UPI: `cn736000@oksbi`"
        back_kb = [[InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")]]
        await query.answer()
        await query.edit_message_text(text=support_text, reply_markup=InlineKeyboardMarkup(back_kb), parse_mode="Markdown")
    elif data == "lucky":
        lucky_text = "🎁 **Lucky / Daily Gift:**\n\nCome back every 24 hours to spin and win random balance!"
        back_kb = [[InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")]]
        await query.answer()
        await query.edit_message_text(text=lucky_text, reply_markup=InlineKeyboardMarkup(back_kb), parse_mode="Markdown")
    elif data == "language":
        lang_text = "🍎 **Language Settings:**\n\nCurrent Language: English (Default)"
        back_kb = [[InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")]]
        await query.answer()
        await query.edit_message_text(text=lang_text, reply_markup=InlineKeyboardMarkup(back_kb), parse_mode="Markdown")
    elif data == "back_to_main":
        await start(update, context)
    else:
        await query.answer("This option is under setup.", show_alert=True)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if text == "/cancel":
        if user_id in waiting_for_utr:
            waiting_for_utr.remove(user_id)
        await update.message.reply_text("Process cancelled.")
        return

    if user_id in waiting_for_utr:
        waiting_for_utr.remove(user_id)
        success_text = (
            "✅ **Payment Submitted Successfully!**\n\n"
            f"UTR / Ref No: `{text}`\n"
            "Your payment is under verification. Key will be delivered shortly."
        )
        await update.message.reply_text(success_text, parse_mode="Markdown")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("cancel", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
