Connections, Pooling, and Observability
========================================

SurrealEngine provides robust connection management for both async and sync applications:

- Connection pooling (async and sync) with validation, health checking, and idle pruning
- ContextVar-backed per-task default connections
- OperationQueue for backpressure with metrics
- Optional OpenTelemetry spans around queries/transactions

Quick start (async)
-------------------

.. code-block:: python

    import asyncio
    from surrealengine.connection import create_connection, set_default_connection, get_default_connection

    async def main():
        conn = create_connection(
            url="ws://localhost:8000/rpc",
            namespace="test_ns",
            database="test_db",
            username="root",
            password="root",
            async_mode=True,
            use_pool=True,
            pool_size=5,
            validate_on_borrow=True,
            max_idle_time=60,
        )
        await conn.connect()
        set_default_connection(conn)
        resolved = get_default_connection(async_mode=True)
        assert resolved is conn
        await conn.client.query("INFO FOR DB;")
        await conn.disconnect()

    asyncio.run(main())

OperationQueue backpressure
---------------------------

Use OperationQueue to buffer operations during reconnects and control memory growth:

.. code-block:: python

    from surrealengine.connection import OperationQueue

    q = OperationQueue(maxsize=1000, drop_policy="drop_oldest")
    q.start_reconnection()

    async def op(n):
        # perform some DB work when connection returns
        ...

    for i in range(5000):
        q.queue_async_operation(op, args=[i])

    # After reconnect
    q.end_reconnection()
    await q.execute_queued_async_operations()
    print(q.metrics)

OpenTelemetry spans (optional)
------------------------------

If opentelemetry-sdk is installed, SurrealEngine creates spans around queries:

.. code-block:: python

    from opentelemetry import trace as _trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter

    _trace.set_tracer_provider(TracerProvider())
    provider = _trace.get_tracer_provider()
    provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))

    # Use SurrealEngine as normal; spans will be printed to console.

See also
--------
- Example script: ``example_scripts/connection_and_observability_example.py``
- LIVE subscriptions require a direct async websocket (no pool). See :doc:`live`.
