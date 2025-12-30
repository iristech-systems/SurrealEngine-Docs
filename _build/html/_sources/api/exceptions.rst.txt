Exceptions
==========

.. currentmodule:: surrealengine.exceptions

This module defines custom exception classes used throughout SurrealEngine.

Core Exceptions
---------------

.. autoclass:: DoesNotExist
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: MultipleObjectsReturned
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: ValidationError
   :members:
   :undoc-members:
   :show-inheritance:

Usage Examples
--------------

Handling DoesNotExist
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from surrealengine.exceptions import DoesNotExist

   try:
       user = await User.objects.get(id="nonexistent")
   except DoesNotExist:
       print("User not found")

Handling MultipleObjectsReturned
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from surrealengine.exceptions import MultipleObjectsReturned

   try:
       user = await User.objects.get(age=25)  # Multiple users with age 25
   except MultipleObjectsReturned:
       print("Multiple users found, use filter() instead")

Handling ValidationError
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from surrealengine.exceptions import ValidationError

   try:
       user = User(email="invalid-email")
       await user.save()
   except ValidationError as e:
       print(f"Validation failed: {e}")

Custom Exception Handling
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from surrealengine.exceptions import DoesNotExist, ValidationError

   async def safe_create_user(name, email):
       try:
           # Check if user already exists
           existing_user = await User.objects.get(email=email)
           return existing_user, False  # User exists
       except DoesNotExist:
           try:
               # Create new user
               user = User(name=name, email=email)
               await user.save()
               return user, True  # User created
           except ValidationError as e:
               print(f"Failed to create user: {e}")
               return None, False