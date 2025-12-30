Aggregation Pipeline
====================

.. currentmodule:: surrealengine.aggregation

This module provides data aggregation utilities for building complex
aggregation pipelines and queries.

Core Classes
------------

.. autoclass:: AggregationPipeline
   :members:
   :undoc-members:
   :show-inheritance:

Usage Examples
--------------

Basic Aggregation Pipeline
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from surrealengine.aggregation import AggregationPipeline
   from surrealengine.materialized_view import Sum, Count, Mean

   class Order(Document):
       customer_id = StringField(required=True)
       amount = DecimalField(required=True)
       status = StringField(required=True)
       created_at = DateTimeField(auto_now_add=True)

   # Create aggregation pipeline
   pipeline = AggregationPipeline(Order) \\
       .match(status="completed") \\
       .group_by("customer_id") \\
       .aggregate(
           total_spent=Sum("amount"),
           order_count=Count(),
           avg_order_value=Mean("amount")
       ) \\
       .sort("-total_spent") \\
       .limit(10)

   # Execute pipeline
   results = await pipeline.execute()

Complex Aggregations
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from datetime import datetime, timedelta

   # Multi-stage aggregation
   monthly_stats = AggregationPipeline(Order) \\
       .match(
           created_at__gte=datetime.now() - timedelta(days=365),
           status__in=["completed", "shipped"]
       ) \\
       .add_fields(
           year_month="CONCAT(YEAR(created_at), '-', MONTH(created_at))"
       ) \\
       .group_by("year_month") \\
       .aggregate(
           monthly_revenue=Sum("amount"),
           monthly_orders=Count(),
           unique_customers=Count("customer_id", distinct=True),
           avg_order_value=Mean("amount")
       ) \\
       .sort("year_month")

   results = await monthly_stats.execute()

Window Functions
----------------

.. code-block:: python

   # Running totals and rankings
   customer_rankings = AggregationPipeline(Order) \\
       .group_by("customer_id") \\
       .aggregate(
           total_spent=Sum("amount"),
           order_count=Count()
       ) \\
       .add_fields(
           rank="RANK() OVER (ORDER BY total_spent DESC)",
           running_total="SUM(total_spent) OVER (ORDER BY total_spent DESC)"
       ) \\
       .sort("rank")

   top_customers = await customer_rankings.execute()

Conditional Aggregations
------------------------

.. code-block:: python

   # Conditional aggregations using CASE expressions
   order_analysis = AggregationPipeline(Order) \\
       .group_by("customer_id") \\
       .aggregate(
           total_orders=Count(),
           high_value_orders=Count(
               condition="amount > 100"
           ),
           revenue_this_month=Sum(
               "amount",
               condition="created_at >= DATE_SUB(NOW(), INTERVAL 1 MONTH)"
           ),
           avg_order_size=Mean("amount")
       ) \\
       .add_fields(
           high_value_ratio="high_value_orders / total_orders",
           customer_tier="""
               CASE 
                   WHEN total_orders > 50 THEN 'VIP'
                   WHEN total_orders > 20 THEN 'Premium'
                   WHEN total_orders > 5 THEN 'Regular'
                   ELSE 'New'
               END
           """
       )

   customer_tiers = await order_analysis.execute()

Geographic Aggregations
-----------------------

.. code-block:: python

   class Store(Document):
       name = StringField(required=True)
       location = GeometryField()  # Point geometry
       region = StringField()

   # Geographic aggregations
   regional_performance = AggregationPipeline(Order) \\
       .lookup(
           from_collection="stores",
           local_field="store_id",
           foreign_field="id",
           as_field="store_info"
       ) \\
       .unwind("store_info") \\
       .group_by("store_info.region") \\
       .aggregate(
           total_revenue=Sum("amount"),
           total_orders=Count(),
           unique_stores=Count("store_id", distinct=True),
           avg_revenue_per_store=Mean("amount")
       )

   regional_stats = await regional_performance.execute()

Time Series Aggregations
------------------------

.. code-block:: python

   # Daily time series with moving averages
   daily_metrics = AggregationPipeline(Order) \\
       .match(
           created_at__gte=datetime.now() - timedelta(days=90)
       ) \\
       .group_by("DATE(created_at)") \\
       .aggregate(
           daily_revenue=Sum("amount"),
           daily_orders=Count(),
           daily_customers=Count("customer_id", distinct=True)
       ) \\
       .sort("DATE(created_at)") \\
       .add_fields(
           revenue_7day_avg="""
               AVG(daily_revenue) OVER (
                   ORDER BY DATE(created_at) 
                   ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
               )
           """,
           revenue_trend="""
               CASE 
                   WHEN daily_revenue > LAG(daily_revenue, 7) OVER (ORDER BY DATE(created_at))
                   THEN 'UP'
                   ELSE 'DOWN'
               END
           """
       )

   time_series = await daily_metrics.execute()

Pipeline Composition
--------------------

.. code-block:: python

   # Reusable pipeline components
   def base_order_pipeline():
       return AggregationPipeline(Order) \\
           .match(status="completed") \\
           .match(created_at__gte=datetime.now() - timedelta(days=365))

   def customer_aggregation(pipeline):
       return pipeline \\
           .group_by("customer_id") \\
           .aggregate(
               total_spent=Sum("amount"),
               order_count=Count(),
               first_order=Min("created_at"),
               last_order=Max("created_at")
           )

   # Compose pipelines
   customer_lifetime_value = customer_aggregation(base_order_pipeline()) \\
       .add_fields(
           days_active="DATEDIFF(last_order, first_order)",
           avg_days_between_orders="days_active / (order_count - 1)"
       ) \\
       .match(total_spent__gte=500)

   valuable_customers = await customer_lifetime_value.execute()

Export and Materialization
--------------------------

.. code-block:: python

   # Export pipeline results
   pipeline = AggregationPipeline(Order) \\
       .group_by("customer_id") \\
       .aggregate(total_spent=Sum("amount"))

   # Export to different formats
   await pipeline.export_to_csv("customer_totals.csv")
   await pipeline.export_to_json("customer_totals.json")

   # Create materialized view from pipeline
   materialized_view = pipeline.materialize(
       view_name="customer_totals_mv",
       refresh_interval="1h"
   )
   await materialized_view.create()

Performance Optimization
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Optimized pipeline with proper indexing hints
   optimized_pipeline = AggregationPipeline(Order) \\
       .use_index("status_created_at_idx") \\
       .match(
           status="completed",
           created_at__gte=datetime.now() - timedelta(days=30)
       ) \\
       .group_by("customer_id") \\
       .aggregate(
           monthly_spent=Sum("amount"),
           monthly_orders=Count()
       ) \\
       .explain()  # Get execution plan

   # Execute with performance metrics
   results, metrics = await optimized_pipeline.execute_with_metrics()
   print(f"Execution time: {metrics['duration']}ms")
   print(f"Documents examined: {metrics['documents_examined']}")
   print(f"Documents returned: {metrics['documents_returned']}")