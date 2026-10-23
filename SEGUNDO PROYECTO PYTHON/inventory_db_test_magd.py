import unittest
import sqlite3
from inventoryDbManager_magd import InventoryDbManager

class InventoryDbManagerTest(unittest.TestCase):

    def setUp(self):
        self.conn = sqlite3.connect(':memory:')
        self.conn.row_factory = sqlite3.Row
        self.dbHandler = InventoryDbManager(self.conn)
        self.dbHandler.createInventoryDb()

    def tearDown(self):
        self.conn.close()


    def tableExists(self, table_name):
        cursor = self.conn.cursor()
        cursor.execute(
            """SELECT name
                        FROM sqlite_master
                        WHERE type='table' AND name=?""",
            (table_name,),
        )
        return cursor.fetchone() is not None


    def test_ProductTable(self):
        # THEN
        self.assertTrue(self.tableExists("product"))


    def test_SupplierTable(self):
        # THEN
        self.assertTrue(self.tableExists("supplier"))


    def test_ProvidedTable(self):
        # THEN
        self.assertTrue(self.tableExists("provided"))


    def test_StockMovementTable(self):
        # THEN
        self.assertTrue(self.tableExists("stockMovement"))


    def test_allTablesCreated(self):
        # GIVEN
        expected_tables = {"product", "supplier", "provided", "stockMovement"}
        # WHEN
        actual_tables = set()
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        for row in cursor.fetchall():
            actual_tables.add(row[0])
        # THEN
        self.assertTrue(expected_tables.issubset(actual_tables))


if __name__ == '__main__':
    unittest.main()