import requests
from config import MIKROTIK_REST_API_URL, MIKROTIK_REST_API_USER, MIKROTIK_REST_API_PASSWORD
from logger import logger

def get_hotspot_profile_list():
    logger.debug("Fetching hotspot profile list")
    try:
        response = requests.get(
            f'{MIKROTIK_REST_API_URL}/ip/hotspot/user/profile',
            auth=(MIKROTIK_REST_API_USER, MIKROTIK_REST_API_PASSWORD)
        )
        response.raise_for_status()
        profiles = response.json()
        profile_info = [f"📋{profile['name']} 🔀 Limit: {profile.get('rate-limit', 'N/A')}" for profile in profiles]
        logger.info("Hotspot profile list fetched successfully")
        return profile_info
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        return [f"Error: {http_err}"]
    except Exception as err:
        logger.error(f"Other error occurred: {err}")
        return [f"Error: {err}"]
