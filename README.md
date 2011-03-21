nos
========

Nos is the simplest orm for python. It just works.

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
