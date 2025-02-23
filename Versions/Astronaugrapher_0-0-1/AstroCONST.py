# AstroCONST: Comprehensive Constants Module
# Houses astrodynamics constants, unit conversions, gravitational parameters, and robust getter methods with validation.

class AstroCONST:
    """
    Contains standard constants, unit conversions, gravitational parameters, and comprehensive getter methods
    with validation and supported body checks.
    """

    # Universal gravitational constant (km³·kg⁻¹·s⁻²)
    G = 6.67430e-20

    # Unit conversions
    KM_TO_M = 1000.0
    M_TO_KM = 0.001
    AU_TO_KM = 149597870.7
    KM_TO_AU = 1.0 / AU_TO_KM
    DAY_TO_SEC = 86400.0
    YEAR_TO_SEC = 31557600.0

    # Physical constants
    SPEED_OF_LIGHT = 299792.458  # km/s
    EARTH_RADIUS_KM = 6371.0  # km

    # Gravitational parameters (μ = GM) in km³/s²
    GRAVITATIONAL_PARAMETERS = {
        'Sun': 1.32712440018e11,
        'Mercury': 2.2032e4,
        'Venus': 3.24859e5,
        'Earth': 3.986004418e5,
        'Moon': 4.9048695e3,
        'Mars': 4.282837e4,
        'Jupiter': 1.26686534e8,
        'Saturn': 3.7931187e7,
        'Uranus': 5.793939e6,
        'Neptune': 6.836529e6,
        'Pluto': 8.71e2
    }

    # Celestial body radii (km)
    BODY_RADII = {
        'Sun': 696340.0,
        'Mercury': 2439.7,
        'Venus': 6051.8,
        'Earth': 6371.0,
        'Moon': 1737.4,
        'Mars': 3389.5,
        'Jupiter': 69911.0,
        'Saturn': 58232.0,
        'Uranus': 25362.0,
        'Neptune': 24622.0,
        'Pluto': 1188.3
    }

    # Celestial body densities (kg/m³)
    BODY_DENSITIES = {
        'Sun': 1408,
        'Mercury': 5427,
        'Venus': 5243,
        'Earth': 5514,
        'Moon': 3344,
        'Mars': 3933,
        'Jupiter': 1326,
        'Saturn': 687,
        'Uranus': 1271,
        'Neptune': 1638,
        'Pluto': 1850
    }

    @staticmethod
    def validate_body_name(body_name: str) -> bool:
        """Checks if the celestial body is supported."""
        return body_name in AstroCONST.GRAVITATIONAL_PARAMETERS

    @staticmethod
    def get_gravitational_parameter(body_name: str) -> float:
        """
        Retrieves the gravitational parameter (μ) for a celestial body.

        Args:
            body_name (str): Name of the celestial body.

        Returns:
            float: μ in km³/s². Returns 0.0 if body not found.
        """
        if AstroCONST.validate_body_name(body_name):
            return AstroCONST.GRAVITATIONAL_PARAMETERS[body_name]
        print(f"Warning: '{body_name}' is not a supported body.")
        return 0.0

    @staticmethod
    def get_body_radius(body_name: str) -> float:
        """Returns the radius (km) of a celestial body."""
        if AstroCONST.validate_body_name(body_name):
            return AstroCONST.BODY_RADII.get(body_name, 0.0)
        print(f"Warning: '{body_name}' is not a supported body.")
        return 0.0

    @staticmethod
    def get_body_density(body_name: str) -> float:
        """Returns the density (kg/m³) of a celestial body."""
        if AstroCONST.validate_body_name(body_name):
            return AstroCONST.BODY_DENSITIES.get(body_name, 0.0)
        print(f"Warning: '{body_name}' is not a supported body.")
        return 0.0

    @staticmethod
    def get_universal_gravitational_constant() -> float:
        """Returns the universal gravitational constant (G)."""
        return AstroCONST.G

    @staticmethod
    def get_speed_of_light() -> float:
        """Returns the speed of light in km/s."""
        return AstroCONST.SPEED_OF_LIGHT

    @staticmethod
    def list_supported_bodies() -> list:
        """Returns a list of supported celestial bodies."""
        return list(AstroCONST.GRAVITATIONAL_PARAMETERS.keys())

    # Unit conversion methods
    @staticmethod
    def convert_km_to_m(value: float) -> float:
        """Converts kilometers to meters."""
        return value * AstroCONST.KM_TO_M

    @staticmethod
    def convert_m_to_km(value: float) -> float:
        """Converts meters to kilometers."""
        return value * AstroCONST.M_TO_KM

    @staticmethod
    def convert_au_to_km(value: float) -> float:
        """Converts astronomical units (AU) to kilometers."""
        return value * AstroCONST.AU_TO_KM

    @staticmethod
    def convert_km_to_au(value: float) -> float:
        """Converts kilometers to astronomical units (AU)."""
        return value * AstroCONST.KM_TO_AU

    @staticmethod
    def convert_day_to_sec(value: float) -> float:
        """Converts days to seconds."""
        return value * AstroCONST.DAY_TO_SEC

    @staticmethod
    def convert_year_to_sec(value: float) -> float:
        """Converts years to seconds."""
        return value * AstroCONST.YEAR_TO_SEC