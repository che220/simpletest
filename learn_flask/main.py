from flask import Flask, url_for, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, index!'

@app.route('/hello')
def hello():
    return 'Hello, hello'

# RESTful API
@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return 'Subpath %s' % subpath

@app.route('/login', methods=['GET', 'POST'])
def login():
    request.get_json(force=True)
    if request.method == 'POST':
        print('JSON request:', request.json)
        resp = {'status' : 'posted image'}
        return jsonify(resp)
    else:
        return 'GET done. But I do not like it!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
    exit(0)

    with app.test_request_context():
        print(url_for('index'))
        print(url_for('hello'))
        print(url_for('show_user_profile', username='John Doe'))
