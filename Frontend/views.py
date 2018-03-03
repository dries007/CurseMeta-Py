import flask
import logging
import werkzeug.exceptions as exceptions

from . import app


_LOGGER = logging.getLogger("Views")
_LOGGER.setLevel(logging.DEBUG)


@app.errorhandler(Exception)
def any_error(e: Exception):
    from jinja2 import TemplateNotFound
    if isinstance(e, TemplateNotFound):
        e = exceptions.NotFound()

    if not isinstance(e, exceptions.HTTPException):
        e = exceptions.InternalServerError()
        _LOGGER.exception("Error handler non HTTPException: %s", e)

    return flask.jsonify({'error': True, 'status': e.code, 'description': e.description}), e.code


@app.route('/<path:p>')
@app.route('/')
def page(p='index'):
    return flask.render_template('{}.html'.format(p))
