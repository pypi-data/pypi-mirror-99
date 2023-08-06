import os
import unittest
from lcbuilder.lcbuilder_class import LcBuilder
from lcbuilder.objectinfo.InputObjectInfo import InputObjectInfo
from lcbuilder.objectinfo.MissionFfiCoordsObjectInfo import MissionFfiCoordsObjectInfo
from lcbuilder.objectinfo.MissionFfiIdObjectInfo import MissionFfiIdObjectInfo
from lcbuilder.objectinfo.MissionInputObjectInfo import MissionInputObjectInfo
from lcbuilder.objectinfo.MissionObjectInfo import MissionObjectInfo


class TestsLcBuilder(unittest.TestCase):
    def test_short_cadence(self):
        lc, lc_data, star_info, transits_min_count, sectors, quarters = \
            LcBuilder().build(MissionObjectInfo("TIC 352315023", 'all'), "./")
        self.assertGreater(len(lc), 0)
        self.__test_star_params(star_info)


    def test_long_cadence(self):
        lc, lc_data, star_info, transits_min_count, sectors, quarters = \
            LcBuilder().build(MissionFfiIdObjectInfo("TIC 352315023", 'all'), "./")
        self.assertGreater(len(lc), 0)
        self.__test_star_params(star_info)

    def test_long_cadence_coords(self):
        lc, lc_data, star_info, transits_min_count, sectors, quarters =\
            LcBuilder().build(MissionFfiCoordsObjectInfo(300.47, -71.96, 'all'), "./")
        self.assertGreater(len(lc), 0)
        self.__test_star_params(star_info)

    def test_input_with_id(self):
        directory = os.path.dirname(__file__) + "/input.csv"
        lc, lc_data, star_info, transits_min_count, sectors, quarters = \
            LcBuilder().build(MissionInputObjectInfo("TIC 352315023", directory), "./")
        self.assertGreater(len(lc), 0)
        self.__test_star_params(star_info)

    def test_input_without_id(self):
        directory = os.path.dirname(__file__) + "/input.csv"
        lc, lc_data, star_info, transits_min_count, sectors, quarters = \
            LcBuilder().build(InputObjectInfo(directory), "./")
        self.assertGreater(len(lc), 0)
        self.assertTrue(star_info.mass_assumed)
        self.assertTrue(star_info.radius_assumed)

    def __test_star_params(self, star_info):
        self.assertAlmostEqual(star_info.mass, 0.47, 1)
        self.assertAlmostEqual(star_info.mass_min, 0.44, 2)
        self.assertAlmostEqual(star_info.mass_max, 0.5, 1)
        self.assertAlmostEqual(star_info.radius, 0.18, 1)
        self.assertAlmostEqual(star_info.radius_min, 0.076, 3)
        self.assertAlmostEqual(star_info.radius_max, 0.284, 3)
        self.assertEqual(star_info.teff, 31000)
        self.assertAlmostEqual(star_info.ra, 300.47, 2)
        self.assertAlmostEqual(star_info.dec, -71.96, 2)


if __name__ == '__main__':
    unittest.main()
