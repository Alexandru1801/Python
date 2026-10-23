import unittest
import sqlite3
from product_magd import Product
from productManager_magd import productManager

class ProductManagerTest(unittest.TestCase):

    def setUp(self):
        self.conn = sqlite3.connect(':memory:')
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()
        
        self.cur.execute("""
            CREATE TABLE product (
                SKU TEXT PRIMARY KEY,
                name TEXT,
                category TEXT,
                unit_price REAL,
                quantity INTEGER,
                rating INTEGER
            )
        """)
        self.test_data = [
            ('12345', 'Orange', 'Fruit', 1.50, 100, 8),
            ('4321', 'Watermelon', 'Fruit', 3.0, 500, 7),
            ('7493', 'Keyboard', 'Periferics', 10.0, 110, 8),
            ('9606', 'Iron-Man', 'Figure', 50.0, 10, 10),
            ('7491', 'Mouse', 'Periferics', 10.0, 50, 8)
        ]
        self.cur.executemany("INSERT INTO product VALUES (?,?,?,?,?,?)", self.test_data)
        self.conn.commit()
        self.manager = productManager(self.conn)


    def tearDown(self):
        self.conn.close()


    def test_getBySku_retrievesMultipleProducts(self):
        # GIVEN
        skus_to_search = ['12345', '4321']

        # WHEN
        results = self.manager.getBySku(skus_to_search)

        # THEN
        self.assertIsNotNone(results)
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].sku, '12345')
        self.assertEqual(results[1].sku, '4321')


    def test_getByName_findsSpecificProduct(self):
        # GIVEN
        search_term = "Iron"

        # WHEN
        results = self.manager.getByName(search_term)

        # THEN
        self.assertIsNotNone(results)
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "Iron-Man")
        self.assertEqual(results[0].sku, "9606")


    def test_getByCategory_groupsCorrectly(self):
        # GIVEN
        category_name = "Peripherals"

        # WHEN
        results = self.manager.getByCategory(category_name)

        # THEN
        self.assertIsNotNone(results)
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].category, "Peripherals")
        self.assertEqual(results[1].category, "Peripherals")


    def test_getByPrice_filtersRange(self):
        # GIVEN
        min_price = 5.0 
        max_price = 15.0

        # WHEN
        results = self.manager.getByPrice(min_price, max_price)

        # THEN
        self.assertIsNotNone(results)
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].unitPrice, 10.0)


    def test_getByStockThreshold_aboveThreshold(self):
        # GIVEN
        threshold = 60
        is_above = True

        # WHEN
        results = self.manager.getByStockThreshold(threshold, is_above)

        # THEN
        self.assertIsNotNone(results)
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 3)


    def test_getByStockThreshold_bellowThreshold(self):
        # GIVEN
        threshold = 60
        is_above = False

        # WHEN
        results = self.manager.getByStockThreshold(threshold, is_above)

        # THEN
        self.assertIsNotNone(results)
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 2)


    def test_getByRatingThreshold_highRating(self):
        # GIVEN
        min_rating = 9
        is_above = True

        # WHEN
        results = self.manager.getByRatingThreshold(min_rating, is_above)

        # THEN
        self.assertIsNotNone(results)
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "Iron-Man")


    def test_getByRatingThreshold_lowRating(self):
        min_rating = 8
        is_above = False

        # WHEN
        results = self.manager.getByRatingThreshold(min_rating, is_above)

        # THEN
        self.assertIsNotNone(results)
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "Watermelon")


if __name__ == '__main__':
    unittest.main()