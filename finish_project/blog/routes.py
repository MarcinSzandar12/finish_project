from flask import render_template, request
from blog import app
from blog.models import Entry, db
from blog.forms import EntryForm

@app.route("/")
def index():
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())

    return render_template("homepage.html", all_posts=all_posts)

@app.route("/post/<int:entry_id>", methods=["GET", "POST", "PUT"])
def create_or_edit_entry(entry_id):
    entry_2 = Entry.query.filter_by(id=entry_id).first_or_404()
    form_1 = EntryForm()
    form_2 = EntryForm(obj=entry_2)
    errors = None
    if request.method == 'POST':
        if form_1.validate_on_submit():
           entry = Entry(
               title=form_1.title.data,
               body=form_1.body.data,
               is_published=form_1.is_published.data
           )
           db.session.add(entry)
           db.session.commit()
        else:
           errors = form_1.errors
    elif request.method == 'PUT':
        if form_2.validate_on_submit():
           form_2.populate_obj(entry_2)
           db.session.commit()
        else:
           errors = form_2.errors
    return render_template("entry_form.html", form=form_2, errors=errors)


