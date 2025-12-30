LIVE Queries (Subscriptions)
============================

SurrealEngine supports SurrealDB LIVE queries via an ergonomic async generator API:

- QuerySet.live(where: Optional[Q|dict] = None, action: Optional[str|List[str]] = None, retry_limit=3, initial_delay=0.5, backoff=2.0)
- Yields typed ``LiveEvent`` objects with ``.action``, ``.data``, ``.ts``, and ``.id`` attributes

LiveEvent Class (v0.5.0+)
--------------------------

The ``LiveEvent`` dataclass provides typed access to LIVE query events:

.. code-block:: python

    @dataclass
    class LiveEvent:
        action: str              # 'CREATE', 'UPDATE', or 'DELETE'
        data: Dict[str, Any]     # Document fields
        ts: Optional[datetime]   # Event timestamp
        id: Optional[RecordID]   # Document ID

        # Convenience properties
        @property
        def is_create(self) -> bool: ...

        @property
        def is_update(self) -> bool: ...

        @property
        def is_delete(self) -> bool: ...

Important: direct async websocket required
------------------------------------------
LIVE subscriptions are long-lived, stateful, and bound to a single websocket. The connection
pool is intended for short, stateless request/response operations and may rotate/prune sockets.
Therefore QuerySet.live() requires a direct async websocket client (use_pool=False).

If you attempt to use a pooled client for LIVE, a NotImplementedError is raised.

Quick start
-----------

.. code-block:: python

    import asyncio
    from surrealengine import create_connection, Document, StringField

    class User(Document):
        name = StringField(required=True)
        class Meta:
            collection = "users"

    async def main():
        # Direct async connection (no pool) for LIVE
        conn = create_connection(
            url="ws://localhost:8000/rpc",
            namespace="test_ns",
            database="test_db",
            username="root",
            password="root",
            async_mode=True,
            use_pool=False,          # IMPORTANT for LIVE
            make_default=True,
        )
        await conn.connect()

        # Subscribe to changes on the users table
        async for evt in User.objects.live():
            print(f"Event: {evt.action}")
            print(f"Data: {evt.data}")
            print(f"ID: {evt.id}")
            print(f"Timestamp: {evt.ts}")

    asyncio.run(main())

Action Filtering (v0.5.0+)
--------------------------

You can filter events by action type using the ``action`` parameter:

.. code-block:: python

    # Subscribe to CREATE events only
    async for evt in User.objects.live(action="CREATE"):
        if evt.is_create:
            print(f"New user created: {evt.id}")

    # Subscribe to multiple action types
    async for evt in User.objects.live(action=["CREATE", "UPDATE"]):
        if evt.is_create:
            print(f"User created: {evt.id}")
        elif evt.is_update:
            print(f"User updated: {evt.id}")

    # Monitor deletions
    async for evt in User.objects.live(action="DELETE"):
        if evt.is_delete:
            print(f"User deleted: {evt.id}")

Client-Side Filtering with WHERE
---------------------------------

The ``live(where=...)`` parameter accepts either a Q object or a simple dict. This predicate is
applied client-side to incoming events for convenience:

.. code-block:: python

    # Filter for active users only
    async for evt in User.objects.live(where={"status": "active"}):
        print(f"Active user event: {evt.action}")

    # Combine action and where filtering
    async for evt in User.objects.live(
        where={"status": "active"},
        action="CREATE"
    ):
        print(f"New active user: {evt.data}")

If you need authoritative server-side filtering, issue a LIVE query with a WHERE clause using
a raw query on the client. QuerySet.live() keeps things simple and portable across driver versions.

Retry and backoff
-----------------
QuerySet.live() provides simple retry behavior on transient disconnects:

- retry_limit (default 3)
- initial_delay (seconds; default 0.5)
- backoff multiplier (default 2.0)

When exceeded, the generator exits.

Integrating with web apps (SSE or WebSocket)
--------------------------------------------
A common pattern is to run the LIVE subscription in a background task and forward events to HTTP clients
via Server‑Sent Events (SSE) or WebSockets. See example_scripts/connection_and_observability_example.py
for connection setup, and refer to the Flask SSE snippet in the README for a full bridge example.

Limitations
-----------
- LIVE currently requires a direct async websocket connection (no pool).
- The pool client does not manage subscription lifecycles or event demultiplexing.

