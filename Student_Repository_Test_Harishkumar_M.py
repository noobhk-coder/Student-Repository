import unittest

from HW09_Harishkumar_M import University

class UniversityTest(unittest.TestCase):
    "This class will test the university for "
    def test_University(self):
        "Method to check the data of pretty table"

        stevens: University = University("Stevens_University_Repository")

        self.assertEqual(stevens._students["10115"].Student_table_data(), 
                        ('10115', 'Wyatt, X', ['CS 545', 'SSW 564', 'SSW 567','SSW 687']))
        self.assertEqual(stevens._students["11399"].Student_table_data(), ('11399', 'Cordova, I', ['SSW 540']))

        self.assertNotEqual(stevens._students["10115"].Student_table_data(), 
                            ('10115', 'Wyatt, X', []))
        self.assertNotEqual(stevens._students["11399"].Student_table_data(), ('11399', 'Darwin, C', ['CS 540']))

        self.assertEqual(stevens._instructor["98760"].Instructor_table_data(), ([['98760', 'Darwin, C', 'SYEN', 'SYS 800', 1],
                                                                 ['98760', 'Darwin, C', 'SYEN', 'SYS 750', 1],
                                                                 ['98760', 'Darwin, C', 'SYEN', 'SYS 611', 2],
                                                                 ['98760', 'Darwin, C', 'SYEN', 'SYS 645', 1]]))
        self.assertNotEqual(stevens._instructor["98765"].Instructor_table_data(), ([['98765', 'Einstein, A', 'SFEN', 'SSW 567', 4]]))


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)