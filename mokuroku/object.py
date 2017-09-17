
# coding=utf-8

import functools
import inspect

from . import backend

from flask import g


def autoassign(func):
	"""
	Automatically assigns the parameters.

	>>> class process:
	...     @initializer
	...     def __init__(self, cmd, reachable=False, user='root'):
	...         pass
	>>> p = process('halt', True)
	>>> p.cmd, p.reachable, p.user
	('halt', True, 'root')
	"""
	"""
	http://stackoverflow.com/questions/1389180/python-automatically-initialize-instance-variables
	"""

	names, varargs, keywords, defaults = inspect.getargspec(func)

	@functools.wraps(func)
	def wrapper(self, *args, **kargs):
		for name, arg in list(zip(names[1:], args)) + list(kargs.items()):
			setattr(self, name, arg)

		for name, default in zip(reversed(names), reversed(defaults)):
			if not hasattr(self, name):
				setattr(self, name, default)

		func(self, *args, **kargs)

	return wrapper


class Mokuroku(backend.Database):
	pass


class DatabaseObject(object):
	def __init__(self, *args, **kwargs):
		super(DatabaseObject, self).__init__(*args, **kwargs)

	@classmethod
	def get(cls, id):
		return cls(**getattr(get(), cls.mappings['id'])(id))

	@classmethod
	def get_all(cls):
		return [cls(**x) for x in getattr(get(), cls.mappings['all'])()]


class Listing(DatabaseObject):
	mappings = {
		"id": "get_listing_by_id",
		"all": "get_listings"
	}

	@autoassign
	def __init__(self, category=None, show=None, episodes=None, rating=None):
		self.show = Show.get(self.show)

	@classmethod
	def get_by_category(cls, category_id):
		return [cls(**x) for x in get().get_listings_in_category(category_id)]


class Show(DatabaseObject):
	mappings = {
		"id": "get_show_by_id",
		"all": "get_shows"
	}

	@autoassign
	def __init__(self, id=None, title=None, description=None, total=None, begin_date=None, end_date=None):
		pass

	def __str__(self):
		return self.title


class Category(DatabaseObject):
	mappings = {
		"id": "get_category_by_id",
		"all": "get_categories"
	}

	categories = {}

	@autoassign
	def __init__(self, id=None, name=None, count=None):
		self.listings = Listing.get_by_category(self.id)

	@classmethod
	def get(cls, id):
		if id in Category.categories:
			return Category.categories[id]
		Category.categories[id] = Category(**get().get_category_by_id(id))
		return Category.categories[id]


def get():
	db = getattr(g, '_mokuroku', None)
	if db is None:
		db = g._mokuroku = Mokuroku()
	return db
