
class AccesRule(object):
    owner_type = 'others'
    owner_id = None
    protocol = True  # any protocol is allowed
    ip = True   # any ip allowed
    date = True  # any date allowed
    time_interval = True  # any time interval allowed
    effective_rights = []  # no read/write/execute allowed
    operators = []  # positional operands 0, 1, 2

    def __init__(self, *args, **kwargs):
        for k in ['owner_type', 'owner_id', 'protocol', 'ip', 'date',
                  'time_interval']:
            value = kwargs.get(k)
            if value:
                self.__dict__[k] = value

    def __str__(self):
        x = ''
        for k in ['owner_type', 'owner_id', 'protocol', 'ip', 'date',
                  'time_interval', 'effective_rights', 'operators']:
            x += "'%s'>%s, " % (k, self.__dict__.get(k))
        return x
