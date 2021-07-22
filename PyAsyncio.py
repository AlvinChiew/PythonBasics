import time
import asyncio
from typing import Dict


##### Request Simulation #####

async def fetch_data(x: int) -> Dict[str, int]:
    print('start fetching')
    await asyncio.sleep(2)
    print('done fetching')
    return {'data' : x}


async def send_request(n):
    for i in range(n):
        print(i)
        await asyncio.sleep(0.25)


async def request_simulation_async():
    t0 = time.time()
    task1 = asyncio.create_task(send_request(10))
    task2 = asyncio.create_task(fetch_data(1))
    # if without `await`, main() will stop as soon as `task1` and `task2` started

    await task2
    await task1
    print(f"Timespan (async) : {(time.time() - t0)*1000:.2f} ms")


async def request_simulation_sync():
    t0 = time.time()
    task1 = await asyncio.create_task(send_request(10))
    task2 = await asyncio.create_task(fetch_data(1))
    # if without `await`, main() will stop as soon as `task1` and `task2` started
    print(f"Timespan (sync) : {(time.time() - t0)*1000:.2f} ms")

asyncio.run(request_simulation_async())
asyncio.run(request_simulation_sync())


##### Multi-Task Simulation #####

def is_prime(x):
    return not any(x//i == x/i for i in range(x-1, 1, -1))


async def highest_prime_below(x):
    print(f"Processing number : {x}")
    for y in range(x-1, 0, -1):
        if is_prime(y):
            print(f"Highest prime below {x} is {y}")
            return y
        # time.sleep(0.01)
        await asyncio.sleep(0.01)   
        # `await` with async-able func allows async happens while process on idle/sleep
        # Useful when dealing with network communication; Specify to sleep while waiting for server and come back after 0.01sec
    return None


async def request_simulation():
    t0 = time.time()
    await asyncio.wait([
            highest_prime_below(1000000),
            highest_prime_below(10000),
            highest_prime_below(1000)
        ])
    print(f"Timespan (sync) : {(time.time() - t0)*1000:.2f} ms")

loop = asyncio.get_event_loop()
loop.run_until_complete(request_simulation())
loop.close()