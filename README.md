nos
========

Nos is the simplest orm for python. It just works.


    Primitive types go in and come out as normal python values.

    >>> import nos
    >>> nos.db_pull( nos.db_push( None ) )
    >>> nos.db_pull( nos.db_push( True ) )
    True
    >>> nos.db_pull( nos.db_push( 2 ) )
    2
    >>> 1.234 < nos.db_pull( nos.db_push( 1.23456789 ) ) < 1.235
    True
    >>> nos.db_pull( nos.db_push( 'abc' ) )
    u'abc'
    


    Objects are easy too.

    >>> class MyModel( nos.Object ):
    ...     def __init__( self, arg ):
    ...         nos.Object.__init__( self )
    ...         self.my_field = arg
    ...
    >>> nos.models["MyModel"] = MyModel
    >>> v = MyModel( 1 )
    >>> v.my_field
    1



    Indexes allow you to find saved objects. Index keys must be strings.

    >>> nos.index["a"] = 5
    >>> nos.index["a"]
    5
    >>> nos.index["user: a@b.cd"] = MyModel(2)
    >>> nos.index["user: a@b.cd"].my_field
    2
