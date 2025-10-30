from lnbits.db import Database, Filters, Page
from lnbits.helpers import urlsafe_short_hash

from .models import (
    ClientData,
    ClientDataFilters,
    CreateClientData,
    CreateOwnerData,
    OwnerData,
    OwnerDataFilters,
)

db = Database("ext_dashboard")


########################### Owner Data ############################
async def create_owner_data(user_id: str, data: CreateOwnerData) -> OwnerData:
    owner_data = OwnerData(**data.dict(), id=urlsafe_short_hash(), user_id=user_id)
    await db.insert("dashboard.owner_data", owner_data)
    return owner_data


async def get_owner_data(
    user_id: str,
    owner_data_id: str,
) -> OwnerData | None:
    return await db.fetchone(
        """
            SELECT * FROM dashboard.owner_data
            WHERE id = :id AND user_id = :user_id
        """,
        {"id": owner_data_id, "user_id": user_id},
        OwnerData,
    )


async def get_owner_data_by_id(
    owner_data_id: str,
) -> OwnerData | None:
    return await db.fetchone(
        """
            SELECT * FROM dashboard.owner_data
            WHERE id = :id
        """,
        {"id": owner_data_id},
        OwnerData,
    )


async def get_owner_data_ids_by_user(
    user_id: str,
) -> list[str]:
    rows: list[dict] = await db.fetchall(
        """
            SELECT DISTINCT id FROM dashboard.owner_data
            WHERE user_id = :user_id
        """,
        {"user_id": user_id},
    )

    return [row["id"] for row in rows]


async def get_owner_data_paginated(
    user_id: str | None = None,
    filters: Filters[OwnerDataFilters] | None = None,
) -> Page[OwnerData]:
    where = []
    values = {}
    if user_id:
        where.append("user_id = :user_id")
        values["user_id"] = user_id

    return await db.fetch_page(
        "SELECT * FROM dashboard.owner_data",
        where=where,
        values=values,
        filters=filters,
        model=OwnerData,
    )


async def update_owner_data(data: OwnerData) -> OwnerData:
    await db.update("dashboard.owner_data", data)
    return data


async def delete_owner_data(user_id: str, owner_data_id: str) -> None:
    await db.execute(
        """
            DELETE FROM dashboard.owner_data
            WHERE id = :id AND user_id = :user_id
        """,
        {"id": owner_data_id, "user_id": user_id},
    )


################################# Client Data ###########################


async def create_client_data(data: CreateClientData) -> ClientData:
    client_data = ClientData(**data.dict(), id=urlsafe_short_hash())
    await db.insert("dashboard.client_data", client_data)
    return client_data


async def get_client_data(
    owner_data_id: str,
    client_data_id: str,
) -> ClientData | None:
    return await db.fetchone(
        """
            SELECT * FROM dashboard.client_data
            WHERE id = :id AND owner_data_id = :owner_data_id
        """,
        {"id": client_data_id, "owner_data_id": owner_data_id},
        ClientData,
    )


async def get_client_data_by_id(
    client_data_id: str,
) -> ClientData | None:
    return await db.fetchone(
        """
            SELECT * FROM dashboard.client_data
            WHERE id = :id
        """,
        {"id": client_data_id},
        ClientData,
    )


async def get_client_data_by_owner_id(
    owner_data_id: str,
) -> list[ClientData]:
    rows: list[dict] = await db.fetchall(
        """
            SELECT DISTINCT id FROM dashboard.client_data
            WHERE owner_data_id = :owner_data_id
        """,
        {"owner_data_id": owner_data_id},
    )

    return [ClientData(**row) for row in rows]


async def get_client_data_paginated(
    owner_data_ids: list[str] | None = None,
    filters: Filters[ClientDataFilters] | None = None,
) -> Page[ClientData]:

    if not owner_data_ids:
        return Page(data=[], total=0)

    where = []
    values = {}
    id_clause = []
    for i, item_id in enumerate(owner_data_ids):
        # owner_data_ids are not user input, but DB entries, so this is safe
        owner_data_id = f"owner_data_id__{i}"
        id_clause.append(f"owner_data_id = :{owner_data_id}")
        values[owner_data_id] = item_id
    or_clause = " OR ".join(id_clause)
    where.append(f"({or_clause})")

    return await db.fetch_page(
        "SELECT * FROM dashboard.client_data",
        where=where,
        values=values,
        filters=filters,
        model=ClientData,
    )


async def update_client_data(data: ClientData) -> ClientData:
    await db.update("dashboard.client_data", data)
    return data


async def delete_client_data(owner_data_id: str, client_data_id: str) -> None:
    await db.execute(
        """
            DELETE FROM dashboard.client_data
            WHERE id = :id AND owner_data_id = :owner_data_id
        """,
        {"id": client_data_id, "owner_data_id": owner_data_id},
    )
