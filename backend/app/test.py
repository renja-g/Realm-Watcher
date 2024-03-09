import asyncio
from beanie import init_beanie, Document
from motor.motor_asyncio import AsyncIOMotorClient
from beanie.odm.utils.encoder import Encoder
from beanie import Document, Link, BackLink
from pydantic import Field


class Person(Document):
    name: str
    age: int
    cars: list[BackLink["Car"]] = Field(original_field="owner")

class Car(Document):
    manufacturer: str
    price: float
    owner: Link[Person]


async def init():
    client = AsyncIOMotorClient(
        "mongodb://localhost:27017",
    )

    await init_beanie(database=client.test_db, document_models=[Person, Car])

    p1 = Person(
        name="John",
        age=25,
    )
    await p1.insert()

    c1 = Car(
        manufacturer="Toyota",
        price=10000,
        owner=p1
    )
    c2 = Car(
        manufacturer="BMW",
        price=20000,
        owner=p1
    )
    await c1.insert()
    await c2.insert()
    person = await Person.find_one(Person.name == "John", fetch_links=True)

    print(person)

asyncio.run(init())


