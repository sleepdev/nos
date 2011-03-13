My nosql Manifesto
==================

1. schemas change, expect this
2. some people do not understand SQL, expect this
3. json is beautiful, exploit this

Examples
--------
    >>> from nosqlsql import connect
    >>> db = connect(host="localhost",database="mydb",user="me",password="mypassword")
    >>> db.signup("user","password")
    >>> u = db.login("user","password")
    >>> u.email = "sleepdev@gmail.com"
    >>> u.email
    u'sleepdev@gmail.com'
    >>> del u.email
    >>> u.email
    >>> 
