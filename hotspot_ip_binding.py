import requests
from config import MIKROTIK_REST_API_URL, MIKROTIK_REST_API_USER, MIKROTIK_REST_API_PASSWORD
from logger import logger

def get_hotspot_ip_binding():
    logger.debug("Fetching hotspot IP binding list")
    try:
        response = requests.get(
            f'{MIKROTIK_REST_API_URL}/ip/hotspot/ip-binding',
            auth=(MIKROTIK_REST_API_USER, MIKROTIK_REST_API_PASSWORD)
        )
        response.raise_for_status()
        bindings = response.json()
        
        def binding_type(type):
            if type == 'bypass':
                return '✅'
            elif type == 'block':
                return '❌'
            else:
                return '🟰'
        
        binding_info_list = [
            f"📱Mac: {binding.get('mac-address', 'N/A')}\n"
            f"🏠Address: {binding.get('address', 'N/A')}\n"
            f"🏘To Address: {binding.get('to-address', 'N/A')}\n"
            f"👁‍🗨Type: {binding_type(binding.get('type', 'regular'))}"
            for binding in bindings
        ]
        
        # Split the list into chunks of 10 items each to avoid long messages
        chunk_size = 10
        binding_info_chunks = [binding_info_list[i:i + chunk_size] for i in range(0, len(binding_info_list), chunk_size)]
        
        logger.info("Hotspot IP binding list fetched successfully")
        return binding_info_chunks
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        return [f"Error: {http_err}"]
    except Exception as err:
        logger.error(f"Other error occurred: {err}")
        return [f"Error: {err}"]
