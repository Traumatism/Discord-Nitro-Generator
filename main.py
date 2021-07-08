"""
TODO:

    - socks4 / socks5 / http proxies support (only 4 for the moment)
    - send the code it to a webhook
    - remove dead proxies

"""

import itertools
import asyncio
import re

from core.logging import Logging
from core.checker import Checker
from core.generator import Generator

async def main():
    Logging.console.print(
        '''

[red]+[bright_black] -- [magenta]Nitro Generator & Checker[/magenta] --[/bright_black]+[/red]
[red]+[bright_black]- -- [bright_blue]twitter.com/toastakerman[/bright_blue] --[/bright_black]+[/red]
[red]+[bright_black]- -- -- [cyan]github.com/traumatism[/cyan] --[/bright_black]+[/red]
    
        '''
    )

    # load proxies from 'proxies.txt'
    with open('proxies.txt', 'r') as file:
        proxies = set([
            (4, str(line.split(':')[0]), int(line.split(':')[1])) # (type: int, ip_address: str, port: int)
            for line in [x.strip() for x in file.readlines()]
            if re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}', line) # validate the line
        ])

        Logging.success(f'loaded {len(proxies)} proxies.')

    proxies = itertools.cycle(proxies)

    while 1:
        codes = Generator.generate() # generate 1k potential gift codes.
        
        Logging.success(f'generated {len(codes)} potential gift codes.')
        
        checker = Checker() # initialize the checker class

        # load the futures
        futures = []

        for code in codes:

            proxy = proxies.__next__() # choose the proxy

            futures.append(asyncio.create_task(
                checker.check(code, proxy)
            ))

        Logging.info(
            f'executing {len(futures)} tasks asynchronously...'
        )

        # execute the futures
        await asyncio.gather(
            *futures
        )

asyncio.run(
    main()
)