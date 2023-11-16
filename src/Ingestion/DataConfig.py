import os

# Config class for data ingestion either raw or reduced for performance testing
class DataConfig:
    USE_REDUCED_DATA = True

    BASE_DIRECTORY = os.path.abspath(os.path.dirname(__file__))

    PATHS = {
        "airports": {
            True: os.path.join(BASE_DIRECTORY, "../../Reduced_Data", "reducedAirports.csv"),
            False: os.path.join(BASE_DIRECTORY, "../../Raw_Data", "airports.csv")
        },
        "airlines": {
            True: os.path.join(BASE_DIRECTORY, "../../Reduced_Data", "reducedAirlines.csv"),
            False: os.path.join(BASE_DIRECTORY, "../../Raw_Data", "airlines.csv")
        },
        "routes": {
            True: os.path.join(BASE_DIRECTORY, "../../Reduced_Data", "reducedRoutes.csv"),
            False: os.path.join(BASE_DIRECTORY, "../../Raw_Data", "routes.csv")
        }
    }

    @classmethod
    def get_path(cls, name):
        return cls.PATHS[name][cls.USE_REDUCED_DATA]