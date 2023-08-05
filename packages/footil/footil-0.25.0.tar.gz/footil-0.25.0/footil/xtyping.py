"""Module to check or manipulate various types."""
import collections
import six
from functools import singledispatch


def is_iterable(obj):
    """Return True if object is iterable, but is not a string."""
    return (isinstance(obj, collections.abc.Iterable) and not
            isinstance(obj, six.string_types))


@singledispatch
def bytes_to_str(val, encoding='utf-8', errors='strict') -> str:
    """Convert bytes string to string.

    If val is string, it will be returned unmodified.

    Args:
        encoding (str): the encoding with which to decode the bytes. (
            default: {'utf-8'})
        errors (str): The error handling scheme to use for the handling
            of decoding errors. (default: {'strict'}) meaning that
            decoding errors raise a UnicodeDecodeError. Other possible
            values are 'ignore' and 'replace' as well as any other name
            registered with codecs.register_error that can handle
            UnicodeDecodeErrors.

    Returns:
        str

    """
    return val.decode(encoding=encoding, errors=errors)


@bytes_to_str.register(str)
def __str_to_str(val, *args, **kw):
    return val


@singledispatch
def str_to_bytes(val, encoding='utf-8', errors='strict') -> bytes:
    """Convert string to bytes string.

    If val is bytes, it will be returned unmodified.

    Args:

        encoding (str): encode val using the codec registered for
            encoding (default: {'utf-8'}).
        errors (str): may be given to set a different error handling
            scheme. (default: {'strict'}) meaning that encoding errors
            raise a UnicodeEncodeError. Other possible values are
            'ignore', 'replace' and 'xmlcharrefreplace' as well as any
            other name registered with codecs.register_error that can
            handle UnicodeEncodeErrors.

    Returns:
        bytes

    """
    return val.encode(encoding=encoding, errors=errors)


@str_to_bytes.register(bytes)
def __bytes_to_bytes(val, *args, **kw):
    return val
