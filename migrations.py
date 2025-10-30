empty_dict: dict[str, str] = {}


async def m002_owner_data(db):
    """
    Initial owner data table.
    """

    await db.execute(
        f"""
        CREATE TABLE dashboard.owner_data (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            name TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT {db.timestamp_now},
            updated_at TIMESTAMP NOT NULL DEFAULT {db.timestamp_now}
        );
    """
    )


async def m003_client_data(db):
    """
    Initial client data table.
    """

    await db.execute(
        f"""
        CREATE TABLE dashboard.client_data (
            id TEXT PRIMARY KEY,
            owner_data_id TEXT NOT NULL,
            name TEXT NOT NULL,
            link TEXT NOT NULL,
            icon TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT {db.timestamp_now},
            updated_at TIMESTAMP NOT NULL DEFAULT {db.timestamp_now}
        );
    """
    )
