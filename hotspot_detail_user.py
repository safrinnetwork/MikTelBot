import requests
from config import MIKROTIK_REST_API_URL, MIKROTIK_REST_API_USER, MIKROTIK_REST_API_PASSWORD
from logger import logger

def get_hotspot_user_details(user_name):
    try:
        response = requests.get(
            f'{MIKROTIK_REST_API_URL}/ip/hotspot/user',
            auth=(MIKROTIK_REST_API_USER, MIKROTIK_REST_API_PASSWORD)
        )
        response.raise_for_status()
        users = response.json()
        
        user = next((user for user in users if user['name'] == user_name), None)
        if not user:
            return f"User {user_name} tidak ditemukan di daftar user hotspot."
        
        result = f"💾Data user\n🚹User: {user['name']}\n🔐Pass: {user['password']}\n📋Profile: {user['profile']}\n"
        
        active_response = requests.get(
            f'{MIKROTIK_REST_API_URL}/ip/hotspot/active',
            auth=(MIKROTIK_REST_API_USER, MIKROTIK_REST_API_PASSWORD)
        )
        active_response.raise_for_status()
        active_users = active_response.json()
        
        active_found_users = [user for user in active_users if user['user'] == user_name]
        
        if active_found_users:
            result += "🛜Hotspot Active\n"
            for active_user in active_found_users:
                result += (
                    f"🚹User: {active_user['user']}\n"
                    f"🏠Address: {active_user['address']}\n"
                    f"📱MAC: {active_user['mac-address']}\n"
                    f"🕐Uptime: {active_user['uptime']}\n"
                )
        
        return result
    
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        return f"Error: {http_err}"
    except Exception as err:
        logger.error(f"Other error occurred: {err}")
        return f"Error: {err}"
