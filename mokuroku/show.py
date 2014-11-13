from .object import get as db

import datetime
from flask import Blueprint, render_template, url_for, request, redirect

blueprint = Blueprint('show', __name__, template_folder='templates')

@blueprint.route('/')
@blueprint.route('/<id>')
def root(id=None):
	show = None
	empty = True
	if not id is None:
		try:
			show = db().get_show_by_id(int(id))
		except:
			return redirect(url_for("routes.root"))
		for item in show:
			if item != "title" and item != "id" and show[item] != None:
				empty = False
				break
	else:
		return redirect(url_for("routes.root"))

	return render_template("show/root.html", show=show, empty=empty)

def verify_date(string):
	try:
		datetime.strptime(string, "%Y-%m-%d")
		return True
	except ValueError:
		return False

def handle_add(title):
	if request.method == "POST":
		title = request.form['title']
	title = title.strip()

	if not title:
		return "must have a title"

	description = None
	if 'description' in request.form:
		t = request.form['description'].strip()
		if t:
			description = t

	total = None
	if 'total' in request.form:
		t = request.form['total'].strip()
		if t:
			try:
				total = int(t)
			except:
				return "total was not a valid integer"

	begin = None
	if 'begin' in request.form:
		t = request.form['begin'].strip()
		if not t or not verify_date(t):
			return "begin date was not valid"
		begin = t

	end = None
	if 'end' in request.form:
		t = request.form['end'].strip()
		if not t or not verify_date(t):
			return "end date was not valid"
		end = t

	db().create_show(title, description, total, begin, end)

	return "success! added show: " + title

@blueprint.route("/add/", methods=['POST', 'GET'])
def add(title=None):
	status = ""
	if request.method == "POST" or not (title is None):
		status = handle_add(title)

	return render_template("show/add.html", status=status)

@blueprint.route("/remove/", methods=['POST', 'GET'])
def remove(id=None):
	pass

@blueprint.route("/edit/", methods=['POST', 'GET'])
def edit(id=None):
	pass
