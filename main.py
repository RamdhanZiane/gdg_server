from manageApp import create_app
from flask_swagger import swagger
from flask import jsonify

app = create_app()

@app.route("/spec")
def spec():
    return jsonify(swagger(app))

if __name__ == '__main__':
    app.run(debug=True)