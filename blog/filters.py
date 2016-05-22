from . import app
from flask import Markup
import mistune as md

@app.template_filter()
def markdown(text):
    return Markup(md.markdown(text,escape=True)) ### Question - whats escape=True?

# Markdown is a text-to-HTML conversion tool
# Markup marks a variable you trust to be "safe" in HTML format
# mistune - markdown parser with render features

@app.template_filter()
def dateformat(date, format):
    if not date:
        return None
    return date.strftime(format)

# template_filter() decorator registers a customer filter to Flask's Jinja environment
# inside the brackets allows you the customer the name e.g @app.template_filter("formatdate")