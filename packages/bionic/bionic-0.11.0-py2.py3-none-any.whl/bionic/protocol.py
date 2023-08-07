from . import protocols
from .utils.misc import oneline

# These are callable with or without arguments.  See BaseProtocol.__call__ for
# why we instantiate them here.
picklable = protocols.PicklableProtocol()  # noqa: F401
dillable = protocols.DillableProtocol()  # noqa: F401
dask = protocols.DaskProtocol()  # noqa: F401
image = protocols.ImageProtocol()  # noqa: F401
numpy = protocols.NumPyProtocol()  # noqa: F401
yaml = protocols.YamlProtocol()  # noqa: F401
path = protocols.PathProtocol()  # noqa: F401
geodataframe = protocols.GeoPandasProtocol()  # noqa: F401
json = protocols.JsonProtocol()  # noqa: F401


def frame(func=None, file_format=None, check_dtypes=None):
    """
    Decorator indicating that an entity will always have a pandas DataFrame
    type.

    The frame values will be serialized to either Parquet (default) or Feather.
    Parquet is more popular, but some types of data or frame structures are
    only supported by one format or the other.  In particular, ordered
    categorical columns are supported by Feather and not Parquet.

    This decorator can be used with or without arguments:

    .. code-block:: python

        @frame
        def dataframe(...):
            ...

        @frame(file_format='feather')
        def dataframe(...):
            ...

    Parameters
    ----------
    file_format: {'parquet', 'feather'} (default: 'parquet')
        Which file format to use when saving values to disk.
    check_dtypes: boolean (default: True)
        Check for column types not supported by the file format.  This
        check is best-effort and not guaranteed to catch all problems.  If
        an unsupported data type is found, an exception will be thrown at
        serialization time.
    """

    # If the first argument is present, we were (hopefully) used as a decorator
    # without any other arguments.
    if func is not None:
        if file_format is not None or check_dtypes is not None:
            raise ValueError("frame can't be called with both a function and keywords")
        if not callable(func):
            raise ValueError(
                oneline(
                    """
                frame must be used either (a) directly as a decorator or
                (b) with keyword arguments;
                it can't take positional arguments.
                """
                )
            )
        return protocols.ParquetDataFrameProtocol()(func)

    # Otherwise, we have arguments and should return a decorator.
    if file_format is None or file_format == "parquet":
        kwargs = {}
        if check_dtypes is not None:
            kwargs["check_dtypes"] = check_dtypes
        return protocols.ParquetDataFrameProtocol(**kwargs)
    elif file_format == "feather":
        return protocols.FeatherDataFrameProtocol()
    else:
        raise ValueError(
            oneline(
                f"""
            file_format must be one of {'parquet', 'feather'};
            got {file_format!r}"""
            )
        )


# These need to be called with arguments.
enum = protocols.EnumProtocol  # noqa: F401
type = protocols.TypeProtocol  # noqa: F401
