SurrealEngine Documentation
===========================

.. image:: https://img.shields.io/pypi/v/surrealengine.svg
   :target: https://pypi.org/project/surrealengine/
   :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/surrealengine.svg
   :target: https://pypi.org/project/surrealengine/
   :alt: Python versions

.. image:: https://img.shields.io/github/license/surrealengine/surrealengine.svg
   :target: https://github.com/surrealengine/surrealengine/blob/main/LICENSE
   :alt: License

SurrealEngine is a comprehensive Object-Document Mapper (ODM) for SurrealDB that provides
an intuitive Python interface for database operations. It supports both synchronous and
asynchronous operations, connection pooling, field validation, query building, and 
graph-based relationships.

Key Features
------------

- **Dual sync/async support** for all operations
- **Connection pooling** and management with automatic retry logic
- **Rich field types** with comprehensive validation
- **Query builder** with Django-style filtering and chaining
- **Graph relationships** and path traversal
- **Materialized views** and data aggregations
- **Schema management** and migrations
- **Signals** for model lifecycle events
- **Multi-backend support** for SurrealDB and ClickHouse

Quick Start
-----------

.. code-block:: python

   from surrealengine import Document, StringField, IntField, create_connection

   # Define a document model
   class User(Document):
       name = StringField(required=True)
       age = IntField()
       
       class Meta:
           collection = "users"

   # Create connection and save user
   async def main():
       connection = create_connection("ws://localhost:8000/rpc")
       await connection.connect()
       
       user = User(name="Alice", age=30)
       await user.save()
       print(f"Created user: {user.id}")

Installation
------------

Install SurrealEngine using pip:

.. code-block:: bash

   pip install surrealengine

Or with optional dependencies:

.. code-block:: bash

   pip install surrealengine[all]

Table of Contents
-----------------

.. toctree::
   :maxdepth: 1
   :hidden:

   README

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   getting_started
   tutorial
   connection_management
   connections_observability
   document_models
   field_types
   querying
   relationships
   schema_management
   signals
   materialized_views
   live
   performance

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/connection
   api/document
   api/fields
   api/query
   api/exceptions
   api/schema
   api/signals
   api/materialized_view
   api/aggregation
   api/utilities

.. toctree::
   :maxdepth: 1
   :caption: Examples

   examples/basic_usage
   examples/async_operations
   examples/relationships
   examples/advanced_queries
   examples/schema_migrations

.. toctree::
   :maxdepth: 1
   :caption: Development

   contributing
   changelog
   license

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`