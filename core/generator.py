import string
import random

from typing import List

class Generator:

    @staticmethod
    def generate(limit: int = 1000) -> List[str]:
        """ Generate (limit) potential nitro codes. """

        codes = []

        while len(codes) <= limit:
            code = ''.join(random.choices(
                string.ascii_letters + string.digits, k=24
            ))

            if code in codes:
                continue

            codes.append(code)

        return codes[:-1]