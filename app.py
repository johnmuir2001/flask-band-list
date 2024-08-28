from flask import Flask
from views import my_view

app = Flask(__name__)
app.register_blueprint(my_view)
app.config['UPLOAD_FOLDER'] = './static'

if __name__ == "__main__":
    app.run(debug=True, port=8000)