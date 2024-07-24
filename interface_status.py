import requests
from config import MIKROTIK_REST_API_URL, MIKROTIK_REST_API_USER, MIKROTIK_REST_API_PASSWORD
from logger import logger

def get_interface_status(interface_name):
    logger.debug(f"Fetching interface status for {interface_name}")
    try:
        response = requests.post(
            f'{MIKROTIK_REST_API_URL}/interface/monitor-traffic',
            auth=(MIKROTIK_REST_API_USER, MIKROTIK_REST_API_PASSWORD),
            json={"interface": interface_name, "once": True}
        )
        response.raise_for_status()
        status = response.json()
        logger.debug(f"Interface status fetched: {status}")
        return status
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        return f"Error fetching interface status: {http_err}"
    except Exception as err:
        logger.error(f"Other error occurred: {err}")
        return f"Error fetching interface status: {err}"
