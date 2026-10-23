import unittest
import sqlite3
from stock_magd import StockMovement
from inventoryDbManager_magd import InventoryDbManager


class TestStockMovement(unittest.TestCase):

    def setUp(self):

        self.conn = sqlite3.connect(":memory:")
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.conn.row_factory = sqlite3.Row
        db = InventoryDbManager(self.conn)
        db.createInventoryDb()
        self.cur = self.conn.cursor()

        self.cur.execute("""
            INSERT INTO product
            VALUES (7493, 'Keyboard', 'Peripherals', 10, 50, 8)
        """)

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


    def tearDown(self):
        self.conn.close()



    def test_from_row_valid_data(self):
        #GIVEN
        stock_id = StockMovement.record_change(
            self.conn,
            7493,
            873681,
            50,
            100
        )

        self.cur.execute("""
            SELECT * FROM stockMovement
            WHERE stockId = ?
        """, (stock_id,))
        row = self.cur.fetchone()

        #WHEN 
        movement = StockMovement.from_row(self.conn, row)

        #THEN
        self.assertIsNotNone(movement)
        self.assertIsInstance(movement, StockMovement)
        self.assertEqual(movement.stock_id, stock_id)
        self.assertEqual(movement.sku, 7493)
        self.assertEqual(movement.supplier_id, 873681)
        self.assertEqual(movement.old_qty, 50)
        self.assertEqual(movement.new_qty, 100)


    def test_from_row_none(self):
        #WHEN/THEN
        movement = StockMovement.from_row(self.conn, None)
        self.assertIsNone(movement)


    def test_recordChange_valid_stock_change(self):
        #WHEN
        stock_id = StockMovement.record_change(
            self.conn,
            7493,
            873681,
            50,
            100
        )

        #THEN
        self.cur.execute("""
            SELECT * FROM stockMovement
            WHERE stockId = ?
        """, (stock_id,))
        row = self.cur.fetchone()

        self.assertIsNotNone(row)
        self.assertEqual(row["SKU"], 7493)
        self.assertEqual(row["supplier_id"], 873681)


    def test_recordChange_invalid_product(self):
        #WHEN/THEN
        with self.assertRaises(sqlite3.IntegrityError):
            StockMovement.record_change(
                self.conn,
                9999,
                873681,
                50,
                100
            )


    def test_recordChange_invalid_supplier(self):
        #WHEN/THEN
        with self.assertRaises(sqlite3.IntegrityError):
            StockMovement.record_change(
                self.conn,
                7493,
                999999,
                50,
                100
            )


if __name__ == "__main__":
    unittest.main()