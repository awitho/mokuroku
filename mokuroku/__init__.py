from flask import Flask

application = Flask("mokuroku")
application.config.from_object("mokuroku.config")

from .routes import main
from .routes import category
from .routes import show
from .routes import listings

application.register_blueprint(show.blueprint, url_prefix="/show")
application.register_blueprint(category.blueprint, url_prefix="/category")
application.register_blueprint(listings.blueprint, url_prefix="/listings")
application.register_blueprint(main.blueprint)
