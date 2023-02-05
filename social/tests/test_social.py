import asyncio

queue = asyncio.Queue()

async def first_task():
    queue.put("Hello from the first task!")

async def second_task():
    message = await queue.get()
    print(message)

async def main():
    await asyncio.gather(first_task(), second_task())

asyncio.run(main())