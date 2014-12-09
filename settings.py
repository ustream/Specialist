__author__ = 'deathowl'
ALCHEMY_URL = 'sqlite:///specialist.db' #Any valid SQLAlchemy connection string.
LISTEN_HOST = "127.0.0.1"
LISTEN_PORT = 5000


# Loading site-specific override settings
import os
special_settings_path = os.getenv('SPECIALIST_SETTINGS_PATH')
if special_settings_path is not None:
    try:
        print 'Loading user-specified settings from %s' % special_settings_path
    except IOError:
        pass
    import imp
    special_settings_module = imp.load_source('special_settings', special_settings_path)
    globals().update(dict([(key, value) for key, value in special_settings_module.__dict__.iteritems() if not key.startswith('__')]))

try:
    print 'Starting with settings', dict([(key, value) for key, value in globals().items() if key.isupper()])
except IOError:
    pass