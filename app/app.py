
import csv
import os
from functools import wraps

from flask import Flask, request, Response, url_for, render_template 

app = Flask(__name__)
username = os.getenv('WEB_USERNAME', '')
password = os.getenv('WEB_PASSWORD', '')

ALLOWED_EXTENSIONS = ['csv']

DEFAULT_CSV_HEADERS = ['test1', 'test2']

def allowed_file(filename):
    """Checks if the filename is an allowed type of file.
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def check_auth(ausername, apassword):
    """Checks that the username / password combination is valid for basic
    HTTP auth.
    """
    return ausername == username and apassword == password

def authenticate():
    return Response(
        'Could not verify your access level for this url.\n'
        'Please login with username and password', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})

def auth_csv_headers(csv_file, correct_headers):
    reader = csv.reader(csv_file)
    headers = next(reader)

    return not headers == correct_headers


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/', methods=['GET', 'POST'])
@requires_auth
def hello_world():
    if request.method == 'POST':
        file = request.files['file']
        filename = None
        if file and allowed_file(file.filename):
            filename = file.filename
            check = auth_csv_headers(file, DEFAULT_CSV_HEADERS)

        return render_template('home.html', 
                check=check,
                upload_filename=filename)

    return render_template('home.html')

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
