import asyncio
import aiohttp

from aiohttp_socks import ProxyConnector

from core.logging import Logging

from typing import Tuple

class Checker:
    def __init__(self) -> None:
        self.url = 'https://discord.com/api/v9/entitlements/gift-codes/%s?with_application=true&with_subscription_plan=true'

    async def check(self, code: str, proxy: Tuple[int, str, int]) -> Tuple[str, bool]:
        """ Check a potential Nitro gift code. """

        url = self.url % code
        type, proxy_host, proxy_port = proxy

        try:
            async with aiohttp.ClientSession(connector=ProxyConnector.from_url('socks%d://%s:%s' % (type, proxy_host, proxy_port))) as session:
                async with session.get(url=url) as response:
                    json_data = await response.json()

                    # Code is valid
                    if response.status == 200:
                        Logging.success(
                            f'valid code: {code}'
                        )

                        return (code, True)

                    # response
                    message = json_data['message']

                    # We have been rate limited by discord, need to wait a given time
                    if message == 'You are being rate limited.':

                        to_wait = json_data['retry_after'] # need to wait that time

                        Logging.info(
                            f'{proxy_host}:{proxy_port} have been rate limited, waiting {to_wait}s.'
                        )

                        await asyncio.sleep(to_wait + 1) # wait until we get "unbanned" by Discord, adding a second for security

                        return (code, None)

                    # Code is invalid
                    elif message == 'Unknown Gift Code':
                        Logging.info(
                            f'invalid code: {code}'
                        )
                        return (code, False)

                    else:
                        Logging.info(
                            f'unknown message (code: {code}): {message}'
                        )

        except Exception:
            pass

        return (code, None)