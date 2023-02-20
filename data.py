from typing import List
from datetime import datetime
from collections import namedtuple

import requests


Earthquake = namedtuple(
    "Earthquake",
    [
        "longitude",
        "latitude",
        "date",
        "id",
        "country",
        "locationName",
        "deaths",
        "eqMagnitude",
        "eqDepth",
        "hour",
        "housesDestroyed",
        "housesDamaged",
        "totalHouses",
        "injuries",
    ],
)


class EarthquakeDataset:
    """Earthquake dataset class, which is used to get earthquake data from the NOAA API"""

    def __init__(self):

        self.api_url = (
            "https://www.ngdc.noaa.gov/hazel/hazard-service" + "/api/v1/earthquakes"
        )
        self.parameters = {}

        self._set_parameters = set(
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
        self._get_necessary_parameters = set(
            [
                "longitude",
                "latitude",
                "year",
                "month",
                "day",
                "id",
                "country",
                "locationName",
                "deaths",
                "eqMagnitude",
                "eqDepth",
            ]
        )

        self._get_optional_parameters = set(
            [
                "hour",
                "housesDestroyed",
                "housesDamaged",
                "totalHouses",
                "injuries",
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

        # Check if the parameters are valid (If you know what you are doing,
        # feel free to change self.simple_parameters)
        if not _parameters.issubset(self._set_parameters):
            _p = _parameters - self._set_parameters
            raise ValueError(
                f"The following parameters are outside the range of this program: {_p}"
            )

        if "year" in _parameters and (
            "minYear" in _parameters or "maxYear" in _parameters
        ):
            raise ValueError("You cannot give year range and year at the same time")

        self.parameters = kwargs

    def request_data(self) -> dict:
        """Request data from the API

        Returns:
            dict: Data from the API in JSON format
        """

        response = requests.get(self.api_url, params=self.parameters, timeout=15)
        if response.status_code == 200:
            return response.json()

        raise ConnectionError(f"Error code: {response.status_code}")

    def _parse_api_data(self, data: List[dict]) -> List[Earthquake]:
        """Parse data from the API

        Args:
            data (List[dict]): Data from the API in JSON format

        Returns:
            List[Earthquake]: List of earthquakes with desired parameters
        """

        earthquakes = []

        for datum in data:

            # Check if the data has all the necessary parameters
            if not self._get_necessary_parameters.issubset(datum.keys()):
                continue

            earthquake = {}

            # Get the necessary parameters
            for parameter in self._get_necessary_parameters:
                earthquake[parameter] = datum[parameter]

            # Get the optional parameters
            for parameter in self._get_optional_parameters:
                if parameter in datum:
                    earthquake[parameter] = datum[parameter]
                else:
                    earthquake[parameter] = None

            # Convert the date to datetime object
            earthquake["date"] = datetime.strptime(
                f"{earthquake['year']}-{earthquake['month']}-{earthquake['day']}",
                "%Y-%m-%d",
            )

            earthquakes.append(
                Earthquake(
                    **{
                        key: value
                        for key, value in earthquake.items()
                        if key not in ["year", "month", "day"]
                    }
                )
            )

        return earthquakes

    def get_data(self) -> List[Earthquake]:
        """Get data from the API

        Returns:
            List[Earthquake] : List of earthquakes
        """

        data = self._parse_api_data(self.request_data()["items"])

        return data

    def __call__(self, **kwargs) -> List[Earthquake]:
        """Get data as an Earthquake list with the given parameters

        Returns:
            List[Earthquake] : List of earthquakes
        """

        self.set_parameters(**kwargs)
        return self.get_data()
