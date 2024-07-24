import requests
from config import MIKROTIK_REST_API_URL, MIKROTIK_REST_API_USER, MIKROTIK_REST_API_PASSWORD

def get_interface_list():
    response = requests.get(
        f'{MIKROTIK_REST_API_URL}/interface',
        auth=(MIKROTIK_REST_API_USER, MIKROTIK_REST_API_PASSWORD)
    )
    response.raise_for_status()  # Akan memunculkan error jika status code bukan 200
    interfaces = response.json()

    # Tambahkan status enable/disable
    for interface in interfaces:
        interface['status'] = 'enabled' if interface.get('disabled') == 'false' else 'disabled'
    
    return interfaces
