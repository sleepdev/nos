"""
Nos is the simplest orm for python. It just works.

To run doctests:
    nosetests --with-doctest



Primitive types go in and come out as normal python values
>>> v = db_push( None )
>>> v
<nos.Row: Void>
>>> db_pull( v )
>>> v = db_push( True )
>>> v
<nos.Row: Boolean>
>>> db_pull( v )
True
>>> v = db_push( 2 )
>>> v
<nos.Row: Integer>
>>> db_pull( v )
2L
>>> v = db_push( 1.2 )
>>> v
<nos.Row: Float>
>>> db_pull( v )
1.2
>>> v = db_push( 'abc' )
>>> v
<nos.Row: String>
>>> db_pull( v )
'abc'


Collection types are just as easy to work with
>>> v = db_push( [] )
>>> v
<nos.Row: List>
>>> v = db_pull( v )
>>> v
<nos.List: instance>
>>> v.append( 1 )
>>> v[0]
1
>>> v = db_push( {} )
>>> v
<nos.Row: Map>
>>> v = db_pull( v )
>>> v
<nos.Map: instance>
>>> v['a'] = 5
>>> v['a']
5


Objects are even easier, just extend nos.Object
>>> class MyModel( nos.Object ):
...     def __init__( self, arg ):
...         self.my_field = arg
...
>>> v = MyModel( 1 )
>>> v.my_field
1


Indexes allow you to find saved objects
Index keys must be strings
>>> index["a"] = []
>>> index["a"]
<nos.List: instance>


"""


import json
import tornado.database

dbconf = json.loads(file("/etc/nos/dbconf.json").read())
db = tornado.database.Connection( **dbconf )


class Row:
    def __init__( self, type, id ):
        self.type = type
        self.id = id
    def __repr__( self ):
        return "<nos.Row: %s>" % self.type

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
    elif isinstance(value,list): 
        id = db.execute("insert heap(type) values('List')")
        for i,v in enumerate(value):
            value_id = db_push( v ).id
            db.execute("insert term_List(id,i,value_id) values(%s,%s,%s)",id,i,value_id)
        return Row( type="List", id=id )
    elif isinstance(value,dict):
        id = db.execute("insert heap(type) values('Map')")
        for k,v in value.items():
            hashk = hash(k)
            value_id = db_push( v ).id
            while True:
                randi = random.randint(-2147483648,2147483647)
                try:
                    db.execute("insert term_Map(id,key_hash,bucket,value_id)",id,hashk,randi,value_id) 
                    return Row( type="Map", id=id )
                except: pass
    elif isinstance(value,List)\
      or isinstance(value,Map)\
      or isinstance(value,Object):
        return Row( type=value.__class__.__name__, id=value.id )
    else:
        raise TypeError("Models must extend nos.object")


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
    elif row.type=="List":
        return List( row.id )
    elif row.type=="Map":
        return Map( row.id )
    elif row.type=="Object":
        #do not call __init__ because this is not a new object, it is just returned from the dead
        model = db.get("select * from term_Object where id=%s",row.id).model
        klass = models[model]
        obj   = object.__new__( klass ) 
        vars(obj)['id'] = row.id
        return obj


