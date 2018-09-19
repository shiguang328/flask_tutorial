from flask import request, Flask
from flask_script import Manager
from flask import current_app, render_template

app = Flask(__name__)

@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    return '<p>Your Browser is %s.</p>' % user_agent


manager = Manager(app)

if __name__ == '__main__':
    manager.run()