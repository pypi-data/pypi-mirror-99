import json
from pyqldb.driver.qldb_driver import QldbDriver
from amazon.ion.json_encoder import IonToJSONEncoder

class QLDBDriver:
    def __init__(self, ledger):
        self.qldb_driver = QldbDriver(ledger_name = ledger)
    
    def to_collection(self, cursor):
        collection = []
        
        for row in cursor:
            json_string = json.dumps(row, cls=IonToJSONEncoder)
            collection.append(json.loads(json_string))

        return collection


    def execute(self, transaction_executor, statement):
        cursor = transaction_executor.execute_statement(statement)
        
        return cursor


    def create_table(self, table_name, primary_key = None):
        statement = f"CREATE TABLE {table_name}"
        cursor = self.qldb_driver.execute_lambda(lambda x: self.execute(x, statement))

        if primary_key is not None:
            statement = f"CREATE INDEX ON {table_name}({primary_key})"
            cursor = self.qldb_driver.execute_lambda(lambda x: self.execute(x, statement))


    def drop_table(self, table_name):
        statement = f"DROP TABLE {table_name}"
        cursor = self.qldb_driver.execute_lambda(lambda x: self.execute(x, statement))


    def list_tables(self):
        collection = []

        for table in self.qldb_driver.list_tables():
            collection.append(table)

        return collection


    def insert_data(self, table_name, data):
        statement = f"INSERT INTO {table_name} `{json.dumps(data)}`"
        cursor = self.qldb_driver.execute_lambda(lambda x: self.execute(x, statement))


    def update_data(self, table_name, primary_key_field, primary_key_value,data):
        statement = f"""
            UPDATE {table_name} AS x 
                SET x = {str(data)} 
            WHERE x.{primary_key_field} = {primary_key_value}"""
        
        cursor = self.qldb_driver.execute_lambda(lambda x: self.execute(x, statement))


    def query(self, statement):
        cursor = self.qldb_driver.execute_lambda(lambda x: self.execute(x, statement))

        return self.to_collection(cursor)


    def query_single(self, statement):
        cursor = self.qldb_driver.execute_lambda(lambda x: self.execute(x, statement))
        collection = self.to_collection(cursor)

        if len(collection) > 1:
            raise Exception('more than 1 result recived')

        return collection[0]
