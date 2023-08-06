import datetime as dt
import json
from typing import Any

from pytz import timezone


class JSONDateTimeDecoder(json.JSONDecoder):
    """Decoder for the standard json library to decode JSON into datetime.
    To be used together with ``JSONDateTimeEncoder``.

    Example:

        .. code-block:: python

            message = json.loads(message_json, cls=JSONDateTimeDecoder)

    """

    def __init__(self, *args, **kwargs) -> None:
        json.JSONDecoder.__init__(
            self, object_hook=self.dict_to_object, *args, **kwargs
        )

    def dict_to_object(self, dct: dict) -> object:
        if "__type__" not in dct:
            return dct

        type_str = dct.pop("__type__")
        zone, _ = dct.pop("tz")
        dct["tzinfo"] = timezone(zone)
        try:
            dateobj = dt.datetime(**dct)
            return dateobj
        except (ValueError, TypeError):
            dct["__type__"] = type_str
            return dct


class JSONDateTimeEncoder(json.JSONEncoder):
    """Encoder for the standard json library to encode datetime into JSON.
    To be used together with ``JSONDateTimeDecoder``.

    Example:

        .. code-block:: python

            message_json = json.dumps(message, cls=JSONDateTimeEncoder)

    """

    def default(self, o: Any) -> Any:
        if isinstance(o, dt.datetime):
            return {
                "__type__": "datetime",
                "year": o.year,
                "month": o.month,
                "day": o.day,
                "hour": o.hour,
                "minute": o.minute,
                "second": o.second,
                "microsecond": o.microsecond,
                "tz": (o.tzinfo.tzname(o), o.utcoffset().total_seconds()),
            }
        else:
            return json.JSONEncoder.default(self, o)
