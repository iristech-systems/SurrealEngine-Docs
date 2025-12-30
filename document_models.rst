Document Models
===============

SurrealEngine provides a powerful Document class that serves as the base for all your
data models. Document models map to SurrealDB tables and provide field validation,
type conversion, and database operations.

Defining Documents
------------------

Basic Document Definition
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from surrealengine import Document, StringField, IntField, DateTimeField

    class User(Document):
        name = StringField(required=True, max_length=100)
        email = StringField(required=True)
        age = IntField(min_value=0, max_value=150)
        created_at = DateTimeField(auto_now_add=True)

        class Meta:
            collection = "users"
            schemafull = True

Meta Options
~~~~~~~~~~~~

Configure document behavior with the Meta class:

.. code-block:: python

    class User(Document):
        name = StringField(required=True)

        class Meta:
            collection = "users"        # Table name
            schemafull = True            # Enforce schema
            drop = False                 # Drop table on migration
            permissions = "FULL"         # Table permissions

Creating and Saving Documents
------------------------------

Async Operations
~~~~~~~~~~~~~~~~

.. code-block:: python

    # Create and save
    user = User(name="Alice", email="alice@example.com", age=30)
    await user.save()
    print(f"Created user: {user.id}")

    # Create with custom ID
    user = User(id="user:alice", name="Alice", email="alice@example.com")
    await user.save()

    # Save updates
    user.age = 31
    await user.save()

Sync Operations (v0.4.1+)
~~~~~~~~~~~~~~~~~~~~~~~~~

All async operations now have synchronous equivalents:

.. code-block:: python

    # Create and save synchronously
    user = User(name="Bob", email="bob@example.com", age=25)
    user.save_sync()
    print(f"Created user: {user.id}")

    # Save updates synchronously
    user.age = 26
    user.save_sync()

Updating Documents
------------------

Partial Updates (v0.4.1+)
~~~~~~~~~~~~~~~~~~~~~~~~~

Update specific fields without loading the entire document:

.. code-block:: python

    # Async partial update
    user = await User.objects.get(id="user:alice")
    await user.update(age=32, email="newemail@example.com")

    # Sync partial update
    user = User.objects.get_sync(id="user:bob")
    user.update_sync(age=27)

The ``update()`` and ``update_sync()`` methods:

- Only modify specified fields
- Don't overwrite other fields
- Automatically refresh the instance with latest data
- More efficient than loading full document and saving

Full Document Save
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Load document
    user = await User.objects.get(id="user:alice")

    # Modify multiple fields
    user.name = "Alice Smith"
    user.age = 33
    user.email = "alice.smith@example.com"

    # Save all changes
    await user.save()

Refreshing Documents
--------------------

Reload document data from the database:

Async Refresh
~~~~~~~~~~~~~

.. code-block:: python

    user = await User.objects.get(id="user:alice")
    # ... some time passes, data might have changed ...
    await user.refresh()
    print(f"Current age: {user.age}")

Sync Refresh (v0.4.1+)
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    user = User.objects.get_sync(id="user:alice")
    # ... some time passes ...
    user.refresh_sync()
    print(f"Current age: {user.age}")

Deleting Documents
------------------

Async Deletion
~~~~~~~~~~~~~~

.. code-block:: python

    user = await User.objects.get(id="user:alice")
    await user.delete()

Sync Deletion (v0.4.1+)
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    user = User.objects.get_sync(id="user:bob")
    user.delete_sync()

Document Validation
-------------------

Documents are automatically validated before saving:

.. code-block:: python

    from surrealengine.exceptions import ValidationError

    try:
        # This will fail - name is required
        user = User(email="test@example.com")
        await user.save()
    except ValidationError as e:
        print(f"Validation error: {e}")

    try:
        # This will fail - age exceeds max_value
        user = User(name="Test", age=200)
        await user.save()
    except ValidationError as e:
        print(f"Validation error: {e}")

Default Values
--------------

Set default values for fields:

.. code-block:: python

    from datetime import datetime

    class Post(Document):
        title = StringField(required=True)
        content = StringField()
        status = StringField(default="draft")
        created_at = DateTimeField(default=datetime.now)
        views = IntField(default=0)

        class Meta:
            collection = "posts"

    # Default values are applied automatically
    post = Post(title="My Post", content="Hello world")
    await post.save()
    print(post.status)  # "draft"
    print(post.views)   # 0

