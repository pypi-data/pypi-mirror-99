import asyncio
import contextlib
from collections.abc import Callable, Collection, Iterable, Mapping
from typing import Any, Optional, Protocol, TypeVar, Union

import yarl

from .base import PathParameters, QueryParameters


class Closable(Protocol):
    async def close(self) -> None:
        ...


TClosable = TypeVar("TClosable", bound=Closable)


async def close_single(item: TClosable) -> None:
    with contextlib.suppress(Exception):
        await item.close()


T = TypeVar("T")


async def close_futures(items: Collection[asyncio.Future[T]], as_close: Callable[[T], TClosable]) -> None:
    for item in items:
        if item.cancelled():
            continue
        try:
            await close_single(as_close(await item))
        except asyncio.CancelledError:
            if not item.cancelled():
                raise


async def close(items: Collection[TClosable]) -> None:
    for item in items:
        await close_single(item)


async def cancel_futures(futures: Collection[asyncio.Future[T]]) -> None:
    for future in futures:
        if future.done():
            continue
        future.cancel()


def substitute_path_parameters(url: yarl.URL, parameters: Optional[PathParameters] = None) -> yarl.URL:
    if not parameters:
        return url

    path = url.path
    for name, value in parameters.items():
        path = path.replace(f"{{{name}}}", str(value))

    build_parameters: dict[str, Any] = dict(
        scheme=url.scheme,
        user=url.user,
        password=url.password,
        host=url.host,
        port=url.port,
        path=path,
        query=url.query,
        fragment=url.fragment,
    )

    return yarl.URL.build(**{k: v for k, v in build_parameters.items() if v is not None})


def build_query_parameters(query_parameters: QueryParameters) -> dict[str, Union[str, list[str]]]:
    parameters: dict[str, Union[str, list[str]]] = {}
    for name, value in query_parameters.items() if isinstance(query_parameters, Mapping) else query_parameters:
        if value is None:
            continue
        if not isinstance(value, str) and isinstance(value, Iterable):
            values = [str(v) for v in value if v is not None]
            if not values:
                continue

            if name in parameters:
                existing_value = parameters[name]
                if isinstance(existing_value, str):
                    parameters[name] = [existing_value, *values]
                else:
                    parameters[name] = [*existing_value, *values]
            else:
                parameters[name] = values
        else:
            if name in parameters:
                existing_value = parameters[name]
                if isinstance(existing_value, str):
                    parameters[name] = [existing_value, str(value)]
                else:
                    parameters[name] = [*existing_value, str(value)]
            else:
                parameters[name] = str(value)
    return parameters


def try_parse_float(value: Optional[str]) -> Optional[float]:
    if value is None:
        return None

    try:
        return float(value)
    except ValueError:
        return None
