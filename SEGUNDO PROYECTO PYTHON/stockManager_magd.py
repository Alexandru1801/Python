import sqlite3
from stock_magd import StockMovement

class StockMovementManager:
    """Query stock movement history using flexible criteria."""

    def __init__(self, conn):
        conn.row_factory = sqlite3.Row
        self._conn = conn
        self._cur = conn.cursor()


    def __getStockMovementList(self, rows):
        """
        Helper method to convert query results into a list of StockMovement objects.
        """
        history = []
        for row in rows:
            history.append(StockMovement.from_row(self._conn, row))
        return history


    def getByProduct(self, sku):
        """
        Return stock movement history for a specific product SKU.

        sku (int): The SKU of the product to filter by.

        Output: A list of StockMovement objects representing the movement history for the specified SKU, ordered by date.
        """
        sql = """SELECT stockId, SKU, supplier_id, date, oldQty, newQty
                FROM stockMovement
                WHERE SKU = ?
                ORDER BY date"""
        self._cur.execute(sql, (sku,))
        return self.__getStockMovementList(self._cur.fetchall())


    def getBySupplier(self, supplier_id):
        """
        Return stock movement history for a specific supplier.

        supplier_id (int): The ID of the supplier to filter by.

        Output: A list of StockMovement objects representing the movement history for the specified supplier, ordered by date.
        """
        sql = """SELECT stockId, SKU, supplier_id, date, oldQty, newQty
                FROM stockMovement
                WHERE supplier_id = ?
                ORDER BY date"""
        self._cur.execute(sql, (supplier_id,))
        return self.__getStockMovementList(self._cur.fetchall())


    def getByDate(self, date):
        """
        Return stock movements recorded on a specific date.

        date (str): The date to filter by, in 'YYYY-MM-DD' format.

        Output: A list of StockMovement objects representing the movements recorded on the specified date, ordered by stockId.
        """
        sql = """SELECT stockId, SKU, supplier_id, date, oldQty, newQty
                FROM stockMovement
                WHERE date = ?
                ORDER BY stockId"""
        self._cur.execute(sql, (date,))
        return self.__getStockMovementList(self._cur.fetchall())


    def getHistory(self, sku=None, supplier_id=None, start_date=None, end_date=None):
        """
        Flexible history search by product, supplier and/or date range.
        All parameters are optional. 
        If multiple parameters are provided, only matching movements will be returned.
        """
        criteria = []
        params = []
        sql = """SELECT stockId, SKU, supplier_id, date, oldQty, newQty
                FROM stockMovement"""

        if sku is not None:
            criteria.append("SKU = ?")
            params.append(sku)
        if supplier_id is not None:
            criteria.append("supplier_id = ?")
            params.append(supplier_id)
        if start_date is not None and end_date is not None:
            criteria.append("date BETWEEN ? AND ?")
            params.extend([start_date, end_date])
        elif start_date is not None:
            criteria.append("date >= ?")
            params.append(start_date)
        elif end_date is not None:
            criteria.append("date <= ?")
            params.append(end_date)

        if criteria:
            sql += "\n WHERE " + " AND ".join(criteria)

        sql += "\n ORDER BY date, stockId"
        self._cur.execute(sql, tuple(params))
        return self.__getStockMovementList(self._cur.fetchall())