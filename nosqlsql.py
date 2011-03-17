"""
Nosqlsql is the simplest orm for python. It just works.


User authentication is the core of this orm.
You cannot do anything without a user object.

>>> delete_user( "a@b.cd" )
>>> signup( "a@b.cd", "abcd" )
<User: a@b.cd>
>>> signin( "a@b.cd", "abcd" )
<User: a@b.cd>
>>> signin( "a@b.cd", "wxyz" )
>>>


Once you create a user object, just use as you normally would.

>>> u = signin( "a@b.cd", "abcd" )
>>> u.email = "a@b.cd"
>>> u.email
u"a@b.cd"
>>> del u.email
>>> u.email
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: User instance has no attribute 'email'
>>>

"""


import json
import tornado.database

dbconf = json.loads(file("/etc/nosqlsql/dbconf.json"))
db = tornado.database.Connection( **dbconf )
models = None


def signup( unique_identifier, password ):
    if db.get("SELECT * FROM user WHERE unique_identifier=%s",unique_identifier):
        return False
    db.execute(
        "INSERT term_user (unique_identifier,pwdhash) VALUES (%s,UNHEX(SHA1(CONCAT(unique_identifier,%s))))",
        unique_identifier,
        password
    )
    return True

def login( unique_identifier, password ):
    user_data = db.get(
        "SELECT id FROM term_user WHERE unique_identifier=%s AND pwdhash=UNHEX(SHA1(CONCAT(unique_identifier,%s)))", 
        unique_identifier,
        password
    )
    if user_data:
        return term_user( user_data["id"] )
    else:
        return None

def safehash( v ):
    if isinstance(v,term_list) or isinstance(v,term_dict)\
    or isinstance(v,term_object): return v.id
    else: return hash(v)

def getmodel( classname ):
    if classname not in models:
        models[classname] = type(classname,(),{})
    return models[classname]

def push_value( value ): pass #internalize and return value_id
def pull_value( row ): 
    if row.type=="NoneType": return None
    elif row.type=="bool":   return row.term_bool
    elif row.type=="int":    return row.term_int
    elif row.type=="float":  return row.term_float
    elif row.type=="str":    return row.term_str 
    else: 
        klass = getmodel( row.type )
        obj = object.__new__(klass)
        vars(obj)["id"] = row["id"]
        return obj

class term_list(list): pass #TODO
class term_dict(dict): pass #TODO
class term_object(object):
    def __getattr__( self, key ):
        if key=="id":
            return vars(self)["id"]
        row = db.get("SELECT term.* FROM term_object,term WHERE term_object.id=%s AND field=%s AND value_id=term.id",self.id,key)
        return pull_value( row )
    def __setattr__( self, key, value ):
        value_id = push_value( value )
        db.execute("INSERT term_object(id,field,value_id) values(%s,%s,%s) ON DUPLICATE KEY UPDATE value_id=%s",self.id,key,value_id,value_id)
    def __delattr__( self, key ):
        db.execute("DELETE FROM term_object WHERE id=%s AND field=%s",self.id,key)

