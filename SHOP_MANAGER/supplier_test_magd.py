import unittest
import sqlite3

from inventoryDbManager_magd import InventoryDbManager
from supplier_magd import Supplier


class SupplierTest(unittest.TestCase):

    def setUp(self):
        self.conn = sqlite3.connect(':memory:')
        self.conn.row_factory = sqlite3.Row
        self.dbHandler = InventoryDbManager(self.conn)
        self.dbHandler.createInventoryDb()


    def tearDown(self):
        self.conn.close()


    def test_SupplierConstructor_correctSupplierObject(self):
        #GIVEN
        new_supplier = Supplier(
            self.conn,
            873681,
            "EcoSupplier",
            "eco@email.com",
            "John Smith",
            "123456789",
            "Europe",
            "Spain",
            "Madrid"
        )

        #WHEN

        #THEN
        self.assertIsNotNone(new_supplier)
        self.assertIsInstance(new_supplier, Supplier)
        self.assertEqual(new_supplier.company_id, 873681)
        self.assertEqual(new_supplier.name, "EcoSupplier")
        self.assertEqual(new_supplier.email, "eco@email.com")
        self.assertEqual(new_supplier.contactPerson, "John Smith")
        self.assertEqual(new_supplier.phone, "123456789")
        self.assertEqual(new_supplier.region, "Europe")
        self.assertEqual(new_supplier.country, "Spain")
        self.assertEqual(new_supplier.address, "Madrid")


    def test_loadSuppliersFromFile_correctCollectionSuppliers(self):
        #GIVEN
        filename = "SupplierData.csv"

        #WHEN
        supplier_rows = Supplier(self.conn).loadSuppliersFromFile(filename)

        #THEN
        self.assertIsNotNone(supplier_rows)
        self.assertIsInstance(supplier_rows, list)
        self.assertGreaterEqual(len(supplier_rows), 1)

        for row in supplier_rows:
            self.assertIsInstance(row, list)
            self.assertEqual(len(row), 8)

            for item in row:
                self.assertTrue(isinstance(item, str) or item is None)


    def test_loadSuppliersFromFile_nonExistentFile(self):
        #GIVEN
        filename = "non_existent_file.csv"

        #WHEN/THEN
        with self.assertRaises(FileNotFoundError):
            Supplier(self.conn).loadSuppliersFromFile(filename)


    def test_insertSupplier(self):
        #GIVEN
        supplier = Supplier(self.conn)
        filename = "SupplierData.csv"

        #WHEN
        supplier.insert(filename)

        #THEN
        row = self.conn.execute("""
            SELECT *
            FROM supplier
            WHERE company_id = 873681
        """).fetchone()

        self.assertIsNotNone(row)
        self.assertEqual(row["name"], "EcoSupplier")


    def test_load_correctlyFillsObject(self):
        #GIVEN
        self.conn.execute("""
            INSERT INTO supplier
            VALUES (
                873681,
                'EcoSupplier',
                'eco@email.com',
                'John Smith',
                '123456789',
                'Europe',
                'Spain',
                'Madrid'
            )
        """)

        supplier = Supplier(self.conn, company_id=873681)

        #WHEN
        supplier.load()

        #THEN
        self.assertEqual(supplier.name, "EcoSupplier")
        self.assertEqual(supplier.country, "Spain")


    def test_load_missingCompanyIdRaisesError(self):
        #GIVEN
        supplier = Supplier(self.conn)

        #WHEN/THEN
        with self.assertRaises(LookupError):
            supplier.load()


    def test_update_modifiesExistingRecord(self):
        #GIVEN
        self.conn.execute("""
            INSERT INTO supplier
            VALUES (
                873681,
                'EcoSupplier',
                'eco@email.com',
                'John Smith',
                '123456789',
                'Europe',
                'Spain',
                'Madrid'
            )
        """)

        supplier = Supplier(
            self.conn,
            company_id=873681,
            name="GreenWorld",
            email="green@email.com",
            contact_person="Maria Perez",
            phone="999999999",
            region="America",
            country="USA",
            address="New York"
        )

        #WHEN
        supplier.update()

        #THEN
        row = self.conn.execute("""
            SELECT name
            FROM supplier
            WHERE company_id = 873681
        """).fetchone()

        self.assertEqual(row["name"], "GreenWorld")


    def test_delete_removesRecord(self):
        #GIVEN
        self.conn.execute("""
            INSERT INTO supplier
            VALUES (
                873681,
                'EcoSupplier',
                'eco@email.com',
                'John Smith',
                '123456789',
                'Europe',
                'Spain',
                'Madrid'
            )
        """)

        supplier = Supplier(self.conn, company_id=873681)

        #WHEN
        supplier.delete()

        #THEN
        row = self.conn.execute("""
            SELECT *
            FROM supplier
            WHERE company_id = 873681
        """).fetchone()

        self.assertIsNone(row)


if __name__ == '__main__':
    unittest.main()