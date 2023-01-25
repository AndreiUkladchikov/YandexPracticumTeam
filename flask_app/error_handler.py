import re
from http import HTTPStatus

from flask import jsonify
from werkzeug.exceptions import HTTPException

from app import app
from errors import ERROR_BASE_CODE, SERVER_ERROR


@app.errorhandler(Exception)
def handle_exception(e):

    if isinstance(e, HTTPException):
        return {
            "code": ERROR_BASE_CODE,
            "msg": re.sub(
                pattern=re.compile("<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});"),
                repl="",
                string=e.get_description(),
            ),
        }, e.code

    elif isinstance(e, Exception):
        return SERVER_ERROR, HTTPStatus.INTERNAL_SERVER_ERROR
