Field Types API Reference
=========================

.. currentmodule:: surrealengine.fields

This module provides field types for defining document schemas with validation,
serialization, and database conversion functionality.

Base Field Classes
------------------

.. autoclass:: surrealengine.fields.base.Field
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: surrealengine.fields.id.RecordIDField
   :members:
   :undoc-members:
   :show-inheritance:

Scalar Fields
-------------

.. autoclass:: surrealengine.fields.scalar.StringField
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: surrealengine.fields.scalar.IntField
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: surrealengine.fields.scalar.FloatField
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: surrealengine.fields.scalar.NumberField
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: surrealengine.fields.scalar.BooleanField
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: surrealengine.fields.specialized.DecimalField
   :members:
   :undoc-members:
   :show-inheritance:

Collection Fields
-----------------

.. autoclass:: surrealengine.fields.collection.ListField
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: surrealengine.fields.collection.DictField
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: surrealengine.fields.collection.SetField
   :members:
   :undoc-members:
   :show-inheritance:

DateTime Fields
---------------

.. autoclass:: surrealengine.fields.datetime.DateTimeField
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: surrealengine.fields.datetime.DurationField
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: surrealengine.fields.datetime.TimeSeriesField
   :members:
   :undoc-members:
   :show-inheritance:

Reference Fields
----------------

.. autoclass:: surrealengine.fields.reference.ReferenceField
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: surrealengine.fields.reference.RelationField
   :members:
   :undoc-members:
   :show-inheritance:

Specialized Fields
------------------

.. autoclass:: surrealengine.fields.specialized.EmailField
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: surrealengine.fields.specialized.URLField
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: surrealengine.fields.specialized.IPAddressField
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: surrealengine.fields.specialized.SlugField
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: surrealengine.fields.specialized.ChoiceField
   :members:
   :undoc-members:
   :show-inheritance:

Geometry Fields
---------------

.. autoclass:: surrealengine.fields.geometry.GeometryField
   :members:
   :undoc-members:
   :show-inheritance:

Additional Fields
-----------------

.. autoclass:: surrealengine.fields.additional.OptionField
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: surrealengine.fields.specialized.LiteralField
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: surrealengine.fields.additional.RangeField
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: surrealengine.fields.additional.FutureField
   :members:
   :undoc-members:
   :show-inheritance:

Usage Examples
--------------

Basic Field Usage
~~~~~~~~~~~~~~~~~

.. code-block:: python

   from surrealengine import Document, StringField, IntField, EmailField

   class User(Document):
       name = StringField(required=True, max_length=100)
       age = IntField(min_value=0, max_value=150)
       email = EmailField(unique=True, indexed=True)

Field Validation
~~~~~~~~~~~~~~~~

.. code-block:: python

   # Automatic validation on assignment
   user = User()
   user.email = "invalid-email"  # Raises ValidationError
   user.email = "user@example.com"  # Valid

   # Custom validation
   class Product(Document):
       name = StringField(required=True)
       price = DecimalField(min_value=0, max_digits=10, decimal_places=2)

Reference Fields
~~~~~~~~~~~~~~~~

.. code-block:: python

   class Author(Document):
       name = StringField(required=True)

   class Book(Document):
       title = StringField(required=True)
       author = ReferenceField(Author, required=True)
       tags = ListField(StringField())

   # Usage
   author = Author(name="Jane Doe")
   await author.save()

   book = Book(
       title="Python Mastery",
       author=author,
       tags=["programming", "python"]
   )
   await book.save()