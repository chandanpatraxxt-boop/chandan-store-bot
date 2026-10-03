import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
TOKEN = "8950227047:AAGcs_cSrkHG52lIqWZN-OgXUUQ_n8nJlnQ"
user_balances = {}

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
        f"🟩 \n🟩 Your Balance: 💰 ₹{balance:.2f} ❞\n🟩 \n\n"
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
        await query.edit_message_text(text=welcome_text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await update.message.reply_text(text=welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    user_id = update.effective_user.id

    if data == "shop":
        shop_text = "┏ 🛒 **PRODUCT STORE – SHOP** ❞\n┗ \n\n⚙️ Select your device type:"
        shop_keyboard = [
            [InlineKeyboardButton("🔑 NONROOT", callback_data="item_nonroot")],
            [InlineKeyboardButton("🎁 IOS", callback_data="item_ios")],
            [InlineKeyboardButton("🔑 ROOT", callback_data="item_root")],
            [InlineKeyboardButton("🔑 GUILD GLORY BOT", callback_data="item_guild")],
            [InlineKeyboardButton("🔑 8 BALL POOL NONROOT+ROOT", callback_data="item_8ball")],
            [InlineKeyboardButton("🎁 ROOT+NONROOT+IOS IPHONE", callback_data="item_all")],
            [InlineKeyboardButton("🔑 CARROM POOL", callback_data="item_carrom")],
            [InlineKeyboardButton("💻 PC", callback_data="item_pc")],
            [InlineKeyboardButton("🔑 CS RANK PAID PUSH", callback_data="item_cs")],
            [InlineKeyboardButton("🔑 CALL BOMBER", callback_data="item_bomber")],
            [InlineKeyboardButton("⬅️️ Back", callback_data="back_to_main")]
        ]
        await query.answer()
        await query.edit_message_text(text=shop_text, reply_markup=InlineKeyboardMarkup(shop_keyboard), parse_mode="Markdown")
    
    elif data == "update":
        await query.answer("Checking for updates... Bot is up to date!", show_alert=True)
        
    elif data == "add_balance":
        bal_text = "💳 **Add Balance:**\n\nContact admin to add balance to your account.\nAdmin Username: @AdminUsername"
        back_kb = [[InlineKeyboardButton("⬅ Back", callback_data="shop")]]
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
        tutorial_text = "❓ **How To Use:**\n\n1. Select Shop / Store Product.\n2. Choose your device/game type.\n3. Complete payment & get your key instantly."
        back_kb = [[InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")]]
        await query.answer()
        await query.edit_message_text(text=tutorial_text, reply_markup=InlineKeyboardMarkup(back_kb), parse_mode="Markdown")
        
    elif data == "reseller":
        reseller_text = "👑 **Upgrade To Reseller:**\n\nBecome a reseller to get discount keys at professional prices. Contact support to upgrade."
        back_kb = [[InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")]]
        await query.answer()
        await query.edit_message_text(text=reseller_text, reply_markup=InlineKeyboardMarkup(back_kb), parse_mode="Markdown")
        
    elif data == "support":
        support_text = "🛠 **Support:**\n\nFor any help or problems, contact our support team: @AdminUsername"
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

    # --- PRODUCTS SECTION ---
    elif data == "item_nonroot":
        nonroot_text = (
            "🔑 **NONROOT PRODUCTS:**\n\n"
            "1️⃣ Nonroot Hack - 1 Day : ₹50\n"
            "2️⃣ Nonroot Hack - 7 Days : ₹200\n"
            "3️⃣ Nonroot Hack - 30 Days : ₹500\n\n"
            "👇 Select an option or add balance to buy:"
        )
        back_kb = [[InlineKeyboardButton("⬅️ Back to Shop", callback_data="shop")]]
        await query.answer()
        await query.edit_message_text(text=nonroot_text, reply_markup=InlineKeyboardMarkup(back_kb), parse_mode="Markdown")

    elif data == "item_root":
        root_text = (
            "🔑 **ROOT PRODUCTS:**\n\n"
            "1️⃣ Root Hack - 1 Day : ₹80\n"
            "2️⃣ Root Hack - 7 Days : ₹300\n"
            "3️⃣ Root Hack - 30 Days : ₹800\n\n"
            "👇 Select an option or add balance to buy:"
        )
        back_kb = [[InlineKeyboardButton("⬅️ Back to Shop", callback_data="shop")]]
        await query.answer()
        await query.edit_message_text(text=root_text, reply_markup=InlineKeyboardMarkup(back_kb), parse_mode="Markdown")

    elif data == "item_ios":
        ios_text = (
            "🎁 **IOS PRODUCTS:**\n\n"
            "1️⃣ iOS IPA Mod - 1 Day : ₹100\n"
            "2️⃣ iOS IPA Mod - 7 Days : ₹350\n"
            "3️⃣ iOS IPA Mod - 30 Days : ₹900\n\n"
            "👇 Select an option or add balance to buy:"
        )
        back_kb = [[InlineKeyboardButton("⬅️ Back to Shop", callback_data="shop")]]
        await query.answer()
        await query.edit_message_text(text=ios_text, reply_markup=InlineKeyboardMarkup(back_kb), parse_mode="Markdown")

    elif data.startswith("item_"):
        other_text = (
            "🛍 **PRODUCT DETAILS:**\n\n"
            "This product category is currently available. To purchase, please make sure you have enough balance in your account.\n\n"
            "Contact admin to add balance."
        )
        back_kb = [
            [InlineKeyboardButton("💳 Add Balance", callback_data="add_balance")],
            [InlineKeyboardButton("⬅️ Back to Shop", callback_data="shop")]
        ]
        await query.answer()
        await query.edit_message_text(text=other_text, reply_markup=InlineKeyboardMarkup(back_kb), parse_mode="Markdown")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
