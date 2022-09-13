import os
import asyncio
from datetime import datetime as dt

import asyncpg


postgres_host = os.environ.get("POSTGRES_HOST")
postgres_port = os.environ.get("POSTGRES_PORT")

connection_string = "postgres://{}:{}@{}:{}/{}".format(
    os.environ.get("POSTGRES_USER"),
    os.environ.get("POSTGRES_PASSWORD"),
    postgres_host,
    postgres_port,
    os.environ.get("POSTGRES_DB"),
)


async def await_connection():
    while True:
        try:
            conn = await asyncpg.connect(connection_string)
            conn.close()
        except Exception as e:
            print(str(e))
            print(
                f"{str(dt.now())} - waiting for postgres at {postgres_host} {postgres_port}..."
            )
        else:
            print(
                f"{str(dt.now())} - got connection to postgres at {postgres_host} {postgres_port}..."
            )
            break
        await asyncio.sleep(1)


event_loop = asyncio.get_event_loop()
wait_tasks = asyncio.wait([event_loop.create_task(await_connection())])
event_loop.run_until_complete(wait_tasks)
event_loop.close()
