import json
import tornado.database

db = None

def connect( host, database, user=None, password=None, max_idle_time=7*3600 ):
    global db
    db = tornado.database.Connection( 
        host=host, 
        database=database, 
        user=user, 
        password=password, 
        max_idle_time=max_idle_time 
    )    

def signup( unique_identifier, password ):
    global db
    db.execute(
        "INSERT user (unique_identifier,pwdhash) VALUES (%s,UNHEX(SHA1(%s)))",
        unique_identifier,
        password
    )

def login( unique_identifier, password ):
    global db
    user_data = db.get(
        "SELECT id FROM user WHERE unique_identifier=%s AND pwdhash=UNHEX(SHA1(%s))", 
        unique_identifier,
        password
    )
    if user_data:
        return User( user_data["id"] )
    else:
        return None

class User:
    def __init__( self, user_id ):
        vars(self)["id"] = user_id
    def __getattr__( self, key ):
        global db
        row = db.get(
            "SELECT _value FROM user_data WHERE user_id=%s AND _key=%s",
            vars(self)["id"],
            key
        )
        if row: 
            return row["_value"]
        else:
            return None
    def __setattr__( self, key, value ):
        global db
        value = json.dumps(value)
        db.execute(
            "INSERT user_data(user_id,_key,_value) values(%s,%s,%s) ON DUPLICATE KEY UPDATE _value=%s",
            vars(self)["id"],
            key,
            value, value
        )
    def __delattr__( self, key ):
        global db
        db.execute(
            "DELETE FROM user_data WHERE user_id=%s AND _key=%s",
            vars(self)["id"],
            key
        )




