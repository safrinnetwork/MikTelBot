import telebot
from telebot import types
from config import TELEGRAM_TOKEN
from menu import get_menu
from interface_list import get_interface_list
from interface_management import disable_interface, enable_interface, change_interface_name
from interface_status import get_interface_status
from hotspot_user import get_hotspot_user_data
from hotspot_find_user import find_hotspot_user
from hotspot_detail_user import get_hotspot_user_details
from hotspot_delete_user import delete_hotspot_user
from hotspot_delete_active import hotspot_delete_active
from hotspot_profile_list import get_hotspot_profile_list
from hotspot_ip_binding import get_hotspot_ip_binding
from hotspot_gen_vc import get_profile_list, generate_vouchers
from logger import logger
import threading

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Dictionary to keep track of interface rename states
interface_rename_state = {}
voucher_generation_state = {}
hotspot_state = {}

# Event to stop the monitoring thread
monitoring_stop_event = threading.Event()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    logger.info(f"Received /start command from {message.chat.id}")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.KeyboardButton("Interface"))
    markup.add(types.KeyboardButton("Hotspot"))
    bot.reply_to(message, "Selamat datang di Bot MikroTik! Silakan pilih menu:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Interface")
def interface_menu(message):
    logger.info(f"Interface menu selected by {message.chat.id}")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.KeyboardButton("List"))
    markup.add(types.KeyboardButton("Disable"))
    markup.add(types.KeyboardButton("Enable"))
    markup.add(types.KeyboardButton("Monitor"))
    markup.add(types.KeyboardButton("Rename"))
    markup.add(types.KeyboardButton("Kembali"))
    bot.reply_to(message, "Silakan pilih perintah interface:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Hotspot")
def hotspot_menu(message):
    logger.info(f"Hotspot menu selected by {message.chat.id}")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.KeyboardButton("Total"))
    markup.add(types.KeyboardButton("Cari"))
    markup.add(types.KeyboardButton("Detail"))
    markup.add(types.KeyboardButton("Hapus"))
    markup.add(types.KeyboardButton("Kick"))
    markup.add(types.KeyboardButton("Profile"))
    markup.add(types.KeyboardButton("Binding"))
    markup.add(types.KeyboardButton("Generate"))
    markup.add(types.KeyboardButton("Kembali"))
    bot.reply_to(message, "Silakan pilih perintah hotspot:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Kembali")
def main_menu(message):
    logger.info(f"Main menu selected by {message.chat.id}")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.KeyboardButton("Interface"))
    markup.add(types.KeyboardButton("Hotspot"))
    bot.reply_to(message, "Silakan pilih menu:", reply_markup=markup)

# Interface Handlers
@bot.message_handler(func=lambda message: message.text == "List")
def send_interface_list(message):
    logger.info(f"Received List command from {message.chat.id}")
    interfaces = get_interface_list()
    interface_info = "\n".join([f"⏹️ {interface['name']} # {interface['type']} # {'✅' if interface['status'] == 'enabled' else '❌'}" for interface in interfaces])
    bot.reply_to(message, interface_info)

