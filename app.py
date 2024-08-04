from flask import Flask, render_template, request, redirect, url_for
import json_parcer
import uuid


app = Flask(__name__)
blog_posts = json_parcer.load_data('data.json')


def generate_random_id():
    """
    Generate a random ID using UUID for the blog post.
    
    Returns:
    str: A randomly generated UUID to be used as the ID for the blog post.
    """
    return str(uuid.uuid4())


def delete_post_by_id(post_id):
    """
    Delete a blog post by its ID from the blog_posts list and update the JSON file.
    
    Args:
    post_id (str): The ID of the post to be deleted.

    Returns:
    bool: True if post is deleted successfully, False if post_id is not found in the list.
    """
    for post in blog_posts:
        if post['id'] == post_id:
            blog_posts.remove(post)
            json_parcer.write_file('data.json', blog_posts)
            return True  # Return True if post is deleted
    return False  # Return False if post_id is not found


def fetch_post_by_id(post_id):
    """
    Fetch a blog post by its ID from the blog_posts list.
    
    Args:
    post_id (str): The ID of the post to be fetched.

    Returns:
    dict or None: The blog post if found, None if the post_id is not found in the list.
    """
    for post in blog_posts:
        if post['id'] == post_id:
            return post


@app.route('/')
def index():
    """
    Render the index.html template with the blog_posts and display it on the home page.
    """
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    Add a new blog post to the blog_posts list and save it to the JSON file.

    If the request method is POST:
    - Get the title, author, and content from the form.
    - Generate a random ID for the blog post.
    - Append the new post to the blog_posts list.
    - Save the updated blog posts to the JSON file.
    - Redirect to the home page.

    If the request method is GET:
    - Render the add.html template for adding a new blog post.
    """
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
    """
    Delete a blog post by its ID and then redirect back to the home page.
    
    Args:
    post_id (str): The ID of the post to be deleted.
    """
    # Find the blog post with the given id and remove it from the list
    # Redirect back to the home page
    if delete_post_by_id(post_id):
            # Redirect to the home page after successful deletion
            return redirect(url_for('index'))

    # If post with given id is not found, redirect to the home page
    return redirect(url_for('index'))


@app.route('/update/<string:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """
    Update a blog post in the blog_posts list and save it to the JSON file.

    Args:
    post_id (str): The ID of the post to be updated.

    If the request method is POST:
    - Update the title and content of the blog post.
    - Save the updated blog posts to the JSON file.
    - Redirect to the home page.
    
    If the request method is GET:
    - Render the update.html template with the current post details for updating the blog post.
    """
    post = fetch_post_by_id(post_id)
    if post is None:
        # Post not found
        return "Post not found", 404
    
    if request.method == 'POST':
        # Update the post in the blog_posts list
        title = request.form.get('title')  # Get the title from the form
        content = request.form.get('content')  # Get the content from the form
        for blog_post in blog_posts:
            if blog_post['id'] == post_id:
                blog_post['title'] = title  # Update the title
                blog_post['content'] = content  # Update the content
                json_parcer.write_file('data.json', blog_posts)  # Save the updated blog posts to the JSON file
                return redirect(url_for('index'))  # Redirect back to the index page
    
    # Display the update.html page with the current post details
    return render_template('update.html', post_id=post_id)


if __name__ == '__main__':
    app.run()