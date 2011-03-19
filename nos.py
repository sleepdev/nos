"""
Nos is the simplest orm for python. It just works.

To run doctests:
    nosetests --with-doctest



Primitive types go in and come out as normal python values
>>> db_pull( db_push( None ) )
None
>>> db_pull( db_push( True ) )
True
>>> db_pull( db_push( 2 ) )
2L
>>> db_pull( db_push( 1.2 ) )
1.2 
>>> db_pull( db_push( 'abc' ) )
'abc'


Collection types are just as easy to work with
>>> v = db_pull( db_push( [] ) )
>>> v
<nos.List instance at ...>
>>> v.append( 1 )
>>> len(v)
1
>>> v[0]
1
>>> v = db_pull( db_push( {} ) )
>>> v
<nos.Map instance at ...>
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
<nos.List instance at ...>


"""


import json
import tornado.database

dbconf = json.loads(file("/etc/nos/dbconf.json").read())
db = tornado.database.Connection( **dbconf )
models = None



def db_push( value ): 
    if value==None:
        return db.execute("insert heap(type) values('Void')")
    elif isinstance(value,bool):
        id = db.execute("insert heap(type) values('Boolean')")
        db.execute("insert term_Boolean(id,value) values(%s,%s)",id,value)
        return id
    elif isinstance(value,int) or isinstance(value,long):
        id = db.execute("insert heap(type) values('Integer')")
        db.execute("insert term_Integer(id,value) values(%s,%s)",id,value)
        return id
    elif isinstance(value,float):
        id = db.execute("insert heap(type) values('Float')")
        db.execute("insert term_Float(id,value) values(%s,%s)",id,value)
        return id 
    elif isinstance(value,str) or isinstance(value,unicode):
        id = db.execute("insert heap(type) values('String')")
        db.execute("insert term_String(id,value) values(%s,%s)",id,value)
        return id
    elif isinstance(value,list): 
        id = db.execute("insert heap(type) values('List')")
        for i,v in enumerate(value):
            v_id = db_push( v )
            db.execute("insert term_List(id,i,value_id) values(%s,%s,%s)",id,i,v_id)
        return id
    elif isinstance(value,dict):
        id = db.execute("insert heap(type) values('Map')")
        for k,v in value.items():
            hashk = hash(k)
            v_id = db_push( v )
            k_id = db_push( k )
            db.execute("insert term_Map(id,hashk,bucket,value_id)",id,hashk,k_id,v_id) 
        return id
    elif isinstance(value,List)\
      or isinstance(value,Map)\
      or isinstance(value,Object):
        return value.id
    else:
        raise TypeError("Models must extend nos.object")



def db_pull( id ):
    type = db.get("select * from heap where id=%s", id).type
    if row.type=="Void": 
        return None
    elif row.type=="Boolean": 
        return True if db.get("select * from term_Boolean where id=%s",id).value else False
    elif row.type=="Integer":
        return db.get("select * from term_Integer where id=%s",id).value
    elif row.type=="Float":
        return db.get("select * from term_Float where id=%s",id).value
    elif row.type=="String":
        return db.get("select * from term_String where id=%s",id).value
    elif row.type=="List":
        return List( id )
    elif row.type=="Map":
        return Map( id )
    elif row.type=="Object":
        #do not call __init__ because this is not a new object, it is just returned from the dead
        model = db.get("select * from term_Object where id=%s",id).model
        klass = models[model]
        obj   = object.__new__( klass ) 
        vars(obj)['id'] = id
        return obj



class List(object):
    def __init__( self, id ):
        self.id = id
    def __getitem__( self, i ):
        value_id = db.get("select * from term_List where id=%s and i=%s",self.id,i).value_id
        return db_pull( value_id )
    def __setitem__( self, i, v ):
        value_id = db_push( v )
        if db.get("select * from term_List where id=%s and i=%s",self.id,i):
            db.execute("update term_List set value_id=%s where id=%s and i=%s",value_id,self.id,i)
        else:
            raise IndexError('list assignment index out of range')
    def __len__( self ):
        return db.get("select count(*) from term_List where id=%s",self.id)["count(*)"]
    def append( self, value ):
        value_id = db_push( value ).id
        i = len( self )
        db.execute("insert term_List(id,i,value_id)",self.id,i,value_id)



class Map(object): 
    def __init__( self, id ):
        self.id = id
    def __hasitem__( self, k ):
        hashk = hash(k)
        buckets = db.query("select * from term_Map where id=%s and hashk=%s",self.id,hashk)
        return k in (db_pull(b.bucket) for b in buckets)
    def __getitem__( self, k ): 
        hashk = hash(k)
        buckets = db.query("select * from term_Map where id=%s and hashk=%s",self.id,hashk)
        for b in buckets:
            if db_pull(k_id)==k:
                return db_pull(b.value_id)
        raise KeyError(k)
    def __setitem__( self, k, v ):
        hashk = hash(k)
        



class Object(object):
    def __init__( self, id ):
        vars(self)['id'] = id





