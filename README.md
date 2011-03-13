my nosql manifesto
==================

1. schemas change, expect this
2. some people do not understand SQL, expect this
3. json is beautiful, exploit this

    &gt;&gt;%gt; import nosqlsql as db
    &gt;&gt;%gt; db.connect(host="localhost",database="mydb",user="me",password="mypassword")
    &gt;&gt;%gt; db.signup("user","password")
    &gt;&gt;%gt; u = db.login("user","password")
    &gt;&gt;%gt; u.email = "sleepdev@gmail.com"
    &gt;&gt;%gt; u.email
    '"sleepdev@gmail.com"'
    &gt;&gt;%gt; del u.email
    &gt;&gt;%gt; u.email
    &gt;&gt;%gt; 
