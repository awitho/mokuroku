from .object import get as db

from flask import Blueprint, render_template, request

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

def handle_add(shows, categories):
	show = None
	if not "show" in request.form:
		return "no show specified"
	else:
		show = request.form['show'].strip()
		if not show or show == "0":
			return "no show specified"

	if db().get_listing_by_show_id(show) != None:
		return "listing for show already exists"

	category = None
	if not "category" in request.form:
		return "no category specified"
	else:
		category = request.form['category'].strip()
		if not category or category == "0":
			return "no show specified"

	rating = None
	if not "rating" in request.form:
		return "no rating specified"
	else:
		try:
			rating = int(request.form['rating'].strip())
		except:
			return "rating was not a valid number"
		if rating < 1 or rating > 10:
			return "rating was not in the range of 1 - 10"

	episodes = None
	if not "episodes" in request.form:
		return "no episodes specified"
	else:
		try:
			episodes = int(request.form['episodes'].strip())
		except:
			return "episodes was not a valid number"
		if episodes < 0:
			return "episodes must be greater than one >:|"

	status = db().create_listing(category, show, episodes, rating)
	if status != None:
		return "created listing for " + shows[int(show)-1]['title']
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
	return "test"

@blueprint.route('/edit/<id>')
def edit(id=None):
	return "test"

@blueprint.route('/increment/', methods=['GET', 'POST'])
@blueprint.route('/increment/<id>')
def increment(id=None):
	return "test"
