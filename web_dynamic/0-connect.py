import uuid

from models import storage
from models.content import Content
from models.location import Location
from models.user import User
from flask import Flask, render_template

from models.user import User

app = Flask(__name__)


# app.jinja_env.trim_blocks = True
# app.jinja_env.lstrip_blocks = True


@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()


@app.route('/content', strict_slashes=False)
def content_list():
    """ displays a HTML page with a list of contents"""
    cache_id = str(uuid.uuid4())
    contents = storage.all(Content).values()
    users = storage.all(User).values()
    locations = storage.all(Location).values()

    return render_template('3-main.html', contents=contents, locations=locations, users=users, cache_id=cache_id)



if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000, debug=True)
