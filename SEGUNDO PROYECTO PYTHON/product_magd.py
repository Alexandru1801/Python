import sqlite3
from stock_magd import StockMovement

class Product:
    """Represents a product item and handles persistence operations.

    Parameters:
        conn (sqlite3.Connection): an open database connection.
        sku (int): unique product SKU.
        name (str): product name.
        category (str): product category.
        unit_price (float): price per unit.
        quantity (int): number of units in stock.
        rating (int): product rating.
    """

    def __init__(self, conn,
                sku = None,
                name = None,
                category = None,
                unit_price = None,
                quantity = None,
                rating = None):
        conn.row_factory = sqlite3.Row
        self.__conn = conn
        self.__cur = conn.cursor()
        self.sku = sku
        self.name = name
        self.category = category
        self.unitPrice = unit_price
        self.quantity = quantity
        self.rating = rating


    def __repr__(self):
        return f"\nSKU: {self.sku:4} | {self.name:12} | {self.category:10} | Price: {self.unitPrice:>5} | Qty: {self.quantity:>4} | Rating: {self.rating}"


    def loadProductsFromFile(self, filename):
        """
        Take the CSV file and prepare the data to be
        inserted into the database.
        """
        productsData = []
        try:
            productFile = open(filename, encoding='utf-8')

            for line in productFile:
                    data = line.strip().split(",")
                    cleaned = []
                    for elem in data:
                        elem = elem.strip()
                        if elem == "":
                            elem = None
                        cleaned.append(elem)
                    productsData.append(cleaned)
            productFile.close()
        except FileNotFoundError:
            raise FileNotFoundError(f"The file {filename} was not found")
        return productsData


    def insert(self, filename):
        """
        Insert the data retrived by the previous method
        into the database.
        """
        try:
            productData = self.loadProductsFromFile(filename)
            if not productData:
                raise ValueError("No data found in file")

            sql = """INSERT OR REPLACE INTO product(SKU, name, category, unit_price, quantity, rating)
                    VALUES (?,?,?,?,?,?)"""
            for row in productData:
                if len(row) < 6 or not row[0]:
                    raise ValueError("Missing fields in row")
                self.__cur.execute(sql, row)
            self.__conn.commit()
            print("The data has been inserted correctly")
            
        except FileNotFoundError:
            raise FileNotFoundError(f"The file {filename} was not found")
        except sqlite3.Error as e:
            self.__conn.rollback()
            raise ValueError(f"Database error: {e}")


    def load(self):
        """
        Fill the object with a product from the database
        where the SKU matches.
        """
        if self.sku == None:
            raise LookupError('Load: a valid SKU must be provided.')
        try:
            sql = """SELECT SKU, name, category, unit_price, quantity, rating
                    FROM product
                    WHERE SKU = ?"""
            params = (self.sku,)
            self.__cur.execute(sql, params)
            row = self.__cur.fetchone()
            self.name = row["name"]
            self.category = row["category"]
            self.unitPrice = row["unit_price"]
            self.quantity = row["quantity"]
            self.rating = row["rating"]
            print("The object has been filled correctly")
        except sqlite3.Error:
            raise LookupError('Load: an error occurred while fetching the product.')


    def update(self):
        """
        Updates the record from the database where the
        SKU matches.
        """
        if self.sku == None:
            raise LookupError('Load: a valid SKU must be provided.')

        sql = """UPDATE product
                SET name = ?,
                    category = ?,
                    unit_price = ?,
                    quantity = ?,
                    rating = ?
                WHERE sku = ?"""
        params = (
            self.name,
            self.category,
            self.unitPrice,
            self.quantity,
            self.rating,
            self.sku,
        )

        try:
            self.__cur.execute(sql, params)
            self.__conn.commit()
        except sqlite3.IntegrityError:
            print(f"Database integrity error")
        except sqlite3.Error:
            print(f"Database error")


    def delete(self):
        """
        Delet the record from the database where the SKU
        matches.
        """
        sql = """DELETE FROM product
                WHERE SKU = ?"""
        params = (self.sku,)
        self.__cur.execute(sql, params)
        self.__conn.commit()


    def change_quantity(self, new_quantity, supplier_id=None):
        """
        Update the product quantity and record a stock movement.

        supplier_id can be None if the change is not associated with a
        specific supplier.
        """
        if self.sku is None:
            raise LookupError('Change quantity: a valid SKU must be provided.')

        if self.quantity is None:
            self.load()

        old_quantity = self.quantity
        self.quantity = new_quantity

        sql = """UPDATE product
                SET quantity = ?
                WHERE SKU = ?"""
        params = (self.quantity, self.sku)
        self.__cur.execute(sql, params)
        self.__conn.commit()

        StockMovement.record_change(self.__conn, self.sku, supplier_id, old_quantity, self.quantity)