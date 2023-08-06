''' Mutable Primitives '''


class Mutable(object): # pylint: disable=useless-object-inheritance
    ''' Base class for mutable primitives '''
    def __init__(self, val, base):
        assert isinstance(val, base)
        self.base = base
        self.val = val

    def get(self):
        ''' get raw value of mutable '''
        return self.val

    def set(self, val):
        ''' set raw value of mutable '''
        self.val = val

    def __eq__(self, other):
        return self.val == other

    def __ne__(self, other):
        return self.val != other

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, self.val)

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.val)
