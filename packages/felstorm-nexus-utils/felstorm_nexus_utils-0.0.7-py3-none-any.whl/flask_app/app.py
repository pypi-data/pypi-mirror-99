from flask import Flask
#from nexus_engine.blueprints import nexus_dev_pages
#from felstorm_nexus_utils.blueprints import nexus_dev_pages
from felstorm_nexus_utils.blueprints import nexus_dev_pages

app = Flask(__name__, static_folder=None)
app.register_blueprint(nexus_dev_pages)
