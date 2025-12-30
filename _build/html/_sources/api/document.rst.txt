Document API Reference
======================

.. currentmodule:: surrealengine.document

This module provides the foundation for defining and working with documents
in SurrealDB using an Object-Document Mapper (ODM) pattern.

Document Classes
----------------

.. autoclass:: Document
   :members:
   :exclude-members: objects
   :undoc-members:
   :show-inheritance:

.. autoattribute:: Document.objects
   :no-index:

.. autoclass:: RelationDocument
   :members:
   :undoc-members:
   :show-inheritance:

Graph and Relations
-------------------

.. automodule:: surrealengine.graph
   :members:
   :undoc-members:
   :show-inheritance:

Schemaless Support
------------------

.. automodule:: surrealengine.schemaless
   :members:
   :undoc-members:
   :show-inheritance:

Metaclasses
-----------

.. autoclass:: surrealengine.document.DocumentMetaclass
   :members:
   :undoc-members:
   :show-inheritance:

Usage Examples
--------------

Basic Document Definition
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from surrealengine import Document, StringField, IntField

   class User(Document):
       name = StringField(required=True)
       age = IntField()
       
       class Meta:
           collection = "users"

Document Operations
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Create and save a document
   user = User(name="Alice", age=30)
   await user.save()

   # Query documents
   users = await User.objects.filter(age__gte=18).all()

   # Update a document
   user.age = 31
   await user.save()

   # Delete a document
   await user.delete()

Relationships
~~~~~~~~~~~~~

.. code-block:: python

   class Book(Document):
       title = StringField(required=True)
       author = ReferenceField(User)

   # Create relationship
   book = Book(title="Python Guide", author=user)
   await book.save()

   # Fetch with references resolved
   book_with_author = await Book.get(book.id, dereference=True)
   print(book_with_author.author.name)  # "Alice"