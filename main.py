import matplotlib
import math
from matplotlib import pyplot as plt

from data import EarthquakeDataset

if __name__ == "__main__":

    dataset = EarthquakeDataset()

    # Get earthquakes from 1920 to 2023 with a magnitude of at least 4.0

    earthquakes = dataset(
        minYear=1920,
        maxYear=2023,
        minEqMagnitude=4.0,
    )

    # Filter earthquakes with no deaths
    earthquakes = [earthquake for earthquake in earthquakes if earthquake.deaths > 0]

    # Plot number of deaths opposed to magnitude

    plt.scatter(
        [earthquake.eqMagnitude for earthquake in earthquakes],
        [math.log10(earthquake.deaths) for earthquake in earthquakes],
        marker=matplotlib.markers.CARETDOWNBASE,
        s=1,
        color="red",
    )
    plt.xlabel("Magnitude")
    plt.ylabel("Deaths (log10)")

    # Write the name of the country next to the earthquake if it is the deatlhliest earthquake with that magnitude
    
    # Divide the earthquakes into groups with 0.1 difference in magnitude
    earthquake_groups = {}
    for earthquake in earthquakes:
        magnitude = earthquake.eqMagnitude
        magnitude = magnitude - magnitude % 0.1
        if magnitude not in earthquake_groups:
            earthquake_groups[magnitude] = []
        earthquake_groups[magnitude].append(earthquake)
    
    # Get the earthquake with the most deaths in each group
    earthquake_groups = {
        magnitude: max(earthquake_group, key=lambda earthquake: earthquake.deaths)
        for magnitude, earthquake_group in earthquake_groups.items()
    }

    # Write the name of the country next to the earthquake if it is the deatlhliest earthquake with that magnitude
    for earthquake in earthquake_groups.values():
        plt.text(
            earthquake.eqMagnitude,
            math.log10(earthquake.deaths),
            earthquake.country,
            fontsize=6,
        )

    plt.show()
