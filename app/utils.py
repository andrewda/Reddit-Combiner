import praw
import sys
import os
import configargparse
import random
import re


def get_args():
    default_config = []

    if "-cf" not in sys.argv and "--config" not in sys.argv:
        default_config = [os.getenv("REDDIT_COMBINER_CONFIG", os.path.join(os.path.dirname(__file__), "../config/config.ini"))]

    parser = configargparse.ArgParser(default_config_files=default_config, auto_env_var_prefix="Earthporn_ShowerThoughts_")

    parser.add_argument("-t", "--text_subreddit", help="display text overlay from top posts in this subreddit")
    parser.add_argument("-i", "--image_subreddit", help="display background image from top post of subreddit")
    parser.add_argument("-l", "--limit", default=35, help="limit to this many top posts")

    parser.add_argument("-ua", "--user_agent", help="reddit user agent")
    parser.add_argument("-cs", "--client_secret", help="reddit client secret")
    parser.add_argument("-ci", "--client_id", help="reddit client id")

    return vars(parser.parse_args())

args = get_args()

r = praw.Reddit(user_agent=args["user_agent"], client_secret=args["client_secret"], client_id=args["client_id"])

def get_top_submissions(t_sub, i_sub, limit):
    image_sub = r.subreddit(i_sub)
    text_sub = r.subreddit(t_sub)

    top_images = image_sub.top(limit = limit)
    top_texts = text_sub.top(limit = limit)

    image_list = [sub for sub in top_images]
    text_list = [sub for sub in top_texts]

    image_url = get_image_url(image_list[random.randint(0, limit - 1)].url)
    text = text_list[random.randint(0, limit - 1)].title

    return image_url, text

def get_image_url(url):
    if "imgur.com" in url and ".png" not in url and ".jpg" not in url:
        prog = re.compile(".*imgur.com/(.*)")
        result = prog.match(url)

        url = "https://i.imgur.com/" + result.group(1) + ".png"

    return url
