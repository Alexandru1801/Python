import sqlite3

class Provided:
    """
    Handles the many-to-many supplier/product link table.

    The Provided manager inserts and removes links between products and
    suppliers, and retrieves suppliers for a product or products for a supplier.
    """

    def __init__(self, conn):
        conn.row_factory = sqlite3.Row
        self._conn = conn
        self._cur = conn.cursor()
        self._cur.execute("PRAGMA foreign_keys = ON")


    def link(self, product_sku, company_id):
        """
        Create an association between a product and a supplier.

        product_sku (int): the SKU of the product to link.
        company_id (int): the supplier company ID.
        """
        if company_id == None or product_sku == None:
            raise ValueError("You must give valid id for both")
        
        sql = """INSERT INTO provided(
                SKU, company_id)
                VALUES (?,?)"""
        try:
            params = (product_sku, company_id)
            self._cur.execute(sql, params)
            self._conn.commit()
        except sqlite3.IntegrityError:
            raise ValueError("Supplier or product does not exist")


    def unlink(self, product_sku, supplier_id):
        """
        Remove the association between a supplier and a product.

        supplier_id (int): the supplier company ID.
        product_sku (int): the SKU of the product.
        """
        sql = """DELETE FROM provided
                WHERE SKU = ? AND company_id = ?"""
        params = (product_sku, supplier_id)
        self._cur.execute(sql, params)
        if self._cur.rowcount == 0:
            raise ValueError("The link does not exist")
        self._conn.commit()


    def getSuppliers(self, product_sku):
        """
        Return all suppliers linked to a given product SKU.
        """
        sql ="""SELECT supplier.company_id, supplier.name, supplier.email,
                    supplier.contact_person, supplier.phone,
                    supplier.region, supplier.country, supplier.address
                FROM supplier
                JOIN provided ON provided.company_id = supplier.company_id
                WHERE provided.SKU = ?"""
        params = (product_sku,)
        self._cur.execute(sql, params)
        return self._cur.fetchall()


    def getProducts(self, company_id):
        """
        Return all products supplied by the specified supplier company ID.
        """
        sql ="""SELECT product.SKU, product.name, product.category,
                product.unit_price, product.quantity, product.rating
                FROM product
                JOIN provided ON provided.SKU = product.SKU
                WHERE company_id = ?"""
        params = (company_id,)
        self._cur.execute(sql, params)
        return self._cur.fetchall()


conn = sqlite3.connect("E:/Python/2º PROYECTO PYTHON/inventoryDb.db")
provided = Provided(conn)
print(provided.getSuppliers(7493))
print(provided.getProducts(873681))