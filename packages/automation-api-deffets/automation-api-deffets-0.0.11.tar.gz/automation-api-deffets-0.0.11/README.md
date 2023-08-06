
# Python API for the automation server database

## Example
```python
  from api.api import DB

  db = DB(dbName='automation3', host="3.123.139.xxx", user="username", password=None, key="/home/username/.ssh/id_rsa", uri=None, port=22, to_host='127.0.0.1', to_port=27017)

  print(db.getUsers())
```

