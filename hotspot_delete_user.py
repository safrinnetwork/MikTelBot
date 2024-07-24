import requests
from config import MIKROTIK_REST_API_URL, MIKROTIK_REST_API_USER, MIKROTIK_REST_API_PASSWORD
from logger import logger

def delete_hotspot_user(username):
    logger.debug(f"Attempting to delete hotspot user {username}")
    try:
        response = requests.delete(
            f'{MIKROTIK_REST_API_URL}/ip/hotspot/user/{username}',
            auth=(MIKROTIK_REST_API_USER, MIKROTIK_REST_API_PASSWORD)
        )
        response.raise_for_status()
        logger.info(f"Hotspot user {username} has been deleted.")
        return f"User {username} telah dihapus dari hotspot."
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        return f"Error: {http_err}"
    except Exception as err:
        logger.error(f"Other error occurred: {err}")
        return f"Error: {err}"
