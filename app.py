from flask import Flask, render_template, request, redirect, url_for
import json_parcer
import uuid

app = Flask(__name__)

blog_posts = json_parcer.load_data('data.json')


def generate_random_id():
    return str(uuid.uuid4())


@app.route('/')
def index():
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form.get('title')  # Get the title from the form
        author = request.form.get('author')  # Get the author from the form
        content = request.form.get('content')  # Get the content from the form
        post_id = generate_random_id()  # Generate a random ID for the blog post
        new_post = {'id': post_id, 'title': title, 'author': author, 'content': content}
        blog_posts.append(new_post)  # Append the new post to the blog_posts list
        json_parcer.write_file('data.json', blog_posts)  # Save the updated blog posts to the JSON file
        return redirect(url_for('index')) 
    return render_template('add.html')


if __name__ == '__main__':
    app.run()