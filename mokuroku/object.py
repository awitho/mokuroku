from . import backend

from flask import g

class DBObject():
	def __init__(dict, db):
		self.dict = dict
		self.db = db

	def save():
		pass

# Basically a wrapper for the lower-level Database object.
class Mokuroku(backend.Database):
	pass

def get():
	db = getattr(g, '_mokuroku', None)
	if db is None:
		db = g._mokuroku = Mokuroku()
	return db