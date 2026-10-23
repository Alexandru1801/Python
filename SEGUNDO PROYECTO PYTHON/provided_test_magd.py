import unittest
import sqlite3
from provided_magd import Provided
from inventoryDbManager_magd import InventoryDbManager


class TestProvided(unittest.TestCase):

    def setUp(self):
        """
        Create a temporary in-memory database and insert test data.
        """
        self.conn = sqlite3.connect(":memory:")
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.conn.row_factory = sqlite3.Row
        db = InventoryDbManager(self.conn)
        db.createInventoryDb()
        self.cur = self.conn.cursor()


        #Insert test products
        self.cur.execute("""
            INSERT INTO product
            VALUES (7493, 'Keyboard', 'Peripherals', 10, 50, 8)
        """)
        self.cur.execute("""
            INSERT INTO product
            VALUES (1234, 'Orange', 'Fruit', 2, 100, 9)
        """)


        #Insert test suppliers
        self.cur.execute("""
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
        self.conn.commit()
        self.provided = Provided(self.conn)


    def tearDown(self):
        """
        Close the database connection after each test.
        """
        self.conn.close()


    def test_link_valid_relation(self):
        """
        Test creating a valid supplier-product relation.
        """
        #GIVEN
        self.provided.link(7493, 873681)

        #WHEN
        self.cur.execute("""
            SELECT * FROM provided
            WHERE SKU = 7493 AND company_id = 873681
        """)
        row = self.cur.fetchone()

        #THEN
        self.assertIsNotNone(row)


    def test_link_invalid_supplier(self):
        """
        Test linking with a non-existing supplier.
        """
        #WHEN/THEN
        with self.assertRaises(ValueError):
            self.provided.link(7493, 999999)


    def test_link_invalid_product(self):
        """
        Test linking with a non-existing product.
        """
        #WHEN/THEN
        with self.assertRaises(ValueError):
            self.provided.link(9999, 873681)



    def test_unlink_existing_relation(self):
        """
        Test deleting an existing relation.
        """
        #GIVEN
        self.provided.link(7493, 873681)
        self.provided.unlink(7493, 873681)

        #WHEN
        self.cur.execute("""
            SELECT * FROM provided
            WHERE SKU = 7493 AND company_id = 873681
        """)
        row = self.cur.fetchone()

        #THEN
        self.assertIsNone(row)


    def test_unlink_non_existing_relation(self):
        """
        Test deleting a non-existing relation.
        """
        #WHEN/THEN
        with self.assertRaises(ValueError):
            self.provided.unlink(7493, 873681)



    def test_get_suppliers(self):
        """
        Test retrieving suppliers for a product.
        """
        #GIVEN
        self.provided.link(7493, 873681)

        #WHEN
        suppliers = self.provided.getSuppliers(7493)

        #THEN
        self.assertIsNotNone(suppliers)
        self.assertIsInstance(suppliers, list)
        self.assertEqual(len(suppliers), 1)
        self.assertEqual(suppliers[0]["name"], "EcoSupplier")



    def test_get_products(self):
        """
        Test retrieving products for a supplier.
        """
        #GIVEN
        self.provided.link(7493, 873681)

        #WHEN
        products = self.provided.getProducts(873681)

        #THEN
        self.assertIsNotNone(products)
        self.assertIsInstance(products, list)
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0]["name"], "Keyboard")


if __name__ == "__main__":
    unittest.main()