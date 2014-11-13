from .object import get as db

from flask import Blueprint, render_template, url_for, redirect, request

blueprint = Blueprint('category', __name__, template_folder='templates')

@blueprint.route('/')
@blueprint.route('/<category>')
def root(category=None, title="listings"):
	rows = None
	listings = []
	if category is None:
		for category in db().get_categories():
			c_listings = db().get_listings_in_category(category['id'])

			listings.append({"heading": True, "category": category})
			if len(c_listings) != 0:
				for listing in c_listings:
					listing['show'] = db().get_show_by_id(listing['show'])

				listings += c_listings
		category = None #oops
	else:
		try:
			category = db().get_category_by_id(int(category))
		except ValueError:
			category = db().get_category_by_name(category)

		if category is None:
			return redirect(url_for("category.root"))

		listings = db().get_listings_in_category(category['id'])
		for listing in listings:
			listing['show'] = db().get_show_by_id(listing['show'])

		title = "category: " + category['name']
	return render_template("category/root.html", category=category, listings=listings, title=title)

def handle_add(name):
	if request.method == "POST":
			name = request.form['name']
	name = name.strip()
	if not name:
		status = "invalid name"

	db().create_category(name)

	return "success! added category: " + name

@blueprint.route('/add/', methods=['POST', 'GET'])
@blueprint.route('/add/<name>')
def add(name=None):
	status = ""
	if request.method == "POST" or not (name is None):
		status = handle_add(name)
	return render_template("category/add.html", status=status)

@blueprint.route('/remove/')
@blueprint.route('/remove/<category>')
def remove(category=None):
	if (category is None):
		return redirect(url_for("category.root"))
	return category