from flask import Flask, abort


app = Flask(__name__)

db = {
    'john': '123456789',
    'mary': '987654321'
}


@app.route('/phone/<string:user>', methods=['GET'])
def get_phone(user):
    if user == 'john':
        return db['john']
    elif user == 'mary':
        return db['mary']
    else:
        abort(404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)
