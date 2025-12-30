Materialized Views API Reference
================================

.. currentmodule:: surrealengine.materialized_view

This module provides support for creating and managing materialized views
in SurrealDB for improved query performance on aggregated data.

Core Classes
------------

.. autoclass:: MaterializedView
   :members:
   :undoc-members:
   :show-inheritance:

Aggregation Functions
---------------------

Base Aggregation
~~~~~~~~~~~~~~~~~

.. autoclass:: Aggregation
   :members:
   :undoc-members:
   :show-inheritance:

Statistical Aggregations
~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: Count
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: Mean
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: Sum
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: Min
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: Max
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: Median
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: StdDev
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: Variance
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: Percentile
   :members:
   :undoc-members:
   :show-inheritance:

Collection Aggregations
~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: ArrayCollect
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: Distinct
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: GroupConcat
   :members:
   :undoc-members:
   :show-inheritance:

Usage Examples
--------------

Basic Materialized View
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from surrealengine import Document, StringField, IntField, DateTimeField
   from surrealengine.materialized_view import MaterializedView, Count, Mean

   class Order(Document):
       customer_id = StringField(required=True)
       amount = DecimalField(required=True)
       status = StringField(required=True)
       created_at = DateTimeField(auto_now_add=True)

   # Create a materialized view for order statistics
   order_stats = MaterializedView(
       name="order_statistics",
       query=Order.objects.group_by("customer_id"),
       aggregations={
           "total_orders": Count(),
           "avg_order_amount": Mean("amount"),
           "total_spent": Sum("amount")
       },
       refresh_interval="1h"
   )

   # Create the view in the database
   await order_stats.create()

Document-Based Materialized Views
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Create materialized view using Document class method
   customer_summary = Order.create_materialized_view(
       name="customer_summary",
       query=Order.objects.filter(status="completed").group_by("customer_id"),
       aggregations={
           "completed_orders": Count(),
           "total_revenue": Sum("amount"),
           "avg_order_value": Mean("amount"),
           "last_order_date": Max("created_at")
       },
       refresh_interval="30m"
   )

   await customer_summary.create()

Advanced Aggregations
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from surrealengine.materialized_view import (
       Percentile, StdDev, ArrayCollect, GroupConcat
   )

   # Advanced statistics view
   advanced_stats = MaterializedView(
       name="advanced_order_stats",
       query=Order.objects.group_by("status"),
       aggregations={
           "order_count": Count(),
           "amount_p95": Percentile("amount", 95),
           "amount_std": StdDev("amount"),
           "customer_list": ArrayCollect("customer_id"),
           "customer_names": GroupConcat("customer_name", separator=", ")
       }
   )

Time-Based Materialized Views
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Daily sales summary
   daily_sales = MaterializedView(
       name="daily_sales",
       query=Order.objects.group_by("DATE(created_at)"),
       aggregations={
           "daily_revenue": Sum("amount"),
           "daily_orders": Count(),
           "unique_customers": Distinct("customer_id")
       },
       refresh_interval="1h"
   )

Querying Materialized Views
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Query the materialized view
   stats = await order_stats.query()
   for row in stats:
       print(f"Customer {row['customer_id']}: {row['total_orders']} orders")

   # Query with filters
   high_value_customers = await order_stats.query(
       filter_condition="total_spent > 1000"
   )

   # Get view metadata
   info = await order_stats.info()
   print(f"View last refreshed: {info['last_refresh']}")

Managing Materialized Views
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Refresh view manually
   await order_stats.refresh()

   # Update view definition
   await order_stats.update(
       aggregations={
           "total_orders": Count(),
           "avg_order_amount": Mean("amount"),
           "max_order_amount": Max("amount")  # Added new aggregation
       }
   )

   # Drop view
   await order_stats.drop()

   # Check if view exists
   exists = await order_stats.exists()

Integration with Query Pipeline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from surrealengine.aggregation import AggregationPipeline

   # Create aggregation pipeline that can be used for materialized views
   pipeline = AggregationPipeline(Order) \\
       .match(status="completed") \\
       .group_by("customer_id") \\
       .aggregate(
           total_spent=Sum("amount"),
           order_count=Count(),
           avg_amount=Mean("amount")
       )

   # Create materialized view from pipeline
   customer_stats = MaterializedView.from_pipeline(
       name="customer_stats_mv",
       pipeline=pipeline,
       refresh_interval="2h"
   )

   await customer_stats.create()

Performance Monitoring
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Monitor view performance
   async def monitor_view_performance():
       views = [order_stats, customer_summary, daily_sales]
       
       for view in views:
           info = await view.info()
           print(f"View: {view.name}")
           print(f"  Size: {info.get('size', 'Unknown')}")
           print(f"  Last refresh: {info.get('last_refresh', 'Unknown')}")
           print(f"  Refresh duration: {info.get('refresh_duration', 'Unknown')}")
           print()

   await monitor_view_performance()