import logging
import base64
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
TOKEN = "8950227047:AAGKQ7D9Jx4cmWrYAWNPYA0IEHrAdErHOlA"

RAZORPAY_KEY_ID = "rzp_test_TjU8CLPgkcpwhb"
RAZORPAY_KEY_SECRET = "mGxoE4fJ3nbAE4p5fBXLvwBq"

user_balances = {}
user_orders = {}
verified_users = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    # Prothombar user ashle ba verified na thakle phone number share korar button dibo
    if user_id not in verified_users:
        verify_text = (
            "┏ 🔒 **VERIFICATION REQUIRED** ❞\n"
            "┗ \n\n"
            "To start shopping, please verify your phone number.\n\n"
            "🟩 **Why we need this:**\n"
            "• Secure your purchases\n"
            "• Deliver keys to you\n"
            "• Protect your account\n\n"
            "👇 Click the button below to share your phone number:"
        )
        contact_keyboard = [[KeyboardButton("📱 Share Phone Number", request_contact=True)]]
        reply_markup = ReplyKeyboardMarkup(contact_keyboard, resize_keyboard=True, one_time_keyboard=True)
        
        if update.callback_query:
            await update.callback_query.message.reply_text(text=verify_text, reply_markup=reply_markup, parse_mode="Markdown")
        else:
            await update.message.reply_text(text=verify_text, reply_markup=reply_markup, parse_mode="Markdown")
        return

    # User verified hole tar balance set hobe (Prothombar 0.00 thakbe)
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

