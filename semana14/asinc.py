import asyncio

async def saludar(nombre):
    for i in range(3):
        print(f"Hola {nombre}, vuelta {i}")
        await asyncio.sleep(1)

async def main():
    await asyncio.gather(
        saludar("A"),
        saludar("B")
    )

asyncio.run(main())
