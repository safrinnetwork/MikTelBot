import requests
import random
import string
from config import MIKROTIK_REST_API_URL, MIKROTIK_REST_API_USER, MIKROTIK_REST_API_PASSWORD
from logger import logger
import datetime

def get_profile_list():
    try:
        response = requests.get(
            f'{MIKROTIK_REST_API_URL}/ip/hotspot/user/profile',
            auth=(MIKROTIK_REST_API_USER, MIKROTIK_REST_API_PASSWORD)
        )
        response.raise_for_status()
        profiles = response.json()
        profile_info = [
            f"📋{profile['name']} 🔀 Limit: {profile.get('rate-limit', 'N/A')}"
            for profile in profiles
        ]
        return profiles, profile_info
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        return [], [f"Error: {http_err}"]
    except Exception as err:
        logger.error(f"Other error occurred: {err}")
        return [], [f"Error: {err}"]

def generate_vouchers(profile_name, voucher_count, digit_length):
    try:
        existing_users_response = requests.get(
            f'{MIKROTIK_REST_API_URL}/ip/hotspot/user',
            auth=(MIKROTIK_REST_API_USER, MIKROTIK_REST_API_PASSWORD)
        )
        existing_users_response.raise_for_status()
        existing_users = existing_users_response.json()

        # Generate a unique comment
        while True:
            random_number = ''.join(random.choices(string.digits, k=3))
            current_date = datetime.datetime.now().strftime("%m.%d.%y")
            comment = f"vc-{random_number}-{current_date}-"
            if not any(user.get('comment', '') == comment for user in existing_users):
                break

        generated_users = []
        for _ in range(voucher_count):
            username = ''.join(random.choices(string.ascii_letters + string.digits, k=digit_length))
            password = username
            user_data = {
                "name": username,
                "password": password,
                "profile": profile_name,
                "comment": comment
            }
            logger.debug(f"Sending user data to server: {user_data}")
            response = requests.put(  # Gunakan metode PUT alih-alih POST
                f'{MIKROTIK_REST_API_URL}/ip/hotspot/user',
                auth=(MIKROTIK_REST_API_USER, MIKROTIK_REST_API_PASSWORD),
                json=user_data
            )
            if response.status_code != 201 and response.status_code != 200:  # Periksa apakah kode respons adalah 200 atau 201
                logger.error(f"Failed to create user: {response.text}")
            response.raise_for_status()
            generated_users.append(f"{username} ({comment})")

        logger.info(f"{voucher_count} vouchers have been generated with comment {comment}.")
        return generated_users
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        return [f"Error: {http_err}"]
    except Exception as err:
        logger.error(f"Other error occurred: {err}")
        return [f"Error: {err}"]
