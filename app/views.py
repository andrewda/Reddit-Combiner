from flask import render_template
from app import app
import utils
from . import args

@app.route("/")
@app.route("/index")
def index():
    image, text = utils.get_top_submissions(args["text_subreddit"], args["image_subreddit"], int(args["limit"]))

    return render_template("base.html", image=image, text=text)
