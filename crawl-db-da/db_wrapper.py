import mysql.connector
from mysql.connector import errorcode

class db_wrapper:
    #conn =None
    #cursor = None

    def __init__(self):
        print("@init method")
        try:
            # sql connection string
            self.conn = mysql.connector.connect(user='root', password='python123',
                                           host='127.0.0.1',
                                           database='data_love')

            print("got connection " )
            print(self.conn)
            self.cursor = self.conn.cursor()
            print("got cursor " )
            print(self.cursor)

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    # Read from  database
    def db_read(self):
        self.cursor.execute('SELECT * FROM data_love.sanctions_names_new;')
        print("executed this read")
        for row in self.cursor:
            print(row)

    # Write to database
    def db_write(self, query):
        self.cursor = self.conn.cursor()
        query = '''

                INSERT INTO  data_love.sanctions_names_new (id, name, description, source, date_added )
                VALUES
                (9,'Data','Test', "kavi checking", now())

                '''

        self.cursor.execute(query)
        self.conn.commit()


insert_query = ''' 
                insert into sanctions.sanctions_addresses (id, id1,address,source) values ( 'OFAC9639', 'OFAC1992812', ' ', 'OFAC-NON-SDN')

            '''
# db_connect = db_wrapper()
# results = db_connect.cursor.execute(insert_query)
# print("results")
# print(results)
# db_connect.cursor.execute("insert into sanctions.sanctions_names  (id, name,description, source, date_added) values ( 'OFAC999639', 'HANIYA, Ismail Abdul Salah', 'individual NS-PLC DOB 1962; POB Shati.', 'OFAC-NON-SDN', '2019-03-01 17:17:07') ")
#
# #
# db_obj.db_write()
# db_obj.db_read()

#
# CREATE TABLE `sanctions`.`sanctions_names` (
#   `id` VARCHAR(45) NOT NULL,
#   `name` VARCHAR(45) NULL,
#   `description` VARCHAR(45) NULL,
#   `source` VARCHAR(45) NULL,
#   `date_added` DATETIME NULL,
#   PRIMARY KEY (`id`))
#
#
#
# CREATE TABLE `sanctions`.`sanctions_addresses` (
#   `id` VARCHAR(45) NOT NULL,
#   `id1` VARCHAR(45) NOT NULL,
#   `address` VARCHAR(45) NULL,
#   `source` VARCHAR(45) NULL,
#   PRIMARY KEY (`id1`))
#
#
#
#
# CREATE TABLE `sanctions`.`sanctions_alternatenames` (
#   `id` INT NOT NULL,
#   `id1` VARCHAR(45) NULL,
#   `name` VARCHAR(45) NULL,
#   `source` VARCHAR(45) NULL,
#    `date_added` DATETIME NULL,
#   PRIMARY KEY (`id1`))

