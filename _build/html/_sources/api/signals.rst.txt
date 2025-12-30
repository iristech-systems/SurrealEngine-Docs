Signals API Reference
=====================

.. currentmodule:: surrealengine.signals

This module provides signal support for model lifecycle events, allowing you to
hook into various stages of document operations.

Available Signals
-----------------

Document Lifecycle Signals
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autodata:: pre_init
   :annotation: Signal sent before document initialization

.. autodata:: post_init
   :annotation: Signal sent after document initialization

.. autodata:: pre_save
   :annotation: Signal sent before document save

.. autodata:: pre_save_post_validation
   :annotation: Signal sent after validation but before save

.. autodata:: post_save
   :annotation: Signal sent after document save

.. autodata:: pre_delete
   :annotation: Signal sent before document deletion

.. autodata:: post_delete
   :annotation: Signal sent after document deletion

Bulk Operation Signals
~~~~~~~~~~~~~~~~~~~~~~~

.. autodata:: pre_bulk_insert
   :annotation: Signal sent before bulk insert operation

.. autodata:: post_bulk_insert
   :annotation: Signal sent after bulk insert operation

Field Operation Signals
~~~~~~~~~~~~~~~~~~~~~~~~

.. autodata:: pre_validate
   :annotation: Signal sent before field validation

.. autodata:: post_validate
   :annotation: Signal sent after field validation

.. autodata:: pre_to_db
   :annotation: Signal sent before converting value to database format

.. autodata:: post_to_db
   :annotation: Signal sent after converting value to database format

.. autodata:: pre_from_db
   :annotation: Signal sent before converting value from database format

.. autodata:: post_from_db
   :annotation: Signal sent after converting value from database format

Signal Constants
----------------

.. autodata:: SIGNAL_SUPPORT
   :annotation: Boolean indicating if signal support is available

Usage Examples
--------------

Connecting to Document Signals
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from surrealengine.signals import pre_save, post_save
   from surrealengine import Document, StringField
   import datetime

   class User(Document):
       name = StringField(required=True)
       created_at = DateTimeField()
       updated_at = DateTimeField()

   # Signal handlers
   def set_timestamps(sender, document, **kwargs):
       now = datetime.datetime.utcnow()
       if not document.created_at:
           document.created_at = now
       document.updated_at = now

   def log_user_save(sender, document, created, **kwargs):
       action = "created" if created else "updated"
       print(f"User {document.name} was {action}")

   # Connect signals
   pre_save.connect(set_timestamps, sender=User)
   post_save.connect(log_user_save, sender=User)

Audit Trail Example
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from surrealengine.signals import post_save, post_delete

   class AuditLog(Document):
       action = StringField(required=True)
       model_name = StringField(required=True)
       object_id = StringField()
       timestamp = DateTimeField(auto_now=True)
       user_id = StringField()

   def create_audit_log(sender, document, created=None, **kwargs):
       action = "created" if created else "updated"
       AuditLog(
           action=action,
           model_name=sender.__name__,
           object_id=str(document.id),
           user_id=getattr(document, 'user_id', None)
       ).save()

   def delete_audit_log(sender, document, **kwargs):
       AuditLog(
           action="deleted",
           model_name=sender.__name__,
           object_id=str(document.id)
       ).save()

   # Connect to all document classes
   post_save.connect(create_audit_log)
   post_delete.connect(delete_audit_log)

Cache Invalidation
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from surrealengine.signals import post_save, post_delete
   import redis

   cache = redis.Redis()

   def invalidate_cache(sender, document, **kwargs):
       # Invalidate specific object cache
       cache_key = f"{sender.__name__.lower()}:{document.id}"
       cache.delete(cache_key)
       
       # Invalidate list caches
       list_key = f"{sender.__name__.lower()}:list:*"
       for key in cache.scan_iter(match=list_key):
           cache.delete(key)

   # Connect to multiple models
   for model in [User, Post, Comment]:
       post_save.connect(invalidate_cache, sender=model)
       post_delete.connect(invalidate_cache, sender=model)

Custom Validation
~~~~~~~~~~~~~~~~~

.. code-block:: python

   from surrealengine.signals import pre_save
   from surrealengine.exceptions import ValidationError

   def validate_user_email_domain(sender, document, **kwargs):
       if hasattr(document, 'email') and document.email:
           allowed_domains = ['company.com', 'partner.com']
           domain = document.email.split('@')[1]
           if domain not in allowed_domains:
               raise ValidationError(f"Email domain {domain} not allowed")

   pre_save.connect(validate_user_email_domain, sender=User)

Conditional Signal Connections
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from surrealengine.signals import post_save
   import os

   def send_welcome_email(sender, document, created, **kwargs):
       if created and hasattr(document, 'email'):
           # Send welcome email logic here
           print(f"Sending welcome email to {document.email}")

   # Only connect in production
   if os.environ.get('ENV') == 'production':
       post_save.connect(send_welcome_email, sender=User)

Signal Disconnection
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from surrealengine.signals import post_save

   # Disconnect specific handler
   post_save.disconnect(log_user_save, sender=User)

   # Disconnect all handlers for a sender
   post_save.disconnect(sender=User)

   # Disconnect handler from all senders
   post_save.disconnect(log_user_save)