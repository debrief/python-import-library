import unittest
import os

from unittest import TestCase
from Store.DataStoreModule import DataStore

FILE_PATH = os.path.dirname(__file__)
TEST_DATA_PATH = os.path.join(FILE_PATH, "sample_data")


class TestDataStorePopulate(TestCase):
    def setUp(self):
        self.sqlite = DataStore("", "", "", 0, ":memory:", db_type="sqlite")
        self.sqlite.initialise()

    def tearDown(self):
        pass

    def test_populate_reference(self):
        """Test whether CSVs successfully imported to SQLite"""

        # Check tables are created but empty
        with self.sqlite.session_scope() as session:
            nationalities = self.sqlite.getNationalities()
            platform_types = self.sqlite.getPlatformTypes()

        # There must be no entities at the beginning
        self.assertEqual(len(nationalities), 0)
        self.assertEqual(len(platform_types), 0)

        # Import CSVs to the related tables
        with self.sqlite.session_scope() as session:
            self.sqlite.populateReference(TEST_DATA_PATH)

        # Check tables filled with correct data
        with self.sqlite.session_scope() as session:
            nationalities = self.sqlite.getNationalities()
            platform_types = self.sqlite.getPlatformTypes()
            nationality_object = self.sqlite.searchNationality("UNITED KINGDOM")
            platform_type_object = self.sqlite.searchPlatformType("TYPE-1")

            # Check whether they are not empty anymore and filled with correct data
            self.assertNotEqual(len(nationalities), 0)
            self.assertNotEqual(len(platform_types), 0)

            self.assertIn(nationality_object.name, "UNITED KINGDOM")
            self.assertIn(platform_type_object.name, "TTYPE-1")

    def test_populate_metadata(self):
        # reference tables must be filled first
        with self.sqlite.session_scope() as session:
            self.sqlite.populateReference(TEST_DATA_PATH)

        # get all table values
        with self.sqlite.session_scope() as session:
            platforms = self.sqlite.getPlatforms()
            datafiles = self.sqlite.getDatafiles()
            sensors = self.sqlite.getSensors()

        # There must be no entities at the beginning
        self.assertEqual(len(platforms), 0)
        self.assertEqual(len(datafiles), 0)
        self.assertEqual(len(sensors), 0)

        # Import CSVs to the related tables
        with self.sqlite.session_scope() as session:
            self.sqlite.populateMetadata(TEST_DATA_PATH)

        with self.sqlite.session_scope() as session:
            platforms = self.sqlite.getPlatforms()
            datafiles = self.sqlite.getDatafiles()
            sensors = self.sqlite.getSensors()

            platform_object = self.sqlite.searchPlatform("PLATFORM-1")
            datafile_object = self.sqlite.searchDatafile("DATAFILE-1")
            sensor_object = self.sqlite.searchSensor("SENSOR-1")

            # Check whether they are not empty anymore and filled with correct data
            self.assertNotEqual(len(platforms), 0)
            self.assertNotEqual(len(datafiles), 0)
            self.assertNotEqual(len(sensors), 0)

            # The following assertions filter objects by foreign key ids and
            # compares values with the data from CSV

            # Platform Object: PLATFORM-1, UNITED KINGDOM, TYPE-1, PRIVACY-1
            nationality = (
                self.sqlite.session.query(self.sqlite.DBClasses.Nationality)
                .filter_by(nationality_id=platform_object.nationality_id)
                .first()
            )
            self.assertEqual(nationality.name, "UNITED KINGDOM")
            platform_type = (
                self.sqlite.session.query(self.sqlite.DBClasses.PlatformType)
                .filter_by(platformtype_id=platform_object.platformtype_id)
                .first()
            )
            self.assertEqual(platform_type.name, "TYPE-1")
            privacy = (
                self.sqlite.session.query(self.sqlite.DBClasses.Privacy)
                .filter_by(privacy_id=platform_object.privacy_id)
                .first()
            )
            self.assertEqual(privacy.name, "PRIVACY-1")

            # Datafile Object: DATAFILE-1, True, PRIVACY-1, DATAFILE-TYPE-1
            self.assertEqual(datafile_object.simulated, True)
            privacy = (
                self.sqlite.session.query(self.sqlite.DBClasses.Privacy)
                .filter_by(privacy_id=datafile_object.privacy_id)
                .first()
            )
            self.assertEqual(privacy.name, "PRIVACY-1")
            datafile_type = (
                self.sqlite.session.query(self.sqlite.DBClasses.DatafileType)
                .filter_by(datafiletype_id=datafile_object.datafiletype_id)
                .first()
            )
            self.assertEqual(datafile_type.name, "DATAFILE-TYPE-1")

            # Sensor Object: SENSOR-1, SENSOR-TYPE-1, PLATFORM-1
            sensor_type = (
                self.sqlite.session.query(self.sqlite.DBClasses.SensorType)
                .filter_by(sensortype_id=sensor_object.sensortype_id)
                .first()
            )
            self.assertEqual(sensor_type.name, "SENSOR-TYPE-1")
            platform = (
                self.sqlite.session.query(self.sqlite.DBClasses.Platform)
                .filter_by(platform_id=sensor_object.platform_id)
                .first()
            )
            self.assertEqual(platform.name, "PLATFORM-1")


if __name__ == "__main__":
    unittest.main()
