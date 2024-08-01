from flask import Flask, render_template, request
import json_parcer

app = Flask(__name__)

blog_posts = json_parcer.load_data('data.json')

@app.route('/')
def index():
    # add code here to fetch the job posts from a file
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # We will fill this in the next step
        pass
    return render_template('add.html')


if __name__ == '__main__':
    app.run()