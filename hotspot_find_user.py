import requests
from config import MIKROTIK_REST_API_URL, MIKROTIK_REST_API_USER, MIKROTIK_REST_API_PASSWORD
from logger import logger

def find_hotspot_user(user_name):
    try:
        response = requests.get(
            f'{MIKROTIK_REST_API_URL}/ip/hotspot/user',
            auth=(MIKROTIK_REST_API_USER, MIKROTIK_REST_API_PASSWORD)
        )
        response.raise_for_status()
        users = response.json()
        
        found_users = [user for user in users if user_name in user['name']]
        
        if not found_users:
            return f"User {user_name} tidak ditemukan"
        
        result = f"🔎Hasil pencarian user {user_name}\n"
        for user in found_users:
            result += f"🚹User: {user['name']}\n"
        
        active_response = requests.get(
            f'{MIKROTIK_REST_API_URL}/ip/hotspot/active',
            auth=(MIKROTIK_REST_API_USER, MIKROTIK_REST_API_PASSWORD)
        )
        active_response.raise_for_status()
        active_users = active_response.json()
        
        active_found_users = [user for user in active_users if user_name in user['user']]
        
        if active_found_users:
            result += "🛜Hotspot Active\n"
            for active_user in active_found_users:
                result += f"🚹User: {active_user['user']}\n"
        
        result += f"🔍Cek data user /hotspot_detail_user {user_name}"
        
        return result
    
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        return f"Error: {http_err}"
    except Exception as err:
        logger.error(f"Other error occurred: {err}")
        return f"Error: {err}"
