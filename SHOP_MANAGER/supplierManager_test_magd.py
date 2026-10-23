import unittest
import sqlite3
from supplier_magd import Supplier
from supplierManager_magd import supplierManager

class TestSupplierManager(unittest.TestCase):

    def setUp(self):
        self.conn = sqlite3.connect(':memory:')
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()
        
        self.cur.execute("""
            CREATE TABLE supplier (
                company_id INTEGER PRIMARY KEY,
                name TEXT, email TEXT, contact_person TEXT, 
                phone TEXT, region TEXT, country TEXT, address TEXT
            )
        """)
        
        self.cur.execute("INSERT INTO supplier VALUES (1, 'Logitech', 'info@logitech.com', 'Jose Perez', '111222', 'Europe', 'Switzerland', 'Morges')")
        self.cur.execute("INSERT INTO supplier VALUES (2, 'EcoSupplies', 'contact@eco.com', 'Maria Garcia', '333444', 'America', 'USA', 'New York')")
        self.conn.commit()
        
        self.manager = supplierManager(self.conn)


    def tearDown(self):
        self.conn.close()



    def test_getByCompanyId_returnsCorrectObject(self):
        # GIVEN
        company_id = 1

        # WHEN
        results = self.manager.getByCompanyId(company_id)

        # THEN
        self.assertEqual(len(results), 1)
        self.assertIsInstance(results[0], Supplier)
        self.assertEqual(results[0].name, 'Logitech')


    def test_getByName_returnsMatches(self):
        # GIVEN
        search_term = "Logi"

        # WHEN
        results = self.manager.getByName(search_term)

        # THEN
        self.assertEqual(len(results), 1)
        self.assertIn("Logitech", results[0].name)


    def test_getByEmail_returnsExactMatch(self):
        # GIVEN
        email_to_find = "contact@eco.com"

        # WHEN
        results = self.manager.getByEmail(email_to_find)

        # THEN
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].company_id, 2)


    def test_getByContactPerson_partialMatch(self):
        # GIVEN
        contact_fragment = "Maria"

        # WHEN
        results = self.manager.getByContactPerson(contact_fragment)

        # THEN
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].contactPerson, "Maria Garcia")


    def test_getByPhone_noMatchReturnsEmptyList(self):
        # GIVEN
        # Un teléfono que sabemos que no existe en nuestra DB de prueba
        fake_phone = '999999999'

        # WHEN
        results = self.manager.getByPhone(fake_phone)

        # THEN
        self.assertEqual(len(results), 0)
        self.assertIsInstance(results, list)


    def test_getByRegion_returnsCorrectList(self):
        # GIVEN
        region_name = "Europe"

        # WHEN
        results = self.manager.getByRegion(region_name)

        # THEN
        self.assertGreaterEqual(len(results), 1)
        self.assertEqual(results[0].region, "Europe")


    def test_getByCountry_nonExistentReturnsEmpty(self):
        # GIVEN
        country_name = "Mars"

        # WHEN
        results = self.manager.getByCountry(country_name)

        # THEN
        self.assertEqual(len(results), 0)
        self.assertIsInstance(results, list)


    def test_getByAddress_returnsCorrectSupplier(self):
        # GIVEN
        # La dirección que insertamos en el setUp para EcoSupplies
        address_to_find = 'New York'

        # WHEN
        results = self.manager.getByAddress(address_to_find)

        # THEN
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].company_id, 2)
        self.assertEqual(results[0].address, 'New York')

if __name__ == '__main__':
    unittest.main()