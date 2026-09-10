import telebot
from telebot import types
import random
import time

# 🚀 توكين البوت الخاص بك من BotFather
BOT_TOKEN = '8918958634:AAFN9FGotOInT2MmD3OE9mnAIoZDmacXBYY'

# 🌐 رابط موقعك المباشر المستضاف على GitHub Pages
WEB_APP_URL = 'https://abwqnas221-ship-it.github.io/earnmarket-app/'

bot = telebot.TeleBot(BOT_TOKEN)

# قاعدة بيانات مؤقتة في الذاكرة لبيانات المستخدمين
users_db = {}

# كتالوج المنتجات المطابق تماماً لكتالوج موقع الويب
PRODUCTS_CATALOG = [
    {
        "id": "p1",
        "title": "ساعة ذكية Ultra SmartWatch Series 9",
        "category": "إلكترونيات شركات",
        "price": 89.99,
        "commission": 18.00,
        "rate": "20%",
        "company": "AliExpress Partner",
        "desc": "شاشة HD، تتبع اللياقة ومعدل ضربات القلب، شحن سريع."
    },
    {
        "id": "p2",
        "title": "سماعات بلوتوث Noise Cancelling Pro",
        "category": "إلكترونيات شركات",
        "price": 129.00,
        "commission": 25.80,
        "rate": "20%",
        "company": "Amazon Associates",
        "desc": "عزل ضوضاء فائق، بطارية تدوم 40 ساعة متواصلة."
    },
    {
        "id": "p3",
        "title": "اشتراك منصة تعليم الذكاء الاصطناعي",
        "category": "خدمات رقمية",
        "price": 199.00,
        "commission": 59.70,
        "rate": "30%",
        "company": "OpenAI Academy",
        "desc": "وصول شامل لأحدث أدوات الذكاء الاصطناعي وصناعة المحتوى."
    },
    {
        "id": "p4",
        "title": "دورة احترف التداول والتحليل الفني",
        "category": "كورس كريبتو",
        "price": 149.00,
        "commission": 44.70,
        "rate": "30%",
        "company": "MEXC Partner Academy",
        "desc": "كورس إلكتروني كامل للتداول في أسواق الكريبتو مع بونوس ترحيبي."
    }
]

def get_user_data(user_id):
    """جلب بيانات المستخدم أو إنشائها"""
    if user_id not in users_db:
        users_db[user_id] = {
            "balance": 35.50,         # رصيد افتتاح تجريبي
            "total_earnings": 35.50,
            "sales_count": 2,
            "clicks_count": 18,
            "mexc_address": "",
            "sales_history": [
                {"item": "سماعات بلوتوث Pro", "amount": 25.80, "country": "🇸🇦 السعودية", "time": "قبل ساعتين"},
                {"item": "حقيبة ظهر ذكية", "amount": 9.70, "country": "🇦🇪 الإمارات", "time": "قبل يوم"}
            ],
            "withdrawals_history": []
        }
    return users_db[user_id]

def get_main_keyboard():
    """إنشاء القائمة الرئيسية للبوت مع زر التطبيق المصغر Mini App"""
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    
    # زر فتح المنصة تفاعلياً داخل تليجرام (Mini App)
    btn_webapp = types.KeyboardButton(
        text="🌐 فتح منصة المتجر والأرباح (Mini App)", 
        web_app=types.WebAppInfo(url=WEB_APP_URL)
    )
    
    btn_store = types.KeyboardButton("🛒 متجر المنتجات")
    btn_dashboard = types.KeyboardButton("📊 لوحة الأرباح")
    btn_withdraw = types.KeyboardButton("💳 سحب إلى MEXC")
    btn_history = types.KeyboardButton("📜 سجل السحوبات")
    btn_simulate = types.KeyboardButton("⚡ محاكاة مبيعة جديدة")
    
    markup.add(btn_webapp)
    markup.add(btn_store, btn_dashboard)
    markup.add(btn_withdraw, btn_history)
    markup.add(btn_simulate)
    return markup

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        f"👋 أهلاً بك **{message.from_user.first_name}** في بوت **EarnMarket Pro**!\n\n"
        "🚀 **منصة العمل الحر والتسويق بالعمولة المباشرة:**\n"
        "• روّج لمنتجات كبرى الشركات واكسب العمولات مجاناً بالـ USDT.\n"
        "• اسحب أرباحك فوراً وبدون رسوم إلى محفظة **MEXC.COM**.\n"
        "• يمكنك فتح التطبيق التفاعلي المباشر الآن عبر الزر بالأسفل `🌐 فتح منصة المتجر`!\n\n"
        "💡 اختر من القائمة للبدء:"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=get_main_keyboard())

