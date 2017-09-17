from ..object import get as db
from ..object import Listing, Category

from flask import Blueprint, render_template, url_for, redirect, request

blueprint = Blueprint('category', __name__, template_folder='templates')


@blueprint.route('/')
@blueprint.route('/<category>')
def root(category=None, title="listings"):
	categories = []
	if category is None:
		categories = Category.get_all()
	else:
		categories = [Category.get(int(category))]
		title = "category: %s" % categories[0].name
	return render_template("category/root.html", categories=categories, title=title)


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
@blueprint.route('/remove/<id>')
def remove(id=None):
	if id is not None:
		try:
			id = int(id)
		except ValueError:
			return render_template("error.html", error="not a valid integer")
		db().remove_category(id)
	return redirect(url_for("routes.root"))
