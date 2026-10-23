from product_magd import Product
import sqlite3

class productManager:
    """Handles collections of Product objects retrieved from the database
    according to given criteria.

    conn (db connection): a SQL database connection.
    """

    def __init__(self, conn):
        conn.row_factory = sqlite3.Row
        self._conn = conn
        self._cur = conn.cursor()


    def __convertToTupple(self, data):
        '''Take a collection of data and return a text string
        wrapping the same data between parenthesis (comma separated).

        data (list, set): a collection of data.

        Output (str): Given data between parenthesis.
        '''
        if isinstance(data, (list, set, tuple)):
            return tuple(data)
        return (data,)


    def __getProductsList(self, rows):
        """
        Transform the given records from the database into Product objects
        and return them into a list.
        """
        result = []
        for product in rows:
            myProduct = Product(
                self._conn,
                product["sku"],
                product["name"],
                product["category"],
                product["unit_price"],
                product["quantity"],
                product["rating"]
            )
            result.append(myProduct)
        return result


    def getBySku(self, skus):
        """
        Retrieve all Products objects according to a given collection of SKUs.

        skus (list, set, int): a collection of unique products SKUs.

        Output (list): a collection of Products objects matching given SKUs.
        """
        params = self.__convertToTupple(skus)
        placeholders = ', '.join(['?'] * len(params))
        sql = f"""SELECT SKU, name, category, unit_price, quantity, rating 
                FROM product
                WHERE SKU IN ({placeholders}) 
                ORDER BY SKU"""
        self._cur.execute(sql, params)
        rows = self._cur.fetchall()
        return self.__getProductsList(rows)


    def getByName(self, name_part):
        """
        Retrieve all Products objects according to a given complete name or part of it.

        name_part (str): a complete name or a part of it.

        Output (list): a collection of Products objects matching given name.
        """
        sql = """SELECT SKU, name, category, unit_price, quantity, rating 
                FROM product
                WHERE name LIKE ? 
                ORDER BY name"""
        params = (f"%{name_part}%",)
        self._cur.execute(sql, params)
        rows = self._cur.fetchall()
        return self.__getProductsList(rows)


    def getByCategory(self, category):
        """
        Retrieve all Products objects according to a given category.

        category (str): a category of a product or products

        Output (list): a collection of Products objects matching given category.
        """
        sql = """SELECT SKU, name, category, unit_price, quantity, rating 
                FROM product
                WHERE category = ? 
                ORDER BY SKU"""
        params = self.__convertToTupple(category)
        self._cur.execute(sql, params)
        rows = self._cur.fetchall()
        return self.__getProductsList(rows)


    def getByPrice(self, min_price, max_price):
        """
        Retrieve all Products objects between two prices.

        min_price (int): lower price
        max_price (int): maximum prise

        Output (list): a collection of Products objects matching given price range.
        """
        sql = """SELECT SKU, name, category, unit_price, quantity, rating 
                FROM product
                WHERE unit_price BETWEEN ? AND ?
                ORDER BY unit_price DESC"""
        params = (min_price, max_price)
        self._cur.execute(sql, params)
        rows = self._cur.fetchall()
        return self.__getProductsList(rows)


    def getByStockThreshold(self, threshold, above = True):
        """
        Retrieve all Products objects that are above or bellow the given
        stock threshold.

        threshold (int): the given threshold
        above (bool): the value to indicate if you want to search above or 
        bellow the given threshold (default: above)

        Output (list): a collection of Products objects matching given threshold.
        """
        if above:
            sql = """SELECT SKU, name, category, unit_price, quantity, rating
                    FROM product
                    WHERE quantity > ?"""
        else:
            sql = """SELECT SKU, name, category, unit_price, quantity, rating
                    FROM product
                    WHERE quantity < ?"""
        params = (threshold,)
        self._cur.execute(sql, params)
        rows = self._cur.fetchall()
        return self.__getProductsList(rows)


    def getByRatingThreshold(self, threshold, above = True):
        """
        Retrieve all Products objects that are above or bellow the given
        rating threshold.

        threshold (int): the given threshold
        above (bool): the value to indicate if you want to search above or 
        bellow the given threshold (default: above)

        Output (list): a collection of Products objects matching given threshold.
        """
        if above:
            sql = """SELECT SKU, name, category, unit_price, quantity, rating
                    FROM product
                    WHERE rating > ?"""
        else:
            sql = """SELECT SKU, name, category, unit_price, quantity, rating
                    FROM product
                    WHERE rating < ?"""
        params = (threshold,)
        self._cur.execute(sql, params)
        rows = self._cur.fetchall()
        return self.__getProductsList(rows)