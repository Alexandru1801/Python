import unittest
import sqlite3
from stock_magd import StockMovement
from stockManager_magd import StockMovementManager
from inventoryDbManager_magd import InventoryDbManager


class TestStockMovementManager(unittest.TestCase):

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
            INSERT INTO product
            VALUES (1234, 'Orange', 'Fruit', 2, 100, 9)
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

        self.cur.execute("""
            INSERT INTO supplier
            VALUES (
                999999,
                'GreenWorld',
                'green@email.com',
                'Alice Brown',
                '987654321',
                'America',
                'USA',
                'New York'
            )
        """)
        self.conn.commit()

        StockMovement.record_change(
            self.conn,
            7493,
            873681,
            50,
            100,
            "2025-01-01"
        )

        StockMovement.record_change(
            self.conn,
            1234,
            999999,
            100,
            120,
            "2025-01-02"
        )

        StockMovement.record_change(
            self.conn,
            7493,
            873681,
            100,
            80,
            "2025-01-03"
        )

        self.manager = StockMovementManager(self.conn)


    def tearDown(self):
        self.conn.close()



    def test_get_by_product(self):
        #WHEN
        history = self.manager.getByProduct(7493)

        #THEN
        self.assertEqual(len(history), 2)
        for movement in history:
            self.assertEqual(movement.sku, 7493)


    def test_get_by_supplier(self):
        # WHEN
        history = self.manager.getBySupplier(873681)

        #THEN
        self.assertEqual(len(history), 2)
        for movement in history:
            self.assertEqual(movement.supplier_id, 873681)


    def test_get_by_date(self):
        #WHEN
        history = self.manager.getByDate("2025-01-02")

        #THEN
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0].date, "2025-01-02")


    def test_get_history_by_product(self):
        #WHEN
        history = self.manager.getHistory(sku=7493)

        #THEN
        self.assertEqual(len(history), 2)
        for movement in history:
            self.assertEqual(movement.sku, 7493)


    def test_get_history_by_supplier(self):
        #WHEN
        history = self.manager.getHistory(supplier_id=999999)

        #THEN
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0].supplier_id, 999999)


    def test_get_history_by_date_range(self):
        #WHEN
        history = self.manager.getHistory(
            start_date="2025-01-01",
            end_date="2025-01-02"
        )

        #THEN
        self.assertEqual(len(history), 2)


    def test_get_history_combined_filters(self):
        #WHEN
        history = self.manager.getHistory(
            sku=7493,
            supplier_id=873681,
            start_date="2025-01-01",
            end_date="2025-01-03"
        )

        #THEN
        self.assertEqual(len(history), 2)

        for movement in history:
            self.assertEqual(movement.sku, 7493)
            self.assertEqual(movement.supplier_id, 873681)


if __name__ == "__main__":
    unittest.main()