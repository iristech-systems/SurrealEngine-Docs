Connection Management
=====================

SurrealEngine provides flexible connection management supporting various connection
schemes, connection pooling, retry logic, and both synchronous and asynchronous operations.

Creating Connections
--------------------

Basic Connection
~~~~~~~~~~~~~~~~

Create a connection to a remote SurrealDB instance:

.. code-block:: python

    from surrealengine import create_connection

    # Async connection
    connection = create_connection(
        url="ws://localhost:8000/rpc",
        namespace="myapp",
        database="production",
        username="root",
        password="root",
        async_mode=True,
        make_default=True
    )

    await connection.connect()

Synchronous Connection
~~~~~~~~~~~~~~~~~~~~~~

For synchronous applications:

.. code-block:: python

    # Sync connection
    connection = create_connection(
        url="ws://localhost:8000/rpc",
        namespace="myapp",
        database="production",
        username="root",
        password="root",
        async_mode=False,
        make_default=True
    )

    connection.connect_sync()

Connection Schemes
------------------

SurrealEngine supports multiple connection schemes for different deployment scenarios.

WebSocket Connections
~~~~~~~~~~~~~~~~~~~~~

Standard WebSocket connections for remote servers:

.. code-block:: python

    # WebSocket (ws://)
    connection = create_connection(
        url="ws://localhost:8000/rpc",
        namespace="myapp",
        database="mydb"
    )

    # Secure WebSocket (wss://)
    connection = create_connection(
        url="wss://db.example.com/rpc",
        namespace="myapp",
        database="mydb"
    )

HTTP Connections
~~~~~~~~~~~~~~~~

HTTP/HTTPS connections:

.. code-block:: python

    # HTTP connection
    connection = create_connection(
        url="http://localhost:8000",
        namespace="myapp",
        database="mydb"
    )

    # HTTPS connection
    connection = create_connection(
        url="https://db.example.com",
        namespace="myapp",
        database="mydb"
    )

Embedded Databases (v0.4.1+)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

SurrealEngine now supports embedded database schemes for local, in-memory, and file-based
databases using the SurrealDB SDK's native embedded capabilities.

Memory Database
^^^^^^^^^^^^^^^

In-memory database - perfect for testing or temporary data:

.. code-block:: python

    from surrealengine import create_connection

    # In-memory database
    connection = create_connection(
        url="mem://",
        namespace="test",
        database="temp",
        async_mode=True,
        make_default=True
    )

    await connection.connect()

    # Data is lost when connection closes
    # Perfect for unit tests!

Use cases:
- Unit testing
- Temporary data processing
- Development without persistent storage
- Fast prototyping

File-Based Database
^^^^^^^^^^^^^^^^^^^

Persistent file-based database:

.. code-block:: python

    # File-based database
    connection = create_connection(
        url="file:///path/to/database/directory",
        namespace="myapp",
        database="mydb",
        async_mode=True,
        make_default=True
    )

    await connection.connect()

    # Data persists to the file system
    # No separate database server needed!

Use cases:
- Desktop applications
- Edge computing
- Offline-first applications
- Single-user applications
- Development and testing

SurrealKV Database
^^^^^^^^^^^^^^^^^^

High-performance key-value store:

.. code-block:: python

    # SurrealKV database
    connection = create_connection(
        url="surrealkv:///path/to/database",
        namespace="myapp",
        database="mydb",
        async_mode=True,
        make_default=True
    )

    await connection.connect()

Use cases:
- High-performance applications
- Low-latency requirements
- Embedded systems
- IoT devices

Embedded Database Examples
^^^^^^^^^^^^^^^^^^^^^^^^^^

Complete examples for embedded databases:

.. code-block:: python

    import asyncio
    from surrealengine import Document, StringField, IntField, create_connection

    class User(Document):
        name = StringField(required=True)
        age = IntField()

        class Meta:
            collection = "users"

    async def test_with_memory_db():
        """Test with in-memory database"""
        conn = create_connection(
            url="mem://",
            namespace="test",
            database="test",
            async_mode=True,
            make_default=True
        )
        await conn.connect()

        # Create and query data
        user = User(name="Alice", age=30)
        await user.save()

        users = await User.objects.all()
        print(f"Found {len(users)} users")

    async def app_with_file_db():
        """Application with file-based database"""
        conn = create_connection(
            url="file:///var/lib/myapp/db",
            namespace="myapp",
            database="production",
            async_mode=True,
            make_default=True
        )
        await conn.connect()

        # Your application logic here
        # Data persists between runs

    def sync_app_with_embedded_db():
        """Synchronous app with embedded database"""
        conn = create_connection(
            url="file://./local_db",
            namespace="myapp",
            database="mydb",
            async_mode=False,
            make_default=True
        )
        conn.connect_sync()

        # Synchronous operations
        user = User(name="Bob", age=25)
        user.save_sync()

Connection Pooling
------------------

Enable connection pooling for better performance with concurrent requests:

.. code-block:: python

    # With connection pooling
    connection = create_connection(
        url="ws://localhost:8000/rpc",
        namespace="myapp",
        database="mydb",
        async_mode=True,
        use_pool=True,
        pool_size=10,
        make_default=True
    )

    await connection.connect()

.. note::

    Connection pooling is not supported with LIVE queries. For LIVE subscriptions,
    use ``use_pool=False`` to get a direct websocket connection.

Pool Options
~~~~~~~~~~~~

Configure connection pool behavior:

