import requests
from config import MIKROTIK_REST_API_URL, MIKROTIK_REST_API_USER, MIKROTIK_REST_API_PASSWORD
from logger import logger

def hotspot_delete_active(username):
    logger.debug(f"Attempting to delete active hotspot user {username}")

    try:
        # Dapatkan daftar pengguna aktif untuk menemukan pengguna yang sesuai
        response = requests.get(
            f'{MIKROTIK_REST_API_URL}/ip/hotspot/active',
            auth=(MIKROTIK_REST_API_USER, MIKROTIK_REST_API_PASSWORD)
        )
        response.raise_for_status()
        active_users = response.json()

        # Logging daftar pengguna aktif
        logger.debug(f"Active users data: {active_users}")

        # Temukan pengguna yang sesuai dengan username
        user_id = None
        for user in active_users:
            if user.get('user') == username:
                user_id = user['.id']
                break
        
        if user_id is None:
            return f"User {username} tidak ditemukan di pengguna aktif."

        # Logging ID pengguna yang akan dihapus
        logger.debug(f"Deleting user with ID: {user_id}")

        # Coba untuk log URL lengkap yang digunakan
        delete_url = f'{MIKROTIK_REST_API_URL}/ip/hotspot/active/{user_id}'
        logger.debug(f"Delete URL: {delete_url}")

        # Hapus pengguna aktif dengan ID yang ditemukan
        delete_response = requests.delete(
            delete_url,
            auth=(MIKROTIK_REST_API_USER, MIKROTIK_REST_API_PASSWORD)
        )
        delete_response.raise_for_status()
        logger.info(f"Active hotspot user {username} has been deleted.")
        return f"User aktif {username} telah dihapus dari hotspot."
    
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        return f"Error: {http_err}"
    except Exception as err:
        logger.error(f"Other error occurred: {err}")
        return f"Error: {err}"
