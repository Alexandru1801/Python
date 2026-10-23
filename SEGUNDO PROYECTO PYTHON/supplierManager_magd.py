import sqlite3
from supplier_magd import Supplier

class supplierManager:
    """Provides query methods for supplier records in the database.

    This manager builds and executes SELECT statements against the supplier
    table and returns Supplier objects for matching records.
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


    def __getSupplierList(self, rows):
        """
        Transform the given records from the database into Supplier objects
        and return them into a list.
        """
        result = []
        for supplier in rows:
            mySupplier = Supplier(
                self._conn,
                supplier["company_id"],
                supplier["name"],
                supplier["email"],
                supplier["contact_person"],
                supplier["phone"],
                supplier["region"],
                supplier["country"],
                supplier["address"]
            )
            result.append(mySupplier)
        return result
    

    def getByCompanyId(self, company_ids):
        """
        Return suppliers whose company IDs match the provided value or set of values.

        companty_ids (list, set, int): a collection of unique company IDs or a single company ID.

        Output (list): a collection of Supplier objects matching given category.
        """
        params = self.__convertToTupple(company_ids)
        placeholders = ', '.join(['?'] * len(params))
        sql = f"""SELECT company_id, name, email, contact_person, phone, region, country, address 
                FROM supplier
                WHERE company_id IN ({placeholders}) 
                ORDER BY company_id"""
        self._cur.execute(sql, params)
        rows = self._cur.fetchall()
        return self.__getSupplierList(rows)


    def getByName(self, name_part):
        """
        Return suppliers whose name contains the given search fragment.

        name_part (str): a complete name or a part of it.

        Output (list): a collection of Supplier objects matching given category.
        """
        sql = """SELECT company_id, name, email, contact_person, phone, region, country, address
                FROM supplier
                WHERE name LIKE ? 
                ORDER BY name"""
        params = (f"%{name_part}%",)
        self._cur.execute(sql, params)
        rows = self._cur.fetchall()
        return self.__getSupplierList(rows)


    def getByEmail(self, email):
        """
        Return suppliers whose email matches exactly the given value.

        email (str): the email address to search for.

        Output (list): a collection of Supplier objects matching given category.
        """
        sql = """SELECT company_id, name, email, contact_person, phone, region, country, address
                FROM supplier
                WHERE email = ? 
                ORDER BY email"""
        params = self.__convertToTupple(email)
        self._cur.execute(sql, params)
        rows = self._cur.fetchall()
        return self.__getSupplierList(rows)


    def getByContactPerson(self, name_part):
        """
        Return suppliers whose contact person matches the provided name fragment.

        name_part (str): a complete person name or a part of it.

        Output (list): a collection of Supplier objects matching given category.
        """
        sql = """SELECT company_id, name, email, contact_person, phone, region, country, address
                FROM supplier
                WHERE contact_person LIKE ? 
                ORDER BY contact_person"""
        params = (f"%{name_part}%",)
        self._cur.execute(sql, params)
        rows = self._cur.fetchall()
        return self.__getSupplierList(rows)


    def getByPhone(self, phone):
        """
        Return suppliers with the specified phone number.

        phone (str): the phone number to search for.

        Output (list): a collection of Supplier objects matching given category.
        """
        sql = """SELECT company_id, name, email, contact_person, phone, region, country, address 
            FROM supplier
            WHERE phone = ?
            ORDER BY phone"""
        params = (phone,)
        self._cur.execute(sql, params)
        rows = self._cur.fetchall()
        return self.__getSupplierList(rows)


    def getByRegion(self, region):
        """
        Return suppliers located in the specified region.

        region (str): the region to search for.

        Output (list): a collection of Supplier objects matching given category.
        """
        sql = """SELECT company_id, name, email, contact_person, phone, region, country, address 
            FROM supplier
            WHERE region = ?
            ORDER BY region"""
        params = (region,)
        self._cur.execute(sql, params)
        rows = self._cur.fetchall()
        return self.__getSupplierList(rows)


    def getByCountry(self, country):
        """
        Return suppliers located in the specified country.

        country (str): the country to search for.

        Output (list): a collection of Supplier objects matching given category.
        """
        sql = """SELECT company_id, name, email, contact_person, phone, region, country, address 
            FROM supplier
            WHERE country = ?
            ORDER BY country"""
        params = (country,)
        self._cur.execute(sql, params)
        rows = self._cur.fetchall()
        return self.__getSupplierList(rows)


    def getByAddress(self, address):
        """
        Return suppliers whose address matches the provided value.

        address (str): the address to search for.

        Output (list): a collection of Supplier objects matching given category.
        """
        sql = """SELECT company_id, name, email, contact_person, phone, region, country, address 
            FROM supplier
            WHERE address = ?
            ORDER BY address"""
        params = (address,)
        self._cur.execute(sql, params)
        rows = self._cur.fetchall()
        return self.__getSupplierList(rows)