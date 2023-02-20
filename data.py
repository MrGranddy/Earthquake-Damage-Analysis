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
        """Set the parameters for the dataset

        Args:
            country (str, optional): Country name.
            minDeaths (int, optional): Minimum number of deaths.
            minEqDepth (int, optional): Minimum earthquake depth.
            minEqMagnitude (int, optional): Minimum earthquake magnitude.
            minYear (int, optional): Minimum year. Cannot be used with year.
            maxDeaths (int, optional): Maximum number of deaths.
            maxYear (int, optional): Maximum year. Cannot be used with year.
            maxEqDepth (int, optional): Maximum earthquake depth.
            maxEqMagnitude (int, optional): Maximum earthquake magnitude.
            year (int, optional): Year. Cannot be used with minYear and maxYear.

        Returns:
            None
        """

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
        """Request data from the API

        Returns:
            dict: Data from the API in JSON format
        """

        response = requests.get(self.api_url, params=self.parameters, timeout=15)
        if response.status_code == 200:
            return response.json()
        else:
            raise ConnectionError(f"Error code: {response.status_code}")
