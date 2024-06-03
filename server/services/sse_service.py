import asyncio

clients = []


async def notify_clients(message: str):
    for client in clients:
        await client.put(message)
