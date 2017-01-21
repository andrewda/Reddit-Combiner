from flask import Flask
from utils import get_args

args = get_args()
app = Flask(__name__)
from app import views
