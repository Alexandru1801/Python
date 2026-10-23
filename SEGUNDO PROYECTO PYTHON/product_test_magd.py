import unittest
import sqlite3
from inventoryDbManager_magd import InventoryDbManager
from product_magd import Product
from productManager_magd import productManager

class ProductTest(unittest.TestCase):

    def setUp(self):
        self.conn = sqlite3.connect(':memory:')
        self.conn.row_factory = sqlite3.Row
        self.dbHandler = InventoryDbManager(self.conn)
        self.dbHandler.createInventoryDb()
        self.productManager = productManager(self.conn)



    def tearDown(self):
        self.conn.close()


    def test_ProductConstructor_correctProductObject(self):
        # GIVEN
        new_product = Product(
            self.conn,
            "12345",
            "Orange",
            "Fruit",
            1.50,
            100,
            8
        )

        # WHEN

        # THEN
        self.assertIsNotNone(new_product)
        self.assertIsInstance(new_product, Product)
        self.assertEqual(new_product.sku, "12345")
        self.assertEqual(new_product.name, "Orange")
        self.assertEqual(new_product.category, "Fruit")
        self.assertEqual(new_product.unitPrice, 1.50)
        self.assertEqual(new_product.quantity, 100)
        self.assertEqual(new_product.rating, 8)


    def test_loadProductFromFile_correctCollectionProducts(self):
        # GIVEN
        filename = "ProductsData.csv"
        product_rows = Product(self.conn).loadProductsFromFile(filename)

        # WHEN

        # THEN
        self.assertIsNotNone(product_rows)
        self.assertIsInstance(product_rows, list)
        self.assertGreaterEqual(len(product_rows), 1)
        for row in product_rows:
            self.assertIsInstance(row, list)
            self.assertEqual(len(row), 6)
            for item in row:
                self.assertTrue(isinstance(item, str) or item is None)


    def test_loadProductFromFile_nonExistentFile(self):
        # GIVEN
        filename = "non_existent_file.csv"

        # WHEN & THEN
        with self.assertRaises(FileNotFoundError):
            Product(self.conn).loadProductsFromFile(filename)


    def test_loadProductFromFile_nonExistentFile(self):
        # GIVEN
        filename = "non_existent_file.csv"

        # WHEN & THEN
        with self.assertRaises(FileNotFoundError):
            Product(self.conn).loadProductsFromFile(filename)


    def test_insertProduct(self):
        # GIVEN
        new_product = Product(self.conn)
        filename = "ProductsData.csv"

        # WHEN
        new_product.insert(filename)

        # THEN
        retrieved_product = self.productManager.getBySku("12345")
        self.assertEqual(len(retrieved_product), 1)
        self.assertEqual(retrieved_product[0].name, "Orange")


    def test_load_correctlyFillsObject(self):
        # GIVEN
        self.conn.execute("INSERT INTO product VALUES ('12345', 'Orange', 'Fruit', 1.50, 100, 8)")
        product = Product(self.conn, sku='12345')

        # WHEN
        product.load()

        # THEN
        self.assertEqual(product.name, "Orange")
        self.assertEqual(product.quantity, 100)


    def test_load_missingSkuRaisesError(self):
        # GIVEN
        product = Product(self.conn)

        # WHEN & THEN
        with self.assertRaises(LookupError):
            product.load()


    def test_update_modifiesExistingRecord(self):
        # GIVEN
        self.conn.execute("INSERT INTO product VALUES ('12345', 'Orange', 'Fruit', 1.50, 100, 8)")
        product = Product(self.conn, sku='12345', name='Strawberry', category='Fruit', unit_price=2.0, quantity=10, rating=5)

        # WHEN
        product.update()

        # THEN
        row = self.conn.execute("SELECT name FROM product WHERE SKU = '12345'").fetchone()
        self.assertEqual(row["name"], "Strawberry")


    def test_delete_removesRecord(self):
        # GIVEN
        self.conn.execute("INSERT INTO product VALUES ('12345', 'Orange', 'Fruit', 1.50, 100, 8)")
        product = Product(self.conn, sku='12345')

        # WHEN
        product.delete()

        # THEN
        row = self.conn.execute("SELECT * FROM product WHERE SKU = '12345'").fetchone()
        self.assertIsNone(row)


    def test_change_quantity_updatesDatabaseAndObject(self):
        # GIVEN
        self.conn.execute("INSERT INTO product VALUES ('12345', 'Orange', 'Fruit', 1.50, 100, 8)")
        product = Product(self.conn, sku='12345', quantity=100)
        new_qty = 150

        # WHEN
        product.change_quantity(new_qty)

        # THEN
        self.assertEqual(product.quantity, 150)
        row = self.conn.execute("SELECT quantity FROM product WHERE SKU = '12345'").fetchone()
        self.assertEqual(row["quantity"], 150)


    def test_change_quantity_recordsStockMovement(self):
        # GIVEN
        self.conn.execute("INSERT INTO product VALUES ('12345', 'Orange', 'Fruit', 1.50, 100, 8)")
        product = Product(self.conn, sku='12345', quantity=100)
        supplier_id = 873681

        # WHEN
        product.change_quantity(120, supplier_id)

        # THEN
        movement = self.conn.execute("SELECT * FROM stockMovement WHERE sku = '12345'").fetchone()
        self.assertIsNotNone(movement)
        self.assertEqual(movement["oldQty"], 100)
        self.assertEqual(movement["newQty"], 120)
        self.assertEqual(movement["supplier_id"], supplier_id)


if __name__ == '__main__':
    unittest.main()