import sqlite3

class InventoryDbManager:
    """Creates and destroys the inventory in the database.

    The database includes products, suppliers, provided links, and stock
    movement tables.

    conn (sqlite3.Connection): an open database connection.
    """

    def __init__(self, conn):
        self.__conn = conn
        self.__cur = conn.cursor()


    def createProductTable(self):
        """
        Create the table to stores the product data
        (sku, name, category, etc...).
        Requires commit operation afterwards.
        """
        sql = """CREATE TABLE IF NOT EXISTS product(
            SKU INT PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            unit_price INT,
            quantity INT,
            rating INT
        )"""
        self.__cur.execute(sql)


    def createSupplierTable(self):
        """
        Create the table to stores the supliers data
        (company_id, name, contact_person, etc...).
        Requires commit operation afterwards.
        """
        sql = """CREATE TABLE IF NOT EXISTS supplier(
            company_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT,
            contact_person TEXT NOT NULL,
            phone TEXT,
            region TEXT,
            country TEXT,
            address TEXT
        )"""
        self.__cur.execute(sql)


    def createProvidedTable(self):
        """
        Create the table to store the provided products
        info data
        (sku_product and company_id).
        Requires commit operation afterwards.
        """
        sql = """CREATE TABLE IF NOT EXISTS provided(
            SKU INTEGER,
            company_id INTEGER,
            PRIMARY KEY (SKU, company_id),
            FOREIGN KEY (SKU) REFERENCES product(SKU),
            FOREIGN KEY (company_id) REFERENCES supplier(company_id)
        )"""
        self.__cur.execute(sql)


    def createStockMovementTable(self):
        """
        Create the table to store the stock movement data
        (date, old_qty, new_qty, etc...)
        Requires commit operation afterwards.
        """
        sql = """CREATE TABLE IF NOT EXISTS stockMovement(
            stockId INTEGER PRIMARY KEY AUTOINCREMENT,
            SKU INTEGER,
            supplier_id INTEGER,
            date DATE,
            oldQty INTEGER,
            newQty INTEGER,
            FOREIGN KEY (SKU) REFERENCES product(SKU),
            FOREIGN KEY (supplier_id) REFERENCES supplier(company_id)
        )"""
        self.__cur.execute(sql)


    def createInventoryDb(self):
        """
        Create the inventory database
        """
        self.createProductTable()
        self.createSupplierTable()
        self.createProvidedTable()
        self.createStockMovementTable()
        self.__conn.commit()



    def removeProductTable(self):
        """
        Removes the product table
        """
        sql = "DROP TABLE IF EXISTS product"
        self.__cur.execute(sql)


    def removeSupplierTable(self):
        """
        Removes the supplier table.
        """
        sql = "DROP TABLE IF EXISTS supplier"
        self.__cur.execute(sql)


    def removeProvidedTable(self):
        """
        Removes the provided table
        """
        sql = "DROP TABLE IF EXISTS provided"
        self.__cur.execute(sql)


    def removeStockMovementTable(self):
        """
        Removes the stock movement table
        """
        sql = "DROP TABLE IF EXISTS stockMovement"
        self.__cur.execute(sql)


    def removeInventoryDb(self):
        """
        Destroy the entire database
        """
        self.removeStockMovementTable()
        self.removeProvidedTable()
        self.removeSupplierTable()
        self.removeProductTable()
        self.__conn.commit()