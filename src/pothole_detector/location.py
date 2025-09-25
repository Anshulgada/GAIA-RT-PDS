from .console import console

try:
    from geopy.geocoders import Nominatim  # type: ignore

    GEOPY_AVAILABLE = True
except Exception:
    Nominatim = None
    GEOPY_AVAILABLE = False


class LocationService:
    """Handle reverse geocoding and location-based services."""

    def __init__(self):
        if GEOPY_AVAILABLE and Nominatim:
            self.geolocator = Nominatim(user_agent="pothole_detection_system")
        else:
            self.geolocator = None
            console.print(
                "[yellow]Warning: geopy not available. Address lookup disabled.[/yellow]"
            )

    def get_address(self, lat: float, lon: float) -> str:
        """Convert coordinates to human-readable address."""
        if not self.geolocator:
            return f"Latitude: {lat:.6f}, Longitude: {lon:.6f}"

        try:
            location = self.geolocator.reverse(f"{lat}, {lon}", timeout=10)
            return (
                location.address
                if location
                else f"Latitude: {lat:.6f}, Longitude: {lon:.6f}"
            )
        except Exception as e:
            console.print(f"[yellow]Warning: Could not get address: {e}[/yellow]")
            return f"Latitude: {lat:.6f}, Longitude: {lon:.6f}"

    def get_maps_link(self, lat: float, lon: float) -> str:
        """Generate Google Maps link from coordinates."""
        return f"https://www.google.com/maps?q={lat},{lon}"
