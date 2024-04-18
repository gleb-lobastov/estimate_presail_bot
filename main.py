import asyncio
import logging

from aiogramm_bot import start_polling


async def main():
    logging.basicConfig(level=logging.INFO)
    await start_polling()


if __name__ == "__main__":
    asyncio.run(main())
