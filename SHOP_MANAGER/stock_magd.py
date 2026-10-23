from datetime import datetime
import sqlite3

class StockMovement:
    """
    Represents a single stock movement record.
    """

    def __init__(self, conn, stock_id=None, sku=None, supplier_id=None, date=None, old_qty=None, new_qty=None):
        conn.row_factory = sqlite3.Row
        self._conn = conn
        self._cur = conn.cursor()
        self.stock_id = stock_id
        self.sku = sku
        self.supplier_id = supplier_id
        self.date = date
        self.old_qty = old_qty
        self.new_qty = new_qty


    def __repr__(self):
        return (f"StockMovement(stock_id={self.stock_id}, sku={self.sku}, supplier_id={self.supplier_id}, "
                f"date={self.date!r}, old_qty={self.old_qty}, new_qty={self.new_qty})")


    @classmethod
    def from_row(StockMovement, conn, row):
        if row is None:
            return None
        return StockMovement(
            conn,
            stock_id=row["stockId"],
            sku=row["SKU"],
            supplier_id=row["supplier_id"],
            date=row["date"],
            old_qty=row["oldQty"],
            new_qty=row["newQty"]
        )


    @classmethod
    def record_change(StockMovement, conn, sku, supplier_id, old_qty, new_qty, date=None):
        """
        Insert a new stock movement record for a quantity change.
        Returns the stockId of the newly created record.
        """
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cur = conn.cursor()
        sql = """INSERT INTO stockMovement (SKU, supplier_id, date, oldQty, newQty)
                VALUES (?, ?, ?, ?, ?)"""
        params = (sku, supplier_id, date, old_qty, new_qty)
        cur.execute(sql, params)
        conn.commit()
        return cur.lastrowid