from .. import config
from sqlite3 import connect

db = connect(config.DATABASE)
f = open('mokuroku/mokuroku.sql', mode='r')
db.cursor().executescript(f.read())
f.close()
db.commit()
db.close()