from flask import Flask, render_template, request, redirect, url_for
import json_parcer
import uuid

app = Flask(__name__)

blog_posts = json_parcer.load_data('data.json')


def generate_random_id():
    return str(uuid.uuid4())


def delete_post_by_id(post_id):
    for post in blog_posts:
        if post['id'] == post_id:
            blog_posts.remove(post)
            json_parcer.write_file('data.json', blog_posts)
            return True  # Return True if post is deleted
    return False  # Return False if post_id is not found


def fetch_post_by_id(post_id):
    for post in blog_posts:
        if post['id'] == post_id:
            return post


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


@app.route('/delete/<string:post_id>')
def delete(post_id):
    # Find the blog post with the given id and remove it from the list
    # Redirect back to the home page
    if delete_post_by_id(post_id):
            # Redirect to the home page after successful deletion
            return redirect(url_for('index'))

    # If post with given id is not found, redirect to the home page
    return redirect(url_for('inxex'))


@app.route('/update/<string:post_id>', methods=['GET', 'POST'])
def update(post_id):
    # Fetch the blog posts from the JSON file
    post = fetch_post_by_id(post_id)
    if post is None:
        # Post not found
        return "Post not found", 404
    
    if request.method == 'POST':
        # Update the post in the JSON file
        # Redirect back to index
        title = request.form.get('title')  # Get the title from the form
        author = request.form.get('author')  # Get the author from the form
        content = request.form.get('content')  # Get the content from the form
        new_post = {'id': post_id, 'title': title, 'author': author, 'content': content}
        blog_posts.append(new_post)  # Append the new post to the blog_posts list
        json_parcer.write_file('data.json', blog_posts)  # Save the updated blog posts to the JSON file
        return redirect(url_for('index')) 

    # Else, it's a GET request
    # So display the update.html page
    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run()