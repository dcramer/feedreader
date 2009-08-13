import dateutil.parser

__all__ = ('parse_date',)

def parse_date(date_string):
    date_string = unicode(date_string)

    return dateutil.parser.parse(date_string)