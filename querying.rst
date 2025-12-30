Querying
========

SurrealEngine provides a powerful QuerySet API for building and executing database queries
with a Django-style interface. This guide covers the query building features and operators
available in SurrealEngine.

Basic Querying
--------------

Use the ``objects`` manager to build queries on your document models:

.. code-block:: python

    from surrealengine import Document, StringField, IntField

    class User(Document):
        name = StringField(required=True)
        age = IntField()
        status = StringField()

        class Meta:
            collection = "users"

    # Get all users
    users = await User.objects.all()

    # Filter users
    active_users = await User.objects.filter(status="active")

    # Chain filters
    young_active = await User.objects.filter(status="active").filter(age__lt=30)

Field Selection
---------------

Omit Fields (v0.5.0+)
~~~~~~~~~~~~~~~~~~~~~

Exclude specific fields from query results to reduce data transfer:

.. code-block:: python

    # Omit sensitive fields
    users = await User.objects.omit("password", "email").all()

    # Combine with filters
    users = await User.objects.filter(status="active").omit("password")

Select Specific Fields
~~~~~~~~~~~~~~~~~~~~~~

Use ``only()`` to select only specific fields:

.. code-block:: python

    # Only get name and age
    users = await User.objects.only("name", "age").all()

Query Performance
-----------------

Timeout (v0.5.0+)
~~~~~~~~~~~~~~~~~

Set a timeout for query execution to prevent long-running queries:

.. code-block:: python

    # 5 second timeout
    users = await User.objects.timeout("5s").all()

    # 1 minute timeout
    users = await User.objects.timeout("1m").filter(status="active")

Tempfiles (v0.5.0+)
~~~~~~~~~~~~~~~~~~~

Enable or disable temporary files for large query results:

.. code-block:: python

    # Enable tempfiles for large result sets
    users = await User.objects.tempfiles(True).all()

    # Disable tempfiles (default)
    users = await User.objects.tempfiles(False).all()

Index Control (v0.5.0+)
~~~~~~~~~~~~~~~~~~~~~~~

Bypass indexes for specific queries:

.. code-block:: python

    # Don't use any indexes
    users = await User.objects.no_index().filter(name="John")

Query Explanation (v0.5.0+)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Analyze query execution plans:

.. code-block:: python

    # Get basic execution plan
    plan = await User.objects.filter(status="active").explain()
    print(plan)

    # Get full execution plan with trace
    full_plan = await User.objects.filter(status="active").explain(full=True)
    print(full_plan)

    # Using the builder pattern
    plan = await User.objects.filter(status="active").with_explain().all()

    # Synchronous version
    plan = User.objects.filter(status="active").explain_sync()

Advanced Filter Operators
--------------------------

Set Operators (v0.5.0+)
~~~~~~~~~~~~~~~~~~~~~~~

SurrealEngine supports advanced set operators for filtering:

.. code-block:: python

    # Contains any - check if field contains any of the values
    users = await User.objects.filter(tags__contains_any=["python", "javascript"])

    # Contains all - check if field contains all of the values
    users = await User.objects.filter(tags__contains_all=["python", "javascript", "rust"])

    # Contains none - check if field contains none of the values
    users = await User.objects.filter(tags__contains_none=["php", "perl"])

    # Inside - check if value is in the list
    users = await User.objects.filter(status__inside=["active", "pending"])

    # Not inside - check if value is not in the list
    users = await User.objects.filter(status__not_inside=["banned", "deleted"])

    # All inside - check if all field values are in the list
    users = await User.objects.filter(tags__all_inside=["python", "javascript", "rust", "go"])

    # Any inside - check if any field value is in the list
    users = await User.objects.filter(tags__any_inside=["python", "javascript"])

    # None inside - check if no field values are in the list
    users = await User.objects.filter(tags__none_inside=["php", "perl"])

Standard Operators
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Equality
    users = await User.objects.filter(name="John")
    users = await User.objects.filter(name__eq="John")

    # Inequality
    users = await User.objects.filter(status__ne="banned")

    # Greater than / Less than
    users = await User.objects.filter(age__gt=18)
    users = await User.objects.filter(age__gte=18)
    users = await User.objects.filter(age__lt=65)
    users = await User.objects.filter(age__lte=65)

    # String operations
    users = await User.objects.filter(name__contains="John")
    users = await User.objects.filter(name__startswith="J")
    users = await User.objects.filter(name__endswith="son")
    users = await User.objects.filter(email__regex=r".*@example\.com")

    # In operator
    users = await User.objects.filter(status__in=["active", "pending"])

Grouping and Aggregation
-------------------------

Group By (v0.5.0+)
~~~~~~~~~~~~~~~~~~

Group query results by one or more fields:

.. code-block:: python

    # Group by single field
    results = await User.objects.group_by("status").all()

    # Group by multiple fields
    results = await User.objects.group_by("status", "age").all()

    # Group all results (v0.5.0+)
    results = await User.objects.group_by(all=True).all()

Complex Queries with Q Objects
-------------------------------

Use Q objects for complex boolean logic:

.. code-block:: python

    from surrealengine import Q

    # OR condition
    users = await User.objects.filter(
        Q(status="active") | Q(status="pending")
    )

    # AND condition
    users = await User.objects.filter(
        Q(status="active") & Q(age__gt=18)
    )

    # NOT condition
    users = await User.objects.filter(~Q(status="banned"))

    # Complex nested conditions
    users = await User.objects.filter(
        Q(status="active") & (Q(age__lt=18) | Q(age__gt=65))
    )

Ordering and Pagination
-----------------------

.. code-block:: python

    # Order by field
    users = await User.objects.order_by("name")

    # Descending order
    users = await User.objects.order_by("-age")

    # Multiple fields
    users = await User.objects.order_by("status", "-age")

    # Limit results
    users = await User.objects.limit(10)

    # Skip results
    users = await User.objects.offset(20)

    # Pagination
    page = await User.objects.page(1, 20)  # page 1, 20 items per page

Fetching Related Documents
--------------------------

Use the ``fetch()`` method to load related documents:

.. code-block:: python

    # Fetch referenced documents
    users = await User.objects.fetch("company").all()

    # Fetch multiple relations
    users = await User.objects.fetch("company", "manager").all()

Synchronous Queries
-------------------

All query methods have synchronous equivalents:

.. code-block:: python

    # Synchronous query
    users = User.objects.filter(status="active").all_sync()

    # Synchronous explain
    plan = User.objects.filter(status="active").explain_sync()

    # Get single object
    user = User.objects.get_sync(id="user:123")

Query Chaining
--------------

All QuerySet methods return a new QuerySet, allowing for flexible query building:

.. code-block:: python

    # Build query progressively
    query = User.objects.filter(status="active")
    query = query.filter(age__gte=18)
    query = query.omit("password")
    query = query.timeout("5s")
    query = query.order_by("-created_at")

    # Execute
    users = await query.all()

    # Or chain in one statement
    users = await (User.objects
        .filter(status="active")
        .filter(age__gte=18)
        .omit("password")
        .timeout("5s")
        .order_by("-created_at")
        .all())
