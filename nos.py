"""
Nos is the simplest orm for python. It just works.

To run doctests:
    nosetests --with-doctest



Primitive types go in and come out as normal python values.
>>> db_pull( db_push( None ) )
>>> db_pull( db_push( True ) )
True
>>> db_pull( db_push( 2 ) )
2
>>> 1.234 < db_pull( db_push( 1.23456789 ) ) < 1.235
True
>>> db_pull( db_push( 'abc' ) )
u'abc'


Objects are easy too.
>>> class MyModel( Object ):
...     def __init__( self, arg ):
...         Object.__init__( self )
...         self.my_field = arg
...
>>> models["MyModel"] = MyModel
>>> v = MyModel( 1 )
>>> v.my_field
1


Indexes allow you to find saved objects.
Index keys must be strings.
>>> index["a"] = 5
>>> index["a"]
5
>>> index["user: a@b.cd"] = MyModel(2)
>>> index["user: a@b.cd"].my_field
2


"""


import json
import tornado.database

dbconf = json.loads(file("/etc/nos/dbconf.json").read())
db = tornado.database.Connection( **dbconf )
models = {}



def db_push( value ): 
    if value==None\
    or isinstance(value,bool) or isinstance(value,int)\
    or isinstance(value,long) or isinstance(value,float)\
    or isinstance(value,str) or isinstance(value,unicode)\
    or isinstance(value,list) or isinstance(value,dict):
        js = json.dumps(value)
        id = db.execute("insert heap(type) values('json')")
        db.execute("insert json(id,js) values(%s,%s)",id,js)
        return id 
    elif isinstance(value,Object):
        return vars(value)["id"]
    else:
        raise TypeError("Models must extend nos.object")



def db_pull( id ):
    type = db.get("select type from heap where id=%s", id).type
    if type=="json": 
        js = db.get("select js from json where id=%s",id).js
        return json.loads(js)
    elif type=="object": 
        #do not call __init__ because this is not a new object, it is just returned from the dead
        klass = db.get("select klass from obj_class where id=%s",id).klass
        obj   = object.__new__( models[klass] ) 
        vars(obj)['id'] = id
        return obj



class Object(object):
    def __init__( self ):
        id = db.execute("insert heap(type) values('object')")
        db.execute("insert obj_class(id,klass) values(%s,%s)",id,self.__class__.__name__)
        vars(self)["id"] = id
    def __getattr__( self, name ):
        id = db.get("select value_id from obj_field where id=%s and field=%s",vars(self)["id"],name).value_id
        return db_pull( id )
    def __setattr__( self, name, val ):
        id = db_push( val )
        db.execute("insert obj_field(id,field,value_id) values(%s,%s,%s) on duplicate key update value_id=%s",
            vars(self)["id"], name, id, id )


class index:
    def __getitem__( self, key ):
        row = db.get("select id from indx where indx=%s",key)
        if row!=None: return db_pull(row.id)
        else: raise KeyError(key)
    def __setitem__( self, key, value ):
        value_id = db_push(value)
        id = db.execute("insert indx(indx,id) values(%s,%s) on duplicate key update id=%s", key, value_id, value_id )
index = index()
