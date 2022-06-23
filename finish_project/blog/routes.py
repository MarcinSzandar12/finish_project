from flask import render_template, request, session, flash, redirect, url_for
from blog import app
from blog.models import Entry, db
from blog.forms import EntryForm, LoginForm

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

@app.route("/post/<int:entry_id>", methods=["POST"])
def delete_entry(entry_id):
    entry = Entry.query.filter_by(id=entry_id).first_or_404()
    errors = None
    try:
        db.session.delete(entry)
        db.session.commit()
        flash('Blog post was deleted!')
    except:
        errors = form.errors
    return render_template("homepage.html", errors=errors)


@app.route("/login/", methods=['GET', 'POST'])
def login():
   form = LoginForm()
   errors = None
   next_url = request.args.get('next')
   if request.method == 'POST':
       if form.validate_on_submit():
           session['logged_in'] = True
           session.permanent = True  # Use cookie to store session.
           flash('You are now logged in.', 'success')
           return redirect(next_url or url_for('index'))
       else:
           errors = form.errors
   return render_template("login_form.html", form=form, errors=errors)


@app.route('/logout/', methods=['GET', 'POST'])
def logout():
   if request.method == 'POST':
       session.clear()
       flash('You are now logged out.', 'success')
   return redirect(url_for('index'))

@app.route("/drafts/", methods=['GET'])
def list_drafts():
   drafts = Entry.query.filter_by(is_published=False).order_by(Entry.pub_date.desc())
   return render_template("drafts.html", drafts=drafts)


