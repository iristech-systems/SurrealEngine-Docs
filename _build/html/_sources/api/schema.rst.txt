Schema API Reference
====================

.. currentmodule:: surrealengine.schema

This module provides utilities for discovering document classes, generating
schema statements, and creating database tables from Python modules.

Schema Functions
----------------

.. autofunction:: get_document_classes

.. autofunction:: create_tables_from_module

.. autofunction:: create_tables_from_module_sync

.. autofunction:: generate_schema_statements

.. autofunction:: generate_schema_statements_from_module

Usage Examples
--------------

Discovering Document Classes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from surrealengine.schema import get_document_classes

   # Get all Document classes from a module
   document_classes = get_document_classes('myapp.models')
   print(f"Found {len(document_classes)} document classes")

Creating Tables
~~~~~~~~~~~~~~~

.. code-block:: python

   from surrealengine.schema import create_tables_from_module

   # Create tables for all documents in a module
   await create_tables_from_module('myapp.models')

   # Create SCHEMALESS tables
   await create_tables_from_module('myapp.models', schemafull=False)

   # Use specific connection
   await create_tables_from_module('myapp.models', connection=my_connection)

Generating Schema Statements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from surrealengine.schema import generate_schema_statements

   class User(Document):
       name = StringField(required=True)
       email = StringField(unique=True, indexed=True)

   # Generate SQL statements
   statements = generate_schema_statements(User)
   for stmt in statements:
       print(stmt)

   # Output:
   # DEFINE TABLE users SCHEMAFULL
   # DEFINE FIELD name ON users TYPE string ASSERT $value != NONE
   # DEFINE FIELD email ON users TYPE string
   # DEFINE INDEX users_email_idx ON users FIELDS email UNIQUE

Schema Migration Workflow
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from surrealengine.schema import (
       get_document_classes,
       generate_schema_statements_from_module
   )

   # Generate migration script
   def generate_migration(module_name: str):
       statements = generate_schema_statements_from_module(module_name)
       
       with open('migration.sql', 'w') as f:
           f.write('-- Auto-generated migration\\n\\n')
           for stmt in statements:
               f.write(f'{stmt};\\n')
       
       print(f"Migration saved to migration.sql with {len(statements)} statements")

   # Usage
   generate_migration('myapp.models')

Conditional Schema Creation
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from surrealengine.schema import get_document_classes

   async def create_tables_if_needed():
       document_classes = get_document_classes('myapp.models')
       
       for doc_class in document_classes:
           # Check if table exists (implementation depends on your needs)
           table_name = doc_class._get_collection_name()
           
           # Create table and indexes
           await doc_class.create_table()
           await doc_class.create_indexes()
           
           print(f"Created table and indexes for {table_name}")

Advanced Schema Features
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   class TimeSeries(Document):
       timestamp = TimeSeriesField()
       value = FloatField()
       
       class Meta:
           collection = "metrics"
           time_series = True
           time_field = "timestamp"
           indexes = [
               {"name": "time_idx", "fields": ["timestamp"]},
               {"name": "value_idx", "fields": ["value"], "unique": False}
           ]

   # This will generate:
   # DEFINE TABLE metrics SCHEMAFULL TYPE TIMESTAMP TIMEFIELD timestamp
   # DEFINE FIELD timestamp ON metrics TYPE datetime
   # DEFINE FIELD value ON metrics TYPE float
   # DEFINE INDEX time_idx ON metrics FIELDS timestamp
   # DEFINE INDEX value_idx ON metrics FIELDS value