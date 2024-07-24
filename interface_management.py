import requests
from config import MIKROTIK_REST_API_URL, MIKROTIK_REST_API_USER, MIKROTIK_REST_API_PASSWORD
from logger import logger
from interface_list import get_interface_list

def disable_interface(interface_name):
    try:
        logger.debug(f"Attempting to disable interface {interface_name}")
        response = requests.patch(
            f'{MIKROTIK_REST_API_URL}/interface/{interface_name}',
            auth=(MIKROTIK_REST_API_USER, MIKROTIK_REST_API_PASSWORD),
            json={"disabled": "yes"}
        )
        response.raise_for_status()
        logger.info(f"Interface {interface_name} has been disabled.")
        return f"Interface {interface_name} telah di-disable."
    except Exception as e:
        logger.error(f"Failed to disable interface {interface_name}: {e}")
        return f"Gagal men-disable interface {interface_name}. Error: {e}"

def enable_interface(interface_name):
    try:
        logger.debug(f"Attempting to enable interface {interface_name}")
        response = requests.patch(
            f'{MIKROTIK_REST_API_URL}/interface/{interface_name}',
            auth=(MIKROTIK_REST_API_USER, MIKROTIK_REST_API_PASSWORD),
            json={"disabled": "no"}
        )
        response.raise_for_status()
        logger.info(f"Interface {interface_name} has been enabled.")
        return f"Interface {interface_name} telah di-enable."
    except Exception as e:
        logger.error(f"Failed to enable interface {interface_name}: {e}")
        return f"Gagal men-enable interface {interface_name}. Error: {e}"

def change_interface_name(old_name, new_name):
    try:
        logger.debug(f"Attempting to change interface name from {old_name} to {new_name}")
        # Cek apakah interface dengan nama lama ada
        interface_list = get_interface_list()
        if not any(interface['name'] == old_name for interface in interface_list):
            return f"Interface {old_name} tidak ditemukan."

        response = requests.patch(
            f'{MIKROTIK_REST_API_URL}/interface/{old_name}',
            auth=(MIKROTIK_REST_API_USER, MIKROTIK_REST_API_PASSWORD),
            json={"name": new_name}
        )
        response.raise_for_status()
        logger.info(f"Interface {old_name} has been renamed to {new_name}.")
        return f"Interface {old_name} telah diganti namanya menjadi {new_name}."
    except Exception as e:
        logger.error(f"Failed to change interface name from {old_name} to {new_name}: {e}")
        return f"Gagal mengganti nama interface {old_name}. Error: {e}"
