Query Building and Execution
============================

.. currentmodule:: surrealengine.query

This module provides query building and execution capabilities with Django-style
filtering and chaining operations.

QuerySet Classes
----------------
.. autoclass:: surrealengine.query.base.QuerySet
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

.. autoclass:: surrealengine.query.relation.RelationQuerySet
   :members:
   :undoc-members:
   :show-inheritance:

Base Query Classes
------------------

.. automodule:: surrealengine.base_query
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

Query Descriptors
------------------

.. autoclass:: surrealengine.query.descriptor.QuerySetDescriptor
   :members:
   :undoc-members:
   :show-inheritance:

Query Expressions
-----------------

.. automodule:: surrealengine.query_expressions
   :members:
   :undoc-members:
   :show-inheritance:

Pagination
----------

.. automodule:: surrealengine.pagination
   :members:
   :undoc-members:
   :show-inheritance:

Usage Examples
--------------

Basic Queries
~~~~~~~~~~~~~

.. code-block:: python

   from surrealengine import Document, StringField, IntField

   class User(Document):
       name = StringField(required=True)
       age = IntField()

   # Get all users
   users = await User.objects.all()

   # Filter users
   adults = await User.objects.filter(age__gte=18).all()

   # Get a single user
   user = await User.objects.get(name="Alice")

Advanced Filtering
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from surrealengine import Q

   # Complex queries with Q objects
   query = Q(age__gte=18) & (Q(name__startswith="A") | Q(name__startswith="B"))
   users = await User.objects.filter(query).all()

   # Ordering and limiting
   recent_users = await User.objects.order_by("-created_at").limit(10).all()

   # Counting
   user_count = await User.objects.filter(age__gte=18).count()

Aggregation
~~~~~~~~~~~

.. code-block:: python

   # Count by group
   age_counts = await User.objects.group_by("age").count()

   # Average age
   avg_age = await User.objects.aggregate(avg_age=Avg("age"))

Relationship Queries
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   class Post(Document):
       title = StringField(required=True)
       author = ReferenceField(User)

   # Query with joins
   posts_with_authors = await Post.objects.select_related("author").all()

   # Reverse relationships
   user_posts = await user.fetch_relation("posts", Post)

Pagination
~~~~~~~~~~

.. code-block:: python

   # Paginated results
   page = await User.objects.paginate(page=1, per_page=20)
   users = page.items
   total_count = page.total

   # Cursor-based pagination
   cursor_page = await User.objects.cursor_paginate(
       cursor="eyJ1c2VyX2lkIjoxMjN9",
       limit=20
   )