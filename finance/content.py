from flask import render_template, session, Blueprint, request, flash, redirect, jsonify
from .helpers import login_required, db
from datetime import datetime
from random import randint
import json
from finance.model.database import Note, Blog


"""  Routes in 'actions blueprint'  ===>  /createblog   /blog   /note   /delete-note     """

content = Blueprint("content", __name__)


@content.route("/blog")
@login_required
def blog():

    # TABLE =====> blog (id, user_id, title, author, content, date, img)
    blogs = db.execute("SELECT * FROM blog").fetchall()

    return render_template("blog.html", blogs=blogs)


@content.route("/createblog", methods=["POST",'GET'])
@login_required
def createblog():

    user_id = session['user_id']
    
    if request.method == "POST":

        title = request.form.get("title")
        author = request.form.get("author")
        content = request.form.get("content")
        img = request.form.get("img")
        
        # --------------------------------------------------------------------------------

        # if user didn't provide an img, give him a random one 
        photos = ['static/blog/1.jpg', 'static/blog/2.jpg', 'static/blog/3.jpg', 'static/blog/4.jpg',
                'static/blog/5.jpg', 'static/blog/6.jpg', 'static/blog/7.jpg', 'static/blog/8.jpg']

        if(not img):
            img = photos[randint(0,7)]

        # --------------------------------------------------------------------------------

        if not title or not author or not content:
            flash("Missing title/author/content",category="error")
            return redirect("blog")

        # --------------------------------------------------------------------------------

        time = datetime.now()
        date = time.strftime("%Y-%m-%d")

        Blog.add(user_id, title, author, content, date, img)
            
        flash("Blog posted Successfuly",category="success")
        return redirect("/blog")

    return render_template("createBlog.html")


@content.route("/delete-blog", methods=["POST"])
@login_required
def delete_blog():

    response = json.loads(request.data)

    blogId = response['jsonkey']
    
    Blog.delete(blogId)

    return jsonify("Blog successfuly deleted")


@content.route("/note", methods=["POST", "GET"])
@login_required
def note():

    user_id = session["user_id"]

    if request.method == "POST":
        note = request.form.get("note")

        if not note:
            flash("No Note", category="error")
            return redirect("/note")

        # --------------------------------------------------------------------------------

        Note.add(user_id, note)

        flash("Note added successfuly", category="success")

        return redirect("/note")

    # TABLE =====> notes (id, user, data)
    notes = db.execute("SELECT * FROM note WHERE user_id = ?", (user_id,)).fetchall()

    return render_template("note.html", notes=notes)



@content.route("/delete-note", methods=["POST"])
@login_required
def delete_note():

    # Except  {'jsonKey': note_id }
    response = json.loads(request.data)

    note_id = response['jsonKey']

    Note.delete(note_id)

    return jsonify('Successfuly note deleted')






