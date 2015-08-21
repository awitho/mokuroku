from .object import get as db

from flask import Blueprint, render_template, request, redirect, url_for

blueprint = Blueprint('listings', __name__, template_folder='templates')

ratings = {
	1: "terrible",
	2: "very bad",
	3: "bad",
	4: "bearable",
	5: "average",
	6: "alright",
	7: "decent",
	8: "entertaining",
	9: "enthralling",
	10: "perfect"
}


def handle_add(shows, categories, update=False):
	if not update:
		show = None
		if "show" not in request.form:
			return "no show specified"
		else:
			show = request.form['show'].strip()
			if not show or show == "0":
				return "no show specified"

		if db().get_listing_by_show_id(show) != None:
			return "listing for show already exists"

	category = None
	if "category" not in request.form:
		return "no category specified"
	else:
		category = request.form['category'].strip()
		if not category or category == "0":
			return "no show specified"

	rating = None
	if "rating" not in request.form:
		return "no rating specified"
	else:
		try:
			rating = int(request.form['rating'].strip())
		except:
			return "rating was not a valid number"
		if rating < 1 or rating > 10:
			return "rating was not in the range of 1 - 10"

	episodes = None
	if "episodes" not in request.form:
		return "no episodes specified"
	else:
		try:
			episodes = int(request.form['episodes'].strip())
		except:
			episodes = 0
		if episodes < 0:
			return "episodes must be greater than one >:|"

	if update:
		status = db().update_listing(update['id'], category, episodes, rating)
		return True
	else:
		status = db().create_listing(category, show, episodes, rating)

	if status is not None:
		return "created listing for " + shows[int(show) - 1]['title']
	else:
		print(status)
		return "failed to create listing"


@blueprint.route('/add/', methods=['GET', 'POST'])
@blueprint.route('/add/c<category>', methods=['GET', 'POST'])
@blueprint.route('/add/s<show>', methods=['GET', 'POST'])
@blueprint.route('/add/c<category>s<show>', methods=['GET', 'POST'])
def add(category=None, show=None):
	status = ""
	shows = db().get_shows()
	categories = db().get_categories()

	if request.method == "POST":
		status = handle_add(shows, categories)

	return render_template("listing/add.html", ratings=ratings, category=category, show=show, shows=shows, categories=categories, status=status)


@blueprint.route('/remove/', methods=['GET', 'POST'])
@blueprint.route('/remove/<id>')
def remove(id=None):
	try:
		id = int(id)
	except ValueError:
		return render_template("error.html", error="not a valid integer")

	db().remove_listing(id)
	return redirect(url_for("routes.root"))


@blueprint.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id=None):
	try:
		id = int(id)
	except ValueError:
		return render_template("error.html", error="not a valid integer")

	status = ""
	shows = db().get_shows()
	categories = db().get_categories()

	if request.method == "POST":
		status = handle_add(shows, categories, update={"id": id})
		if status is True:
			return redirect(url_for("routes.root"))

	listing = db().get_listing_by_show_id(id)
	category = listing['category']

	return render_template("listing/add.html", status=status, ratings=ratings, listing=listing, shows=shows, categories=categories, category=category, show=None)


@blueprint.route('/increment/', methods=['GET', 'POST'])
@blueprint.route('/increment/<id>')
def increment(id=None):
	if id is None:
		return render_template("error.html", error="not a valid id")
	try:
		id = int(id)
	except ValueError:
		return render_template("error.html", error="not a valid id")
	db().increment_listing(id, 1)
	return redirect(url_for("routes.root"))
