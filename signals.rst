Signals
=======

SurrealEngine provides Django-style signals for document lifecycle events.

Available Signals
-----------------

- ``pre_save`` - Before document is saved
- ``post_save`` - After document is saved
- ``pre_delete`` - Before document is deleted
- ``post_delete`` - After document is deleted

Using Signals
-------------

.. code-block:: python

    from surrealengine.signals import pre_save, post_save

    @pre_save.connect
    def before_save(sender, document, **kwargs):
        print(f"About to save: {document}")
    
    @post_save.connect
    def after_save(sender, document, **kwargs):
        print(f"Saved: {document.id}")

Practical Examples
------------------

Audit Logging:

.. code-block:: python

    @post_save.connect
    def log_changes(sender, document, **kwargs):
        logger.info(f"Document {document.id} was modified")

Cache Invalidation:

.. code-block:: python

    @post_delete.connect
    def invalidate_cache(sender, document, **kwargs):
        cache.delete(f"doc:{document.id}")

Note: Signals require the ``blinker`` package:

.. code-block:: bash

    pip install surrealengine[signals]
