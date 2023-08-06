import asyncio
import logging
import time
from typing import Callable, Awaitable

logger = logging.getLogger(__name__)


def timestamp() -> int:
    """
    In milliseconds (UTC based)
    """
    return int(round(time.time() * 1000))


class RetryException(Exception):
    pass


async def retry_with_backoff(
    wrapped: Callable[[], Awaitable],
    retries: int = 5,
    retry_exponent: float = 3.0,
    exc_type: Exception = Exception,
):
    for trial in range(1, retries + 1):
        try:
            await wrapped()
            return
        except exc_type as e:
            sleep = retry_secs(retries, retry_exponent)[trial - 1]
            logger.warning(f"{wrapped} failed. Retrying in {sleep} secs", exc_info=e)
            await asyncio.sleep(sleep)
    raise RetryException(f"Failed to execute {wrapped}. Giving up after {trial} trials")


def retry_secs(retries, retry_exponent):
    return [int(i ** retry_exponent) for i in range(1, retries + 1)]
