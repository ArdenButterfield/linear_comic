""" 
This program turns the website into a static site, which is
what I needed for the hosting service.
"""

from flask_frozen import Freezer
from flask_comic import app
from flask import url_for


freezer = Freezer(app)

@freezer.register_generator
def linear_pages_url_generator():
    for i in range(60):
        yield f"/linear/{i}/"

if __name__ == "__main__":

    freezer.freeze()