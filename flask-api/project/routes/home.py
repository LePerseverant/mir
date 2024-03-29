from sqlite3 import Error
from flask import Blueprint, request


bp = Blueprint("home", __name__, url_prefix="/home")
