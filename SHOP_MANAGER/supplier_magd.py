import sqlite3

class Supplier:
    """Represents a supplier record and handles persistence operations.

    Parameters:
        conn (sqlite3.Connection): an open database connection.
        company_id (int): unique supplier company ID.
        name (str): supplier name.
        email (str): supplier email address.
        contact_person (str): supplier contact person.
        phone (str|int): supplier phone number.
        region (str): supplier region.
        country (str): supplier country.
        address (str): supplier address.
    """

    def __init__(self, conn,
                company_id = None,
                name = None,
                email = None,
                contact_person = None,
                phone = None,
                region = None,
                country = None,
                address = None):
        conn.row_factory = sqlite3.Row
        self.__conn = conn
        self.__cur = conn.cursor()
        self.company_id = company_id
        self.name = name
        self.email = email
        self.contactPerson = contact_person
        self.phone = phone
        self.region = region
        self.country = country
        self.address = address


    def __repr__(self):
        return (f"Supplier(company_id={self.company_id}, name={self.name!r}, "
                f"email={self.email!r}, contactPerson={self.contactPerson!r}, "
                f"phone={self.phone!r}, region={self.region!r}, "
                f"country={self.country!r}, address={self.address!r})")


    def loadSuppliersFromFile(self, filename):
        """
        Take the CSV file and prepare the data to be
        inserted into the database.
        """
        suppliersData = []
        try:
            supplierFile = open(filename, encoding='utf-8')

            for line in supplierFile:
                    data = line.strip().split(",")
                    cleaned = []
                    for elem in data:
                        elem = elem.strip()
                        if elem == "":
                            elem = None
                        cleaned.append(elem)
                    suppliersData.append(cleaned)
            supplierFile.close()
        except FileNotFoundError:
            raise FileNotFoundError(f"The file {filename} was not found")
        return suppliersData


    def insert(self, filename):
        """
        Insert the data retrived by the previous method
        into the database.
        """
        supplierData = self.loadSuppliersFromFile(filename)
        sql = """INSERT OR REPLACE INTO supplier(
                company_id, name, email, contact_person, phone, region, country, address)
                VALUES (?,?,?,?,?,?,?,?)"""
        for suppliers in supplierData:
            self.__cur.execute(sql, suppliers)
        self.__conn.commit()


    def load(self):
        """
        Fill the object with a suplier from the database
        where the company ID matches.
        """
        if self.company_id == None:
            raise LookupError('Load: a valid company_id must be provided.')
        sql = """SELECT company_id, name, email, contact_person, phone, region, country, address
                FROM supplier
                WHERE company_id = ?"""
        params = (self.company_id,)
        self.__cur.execute(sql, params)
        row = self.__cur.fetchone()
        self.name = row["name"]
        self.email = row["email"]
        self.contactPerson = row["contact_person"]
        self.phone = row["phone"]
        self.region = row["region"]
        self.country = row["country"]
        self.address = row["address"]


    def update(self):
        """
        Updates the record from the database where the
        company ID matches.
        """
        if self.company_id == None:
            raise LookupError('Load: a valid company_id must be provided.')
        sql = """UPDATE supplier
                SET name = ?,
                    email = ?,
                    contact_person = ?,
                    phone = ?,
                    region = ?,
                    country = ?,
                    address = ?
                WHERE company_id = ?"""
        params = (
            self.name,
            self.email,
            self.contactPerson,
            self.phone,
            self.region,
            self.country,
            self.address,
            self.company_id
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
        Delete the record from the database where the SKU
        matches.
        """
        sql = """DELETE FROM supplier
                WHERE company_id = ?"""
        params = (self.company_id,)
        self.__cur.execute(sql, params)
        self.__conn.commit()