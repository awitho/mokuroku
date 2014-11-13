from flask import Flask

application = Flask("mokuroku")
application.config.from_object("mokuroku.config")

from . import routes
from . import category
from . import show
from . import listings

application.register_blueprint(show.blueprint, url_prefix="/show")
application.register_blueprint(category.blueprint, url_prefix="/category")
application.register_blueprint(listings.blueprint, url_prefix="/listings")
application.register_blueprint(routes.blueprint)