Auto-Generated Fields
---------------------

Some fields can auto-populate:

.. code-block:: python

    class Article(Document):
        title = StringField(required=True)
        created_at = DateTimeField(auto_now_add=True)  # Set on creation
        updated_at = DateTimeField(auto_now=True)      # Update on each save

        class Meta:
            collection = "articles"

    article = Article(title="New Article")
    await article.save()
    print(article.created_at)  # Automatically set

    article.title = "Updated Article"
    await article.save()
    print(article.updated_at)  # Automatically updated

Relation Documents
------------------

For graph edge relationships:

.. code-block:: python

    from surrealengine import RelationDocument, ReferenceField

    class Follows(RelationDocument):
        since = DateTimeField(auto_now_add=True)

        class Meta:
            collection = "follows"
            in_doc = "User"
            out_doc = "User"

    # Create relationship
    follows = Follows(
        in_doc="user:alice",
        out_doc="user:bob",
    )
    await follows.save()

    # Update relationship (v0.4.1+)
    await follows.update(since=datetime.now())
    follows.update_sync(since=datetime.now())

Document Lifecycle
------------------

Document operations follow this lifecycle:

1. **Instantiation**: Create document instance
2. **Validation**: Fields are validated
3. **Pre-save**: Signals fired (if enabled)
4. **Save/Update**: Data persisted to database
5. **Post-save**: Signals fired (if enabled)
6. **Refresh**: Reload from database if needed
7. **Delete**: Remove from database

.. code-block:: python

    # 1. Create
    user = User(name="Charlie", email="charlie@example.com")

    # 2. Validation happens here
    await user.save()  # 3-5: Pre-save, save, post-save

    # 6. Refresh if needed
    await user.refresh()

    # 7. Delete
    await user.delete()

API Parity
----------

Complete sync/async parity (v0.4.1+):

.. list-table::
   :header-rows: 1
   :widths: 40 30 30

   * - Operation
     - Async
     - Sync
   * - Save document
     - ``await doc.save()``
     - ``doc.save_sync()``
   * - Update fields
     - ``await doc.update(**kwargs)``
     - ``doc.update_sync(**kwargs)``
   * - Refresh from DB
     - ``await doc.refresh()``
     - ``doc.refresh_sync()``
   * - Delete document
     - ``await doc.delete()``
     - ``doc.delete_sync()``
   * - Get by ID
     - ``await Model.objects.get(id=...)``
     - ``Model.objects.get_sync(id=...)``
   * - Filter query
     - ``await Model.objects.filter(...).all()``
     - ``Model.objects.filter(...).all_sync()``

Best Practices
--------------

1. **Use update() for partial updates**:

   .. code-block:: python

       # Good - only updates specified fields
       await user.update(age=30)

       # Less efficient - loads and saves entire document
       user = await User.objects.get(id=user_id)
       user.age = 30
       await user.save()

2. **Choose sync or async consistently**:

   .. code-block:: python

       # Good - all async
       user = await User.objects.get(id=user_id)
       await user.update(age=30)
       await user.refresh()

       # Good - all sync
       user = User.objects.get_sync(id=user_id)
       user.update_sync(age=30)
       user.refresh_sync()

       # Avoid mixing - may cause issues
       user = await User.objects.get(id=user_id)
       user.update_sync(age=30)  # Mixed sync/async

3. **Validate before saving**:

   .. code-block:: python

       user = User(name="Test")
       try:
           await user.save()
       except ValidationError as e:
           print(f"Fix these errors: {e}")

4. **Use auto fields for timestamps**:

   .. code-block:: python

       class Document:
           created_at = DateTimeField(auto_now_add=True)
           updated_at = DateTimeField(auto_now=True)

5. **Set defaults in field definition**:

   .. code-block:: python

       status = StringField(default="draft")  # Better
       # Instead of setting in __init__

Migration Guide
---------------

If upgrading from versions before v0.4.1, you can now use sync methods:

.. code-block:: python

    # OLD - only async available
    user = await User.objects.get(id=user_id)
    user.age = 30
    await user.save()

    # NEW - sync methods available (v0.4.1+)
    user = User.objects.get_sync(id=user_id)
    user.update_sync(age=30)

    # NEW - more efficient partial updates (v0.4.1+)
    await user.update(age=30)  # Only updates age field
