"""
Nosqlsql is the simplest orm for python. It just works.

To run doctests:
    nosetests --with-doctest


Primitive types go in and come out as normal python values
>>> v = db_push( None )
>>> v
<Row: Void>
>>> db_pull( v )
>>> v = db_push( True )
>>> v
<Row: Boolean>
>>> db_pull( v )
True
>>> v = db_push( 2 )
>>> v
<Row: Integer>
>>> db_pull( v )
2L
>>> v = db_push( 1.2 )
>>> v
<Row: Float>
>>> db_pull( v )
1.2
>>> v = db_push( 'abc' )
>>> v
<Row: String>
>>> db_pull( v )
'abc'

TODO: Index, List, Map, Object spec & implementations




#All operations start from an index.
#An index here, unlike those from relational databases, uniquely identifies only one object.
#This is the only way to persist objects across sessions.

#>>> u = Object( type='User' )
#>>> u
#<User: @x1533325>
#>>> index['a@b.cd'] = u
#>>> index['a@b.cd']
#<User: @x1533325>
#>>> 'a@b.cd' in index
#True
#>>> del index['a@b.cd']
#>>> 'a@b.cd' in index
#False



#Persistent objects behave like normal python objects

#>>> u.email = 'a@b.cd'
#>>> u.email
#'a@b.cd'
#>>> del u.email
#>>> u.email
#Traceback (most recent call last):
#  File "<stdin>", line 1, in <module>
#AttributeError: User instance has no attribute 'email'
#>>>

"""


import json
import tornado.database

dbconf = json.loads(file("/etc/nosqlsql/dbconf.json").read())
db = tornado.database.Connection( **dbconf )


class Row:
    def __init__( self, type, id ):
        self.type = type
        self.id = id
    def __repr__( self ):
        return "<Row: %s>" % self.type

def db_push( value ): 
    if value==None:
        id = db.execute("insert heap(type) values('Void')")
        return Row( type="Void", id=id )
    elif isinstance(value,bool):
        id = db.execute("insert heap(type) values('Boolean')")
        db.execute("insert term_Boolean(id,value) values(%s,%s)",id,value)
        return Row( type="Boolean", id=id )
    elif isinstance(value,int) or isinstance(value,long):
        id = db.execute("insert heap(type) values('Integer')")
        db.execute("insert term_Integer(id,value) values(%s,%s)",id,value)
        return Row( type="Integer", id=id )
    elif isinstance(value,float):
        id = db.execute("insert heap(type) values('Float')")
        db.execute("insert term_Float(id,value) values(%s,%s)",id,value)
        return Row( type="Float", id=id )
    elif isinstance(value,str) or isinstance(value,unicode):
        id = db.execute("insert heap(type) values('String')")
        db.execute("insert term_String(id,value) values(%s,%s)",id,value)
        return Row( type="String", id=id )
    else:
        raise NotImplementedError()


def db_pull( row ):
    if row.type=="Void": 
        return None
    elif row.type=="Boolean": 
        return True if db.get("select * from term_Boolean where id=%s",row.id).value else False
    elif row.type=="Integer":
        return db.get("select * from term_Integer where id=%s",row.id).value
    elif row.type=="Float":
        return db.get("select * from term_Float where id=%s",row.id).value
    elif row.type=="String":
        return db.get("select * from term_String where id=%s",row.id).value
    else:
        raise NotImplementedError()