@bot.message_handler(func=lambda message: True)
def handle_menu_click(message):
    user_id = message.from_user.id
    user_data = get_user_data(user_id)
    text = message.text

    if text == "🛒 متجر المنتجات":
        show_products_catalog(message.chat.id)

    elif text == "📊 لوحة الأرباح":
        show_dashboard(message.chat.id, user_data)

    elif text == "💳 سحب إلى MEXC":
        start_withdrawal_flow(message)

    elif text == "📜 سجل السحوبات":
        show_history(message.chat.id, user_data)

    elif text == "⚡ محاكاة مبيعة جديدة":
        simulate_sale(message.chat.id, user_data)

def show_products_catalog(chat_id):
    bot.send_message(chat_id, "📦 **كتالوج منتجات الشركات المتاحة للترويج والربح:**", parse_mode="Markdown")
    
    for product in PRODUCTS_CATALOG:
        markup = types.InlineKeyboardMarkup()
        btn_get_link = types.InlineKeyboardButton(
            text="🔗 احصل على رابط التسويق", 
            callback_data=f"get_link_{product['id']}"
        )
        markup.add(btn_get_link)
        
        caption = (
            f"🔹 **{product['title']}**\n"
            f"🏢 الشركة: `{product['company']}`\n"
            f"🏷️ الفئة: {product['category']}\n"
            f"💰 السعر: ${product['price']}\n"
            f"🎁 عمولتك المباشرة: **${product['commission']} USDT** ({product['rate']})\n"
            f"📝 {product['desc']}"
        )
        bot.send_message(chat_id, caption, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('get_link_'))
def process_product_link(call):
    prod_id = call.data.replace('get_link_', '')
    product = next((p for p in PRODUCTS_CATALOG if p['id'] == prod_id), None)
    
    if product:
        affiliate_link = f"{WEB_APP_URL}?usr={call.from_user.id}&prod={product['id']}"
        response_msg = (
            f"✅ **رابط التسويق الخارجي الخاص بك جاهز:**\n\n"
            f"`{affiliate_link}`\n\n"
            f"📌 **المنتج:** {product['title']}\n"
            f"💵 **العمولة عند الشراء:** `${product['commission']} USDT`\n\n"
            f"شارك هذا الرابط في شبكات التواصل الاجتماعي أو مجموعات تليجرام. عند تنفيذ أي شراء تُضاف أرباحك تلقائياً!"
        )
        bot.send_message(call.message.chat.id, response_msg, parse_mode="Markdown")
        bot.answer_callback_query(call.id, "تم توليد رابطك التسويقي بنجاح!")

def show_dashboard(chat_id, user_data):
    dash_text = (
        "📊 **لوحة الأرباح والإحصائيات الحالية:**\n\n"
        f"💵 **الرصيد المتاح للسحب:** `${user_data['balance']:.2f} USDT`\n"
        f"📈 **إجمالي العمولات المكتسبة:** `${user_data['total_earnings']:.2f}`\n"
        f"🛒 **عدد المبيعات الناجحة:** `{user_data['sales_count']}`\n"
        f"👆 **عدد الزيارات لروابطك:** `{user_data['clicks_count']}`\n\n"
        f"🏛️ **عنوان محفظة MEXC المسجل:**\n"
        f"`{user_data['mexc_address'] if user_data['mexc_address'] else 'لم يتم الحفظ بعد'}`"
    )
    bot.send_message(chat_id, dash_text, parse_mode="Markdown")

