import typing

T = typing.TypeVar("T")


@typing.overload
def list_(
        v: typing.Iterable[T],
        /,
) -> typing.List[T]:
    ...


@typing.overload
def list_(
        v: T,
        /,
) -> typing.List[T]:
    ...


@typing.overload
def list_(
        v: typing.Any,
        class_or_tuple: typing.Union[
            typing.Type[T],
            typing.Tuple[typing.Type[T], ...],
        ] = ...,
        /,
) -> typing.List[T]:
    ...
