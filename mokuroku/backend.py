from . import config

from sqlite3 import connect


def dict_factory(cursor, row):
	d = {}
	for idx, col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d


class _Database():
	def __init__(self):
		self.db = self.connect()

	def query(self, query, args=(), one=False, factory=dict_factory):
		try:
			cur = self.db.execute(query, args)

			cur.row_factory = factory

			rv = cur.fetchall()

			self.rowid = cur.lastrowid

			cur.close()
			self.db.commit()
			return (rv[0] if rv else None) if one else rv
		except Exception as e:
			return e

	def connect(self):
		return connect(config.DATABASE)


class Database(_Database):
	def __init__(self):
		super().__init__()

	# Shows
	def create_show(self, title, description, total, begin_date, end_date):
		self.query("INSERT INTO shows (title, description, total, begin_date, end_date) VALUES (?, ?, ?, ?, ?);", args=(title, description, total, begin_date, end_date), one=True)
		return self.rowid

	def remove_show(self, id):
		return self.query("DELETE FROM shows WHERE id=?;", args=(id,), one=True)

	def get_show_by_id(self, id):
		return self.query("SELECT * FROM shows WHERE id=?;", args=(id,), one=True)

	def get_shows(self):
		return self.query("SELECT * FROM shows;")

	# Categories
	def create_category(self, name):
		self.query("INSERT INTO categories (name) VALUES (?);", args=(name,), one=True)
		return self.rowid

	def modify_category(self, id, num):
		return self.query("UPDATE categories SET count=count+? WHERE id=?;", args=(num, id), one=True)

	def remove_category(self, id):
		# Sqlite should handle this, with foreign keys.
		#for row in self.get_listings_in_category(id):
		#	self.remove_listing(row['row_id'])
		return self.query("DELETE FROM categories WHERE id=?;", args=(id,), one=True)

	def get_category_by_id(self, id):
		return self.query("SELECT * FROM categories WHERE id=?;", args=(id,), one=True)

	def get_category_by_name(self, name):
		return self.query("SELECT * FROM categories WHERE name=?;", args=(name,), one=True)

	def get_categories(self):
		return self.query("SELECT * FROM categories;")

	# Listings
	def create_listing(self, category, show, episodes, rating):
		self.modify_category(category, 1)
		self.query("INSERT INTO listings (category, show, episodes, rating) values (?, ?, ?, ?);", args=(category, show, episodes, rating), one=True)
		return self.rowid

	def remove_listing(self, id):
		self.modify_category(self.get_listing_by_id(id)['category'], -1)
		return self.query("DELETE FROM listings WHERE id=?;", args=(id,), one=True)

	def get_listing_by_id(self, id):
		return self.query("SELECT * FROM listings WHERE id=?;", args=(id,), one=True)

	def get_listing_by_show_id(self, id):
		return self.query("SELECT * FROM listings WHERE show=?;", args=(id,), one=True)

	def get_listings_in_category(self, id):
		return self.query("SELECT * FROM listings WHERE category=?;", args=(id,))