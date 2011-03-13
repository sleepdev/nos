import json
import tornado.database

class connect( tornado.database.Connection ):
    def __init__( self, host, database, user=None, password=None, max_idle_time=7*3600 ):
        tornado.database.Connection.__init__(
            self, 
            host=host, 
            database=database, 
            user=user, 
            password=password, 
            max_idle_time=max_idle_time 
        )    

    def signup( self, unique_identifier, password ):
        self.execute(
            "INSERT user (unique_identifier,pwdhash) VALUES (%s,UNHEX(SHA1(%s)))",
            unique_identifier,
            password
        )

    def login( self, unique_identifier, password ):
        user_data = self.get(
            "SELECT id FROM user WHERE unique_identifier=%s AND pwdhash=UNHEX(SHA1(%s))", 
            unique_identifier,
            password
        )
        if user_data:
            return User( self, user_data["id"] )
        else:
            return None

class User:
    def __init__( self, db, user_id ):
        vars(self)["db"] = db
        vars(self)["id"] = user_id
    def __getattr__( self, key ):
        row = vars(self)["db"].get(
            "SELECT _value FROM user_data WHERE user_id=%s AND _key=%s",
            vars(self)["id"],
            key
        )
        if row: 
            return json.loads(row["_value"])
        else:
            return None
    def __setattr__( self, key, value ):
        value = json.dumps(value)
        vars(self)["db"].execute(
            "INSERT user_data(user_id,_key,_value) values(%s,%s,%s) ON DUPLICATE KEY UPDATE _value=%s",
            vars(self)["id"],
            key,
            value, value
        )
    def __delattr__( self, key ):
        vars(self)["db"].execute(
            "DELETE FROM user_data WHERE user_id=%s AND _key=%s",
            vars(self)["id"],
            key
        )