async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    contact = update.message.contact
    
    if contact:
        verified_users.add(user_id)
        if user_id not in user_balances:
            user_balances[user_id] = 0.0
        await update.message.reply_text("✅ Phone number verified successfully!", reply_markup=ReplyKeyboardRemove())
        await start(update, context)

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
        if user_id not in user_orders:
            user_orders[user_id] = {}
        user_orders[user_id]["product"] = prod_name
        
        plan_text = f"┏ 🛒 **{prod_name}** ❞\n┗ \n\n👑 Choose a plan:\n\n• 1 Day - 💰 ₹40.00\n• 7 Days - 💰 ₹160.00\n• 14 Days - 💰 ₹240.00\n• 30 Days - 💰 ₹360.00"
        plan_keyboard = [
            [InlineKeyboardButton("🛒 1 Day - ₹40.00", callback_data="plan_1")],
            [InlineKeyboardButton("🛒 7 Days - ₹160.00", callback_data="plan_7")],
            [InlineKeyboardButton("🛒 14 Days - ₹240.00", callback_data="plan_14")],
            [InlineKeyboardButton("🛒 30 Days - ₹360.00", callback_data="plan_30")],
            [InlineKeyboardButton("⬅️️ Back", callback_data="cat_root")]
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

        prod = user_orders[user_id].get("product", "PRODUCT")
        summary_text = (
            "┏ 🛒 **ORDER SUMMARY** ❞\n┗ \n\n"
            f"🔑 **Product:** {prod}\n"
            f"⚙️ **Plan:** {plan_name}\n"
            f"💰 **Price:** ₹{price:.2f}\n\n"
            f"🟩 **Final Total: ₹{price:.2f}** ❞"
        )
        summary_kb = [
            [InlineKeyboardButton("✅ Confirm & Pay", callback_data="confirm_pay")],
            [InlineKeyboardButton("⬅️ Back to Plans", callback_data="shop")]
        ]
        await query.answer()
        await query.edit_message_text(text=summary_text, reply_markup=InlineKeyboardMarkup(summary_kb), parse_mode="Markdown")

    elif data == "confirm_pay":
        order = user_orders.get(user_id, {"price": 40.0, "product": "Store Item"})
        amount_in_paise = int(order.get("price", 40.0) * 100)
        
        url = "https://api.razorpay.com/v1/qr_codes"
        payload = {
            "type": "upi_qr",
            "name": f"Order-{user_id}",
            "usage": "single_use",
            "fixed_amount": True,
            "payment_amount": amount_in_paise,
            "description": f"Payment for {order.get('product')}"
        }
        
        auth = base64.b64encode(f"{RAZORPAY_KEY_ID}:{RAZORPAY_KEY_SECRET}".encode()).decode()
        headers = {
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/json"
        }
        
        await query.answer("Generating Dynamic UPI QR Code...")
        try:
            response = requests.post(url, json=payload, headers=headers)
            res_data = response.json()
            
            if response.status_code == 200 and "image_url" in res_data:
                qr_image_url = res_data["image_url"]
                qr_id = res_data["id"]
                user_orders[user_id]["qr_id"] = qr_id
                
                qr_caption = (
                    "┏ 💳 **RAZORPAY UPI QR CODE** ❞\n┗ \n\n"
                    f"Scan & pay exactly **₹{order.get('price'):.2f}** via UPI.\n\n"
                    "🟩 Payment complete korar por niche **'CHECK PAYMENT STATUS'** dabayein.\n"
                    "🟩 This QR expires in 5 minutes."
                )
                pay_kb = [
                    [InlineKeyboardButton("🔄 CHECK PAYMENT STATUS", callback_data="check_payment")],
                    [InlineKeyboardButton("❌ Cancel Payment", callback_data="shop")]
                ]
                try:
                    await query.message.delete()
                except:
                    pass
                await context.bot.send_photo(chat_id=user_id, photo=qr_image_url, caption=qr_caption, reply_markup=InlineKeyboardMarkup(pay_kb), parse_mode="Markdown")
            else:
                await query.edit_message_text(text="⚠️ Error generating QR code from Razorpay. Please try again later.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="shop")]]))
        except Exception as e:
            logging.error(f"QR Gen Error: {e}")
            await query.edit_message_text(text="⚠️ Gateway connection error. Try again later.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="shop")]]))

    elif data == "check_payment":
        order = user_orders.get(user_id, {})
        qr_id = order.get("qr_id")
        
        if not qr_id:
            await query.answer("No active payment session found. Please start over.", show_alert=True)
            return

        auth = base64.b64encode(f"{RAZORPAY_KEY_ID}:{RAZORPAY_KEY_SECRET}".encode()).decode()
        headers = {"Authorization": f"Basic {auth}"}
        
        await query.answer("Verifying payment with Razorpay...")
        try:
            res = requests.get(f"https://api.razorpay.com/v1/qr_codes/{qr_id}/payments", headers=headers)
            payments_data = res.json()
            
            items = payments_data.get("items", [])
            if items and len(items) > 0:
                prod = order.get("product", "Digital Item")
                plan = order.get("plan", "1 Day")
                
                success_text = (
                    "┏ ✅ **PAYMENT SUCCESSFUL!** ❞\n┗ \n\n"
                    f"🔑 **Product:** {prod}\n"
                    f"⚙️ **Plan:** {plan}\n\n"
                    "🎉 **Your License Key:** `CHANDAN-TEST-KEY-XYZ123`\n\n"
                    "Thank you for your purchase!"
                )
                back_kb = [[InlineKeyboardButton("⬅️ Main Menu", callback_data="back_to_main")]]
                try:
                    await query.message.delete()
                except:
                    pass
                await context.bot.send_message(chat_id=user_id, text=success_text, reply_markup=InlineKeyboardMarkup(back_kb), parse_mode="Markdown")
            else:
                await query.answer("⚠️ Payment not received yet! Please complete the payment by scanning the QR code first.", show_alert=True)
        except Exception as e:
            logging.error(f"Payment check error: {e}")
            await query.answer("⚠️ Error verifying payment. Try again in a few seconds.", show_alert=True)

    elif data == "update":
        await query.answer("Checking for updates... Bot is up to date!", show_alert=True)
    elif data == "add_balance":
        bal_text = "💳 **Add Balance:**\n\nContact admin to add balance to your account."
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
        tutorial_text = "❓ **How To Use:**\n\n1. Select Shop / Store Product.\n2. Choose your device & game type.\n3. Scan QR & check payment to get your key instantly."
        back_kb = [[InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")]]
        await query.answer()
        await query.edit_message_text(text=tutorial_text, reply_markup=InlineKeyboardMarkup(back_kb), parse_mode="Markdown")
    elif data == "reseller":
        reseller_text = "👑 **Upgrade To Reseller:**\n\nBecome a reseller to get discount keys at professional prices."
        back_kb = [[InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")]]
        await query.answer()
        await query.edit_message_text(text=reseller_text, reply_markup=InlineKeyboardMarkup(back_kb), parse_mode="Markdown")
    elif data == "support":
        support_text = "🛠 **Support:**\n\nFor any help, contact admin."
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

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("cancel", start))
    app.add_handler(MessageHandler(filters.CONTACT, contact_handler))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
