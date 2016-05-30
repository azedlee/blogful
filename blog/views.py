from flask import render_template, request, redirect, url_for, flash
from flask.ext.login import login_user, login_required, current_user, logout_user
from werkzeug.security import check_password_hash
from werkzeug.exceptions import Forbidden

from . import app
from .database import session, Entry, User

# How many entries per page (FYI, ALL_UPPERCASE_NAME is constant, by convention)
PAGINATE_BY = 10

@app.route("/")
@app.route("/page/<int:page>") # Designed to take you to a specific page of content
def entries(page=1):
    # Zero-indexed page
    page_index = page - 1
    
    args = request.args
    if "limit" in args:
        limit = int(args["limit"])
    else:
        limit = PAGINATE_BY
    
    # Use count method of a query object to find out how many entries there are in total
    count = session.query(Entry).count()
    
    # Index of the first entry you should see
    start = page_index * limit
    
    # Index of the last entry you should see
    end = start + limit
    
    # Total number of pages of content
    total_pages = (count - 1) // limit + 1
    
    # IF there is a page after the current one
    has_next = page_index < total_pages - 1
    
    # IF there is a page before the current one
    has_prev = page_index > 0
    
    entries = session.query(Entry)
    entries = entries.order_by(Entry.datetime.desc())
    entries = entries[start:end]
    # Render a template called entries.html, passing in the list of entries
    return render_template("entries.html", 
                            entries=entries,
                            has_next=has_next,
                            has_prev=has_prev,
                            page=page,
                            total_pages=total_pages,
                            limit=limit # parameter for the html
                            )

# The methods=["GET"] parameter specifies that the route will only be used for GET requests to the page
@app.route("/entry/add", methods=["GET"])
@login_required
def add_entry_get():
    return render_template("add_entry.html")

# The methods=["POST"] parameter specifies that the route will only accept POST requests.
@app.route("/entry/add", methods=["POST"])
@login_required
def add_entry_post():
    # The request.form dictionary to access the data submitted with your form and assign it to the correct fields in the entry
    entry = Entry(
        title=request.form["title"],
        content=request.form["content"],
        author=current_user
        )
    session.add(entry)
    session.commit()
    # The redirect function sends the user back to the front page once their entry has been created
    return redirect(url_for("entries"))

@app.route("/entry/<int:eid>")
def view_entry(eid):
    entry = session.query(Entry).filter_by(id=eid).first()
    return render_template("entry.html", entries=entry)
    
@app.route("/entry/<int:eid>/edit", methods=["GET"])
def edit_entry_get(eid):
    entry = session.query(Entry).filter_by(id=eid).first()
    
    if not all([entry.author, current_user]) or entry.author.id != current_user.id:
        raise Forbidden("Only Author can edit this post")
    
    title = entry.title
    content = entry.content
    return render_template("edit_entry.html",
                            title=title,
                            content=content,
                            entries=entry)

@app.route("/entry/<int:eid>/edit", methods=["POST"])
def edit_entry_post(eid):
    entry = session.query(Entry).filter_by(id=eid).first()
    
    if not all([entry.author, current_user]) or entry.author.id != current_user.id:
        raise Forbidden("Only Author can edit this post")
    
    entry.title=request.form["title"],
    entry.content=request.form["content"]
    session.commit()
    return redirect(url_for("entries"))
    
@app.route("/entry/<int:eid>/delete", methods=["GET"])
def delete_entry(eid):
    entry = session.query(Entry).filter_by(id=eid).delete()
    
    if not all([entry.author, current_user]) or entry.author.id != current_user.id:
        raise Forbidden("Only Author can delete this post")
    
    session.commit()
    return redirect(url_for("entries"))

@app.route("/login", methods=["GET"])
def login_get():
    return render_template("login.html")
    
@app.route("/login", methods=["POST"])
def login_post():
    email = request.form["email"]
    password = request.form["password"]
    user = session.query(User).filter_by(email=email).first()
    # Check if that user exists and use Werkzeug's check_password_hash function to compare
    # the password the user entered with the hash stored in the database
    if not user or not check_password_hash(user.password, password):
        # flash function stores a message which you can use when you render the next page
        flash("Incorrect username or password", "danger")
        return redirect(url_for("login_get"))
    
    # login_user function allows cookies (a small chunk of data) to the user's browser which is used to identify the user
    # when the user tries to access a protected resource, Flask-Login will make sure that they have the cookie set and allowed to access
    login_user(user)
    # After user logged in, redirect the user
    # Normally, redirect to user to the entries page
    # If there is a 'next' parameter, then redirect to that address
    # Flask uses this so that the user can access the intended resource after logging in
    return redirect(request.args.get('next') or url_for("entries"))

@app.route("/logout")
@login_required
def log_out():
    logout_user()
    flash("You have logged out.")
    return redirect(url_for("login_get"))