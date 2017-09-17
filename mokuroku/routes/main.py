
# coding=utf-8

from pprint import pprint

from . import category
from ..object import Show, Listing, Category

from flask import Blueprint

blueprint = Blueprint('routes', __name__, template_folder='templates')


@blueprint.route('/')
def root():
	return category.root(None)


@blueprint.route('/debug')
def debug():
	listings = Listing.get_by_category(1)

	response = ""
	for category in sorted(Listing.categories.values(), key=lambda x: x.name):
		response += "<br/><h1>%s</h1><br/>" % category.name
		for listing in sorted(category.listings, key=lambda x: x.show.title):
			response += "%s: %s<br/>" % (listing.show.title, listing.episodes)
	return response
