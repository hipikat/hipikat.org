
import os
from collections import Mapping


###
# Logging
###
LOGGING_SETTINGS_DEFAULTS = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {}
    'filters': {},
    'handlers': {},
    'loggers': {}
}
LOGFILE_DEFAULTS = { 
    'level': 'DEBUG',   # Level's set by loggers, so debug here catch anything.
    'class': 'logging.handlers.RotatingFileHandler',    # Keep files,
    'backupCount': 2,                                   # up to 3,
    'maxBytes': (10 ** 7)                               # of 10 MB each.
    'formatter': 'verbose',     # Including all potentailly useful information.
}


class LoggingSettings(dict):
    def __init__(*args, **kwargs):
        # Update self with dicts passed to the constructor.
        for arg in args:
            if isinstance(args, Mapping):
                self.deep_update(arg)
            else:
                raise TypeError("Only Mappings are accepted as arguments.")
        # Install the default keys/values, either passed in or defined above.
        self.deep_update(kwargs.pop('defaults') if 'defaults' in kwargs \
            else LOGGING_SETTINGS_DEFAULTS)
        # Set logfile defaults from a passed paramter or the defaults above.
        self.logfile_defaults = kwargs.pop('logfile_defaults') \
            if 'logfile_defaults' in kwargs else LOGFILE_DEFAULTS
        # Set the logfile_dir if one was specified.
        self.logfile_dir = kwargs.pop('logfile_dir') \
            if 'logfile_dir' in kwargs else None
        # Apply any remaining keyword arguments as attributes on self.
        for (k, v) in kwargs.iteritems():
            self[k] = v

    def deep_update(self, u):
        """
        Deep, non-destructive updating for dictionaries.
        From: http://stackoverflow.com/a/3233356/218397
        """
        for (k, v) in u.iteritems():
            if isinstance(v, Mapping):
                self[k] = LoggingSettings.deep_update(
                    self.get(k, LoggingSettings()), v
                )
            else:
                self[k] = u[k]
        return self

    def add_logfile_handler_for_app(app_name=None, *prefixes, **kwargs):
        """ 
        Creates an '[prefix1-prefix2-...](app_name)-logfile' logging handler,
        using LOGFILE_DEFAULTS or a passed logfile_defaults, which write to
        [prefix1.prefix2.etc.]app_name.log, in the directory self.log_dir (a
        string to a writable directory you should set when initialising an
        instance of this class (or whenever, really)).
        """
        # Get the full path to a logfile to be written or die trying.
        if 'file_path' in kwargs:
            file_path = kwargs.pop('file_path')
        else:
            try:
                logfile_dir = kwargs.get('logfile_dir', self.logfile_dir)
            except KeyError:
                raise RuntimeError("A logfile_dir attribute must be set on " +
                "this class or passed to this function as a keyword argument.")
        if logfile_dir[-1] != os.sep:
            logfile_dir += os.sep
        dot_prefix = ".".join(prefixes) + '.' if prefixes else ''
        file_path = dot_prefix + app_name + '.log'
        # Construct a name for the handler, which is set in the logger.
        dash_prefix = "-".join(prefixes) + '-' if prefixes else ''
        handler_name = dash_prefix + app_name + '_logfile'
        # Set the properties of the handler from known defaults and kwargs.
        self['handlers'][handler_name] = self.logfile_defaults.copy() \
            if 'defaults' not in kwargs else kwargs.pop('defaults')
        self['handlers'][handler_name]['filename'] = file_path
        # Set any remaining keywoard arguments as attributes of the handler.
        for (k, v) in kwargs.iteritems():
            self['handlers'][handler_name][k] = v

    def add_logfile_handlers_for_apps(*apps, **kwargs):
        """
        Convenience for setting logfile handlers for multiple apps
        simultaneously. Same as add_logfile_handler_for_app, but *prefixes can
        be supplied as a list, or a single prefix as a string, via the keyword
        arguments prefixes or prefix, respectively.
        """
        prefixes = kwargs.pop('prefixes') if 'prefixes' in kwargs \
            else [kwargs.pop('prefix', '')]
        for app in apps:
            self.add_logfile_handler_for_app(app, prefixes, **kwargs)
