import unittest
from data import EarthquakeDataset, Earthquake


class TestData(unittest.TestCase):
    def test_initiate(self):
        """Test if the class is initiated correctly"""

        # Create dataset
        dataset = EarthquakeDataset()
        self.assertIsInstance(dataset, EarthquakeDataset)

    def test_set_parameters(self):
        """Test if the parameters are set correctly"""

        # Create dataset
        dataset = EarthquakeDataset()
        self.assertIsInstance(dataset, EarthquakeDataset)

        # Set parameters
        dataset.set_parameters(
            country="Turkey",
            minDeaths=100,
            minEqDepth=100,
            minEqMagnitude=100,
            minYear=100,
            maxDeaths=100,
            maxYear=100,
            maxEqDepth=100,
            maxEqMagnitude=100,
        )
        self.assertEqual(
            dataset.parameters,
            {
                "country": "Turkey",
                "minDeaths": 100,
                "minEqDepth": 100,
                "minEqMagnitude": 100,
                "minYear": 100,
                "maxDeaths": 100,
                "maxYear": 100,
                "maxEqDepth": 100,
                "maxEqMagnitude": 100,
            },
        )

    def test_set_parameters_with_invalid_parameters(self):
        """Test parameters with invalid parameters"""

        # Create dataset
        dataset = EarthquakeDataset()

        # Add "invalidParameter" to the parameters
        with self.assertRaises(ValueError) as context:
            dataset.set_parameters(
                country="Turkey",
                minDeaths=100,
                minEqDepth=100,
                minEqMagnitude=100,
                minYear=100,
                maxDeaths=100,
                maxYear=100,
                maxEqDepth=100,
                maxEqMagnitude=100,
                invalidParameter=100,
            )
        self.assertEqual(
            str(context.exception),
            "The following parameters are outside the range of this program: {'invalidParameter'}",
        )

        # Give year range and year at the same time
        with self.assertRaises(ValueError) as context:
            dataset.set_parameters(
                country="Turkey",
                minDeaths=100,
                minEqDepth=100,
                minEqMagnitude=100,
                minYear=100,
                maxDeaths=100,
                maxYear=100,
                maxEqDepth=100,
                maxEqMagnitude=100,
                year=100,
            )
        self.assertEqual(
            str(context.exception),
            "You cannot give year range and year at the same time",
        )

    def test_request_data_with_no_matching_data(self):
        """Test if the data is requested correctly with no matching data"""

        # Create dataset
        dataset = EarthquakeDataset()

        # Set parameters
        dataset.set_parameters(
            country="Turkey",
            minDeaths=100,
            minEqDepth=0,
            minEqMagnitude=5,
            minYear=1998,
            maxDeaths=30000,
            maxYear=1998,
            maxEqDepth=20,
            maxEqMagnitude=9.9,
        )

        # Request data from API
        data = dataset.request_data()
        eartquakes = data["items"]
        self.assertIsInstance(eartquakes, list)

        # Check if earthquake list is empty
        self.assertEqual(len(eartquakes), 0)

    def test_request_data_with_no_parameters(self):
        """Test if the data is requested correctly with no parameters"""

        # Create dataset
        dataset = EarthquakeDataset()

        # Request data from API
        data = dataset.request_data()
        eartquakes = data["items"]
        self.assertIsInstance(eartquakes, list)

        # Check if the data is valid
        self.assertGreaterEqual(
            len(eartquakes), 6300
        )  # There were 6348 earthquakes when I wrote this test

    def test_request_data(self):
        """Test if the data is requested correctly"""

        # Create dataset
        dataset = EarthquakeDataset()

        # Set parameters
        dataset.set_parameters(
            country="Turkey",
            minDeaths=100,
            minEqDepth=0,
            minEqMagnitude=5,
            minYear=1999,
            maxDeaths=30000,
            maxYear=1999,
            maxEqDepth=20,
            maxEqMagnitude=9.9,
        )

        # Request data from API
        data = dataset.request_data()
        eartquakes = data["items"]
        self.assertIsInstance(eartquakes, list)

        # Check if the data is valid
        self.assertGreater(
            len(eartquakes), 1
        )  # There is only 1 earthquake with the given parameters
        eartquake = eartquakes[0]
        self.assertIsInstance(eartquake, dict)

        # Check if the data is correct
        self.assertEqual(eartquake["country"], "TURKEY")
        self.assertEqual(eartquake["eqDepth"], 13)
        self.assertEqual(eartquake["eqMagnitude"], 7.6)
        self.assertEqual(eartquake["year"], 1999)
        self.assertEqual(eartquake["deaths"], 17118)

    def test_get_data(self):
        """Test if the data is returned correctly"""

        # Create dataset
        dataset = EarthquakeDataset()

        # Set parameters
        dataset.set_parameters(
            country="Turkey",
            minYear=1920,
            maxYear=2023,
        )

        # Request data from API
        data = dataset.get_data()
        self.assertIsInstance(data, list)

        # Check if data type is correct
        self.assertIsInstance(data[0], Earthquake)

    def test_call(self):
        """Test the query and data retrieval"""

        # Create dataset
        dataset = EarthquakeDataset()

        # Query data
        data = dataset(
            country="Turkey",
            minYear=1920,
            maxYear=2023,
        )

        # Check if data type is correct
        self.assertIsInstance(data, list)

        # Check if data type is correct
        self.assertIsInstance(data[0], Earthquake)

    def test_call_with_invalid_parameters(self):
        """Test the query and data retrieval with invalid parameters"""

        # Create dataset
        dataset = EarthquakeDataset()

        # Query data
        with self.assertRaises(ValueError) as context:
            dataset(
                country="Turkey",
                minYear=1920,
                maxYear=2023,
                invalidParameter=100,
            )
        self.assertEqual(
            str(context.exception),
            "The following parameters are outside the range of this program: {'invalidParameter'}",
        )

    def test_call_with_no_matching_data(self):
        """Test the query and data retrieval with no matching data"""

        # Create dataset
        dataset = EarthquakeDataset()

        # Query data
        data = dataset(
            country="Turkey",
            minDeaths=100,
            minEqDepth=0,
            minEqMagnitude=5,
            minYear=1998,
            maxDeaths=30000,
            maxYear=1998,
            maxEqDepth=20,
            maxEqMagnitude=9.9,
        )

        # Check if data type is correct
        self.assertIsInstance(data, list)

        # Check if earthquake list is empty
        self.assertEqual(len(data), 0)