.. code-block:: python

    connection = create_connection(
        url="ws://localhost:8000/rpc",
        namespace="myapp",
        database="mydb",
        async_mode=True,
        use_pool=True,
        pool_size=20,              # Maximum connections in pool
        pool_max_idle=300,         # Seconds before idle connection is closed
        pool_validation=True,      # Validate connections before use
        make_default=True
    )

Retry and Timeout
-----------------

Configure retry logic and timeouts:

.. code-block:: python

    connection = create_connection(
        url="ws://localhost:8000/rpc",
        namespace="myapp",
        database="mydb",
        async_mode=True,
        retry_limit=3,             # Number of retry attempts
        initial_delay=0.5,         # Initial retry delay in seconds
        backoff=2.0,               # Backoff multiplier
        timeout=30.0,              # Connection timeout in seconds
        make_default=True
    )

Default Connections
-------------------

Set a default connection for all operations:

.. code-block:: python

    # Create and set as default
    connection = create_connection(
        url="ws://localhost:8000/rpc",
        namespace="myapp",
        database="mydb",
        async_mode=True,
        make_default=True  # Sets as default
    )

    await connection.connect()

    # Now all operations use this connection by default
    user = User(name="Alice")
    await user.save()  # Uses default connection

    # Query without explicit connection
    users = await User.objects.all()

Multiple Connections
--------------------

Manage multiple database connections:

.. code-block:: python

    # Primary database
    primary = create_connection(
        url="ws://primary.example.com/rpc",
        namespace="myapp",
        database="production",
        async_mode=True,
        make_default=True
    )
    await primary.connect()

    # Analytics database
    analytics = create_connection(
        url="ws://analytics.example.com/rpc",
        namespace="myapp",
        database="analytics",
        async_mode=True,
        make_default=False
    )
    await analytics.connect()

    # Use default connection
    user = User(name="Alice")
    await user.save()  # Saves to primary

    # Use specific connection
    await user.save(connection=analytics)  # Saves to analytics

Connection Registry
-------------------

Retrieve connections from the registry:

.. code-block:: python

    from surrealengine import ConnectionRegistry

    # Get default async connection
    conn = ConnectionRegistry.get_default_connection(async_mode=True)

    # Get default sync connection
    conn = ConnectionRegistry.get_default_connection(async_mode=False)

Connection Context Managers
---------------------------

Use connections with context managers for automatic cleanup:

.. code-block:: python

    async def process_data():
        connection = create_connection(
            url="ws://localhost:8000/rpc",
            namespace="myapp",
            database="mydb",
            async_mode=True
        )

        async with connection:
            # Connection automatically connects and closes
            user = User(name="Alice")
            await user.save()

Best Practices
--------------

1. **Use embedded databases for local applications (v0.4.1+)**:

   .. code-block:: python

       # Desktop app - use file://
       conn = create_connection(url="file://./app_data/db", ...)

       # Testing - use mem://
       conn = create_connection(url="mem://", ...)

2. **Set make_default=True for primary connection**:

   .. code-block:: python

       primary = create_connection(..., make_default=True)

3. **Use connection pooling for web applications**:

   .. code-block:: python

       conn = create_connection(..., use_pool=True, pool_size=20)

4. **Disable pooling for LIVE queries**:

   .. code-block:: python

       conn = create_connection(..., use_pool=False)  # Required for LIVE

5. **Configure appropriate timeouts and retries**:

   .. code-block:: python

       conn = create_connection(
           ...,
           timeout=30.0,
           retry_limit=3
       )

6. **Use HTTPS/WSS in production**:

   .. code-block:: python

       conn = create_connection(url="wss://db.example.com/rpc", ...)

7. **Choose the right scheme for your use case**:

   - ``ws://`` / ``wss://`` - Remote database server
   - ``http://`` / ``https://`` - HTTP-based connections
   - ``mem://`` - Testing and temporary data (v0.4.1+)
   - ``file://`` - Desktop/offline apps (v0.4.1+)
   - ``surrealkv://`` - High-performance embedded (v0.4.1+)

Connection Lifecycle
--------------------

Typical connection lifecycle:

.. code-block:: python

    # 1. Create connection
    connection = create_connection(...)

    # 2. Connect
    await connection.connect()

    # 3. Use connection
    user = User(name="Alice")
    await user.save()

    # 4. Close connection (optional, but recommended)
    await connection.close()

Health Checks
-------------

Monitor connection health:

.. code-block:: python

    # Check if connected
    if connection.is_connected():
        print("Connected to database")

    # Ping the database
    await connection.ping()

Troubleshooting
---------------

Common Connection Issues
~~~~~~~~~~~~~~~~~~~~~~~~

1. **Connection refused**:

   - Check that SurrealDB is running
   - Verify the URL and port
   - Check firewall settings

2. **Authentication failed**:

   - Verify username and password
   - Check namespace and database names
   - Ensure user has proper permissions

3. **Timeout errors**:

   - Increase timeout setting
   - Check network connectivity
   - Verify database server is responsive

4. **Pool exhausted**:

   - Increase pool_size
   - Check for connection leaks
   - Ensure connections are being released

5. **LIVE queries not working**:

   - Set ``use_pool=False``
   - Use async websocket connection
   - Check SurrealDB version supports LIVE

Migration Guide
---------------

Embedded Database Support (v0.4.1+)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

New embedded database schemes are now available:

.. code-block:: python

    # NEW (v0.4.1+) - Embedded databases
    conn = create_connection(url="mem://", ...)
    conn = create_connection(url="file:///path/to/db", ...)
    conn = create_connection(url="surrealkv:///path/to/db", ...)

    # Still supported - Remote databases
    conn = create_connection(url="ws://localhost:8000/rpc", ...)