def simulate_sale(chat_id, user_data):
    prod = random.choice(PRODUCTS_CATALOG)
    countries = ['🇸🇦 السعودية', '🇦🇪 الإمارات', '🇶🇦 قطر', '🇰🇼 الكويت', '🇪غت مصر', '🇴🇲 عمان']
    c_selected = random.choice(countries)
    
    user_data['balance'] += prod['commission']
    user_data['total_earnings'] += prod['commission']
    user_data['sales_count'] += 1
    user_data['clicks_count'] += random.randint(1, 5)
    
    user_data['sales_history'].insert(0, {
        "item": prod['title'],
        "amount": prod['commission'],
        "country": c_selected,
        "time": "الآن"
    })
    
    success_msg = (
        f"🔥 **مبروك! تمت مبيعة جديدة عبر رابطك!**\n\n"
        f"📦 المنتج: {prod['title']}\n"
        f"🌍 الدولة: {c_selected}\n"
        f"💰 العمولة المضافة: **+${prod['commission']:.2f} USDT**\n\n"
        f"✨ رصيدك الحالي المتاح للسحب إلى MEXC: **${user_data['balance']:.2f} USDT**"
    )
    bot.send_message(chat_id, success_msg, parse_mode="Markdown")

def start_withdrawal_flow(message):
    user_id = message.from_user.id
    user_data = get_user_data(user_id)
    
    if user_data['balance'] < 10.0:
        bot.send_message(
            message.chat.id, 
            f"❌ **الحد الأدنى للسحب هو $10.00 USDT.**\nرصيدك الحالي: `${user_data['balance']:.2f} USDT`",
            parse_mode="Markdown"
        )
        return
        
    prompt = (
        f"💳 **سحب الأرباح إلى منصة MEXC.COM**\n\n"
        f"الرصيد المتاح للسحب: `${user_data['balance']:.2f} USDT`\n\n"
        f"يرجى إرسال **عنوان محفظة USDT (TRC20 أو BEP20)** الخاص بك في MEXC الآن:"
    )
    msg = bot.send_message(message.chat.id, prompt, parse_mode="Markdown")
    bot.register_next_step_handler(msg, process_withdrawal_address)

def process_withdrawal_address(message):
    address = message.text.strip()
    if len(address) < 10:
        bot.send_message(message.chat.id, "❌ **عنوان محفظة غير صالح.** يرجى المحاولة مجدداً.")
        return
        
    user_data = get_user_data(message.from_user.id)
    user_data['mexc_address'] = address
    
    prompt = (
        f"✅ تم تسجيل العنوان: `{address}`\n\n"
        f"أدخل المبلغ المراد سحبه بالـ USDT (الحد الأدنى 10، المتاح: `${user_data['balance']:.2f}`):"
    )
    msg = bot.send_message(message.chat.id, prompt, parse_mode="Markdown")
    bot.register_next_step_handler(msg, process_withdrawal_amount)

def process_withdrawal_amount(message):
    user_id = message.from_user.id
    user_data = get_user_data(user_id)
    
    try:
        amount = float(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, "❌ **يرجى كتابة أرقام فقط.**")
        return
        
    if amount < 10 or amount > user_data['balance']:
        bot.send_message(message.chat.id, "❌ **المبلغ المدخل خارج نطاق رصيدك المتاح.**")
        return
        
    user_data['balance'] -= amount
    tx_hash = "0x" + "".join(random.choices("0123456789abcdef", k=16))
    
    user_data['withdrawals_history'].insert(0, {
        "tx_id": tx_hash,
        "amount": amount,
        "address": user_data['mexc_address'],
        "time": time.strftime("%Y-%m-%d %H:%M")
    })
    
    success_text = (
        f"🎉 **تم معالجة طلب السحب بنجاح إلى MEXC!**\n\n"
        f"💵 المبلغ: `${amount:.2f} USDT`\n"
        f"🏛️ المحفظة: `{user_data['mexc_address']}`\n"
        f"🔗 رقم العملية (TxID):\n`{tx_hash}`\n\n"
        f"الرصيد المتبقي: `${user_data['balance']:.2f} USDT`"
    )
    bot.send_message(message.chat.id, success_text, parse_mode="Markdown")

def show_history(chat_id, user_data):
    if not user_data['withdrawals_history']:
        bot.send_message(chat_id, "📜 **سجل السحوبات فارغ حتى الآن.**")
        return
        
    history_text = "📜 **سجل السحوبات المكتملة إلى MEXC:**\n\n"
    for w in user_data['withdrawals_history']:
        history_text += (
            f"🔹 المبلغ: `${w['amount']:.2f} USDT`\n"
            f"⏱️ التاريخ: {w['time']}\n"
            f"🔗 TxID: `{w['tx_id']}`\n"
            "------------------------\n"
        )
    bot.send_message(chat_id, history_text, parse_mode="Markdown")

if __name__ == '__main__':
    print("🤖 Bot EarnMarket Pro is running...")
    bot.infinity_polling()