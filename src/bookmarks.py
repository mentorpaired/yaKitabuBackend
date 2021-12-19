from flask import Blueprint

bookmarks = Blueprint("bookmarks", __name__, url_prefix="login/user/bookmarks")

@bookmarks.get('/')
def get_all():
    return []

@bookmarks.get("/me")
def me():
    return {"user": "me"}
 