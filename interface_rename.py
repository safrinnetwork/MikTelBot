import requests
from config import MIKROTIK_REST_API_URL, MIKROTIK_REST_API_USER, MIKROTIK_REST_API_PASSWORD
from logger import logger

def rename_interface(old_name, new_name):
    logger.debug(f"Attempting to rename interface {old_name} to {new_name}")
    try:
        response = requests.patch(
            f'{MIKROTIK_REST_API_URL}/interface/{old_name}',
            auth=(MIKROTIK_REST_API_USER, MIKROTIK_REST_API_PASSWORD),
            json={"name": new_name}
        )
        response.raise_for_status()
        logger.info(f"Interface {old_name} has been renamed to {new_name}.")
        return f"Nama interface {old_name} berhasil diganti menjadi {new_name}."
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        return f"Error: {http_err}"
    except Exception as err:
        logger.error(f"Other error occurred: {err}")
        return f"Error: {err}"
