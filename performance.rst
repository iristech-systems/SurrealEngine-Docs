Performance Optimization
========================

Tips and techniques for optimizing SurrealEngine applications.

For examples, see: ``example_scripts/test_performance_optimizations.py``

Indexing
--------

Add indexes to frequently queried fields:

.. code-block:: python

    class User(Document):
        email = StringField(indexed=True, unique=True)
        status = StringField(indexed=True)
        
        class Meta:
            indexes = [
                {"fields": ["created_at"]},
                {"fields": ["status", "created_at"]}
            ]

Connection Pooling
------------------

.. code-block:: python

    connection = create_connection(
        url="ws://localhost:8000/rpc",
        use_pool=True,
        pool_size=20,
        pool_max_idle=300
    )

Query Optimization
------------------

.. code-block:: python

    # Use omit() to exclude fields
    users = await User.objects.omit("large_field").all()
    
    # Use explain() to analyze
    plan = await User.objects.filter(status="active").explain()
    
    # Limit results
    users = await User.objects.limit(100)

Batch Operations
----------------

.. code-block:: python

    # Batch create
    for user in users:
        await user.save()
    
    # Batch update
    await User.objects.filter(status="pending").update(status="active")

For more optimization techniques, see :doc:`querying` and the performance examples.