@bot.message_handler(func=lambda message: message.text == "Disable")
def disable_interface_menu(message):
    logger.info(f"Disable menu selected by {message.chat.id}")
    interfaces = get_interface_list()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for interface in interfaces:
        markup.add(types.KeyboardButton(f"Disable {interface['name']}"))
    markup.add(types.KeyboardButton("Kembali"))
    bot.reply_to(message, "Silakan pilih interface yang akan di-disable:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text.startswith("Disable "))
def handle_disable_interface(message):
    interface_name = message.text.split("Disable ")[1]
    logger.info(f"Received /interface_disable command for {interface_name} from {message.chat.id}")
    result = disable_interface(interface_name)
    bot.reply_to(message, result)

@bot.message_handler(func=lambda message: message.text == "Enable")
def enable_interface_menu(message):
    logger.info(f"Enable menu selected by {message.chat.id}")
    interfaces = get_interface_list()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for interface in interfaces:
        markup.add(types.KeyboardButton(f"Enable {interface['name']}"))
    markup.add(types.KeyboardButton("Kembali"))
    bot.reply_to(message, "Silakan pilih interface yang akan di-enable:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text.startswith("Enable "))
def handle_enable_interface(message):
    interface_name = message.text.split("Enable ")[1]
    logger.info(f"Received /interface_enable command for {interface_name} from {message.chat.id}")
    result = enable_interface(interface_name)
    bot.reply_to(message, result)

@bot.message_handler(func=lambda message: message.text == "Monitor")
def monitor_interface_menu(message):
    logger.info(f"Monitor menu selected by {message.chat.id}")
    interfaces = get_interface_list()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for interface in interfaces:
        markup.add(types.KeyboardButton(f"Monitor {interface['name']}"))
    markup.add(types.KeyboardButton("Kembali"))
    bot.reply_to(message, "Silakan pilih interface yang akan dimonitor:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text.startswith("Monitor "))
def handle_monitor_interface(message):
    interface_name = message.text.split("Monitor ")[1]
    logger.info(f"Received /interface_status command for {interface_name} from {message.chat.id}")
    monitoring_stop_event.clear()
    status = get_interface_status(interface_name)
    
    if isinstance(status, str) and status.startswith("Error"):
        bot.reply_to(message, status)
    else:
        formatted_status = (
            f"Monitoring Traffic {interface_name}\n\n"
            f"Upload: {int(status[0]['tx-bits-per-second']) / 1_000_000:.2f} Mbps ⬆️\n"
            f"Download: {int(status[0]['rx-bits-per-second']) / 1_000_000:.2f} Mbps ⬇️\n\n"
            "Tekan tombol ini untuk menghentikan proses monitoring."
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Stop", callback_data="stop_monitoring"))
        sent_message = bot.reply_to(message, formatted_status, reply_markup=markup)
        
        # Start monitoring in a new thread
        monitoring_thread = threading.Thread(target=monitor_interface_status, args=(message.chat.id, sent_message.message_id, interface_name))
        monitoring_thread.start()

@bot.callback_query_handler(func=lambda call: call.data == "stop_monitoring")
def stop_monitoring_callback(call):
    logger.info(f"Received stop monitoring command from {call.message.chat.id}")
    monitoring_stop_event.set()
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Monitoring dihentikan.")

@bot.message_handler(func=lambda message: message.text == "Rename")
def rename_interface_menu(message):
    logger.info(f"Rename menu selected by {message.chat.id}")
    interfaces = get_interface_list()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for interface in interfaces:
        markup.add(types.KeyboardButton(f"Rename {interface['name']}"))
    markup.add(types.KeyboardButton("Kembali"))
    bot.reply_to(message, "Silakan pilih interface yang akan di-rename:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text.startswith("Rename "))
def handle_rename_interface(message):
    interface_name = message.text.split("Rename ")[1]
    logger.info(f"Received /interface_c_name command for {interface_name} from {message.chat.id}")
    interface_rename_state[message.chat.id] = interface_name
    bot.reply_to(message, f"Masukkan nama baru untuk interface {interface_name}:")

@bot.message_handler(func=lambda message: message.chat.id in interface_rename_state)
def handle_new_interface_name(message):
    old_name = interface_rename_state.pop(message.chat.id, None)
    if old_name:
        new_name = message.text.strip()
        logger.info(f"Renaming interface {old_name} to {new_name}")
        result = change_interface_name(old_name, new_name)
        bot.reply_to(message, result)
        bot.reply_to(message, "Gunakan perintah List untuk mengecek apakah nama interface sudah berhasil di ganti.")
    else:
        bot.reply_to(message, "Tidak ada permintaan perubahan nama interface yang aktif.")

def monitor_interface_status(chat_id, message_id, interface_name):
    import time
    previous_status = ""
    while not monitoring_stop_event.is_set():
        status = get_interface_status(interface_name)
        if isinstance(status, str) and status.startswith("Error"):
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=status)
            break
        else:
            formatted_status = (
                f"Monitoring Traffic {interface_name}\n\n"
                f"Upload: {int(status[0]['tx-bits-per-second']) / 1_000_000:.2f} Mbps ⬆️\n"
                f"Download: {int(status[0]['rx-bits-per-second']) / 1_000_000:.2f} Mbps ⬇️\n\n"
                "Tekan tombol ini untuk menghentikan proses monitoring."
            )
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Stop", callback_data="stop_monitoring"))
            if formatted_status != previous_status:
                try:
                    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=formatted_status, reply_markup=markup)
                    previous_status = formatted_status
                except telebot.apihelper.ApiTelegramException as e:
                    if "message is not modified" in str(e):
                        continue
                    else:
                        raise e
        time.sleep(3)

# Hotspot Handlers
@bot.message_handler(func=lambda message: message.text == "Total")
def handle_hotspot_user(message):
    logger.info(f"Received /hotspot_user command from {message.chat.id}")
    result = get_hotspot_user_data()
    bot.reply_to(message, result)

@bot.message_handler(func=lambda message: message.text == "Cari")
def handle_hotspot_find_user_prompt(message):
    hotspot_state[message.chat.id] = 'find_user'
    bot.reply_to(message, "Masukkan nama user yang akan dicari:")

@bot.message_handler(func=lambda message: message.text == "Detail")
def handle_hotspot_detail_user_prompt(message):
    hotspot_state[message.chat.id] = 'detail_user'
    bot.reply_to(message, "Masukkan nama user yang akan diperiksa secara detail:")

@bot.message_handler(func=lambda message: message.text == "Hapus")
def handle_hotspot_delete_user_prompt(message):
    hotspot_state[message.chat.id] = 'delete_user'
    bot.reply_to(message, "Masukkan nama user yang akan dihapus:")

@bot.message_handler(func=lambda message: message.text == "Kick")
def handle_hotspot_delete_active_user_prompt(message):
    hotspot_state[message.chat.id] = 'kick_user'
    bot.reply_to(message, "Masukkan nama user yang akan di-kick:")

@bot.message_handler(func=lambda message: message.chat.id in hotspot_state)
def handle_hotspot_actions(message):
    action = hotspot_state.pop(message.chat.id)
    user_name = message.text.strip()
    if action == 'find_user':
        result = find_hotspot_user(user_name)
        bot.reply_to(message, result)
    elif action == 'detail_user':
        result = get_hotspot_user_details(user_name)
        bot.reply_to(message, result)
    elif action == 'delete_user':
        result = delete_hotspot_user(user_name)
        bot.reply_to(message, result)
    elif action == 'kick_user':
        result = hotspot_delete_active(user_name)
        bot.reply_to(message, result)

@bot.message_handler(func=lambda message: message.text == "Profile")
def handle_hotspot_profile_list(message):
    logger.info(f"Received /hotspot_profile_list command from {message.chat.id}")
    profiles, profile_info = get_profile_list()
    bot.reply_to(message, "\n".join(profile_info))

@bot.message_handler(func=lambda message: message.text == "Binding")
def handle_hotspot_ip_binding(message):
    logger.info(f"Received /hotspot_ip_binding command from {message.chat.id}")
    results = get_hotspot_ip_binding()
    for result in results:
        bot.reply_to(message, result)

@bot.message_handler(func=lambda message: message.text == "Generate")
def hotspot_gen_vc(message):
    logger.info(f"Received /hotspot_gen_vc command from {message.chat.id}")
    profiles, profile_info = get_profile_list()
    if profiles:
        voucher_generation_state[message.chat.id] = {"step": "choose_profile", "profiles": profiles}
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, input_field_placeholder="Pilih profile")
        for profile in profile_info:
            markup.add(types.KeyboardButton(profile.split(' 🔀 ')[0].replace("📋", "")))
        bot.reply_to(message, "Silahkan pilih profile:", reply_markup=markup)
    else:
        bot.reply_to(message, "\n".join(profile_info))

@bot.message_handler(func=lambda message: voucher_generation_state.get(message.chat.id, {}).get("step") == "choose_profile")
def choose_profile(message):
    profile_name = message.text.strip()
    profiles = voucher_generation_state[message.chat.id]["profiles"]
    profile_names = [profile["name"] for profile in profiles]
    if profile_name in profile_names:
        voucher_generation_state[message.chat.id]["profile"] = profile_name
        voucher_generation_state[message.chat.id]["step"] = "enter_count"
        bot.reply_to(message, f"Profile {profile_name} dipilih. Berapa voucher yang akan di-generate?")
    else:
        bot.reply_to(message, f"Profile {profile_name} tidak ditemukan. Silahkan pilih profile yang benar.")

@bot.message_handler(func=lambda message: voucher_generation_state.get(message.chat.id, {}).get("step") == "enter_count")
def enter_count(message):
    try:
        voucher_count = int(message.text.strip())
        if voucher_count <= 0:
            raise ValueError("Voucher count must be positive.")
        voucher_generation_state[message.chat.id]["voucher_count"] = voucher_count
        voucher_generation_state[message.chat.id]["step"] = "enter_length"
        bot.reply_to(message, f"{voucher_count} voucher akan di-generate. Berapa digit format voucher?")
    except ValueError:
        bot.reply_to(message, "Silahkan masukkan jumlah voucher yang valid.")

@bot.message_handler(func=lambda message: voucher_generation_state.get(message.chat.id, {}).get("step") == "enter_length")
def enter_length(message):
    try:
        digit_length = int(message.text.strip())
        if digit_length <= 0:
            raise ValueError("Digit length must be positive.")
        profile_name = voucher_generation_state[message.chat.id]["profile"]
        voucher_count = voucher_generation_state[message.chat.id]["voucher_count"]
        generated_users = generate_vouchers(profile_name, voucher_count, digit_length)
        voucher_generation_state.pop(message.chat.id, None)
        bot.reply_to(message, f"{voucher_count} voucher telah di-generate:\n\n" + "\n".join(generated_users))
    except ValueError:
        bot.reply_to(message, "Silahkan masukkan panjang digit yang valid.")

bot.polling()
