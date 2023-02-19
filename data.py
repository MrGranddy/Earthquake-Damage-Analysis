import requests


class EarthquakeDataset:
    """Earthquake dataset class, which is used to get earthquake data from the NOAA API"""

    def __init__(self):

        self.api_url = (
            "https://www.ngdc.noaa.gov/hazel/hazard-service" + "/api/v1/earthquakes"
        )
        self.parameters = {}
        self.simple_parameters = set(
            [
                "country",
                "minDeaths",
                "minEqDepth",
                "minEqMagnitude",
                "minYear",
                "maxDeaths",
                "maxYear",
                "maxEqDepth",
                "maxEqMagnitude",
                "year",
            ]
        )

    def set_parameters(self, **kwargs):

        _parameters = set(kwargs.keys())

        # Check if the parameters are valid (If you know what you are doing, feel free to change self.simple_parameters)
        if not _parameters.issubset(self.simple_parameters):
            raise ValueError(
                f"The following parameters are outside the range of this program: {_parameters - self.simple_parameters}"
            )

        if "year" in _parameters and (
            "minYear" in _parameters or "maxYear" in _parameters
        ):
            raise ValueError("You cannot give year range and year at the same time")

        self.parameters = kwargs

    def request_data(self):

        response = requests.get(self.api_url, params=self.parameters, timeout=15)
        if response.status_code == 200:
            return response.json()
        else:
            raise ConnectionError(f"Error code: {response.status_code}")
