#!/usr/bin/env python

"""
server.py

written by: Oliver Cordes 2022-03-29
changed by: Oliver Cordes 2022-05-28

"""

__author__    = 'Oliver Cordes'
__version__   = '0.0.2'
__copyright__ = f'2022 by {__author__}'


# used for the cli extension
import click
from flask.cli import AppGroup

from flask import g, request, session

# the defaults for the APP
from app import create_app, db, babel
from app.models import User #, WhitelistUser, WhitelistGroup

import logging

# load extra local variables from .env in the local directory
from dotenv import load_dotenv
load_dotenv()




# create an application
application = create_app()
#app = application.app
app = application


"""
make_shell_context

the function provides default variables in the flask shell
environment
"""
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User } #, 'Whitelistuser': Whitelistuser,
#        'Whitelistgroup': Whitelistgroup }


"""
utility_processor

the function defines some extra variables in the jinja2
environment for the templates, the context of the
current app status is used!
"""
@app.context_processor
def utility_processor():
    return { 'app_version': __version__,
             'app_copyright': __copyright__,
             'app_name': app.config['APP_NAME'],
             'languages': app.config['LANGUAGES'],
             'flags': app.config['FLAGS'],
             'cur_lang': session.get('language', 'en')}



"""
babel configurations

"""

@babel.localeselector
def get_locale():
    if request.args.get('language'):
        session['language'] = request.args.get('language')
    return session.get('language', 'en')


@babel.timezoneselector
def get_timezone():
    user = getattr(g, 'user', None)
    if user is not None:
        return user.timezone


# test this file
if __name__ == "__main__":
    app.run(
    #socketio.run(app,
            host='0.0.0.0',
            port=4555,
            debug=True,
            extra_files=['./app/translations/de/LC_MESSAGES/messages.mo'],
            #extra_files=['./app/api/openapi.yaml']
            )
    #app.run(port=4555)
