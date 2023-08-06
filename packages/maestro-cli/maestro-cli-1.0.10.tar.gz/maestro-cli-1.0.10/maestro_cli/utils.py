import datetime
import decimal
import json


class ComplexEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        if isinstance(obj, datetime.timedelta):
            return obj.total_seconds()
        if isinstance(obj, decimal.Decimal):
            return float(obj)

        return super(ComplexEncoder, self).default(obj)


def json_dumps(datas):
    """
    JSON Pretty dumping
    """
    return json.dumps(
        datas,
        cls=ComplexEncoder
    )


def deep_get(source_datas, keys, default=None):
    """
    Accessor for getting value into nested dicts
    mixed with list.
    """
    def accessor(datas, key):
        try:
            return datas.get(key, default)
        except AttributeError:
            try:
                return datas[int(key)]
            except (IndexError, ValueError, TypeError):
                return default

    return reduce(accessor, keys.split('.'), source_datas)
