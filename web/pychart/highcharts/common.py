'''
Common objects used in this package.
'''
import copy


class HighchartError(Exception):
    '''Base class for errors in the highchart package.'''


class DictBacked(object):
    '''
    A class that stores it's attributes in a dictionary
    and json encodes to the value of that dictionary.
    '''
    defaults = None
    available_options = []

    def __init__(self, **kwargs):
        self.options = {}
        if self.defaults is None:
            self.defaults = {}

        for key, value in self.defaults.items():
            # If it is a ConfigSection, we instantiate it.
            if hasattr(value, '__bases__') and ConfigSection in value.__bases__:
                self.options[key] = value()
            else:
                self.options[key] = copy.deepcopy(value)

        self.update(**kwargs)

    def __setattr__(self, attr, val):
        if attr in self.available_options:
            self.options[attr] = val
        else:
            super(DictBacked, self).__setattr__(attr, val)

    def __getattr__(self, attr):
        if attr in self.available_options:
            return self.__dict__['options'].get(attr, None)
        else:
            raise AttributeError

    def __delattr__(self, attr):
        if attr in self.available_options:
            del self.options[attr]
        else:
            raise AttributeError

    def update(self, **kwargs):
        '''A shortcut to set many options at once.'''
        for key, value in kwargs.items():
            if key in self.available_options:
                self.options[key] = value
            else:
                raise AttributeError('Invalid option %s' % key)

    def as_json(self):
        return self.options



class ConfigSection(DictBacked):
    '''Just a marker to specifiy that an object in a defaults list should be instantiated.'''

