import requests
from config import MIKROTIK_REST_API_URL, MIKROTIK_REST_API_USER, MIKROTIK_REST_API_PASSWORD
from logger import logger

def get_hotspot_user_data():
    logger.debug("Fetching hotspot user data")
    try:
        response_users = requests.get(
            f'{MIKROTIK_REST_API_URL}/ip/hotspot/user',
            auth=(MIKROTIK_REST_API_USER, MIKROTIK_REST_API_PASSWORD)
        )
        response_users.raise_for_status()
        users = response_users.json()

        response_active = requests.get(
            f'{MIKROTIK_REST_API_URL}/ip/hotspot/active',
            auth=(MIKROTIK_REST_API_USER, MIKROTIK_REST_API_PASSWORD)
        )
        response_active.raise_for_status()
        active_users = response_active.json()

        response_hosts = requests.get(
            f'{MIKROTIK_REST_API_URL}/ip/hotspot/host',
            auth=(MIKROTIK_REST_API_USER, MIKROTIK_REST_API_PASSWORD)
        )
        response_hosts.raise_for_status()
        hosts = response_hosts.json()

        logger.info("Hotspot user data fetched successfully")
        return f"Total data\n🚹User: {len(users)}\n🛜Active: {len(active_users)}\n🛗Host: {len(hosts)}"
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        return f"Error fetching hotspot user data: {http_err}"
    except Exception as err:
        logger.error(f"Other error occurred: {err}")
        return f"Error fetching hotspot user data: {err}"
