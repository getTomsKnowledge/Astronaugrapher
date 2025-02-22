"""
@project: Astronaugrapher
@author: Tom W and Chat G
@date: 02/21/2025

This module retrieves initial state data from NASA JPL Horizons.
FIX: Reformatted START_TIME and STOP_TIME to comply with Horizons API time format requirements.
      - START_TIME and STOP_TIME now use "YYYY-MM-DD HH:MM:SS" format.
      - STOP_TIME set to START_TIME + 1 second to satisfy Horizons requirement.
"""

import requests
from datetime import datetime, timedelta
from urllib.parse import urlencode, quote 

# Mapping of body names to Horizons IDs
HORIZONS_IDS = {
    'Sun': '10',
    'Mercury': '199',
    'Venus': '299',
    'Earth': '399',
    'Moon': '301',
    'Mars': '499',
    'Jupiter': '599',
    'Saturn': '699',
    'Uranus': '799',
    'Neptune': '899',
    'Pluto': '999'
}


# Custom quoting function to preserve '@'
def custom_quote(s, safe='/', encoding=None, errors=None):
    return quote(s, safe=safe + '@: ', encoding=encoding, errors=errors)  # Preserve '@', ':', and ' '

def format_horizons_time(dt):
    """
    Formats a datetime object into a Horizons-compliant time string with single quotes.

    Horizons expects date-time strings wrapped in single quotes:
    Example: '2025-01-01 00:00:00'

    Parameters:
        dt (datetime): Datetime object to format.

    Returns:
        str: Formatted time string wrapped in single quotes.
    """
    return f"'{dt.strftime('%Y-%m-%d %H:%M:%S')}'"  # Include single quotes as required

def retrieve_data(bodies, START_TIME, EPHEM_TYPE="VECTORS", CENTER="500@0", STEP_SIZE=60, OUT_UNITS="'KM-S'",
                   VEC_TABLE="3", REF_PLANE="ECLIPTIC", REF_SYSTEM="J2000", VEC_CORR="NONE", ANG_FORMAT="DEG",
                   CSV_FORMAT="YES", OBJ_DATA="NO"):
    """
    Retrieves initial state data for each celestial body from NASA JPL Horizons.

    Parameters:
        bodies (list): List of celestial body names.
        START_TIME (datetime or str): Start date/time as datetime object or compliant string.
        Other parameters: Horizons API parameters.

    Returns:
        dict: Positions and velocities for each body.
    """

    # Convert START_TIME to datetime if it's a string
    if isinstance(START_TIME, str):
        try:
            START_TIME = datetime.strptime(START_TIME, "%Y-%m-%d")
        except ValueError:
            print(f"Error: START_TIME '{START_TIME}' is not in the required format 'YYYY-MM-DD'.")
            return {}

    if not isinstance(START_TIME, datetime):
        print("Error: START_TIME must be a datetime object or a correctly formatted string.")
        return {}

    # Format times to Horizons-compliant strings with single quotes
    start_time_str = format_horizons_time(START_TIME)
    float_step_size = float(STEP_SIZE.strip("'").split()[0])
    step_unit = STEP_SIZE[-1]
    if (step_unit.lower() == 's'):
        stop_time_str = format_horizons_time(START_TIME + timedelta(seconds=float_step_size*10)) # STOP_TIME must be after START_TIME
    else:
        stop_time_str = format_horizons_time(START_TIME + timedelta(hours=float_step_size*10)) # STOP_TIME must be after START_TIME
    

    HORIZONS_API_URL = "https://ssd.jpl.nasa.gov/api/horizons.api"
    data = {}

    for body in bodies:
        body_id = HORIZONS_IDS.get(body)
        if not body_id:
            print(f"Warning: '{body}' is not a supported body.")
            continue
        
        query_params = {
            'format': 'json',
            'COMMAND': body_id,                   # No extra quotes required around the ID
            'CENTER': CENTER,
            'EPHEM_TYPE': EPHEM_TYPE,
            'START_TIME': start_time_str,         # Single-quoted time string
            'STOP_TIME': stop_time_str,           # Single-quoted time string, one second after START_TIME
            'STEP_SIZE': str(int(float_step_size)),  # + '%20' + step_unit,          # Ensure it's a string without units
            'OUT_UNITS': OUT_UNITS,               # Already enclosed in single quotes if passed correctly
            'VEC_TABLE': VEC_TABLE,
            'REF_PLANE': REF_PLANE,
            'REF_SYSTEM': REF_SYSTEM,
            'VEC_CORR': VEC_CORR,
            'ANG_FORMAT': ANG_FORMAT,
            'CSV_FORMAT': CSV_FORMAT,
            'OBJ_DATA': OBJ_DATA
        }
        

        try:
            # URL-encode parameters to ensure compliance with Horizons API
            encoded_params = urlencode(query_params, quote_via=custom_quote)
            request_url = f"{HORIZONS_API_URL}?{encoded_params}"

            print(f"Retrieving data for {body} with URL:\n{request_url}")

            response = requests.get(HORIZONS_API_URL, params=query_params, timeout=30)
            response.raise_for_status()
            result = response.json().get('result', '')

            if "$$SOE" not in result:
                print(f"Warning: No data for {body}. Response:\n{result}")
                continue

            vectors = result.split("$$SOE")[1].split("$$EOE")[0].strip().split("\n")
            positions, velocities = [], []

            for line in vectors:
                elements = line.strip().split(',')
                if len(elements) >= 8:
                    try:
                        pos = [float(elements[2]), float(elements[3]), float(elements[4])]
                        vel = [float(elements[5]), float(elements[6]), float(elements[7])]
                        positions.append(pos)
                        velocities.append(vel)
                    except ValueError:
                        print(f"Malformed data line for {body}: {line}")

            if positions and velocities:
                data[body] = {'positions': positions, 'velocities': velocities}
            else:
                print(f"Warning: No valid position/velocity data for {body}.")

        except Exception as e:
            print(f"Error retrieving {body}: {e}")

    return data