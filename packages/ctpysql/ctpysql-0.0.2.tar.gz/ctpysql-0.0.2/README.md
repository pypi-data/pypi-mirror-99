# cautious-pysql
CTpysql helps you to code mysql queries as fast as possible 🚄🔥

### Usage
#### Installation
Use `pip install ctpysql` to install the *ctpysql* and it's dependencies on your pc (or venv).

import module with:

`from ctpysql import ctpysql`

to use it in your project.
#### How it works?
You may import mysql.connector to work with ctpysql, just use:

`from mysql.connector import (connection, Error)`

and make a connection like this:

`cnx = connection.MySQLConnection(user='root', password='password, host='127.0.0.1', database='db')`

then make an object from *ctpysql* class using this connection:

`obj = ctpysql(cnx)`

after these steps you are able to use this library correctly, for example, insert query using dictionary values:

`obj.insert('users', {'username': 'user1', 'password': 'password1'})`
