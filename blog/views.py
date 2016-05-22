from flask import render_template, request, redirect, url_for

from . import app
from .database import session, Entry

# How many entries per page (FYI, ALL_UPPERCASE_NAME is constant, by convention)
PAGINATE_BY = 10

@app.route("/")
@app.route("/page/<int:page>") # Designed to take you to a specific page of content
def entries(page=1):
    # Zero-indexed page
    page_index = page - 1
    
    # Use count method of a query object to find out how many entries there are in total
    count = session.query(Entry).count()
    
    # Index of the first entry you should see
    start = page_index * PAGINATE_BY
    
    # Index of the last entry you should see
    end = start + PAGINATE_BY
    
    # Total number of pages of content
    total_pages = (count - 1) // PAGINATE_BY + 1
    
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
                            total_pages=total_pages
                            )

# The methods=["GET"] parameter specifies that the route will only be used for GET requests to the page
@app.route("/entry/add", methods=["GET"])
def add_entry_get():
    return render_template("add_entry.html")

# The methods=["POST"] parameter specifies that the route will only accept POST requests.
@app.route("/entry/add", methods=["POST"])
def add_entry_post():
    # The request.form dictionary to access the data submitted with your form and assign it to the correct fields in the entry
    entry = Entry(
        title=request.form["title"],
        content=request.form["content"]
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
    title = entry.title
    content = entry.content
    return render_template("edit_entry.html",
                            title=title,
                            content=content,
                            entries=entry)

@app.route("/entry/<int:eid>/edit", methods=["POST"])
def edit_entry_post(eid):
    entry = session.query(Entry).filter_by(id=eid).first()
    entry.title=request.form["title"],
    entry.content=request.form["content"]
    session.commit()
    return redirect(url_for("entries"))
    
@app.route("/entry/<int:eid>/delete", methods=["GET"])
def delete_entry(eid):
    entry = session.query(Entry).filter_by(id=eid).delete()
    session.commit()
    return redirect(url_for("entries"))