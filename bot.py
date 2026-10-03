import logging
import base64
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = "8950227047:AAHLi_yFLXCUCCafr3rXBeSNLkYb1rgSKSY"
RAZORPAY_KEY_ID = "rzp_test_Tju8CLPgkcpwhb"
RAZORPAY_KEY_SECRET = "mGgetXe4fJ3nbAE4p5fBXLvwBc"

user_balances = {}
user_orders = {}
waiting_for_amount = set()

SECRET_GROUP_LINK = "https://t.me/+YourSecretGroupInviteLink"
PRODUCT_PRICES = {
    "RAPID CORE FF ROOT ANDROID": 40.0,
    "NONROOT PANEL VIP": 99.0,
    "IOS IPA MOD VIP": 150.0
}
DUMMY_KEYS = {
    "RAPID CORE FF ROOT ANDROID": "RAPID-CORE-XYZ123-ABC789",
    "NONROOT PANEL VIP": "NONROOT-VIP-999888-XYZ",
    "IOS IPA MOD VIP": "IOS-MOD-VIP-777666-ABC"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_balances:
        user_balances[user_id] = 0.0
    balance = user_balances[user_id]
    
    welcome_text = (
        "┏ 🤖 **CHANDAN x STORE** ⚡\n"
        "┣ 🛒 Shop Products (Direct Pay or Wallet)\n"
        "┣ 💳 Add Money to Wallet (Custom Amount)\n"
        "┣ 👤 Check Profile & Balance\n"
        "┗ 🍎 Language : English\n\n"
        f"🟩 Your Wallet Balance: 💰 ₹{balance:.2f}\n\n"
        "👇 Select an option from the menu below:"
    )
    keyboard = [
        [InlineKeyboardButton("🛒 Shop / Store Product", callback_data="shop")],
        [InlineKeyboardButton("💳 Add Money (Wallet Topup)", callback_data="add_balance")],
        [InlineKeyboardButton("📜 My Profile", callback_data="profile")],
        [InlineKeyboardButton("🛠 Support", callback_data="support")]
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
        shop_text = "┏ 🛒 **PRODUCT STORE – SHOP** ❞\n┗ \n\n⚙️ Select your product:"
        shop_keyboard = [
            [InlineKeyboardButton("🔑 RAPID CORE FF (₹40)", callback_data="prod_RAPID CORE FF ROOT ANDROID")],
            [InlineKeyboardButton("🔑 NONROOT PANEL VIP (₹99)", callback_data="prod_NONROOT PANEL VIP")],
            [InlineKeyboardButton("🎁 IOS IPA MOD VIP (₹150)", callback_data="prod_IOS IPA MOD VIP")],
            [InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")]
        ]
        await query.answer()
        await query.edit_message_text(text=shop_text, reply_markup=InlineKeyboardMarkup(shop_keyboard), parse_mode="Markdown")

    elif data.startswith("prod_"):
        prod_name = data.replace("prod_", "")
        price = PRODUCT_PRICES.get(prod_name, 40.0)
        user_orders[user_id] = {"product": prod_name, "price": price}

        prod_menu_text = (
            f"┏ 🛒 **{prod_name}**\n"
            f"💰 Price: ₹{price:.2f}\n\n"
            "Apni kivabe payment korte chan select korun:"
        )
        kb = [
            [InlineKeyboardButton("💳 Pay Directly (Razorpay QR)", callback_data="direct_pay")],
            [InlineKeyboardButton("💰 Pay via Wallet Balance", callback_data="wallet_pay")],
            [InlineKeyboardButton("⬅️ Back to Shop", callback_data="shop")]
        ]
        await query.answer()
        await query.edit_message_text(text=prod_menu_text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    elif data == "wallet_pay":
        order_info = user_orders.get(user_id, {})
        prod_name = order_info.get("product", "RAPID CORE FF ROOT ANDROID")
        price = order_info.get("price", 40.0)
        user_balance = user_balances.get(user_id, 0.0)

        if user_balance >= price:
            user_balances[user_id] -= price
            key = DUMMY_KEYS.get(prod_name, "KEY-12345")
            success_msg = (
                "✅ **Purchase Successful (Via Wallet)!** 🎉\n\n"
                f"📦 **Product:** {prod_name}\n"
                f"💰 **Deducted:** ₹{price:.2f}\n"
                f"🟩 **Remaining Wallet Balance:** ₹{user_balances[user_id]:.2f}\n\n"
                f"🔑 **Your Key:** `{key}`\n"
                f"✈️ **Join Group:** [Click Here]({SECRET_GROUP_LINK})"
            )
            await query.answer("Purchase successful!", show_alert=True)
            await query.edit_message_text(text=success_msg, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Main Menu", callback_data="back_to_main")]]))
        else:
            low_text = (
                f"❌ **Insufficient Wallet Balance!**\n\n"
                f"Required: ₹{price:.2f}\n"
                f"Your Wallet Balance: ₹{user_balance:.2f}\n\n"
                "Apni chaile direct payment korte paren ba wallet-e taka add kore nite paren."
            )
            kb = [
                [InlineKeyboardButton("💳 Pay Directly Instead", callback_data="direct_pay")],
                [InlineKeyboardButton("💳 Add Money to Wallet", callback_data="add_balance")],
                [InlineKeyboardButton("⬅️ Back", callback_data="shop")]
            ]
            await query.answer("Low balance!", show_alert=True)
            await query.edit_message_text(text=low_text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    elif data == "direct_pay":
        order_info = user_orders.get(user_id, {})
        prod_name = order_info.get("product", "RAPID CORE FF ROOT ANDROID")
        price = order_info.get("price", 40.0)

        # Razorpay Dynamic QR for Direct Product Purchase
        url = "https://api.razorpay.com/v1/qr_codes"
        auth = base64.b64encode(f"{RAZORPAY_KEY_ID}:{RAZORPAY_KEY_SECRET}".encode()).decode()
        headers = {
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/json"
        }
        payload = {
            "type": "upi_qr",
            "name": f"Direct Buy {user_id}",
            "usage": "single_use",
            "fixed_amount": True,
            "payment_amount": int(price * 100),
            "description": f"Purchase {prod_name} by {user_id}"
        }
        
        response = requests.post(url, json=payload, headers=headers)
        data_res = response.json()
        
        if response.status_code == 200 and 'image_url' in data_res:
            qr_url = data_res['image_url']
            qr_id = data_res['id']
            user_orders[user_id]["qr_id"] = qr_id
            
            qr_caption = (
                f"┏ 💳 **DIRECT PAYMENT QR** ❞\n┗ \n\n"
                f"📦 **Product:** {prod_name}\n"
                f"Scan & pay exactly **₹{price:.2f}** via any UPI app.\n\n"
                "🟩 Payment korar por niche **'✅ VERIFY DIRECT PAYMENT'** button-এ click korun."
            )
            pay_kb = [
                [InlineKeyboardButton("✅ VERIFY DIRECT PAYMENT", callback_data="verify_direct_pay")],
                [InlineKeyboardButton("❌ Cancel", callback_data="shop")]
            ]
            await query.answer()
            try:
                await query.message.delete()
            except:
                pass
            await context.bot.send_photo(chat_id=user_id, photo=qr_url, caption=qr_caption, reply_markup=InlineKeyboardMarkup(pay_kb), parse_mode="Markdown")
        else:
            await query.answer("⚠️️ Error generating Razorpay QR. Try again later.", show_alert=True)

    elif data == "verify_direct_pay":
        order_info = user_orders.get(user_id, {})
        qr_id = order_info.get("qr_id")
        prod_name = order_info.get("product", "RAPID CORE FF ROOT ANDROID")
        
        if not qr_id:
            await query.answer("❌ No active payment found.", show_alert=True)
            return

        url = f"https://api.razorpay.com/v1/qr_codes/{qr_id}/payments"
        auth = base64.b64encode(f"{RAZORPAY_KEY_ID}:{RAZORPAY_KEY_SECRET}".encode()).decode()
        headers = {"Authorization": f"Basic {auth}"}
        
        response = requests.get(url, headers=headers)
        res_data = response.json()
        
        paid = False
        if response.status_code == 200:
            items = res_data.get("items", [])
            if len(items) > 0:
                for pay in items:
                    if pay.get("status") == "captured":
                        paid = True
                        break

        if paid:
            key = DUMMY_KEYS.get(prod_name, "KEY-12345")
            success_msg = (
                "✅ **Payment Verified & Purchase Successful!** 🎉\n\n"
                f"📦 **Product:** {prod_name}\n\n"
                f"🔑 **Your Key:** `{key}`\n"
                f"✈️ **Join Group:** [Click Here]({SECRET_GROUP_LINK})"
            )
            await query.answer("Payment verified!", show_alert=True)
            await query.message.edit_caption(caption=success_msg, parse_mode="Markdown")
        else:
            await query.answer("⚠️ Payment not received yet! Please complete payment by scanning the QR code.", show_alert=True)

    elif data == "add_balance":
        waiting_for_amount.add(user_id)
        msg = (
            "💳 **Add Money to Wallet:**\n\n"
            "Apnar ichchamoto amount type kore send korun (Jemon: `50`, `500`, `1000` ba যত খুশি)।\n\n"
            "Cancel korar jonno /cancel send korun."
        )
        await query.answer()
        await query.edit_message_text(text=msg, parse_mode="Markdown")

    elif data.startswith("verify_topup_"):
        qr_id = data.replace("verify_topup_", "")
        url = f"https://api.razorpay.com/v1/qr_codes/{qr_id}/payments"
        auth = base64.b64encode(f"{RAZORPAY_KEY_ID}:{RAZORPAY_KEY_SECRET}".encode()).decode()
        headers = {"Authorization": f"Basic {auth}"}
        
        response = requests.get(url, headers=headers)
        res_data = response.json()
        
        paid = False
        amount_paid = 0
        if response.status_code == 200:
            items = res_data.get("items", [])
            if len(items) > 0:
                for pay in items:
                    if pay.get("status") == "captured":
                        paid = True
                        amount_paid = pay.get("amount", 0) / 100
                        break

        if paid:
            user_balances[user_id] = user_balances.get(user_id, 0.0) + amount_paid
            success_text = (
                "✅ **Wallet Topup Successful!** 🎉\n\n"
                f"💰 Added Amount: ₹{amount_paid:.2f}\n"
                f"🟩 **New Wallet Balance:** ₹{user_balances[user_id]:.2f}"
            )
            await query.answer("Payment verified and added to wallet!", show_alert=True)
            kb = [[InlineKeyboardButton("🛒 Go to Shop", callback_data="shop"), InlineKeyboardButton("🏠 Main Menu", callback_data="back_to_main")]]
            await query.message.edit_caption(caption=success_text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb))
        else:
            await query.answer("⚠️ Payment not received yet! Please complete payment first.", show_alert=True)

    elif data == "profile":
        balance = user_balances.get(user_id, 0.0)
        profile_text = f"👤 **My Profile:**\n\n🆔 User ID: `{user_id}`\n💰 Wallet Balance: ₹{balance:.2f}"
        back_kb = [[InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")]]
        await query.answer()
        await query.edit_message_text(text=profile_text, reply_markup=InlineKeyboardMarkup(back_kb), parse_mode="Markdown")

    elif data == "support":
        support_text = "🛠 **Support:**\n\nFor any help, contact admin UPI: `cn736000@oksbi`"
        back_kb = [[InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")]]
        await query.answer()
        await query.edit_message_text(text=support_text, reply_markup=InlineKeyboardMarkup(back_kb), parse_mode="Markdown")

    elif data == "back_to_main":
        await start(update, context)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if text == "/cancel":
        if user_id in waiting_for_amount:
            waiting_for_amount.remove(user_id)
        await update.message.reply_text("Process cancelled.")
        return

    if user_id in waiting_for_amount:
        waiting_for_amount.remove(user_id)
        try:
            amount = float(text)
            if amount <= 0:
                raise ValueError()
            
            url = "https://api.razorpay.com/v1/qr_codes"
            auth = base64.b64encode(f"{RAZORPAY_KEY_ID}:{RAZORPAY_KEY_SECRET}".encode()).decode()
            headers = {
                "Authorization": f"Basic {auth}",
                "Content-Type": "application/json"
            }
            payload = {
                "type": "upi_qr",
                "name": f"Wallet Topup {user_id}",
                "usage": "single_use",
                "fixed_amount": True,
                "payment_amount": int(amount * 100),
                "description": f"Custom topup of {amount} for {user_id}"
            }
            
            response = requests.post(url, json=payload, headers=headers)
            data_res = response.json()
            
            if response.status_code == 200 and 'image_url' in data_res:
                qr_url = data_res['image_url']
                qr_id = data_res['id']
                
                qr_caption = (
                    "┏ 💳 **CUSTOM WALLET TOPUP QR** ❞\n┗ \n\n"
                    f"Scan & pay exactly **₹{amount:.2f}** via any UPI app.\n\n"
                    "🟩 Payment korar por niche **'✅ VERIFY PAYMENT'** button-এ click korun."
                )
                pay_kb = [
                    [InlineKeyboardButton("✅ VERIFY PAYMENT", callback_data=f"verify_topup_{qr_id}")],
                    [InlineKeyboardButton("❌ Cancel", callback_data="back_to_main")]
                ]
                await update.message.reply_photo(photo=qr_url, caption=qr_caption, reply_markup=InlineKeyboardMarkup(pay_kb), parse_mode="Markdown")
            else:
                await update.message.reply_text("⚠️ Error generating Razorpay QR. Please try again.")
        except ValueError:
            await update.message.reply_text("❌ Kripya ekti sothik number type korun (Example: 100, 500)।")

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
