Schema Management
=================

SurrealEngine provides tools for managing database schemas, creating tables,
indexes, and handling migrations.

For complete examples, see: ``example_scripts/schema_management_example.py``

Creating Tables
---------------

.. code-block:: python

    from surrealengine import Document, StringField

    class User(Document):
        name = StringField(required=True)
        
        class Meta:
            collection = "users"
            schemafull = True

    # Create table
    await User.create_table()
    
    # Create table (sync)
    User.create_table_sync()

Automatic Table Creation
-------------------------

Create all tables from a module:

.. code-block:: python

    from surrealengine import create_tables_from_module
    import models

    # Create all document tables
    await create_tables_from_module(models, schemafull=True)

Managing Indexes
----------------

Define indexes in Meta class:

.. code-block:: python

    class User(Document):
        email = StringField(required=True)
        username = StringField(required=True)
        
        class Meta:
            collection = "users"
            indexes = [
                {"name": "email_idx", "fields": ["email"], "unique": True},
                {"name": "username_idx", "fields": ["username"], "unique": True}
            ]

    # Create indexes
    await User.create_indexes()

Schema Migrations
-----------------

Basic migration workflow:

.. code-block:: python

    # 1. Update your document models
    class User(Document):
        # Add new field
        phone = StringField()
        
        class Meta:
            collection = "users"

    # 2. Create/update table
    await User.create_table()

Schemafull vs Schemaless
-------------------------

.. code-block:: python

    # Schemafull - enforces schema
    class User(Document):
        class Meta:
            schemafull = True

    # Schemaless - flexible schema
    class User(Document):
        class Meta:
            schemafull = False

For more details, see ``example_scripts/schema_management_example.py``
