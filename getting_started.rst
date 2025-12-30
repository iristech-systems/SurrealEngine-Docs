Getting Started
===============

This guide will help you get up and running with SurrealEngine quickly.

Installation
------------

Install SurrealEngine using pip:

.. code-block:: bash

    pip install surrealengine

Or with all optional dependencies:

.. code-block:: bash

    pip install surrealengine[all]

Prerequisites
-------------

You'll need a SurrealDB instance running. The easiest way is with Docker:

.. code-block:: bash

    # Start SurrealDB
    docker run --rm --pull always -p 8000:8000 \
        surrealdb/surrealdb:latest \
        start --user root --pass root

Or using the SurrealDB binary:

.. code-block:: bash

    surreal start --user root --pass root

Your First SurrealEngine Application
-------------------------------------

Async Application
~~~~~~~~~~~~~~~~~

Here's a complete async example:

.. code-block:: python

    import asyncio
    from surrealengine import (
        Document, StringField, IntField,
        create_connection
    )

    # Define your document model
    class User(Document):
        name = StringField(required=True)
        email = StringField(required=True)
        age = IntField(min_value=0)

        class Meta:
            collection = "users"

    async def main():
        # Create connection
        connection = create_connection(
            url="ws://localhost:8000/rpc",
            namespace="myapp",
            database="mydb",
            username="root",
            password="root",
            async_mode=True,
            make_default=True
        )

        await connection.connect()
        print("✓ Connected to SurrealDB")

        # Create table
        await User.create_table()
        print("✓ Created users table")

        # Create a user
        user = User(
            name="Alice",
            email="alice@example.com",
            age=30
        )
        await user.save()
        print(f"✓ Created user: {user.id}")

        # Query users
        users = await User.objects.all()
        print(f"✓ Found {len(users)} users")

        # Filter users
        alice = await User.objects.filter(name="Alice").first()
        print(f"✓ Found Alice: {alice.email}")

        # Update user
        await alice.update(age=31)
        print(f"✓ Updated Alice's age to {alice.age}")

        # Delete user
        await alice.delete()
        print("✓ Deleted Alice")

    if __name__ == "__main__":
        asyncio.run(main())

Synchronous Application
~~~~~~~~~~~~~~~~~~~~~~~~

For synchronous applications, use the sync API:

.. code-block:: python

    from surrealengine import (
        Document, StringField, IntField,
        create_connection
    )

    class User(Document):
        name = StringField(required=True)
        email = StringField(required=True)
        age = IntField(min_value=0)

        class Meta:
            collection = "users"

    def main():
        # Create synchronous connection
        connection = create_connection(
            url="ws://localhost:8000/rpc",
            namespace="myapp",
            database="mydb",
            username="root",
            password="root",
            async_mode=False,  # Key parameter for sync
            make_default=True
        )

        connection.connect_sync()
        print("✓ Connected to SurrealDB")

        # Create table
        User.create_table_sync()
        print("✓ Created users table")

        # Create a user
        user = User(name="Bob", email="bob@example.com", age=25)
        user.save_sync()
        print(f"✓ Created user: {user.id}")

        # Query users
        users = User.objects.all_sync()
        print(f"✓ Found {len(users)} users")

        # Filter users
        bob = User.objects.filter(name="Bob").first_sync()
        print(f"✓ Found Bob: {bob.email}")

        # Update user
        bob.update_sync(age=26)
        print(f"✓ Updated Bob's age to {bob.age}")

    if __name__ == "__main__":
        main()

Embedded Database (No Server Required)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use an embedded database for local or offline applications:

.. code-block:: python

    import asyncio
    from surrealengine import Document, StringField, create_connection

    class Task(Document):
        title = StringField(required=True)
        completed = BooleanField(default=False)

        class Meta:
            collection = "tasks"

    async def main():
        # Use file-based database (no server needed!)
        connection = create_connection(
            url="file://./my_app_data",
            namespace="myapp",
            database="mydb",
            async_mode=True,
            make_default=True
        )

        await connection.connect()

        # Create and query data
        task = Task(title="Learn SurrealEngine")
        await task.save()

        tasks = await Task.objects.all()
        print(f"Tasks: {[t.title for t in tasks]}")

    asyncio.run(main())

Connection Options
------------------

SurrealEngine supports multiple connection schemes:

Remote Server
~~~~~~~~~~~~~

.. code-block:: python

    # WebSocket
    connection = create_connection(url="ws://localhost:8000/rpc", ...)

    # Secure WebSocket
    connection = create_connection(url="wss://db.example.com/rpc", ...)

    # HTTP
    connection = create_connection(url="http://localhost:8000", ...)

    # HTTPS
    connection = create_connection(url="https://db.example.com", ...)

Embedded Database
~~~~~~~~~~~~~~~~~

.. code-block:: python

    # In-memory (perfect for testing)
    connection = create_connection(url="mem://", ...)

    # File-based (persistent storage)
    connection = create_connection(url="file:///path/to/db", ...)

    # SurrealKV (high-performance)
    connection = create_connection(url="surrealkv:///path/to/db", ...)

Core Concepts
-------------

Documents
~~~~~~~~~

Documents are the main data models in SurrealEngine:

.. code-block:: python

    from surrealengine import Document, StringField, IntField

    class Product(Document):
        name = StringField(required=True, max_length=100)
        price = IntField(min_value=0)
        sku = StringField(unique=True)

        class Meta:
            collection = "products"
            schemafull = True

