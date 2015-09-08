from . import category

from flask import Blueprint

blueprint = Blueprint('routes', __name__, template_folder='templates')


@blueprint.route('/')
def root():
	return category.root(None)
