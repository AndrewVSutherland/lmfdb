
from lmfdb.app import app
from lmfdb.logger import make_logger
from flask import Blueprint

artin_representations_page = Blueprint(
    "artin_representations", __name__, template_folder='templates', static_folder="static")
artin_logger = make_logger("artin", hl=True)

# artin_logger.info("Initializing Artin representations blueprint")


@artin_representations_page.context_processor
def body_class():
    return {'body_class': 'artin_representations'}

from . import main
assert main # silence pyflakes

app.register_blueprint(artin_representations_page, url_prefix="/ArtinRepresentation")

# API2 has been disabled for now
#from lmfdb.api2.searchers import register_search_function
#register_search_function(
#    "artin_representations",
#    "Artin representations",
#    "Search over Artin representations",
#    auto_search = 'artin_reps'
#)