Fields
~~~~~~

SurrealEngine provides rich field types:

.. code-block:: python

    from surrealengine import (
        StringField, IntField, FloatField, BoolField,
        DateTimeField, ListField, DictField,
        ReferenceField, EmailField, URLField
    )

    class Article(Document):
        title = StringField(required=True)
        content = StringField()
        views = IntField(default=0)
        rating = FloatField(min_value=0.0, max_value=5.0)
        published = BoolField(default=False)
        created_at = DateTimeField(auto_now_add=True)
        tags = ListField(StringField())
        metadata = DictField()
        author = ReferenceField("User")

Querying
~~~~~~~~

Django-style query API:

.. code-block:: python

    # Get all
    products = await Product.objects.all()

    # Filter
    expensive = await Product.objects.filter(price__gte=100)

    # Chain filters
    results = await Product.objects.filter(
        category="electronics"
    ).filter(
        price__lt=500
    ).order_by("-price")

    # Limit and pagination
    page1 = await Product.objects.limit(10).offset(0)
    page2 = await Product.objects.page(2, 10)

    # Get single object
    product = await Product.objects.get(id="product:123")
    first = await Product.objects.filter(name="Phone").first()

Common Patterns
---------------

CRUD Operations
~~~~~~~~~~~~~~~

.. code-block:: python

    # Create
    user = User(name="Alice", email="alice@example.com")
    await user.save()

    # Read
    user = await User.objects.get(id=user.id)
    users = await User.objects.filter(age__gte=18)

    # Update
    await user.update(age=31)
    # or
    user.age = 31
    await user.save()

    # Delete
    await user.delete()

Batch Operations
~~~~~~~~~~~~~~~~

.. code-block:: python

    # Bulk create
    users = [
        User(name=f"User{i}", email=f"user{i}@example.com")
        for i in range(100)
    ]
    for user in users:
        await user.save()

    # Bulk update
    await User.objects.filter(status="pending").update(status="active")

    # Bulk delete
    await User.objects.filter(age__lt=18).delete()

Relationships
~~~~~~~~~~~~~

.. code-block:: python

    from surrealengine import ReferenceField

    class Comment(Document):
        content = StringField(required=True)
        author = ReferenceField("User", required=True)
        post = ReferenceField("Post", required=True)

        class Meta:
            collection = "comments"

    # Create with references
    comment = Comment(
        content="Great post!",
        author="user:alice",
        post="post:123"
    )
    await comment.save()

    # Fetch with related documents
    comments = await Comment.objects.fetch("author", "post").all()
    print(comments[0].author.name)  # Access author's name

Error Handling
--------------

.. code-block:: python

    from surrealengine.exceptions import (
        ValidationError,
        DoesNotExist,
        MultipleObjectsReturned
    )

    try:
        # Validation error
        user = User(email="invalid")  # Missing required 'name'
        await user.save()
    except ValidationError as e:
        print(f"Validation failed: {e}")

    try:
        # Does not exist
        user = await User.objects.get(id="user:nonexistent")
    except DoesNotExist:
        print("User not found")

    try:
        # Multiple objects returned
        user = await User.objects.get(name="John")  # Multiple Johns
    except MultipleObjectsReturned:
        print("Multiple users found")

Next Steps
----------

Now that you're familiar with the basics, explore these topics:

- :doc:`tutorial` - In-depth tutorial building a complete application
- :doc:`document_models` - Learn about document models and sync API
- :doc:`field_types` - Explore all available field types
- :doc:`querying` - Master advanced querying techniques
- :doc:`relationships` - Work with graph relationships
- :doc:`connection_management` - Connection pooling and embedded databases
- :doc:`materialized_views` - Create aggregated views
- :doc:`live` - Real-time subscriptions with LIVE queries

Tips for Success
-----------------

1. **Start with embedded databases** for development:

   .. code-block:: python

       # Development
       connection = create_connection(url="mem://", ...)

2. **Use schemafull tables** for production:

   .. code-block:: python

       class User(Document):
           class Meta:
               schemafull = True

3. **Add indexes** for frequently queried fields:

   .. code-block:: python

       class User(Document):
           email = StringField(indexed=True, unique=True)

4. **Use validation** at the field level:

   .. code-block:: python

       age = IntField(min_value=0, max_value=150)

5. **Choose sync or async** consistently throughout your app

6. **Enable connection pooling** for web applications:

   .. code-block:: python

       connection = create_connection(..., use_pool=True, pool_size=20)

Getting Help
------------

- **Documentation**: https://surrealengine.readthedocs.io
- **GitHub Issues**: https://github.com/iristech-systems/surrealengine/issues
- **Examples**: Check the ``example_scripts/`` directory in the repository
- **SurrealDB Docs**: https://surrealdb.com/docs

Troubleshooting
---------------

Connection Issues
~~~~~~~~~~~~~~~~~

If you can't connect to SurrealDB:

1. Check that SurrealDB is running: ``curl http://localhost:8000/health``
2. Verify credentials are correct
3. Check namespace and database names
4. Look for firewall issues

Import Errors
~~~~~~~~~~~~~

If imports fail:

.. code-block:: bash

    # Reinstall with all dependencies
    pip install -U surrealengine[all]

Performance Issues
~~~~~~~~~~~~~~~~~~

For slow queries:

1. Add indexes to frequently queried fields
2. Use ``select()`` or ``omit()`` to limit returned fields
3. Enable connection pooling
4. Use ``explain()`` to analyze query plans
