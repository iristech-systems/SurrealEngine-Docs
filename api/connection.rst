Connection API Reference
========================

.. currentmodule:: surrealengine.connection

This module provides connection management for SurrealDB with pooling and registry support.

Connection Classes
------------------

.. autoclass:: SurrealEngineAsyncConnection
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: SurrealEngineSyncConnection
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: BaseSurrealEngineConnection
   :members:
   :undoc-members:
   :show-inheritance:

Connection Pooling
------------------

.. autoclass:: ConnectionPoolBase
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: AsyncConnectionPool
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: SyncConnectionPool
   :members:
   :undoc-members:
   :show-inheritance:

Connection Registry
-------------------

.. autoclass:: ConnectionRegistry
   :members:
   :undoc-members:
   :show-inheritance:

Utility Functions
-----------------

.. autofunction:: create_connection

.. autofunction:: parse_connection_string

Event Handling
--------------

.. autoclass:: ConnectionEvent
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: ConnectionEventListener
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: ConnectionEventEmitter
   :members:
   :undoc-members:
   :show-inheritance:

Operation Queue
---------------

.. autoclass:: OperationQueue
   :members:
   :undoc-members:
   :show-inheritance:

Reconnection Strategy
---------------------

.. autoclass:: ReconnectionStrategy
   :members:
   :undoc-members:
   :show-inheritance:

Retry Strategy
--------------

.. autoclass:: RetryStrategy
   :members:
   :undoc-members:
   :show-inheritance: