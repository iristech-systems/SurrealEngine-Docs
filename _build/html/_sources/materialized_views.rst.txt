Materialized Views
==================

SurrealEngine provides support for SurrealDB materialized views, allowing you to create
pre-computed aggregations and transformations of your data. In SurrealDB 2.x+, materialized
views are live and automatically update when underlying data changes.

Creating Materialized Views
----------------------------

Basic Creation
~~~~~~~~~~~~~~

Create a materialized view from a document model:

.. code-block:: python

    from surrealengine import Document, StringField, IntField, FloatField
    from surrealengine import MaterializedView

    class Product(Document):
        name = StringField(required=True)
        category = StringField(required=True)
        price = FloatField(required=True)
        quantity = IntField()

        class Meta:
            collection = "products"

    # Create a materialized view
    class ProductStats(MaterializedView):
        table_name = "product_stats"

        @classmethod
        def get_source_query(cls):
            return Product.objects.group_by("category")

    # Create the view in the database
    await ProductStats.create()

Create Options (v0.5.0+)
~~~~~~~~~~~~~~~~~~~~~~~~

Control how the materialized view table is created:

.. code-block:: python

    # Create with overwrite - replaces existing table
    await ProductStats.create(overwrite=True)

    # Create only if it doesn't exist
    await ProductStats.create(if_not_exists=True)

    # Basic create (will fail if table exists)
    await ProductStats.create()

These options map to SurrealDB's ``DEFINE TABLE`` clauses:

- ``overwrite=True`` → ``DEFINE TABLE OVERWRITE ...``
- ``if_not_exists=True`` → ``DEFINE TABLE IF NOT EXISTS ...``

Advanced View Configuration
---------------------------

Group By with Aggregations (v0.5.0+)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create views with aggregated data using improved GROUP BY parsing:

.. code-block:: python

    class CategoryStats(MaterializedView):
        table_name = "category_stats"

        @classmethod
        def get_source_query(cls):
            return (Product.objects
                .group_by("category")
                .select("category", "COUNT(*) as total", "AVG(price) as avg_price"))

    await CategoryStats.create()

Group All (v0.5.0+)
~~~~~~~~~~~~~~~~~~~

Aggregate across all records without grouping:

.. code-block:: python

    class OverallStats(MaterializedView):
        table_name = "overall_stats"

        @classmethod
        def get_source_query(cls):
            return (Product.objects
                .group_by(all=True)
                .select("COUNT(*) as total_products", "SUM(quantity) as total_inventory"))

    await OverallStats.create()

Querying Materialized Views
----------------------------

Query materialized views like regular documents:

.. code-block:: python

    # Get all stats
    stats = await ProductStats.objects.all()

    # Filter stats
    electronics = await ProductStats.objects.filter(category="electronics")

    # Order by aggregated values
    top_categories = await ProductStats.objects.order_by("-total_sales").limit(10)

    # Use with other query methods
    stats = await (ProductStats.objects
        .filter(total_sales__gt=1000)
        .omit("internal_field")
        .timeout("5s")
        .all())

Synchronous Operations
----------------------

All async operations have synchronous equivalents:

.. code-block:: python

    # Create view synchronously
    ProductStats.create_sync()
    ProductStats.create_sync(overwrite=True)
    ProductStats.create_sync(if_not_exists=True)

    # Query synchronously
    stats = ProductStats.objects.all_sync()
    stats = ProductStats.objects.filter(category="electronics").all_sync()

Deprecation Notice
------------------

.. warning::

    **refresh() and refresh_sync() are deprecated (v0.5.0+)**

    In SurrealDB 2.x+, materialized views derived from tables are **live** and automatically
    update when underlying data changes. Manual refresh is not needed and these methods are
    now no-ops:

    .. code-block:: python

        # DEPRECATED - No longer needed
        await ProductStats.refresh()
        ProductStats.refresh_sync()

    These methods will be removed in a future version. Simply query the view to get
    current data:

    .. code-block:: python

        # Correct way - views are always up to date
        stats = await ProductStats.objects.all()

Live Updates
------------

SurrealDB materialized views are live, meaning they automatically update when:

- Source table data is inserted
- Source table data is updated
- Source table data is deleted

No manual refresh or rebuild is required. Just query the view to get current aggregated data.

Complex Aggregations
--------------------

Use aggregation pipelines for complex transformations:

.. code-block:: python

    from surrealengine import AggregationPipeline
    from surrealengine.aggregation import Count, Sum, Avg, Max, Min

    class SalesSummary(MaterializedView):
        table_name = "sales_summary"

        @classmethod
        def get_source_query(cls):
            pipeline = AggregationPipeline(Product.objects)
            return (pipeline
                .group(by_fields="category",
                       total_items=Count("*"),
                       total_revenue=Sum("price * quantity"),
                       avg_price=Avg("price"),
                       max_price=Max("price"),
                       min_price=Min("price"))
                .sort(total_revenue="DESC")
                .limit(50))

    await SalesSummary.create(if_not_exists=True)

Best Practices
--------------

1. **Use if_not_exists for idempotency**:

   .. code-block:: python

       await ProductStats.create(if_not_exists=True)

2. **Choose meaningful view names**:

   .. code-block:: python

       class UserActivitySummary(MaterializedView):
           table_name = "user_activity_summary"

3. **Don't use refresh()** - views are live and always current

4. **Index view columns** used in filters:

   .. code-block:: python

       class ProductStats(MaterializedView):
           table_name = "product_stats"

           class Meta:
               indexes = [
                   {"fields": ["category"], "unique": False},
                   {"fields": ["total_sales"], "unique": False}
               ]

5. **Use GROUP ALL for global aggregations**:

   .. code-block:: python

       # For global stats across all records
       return Product.objects.group_by(all=True).select(...)

Performance Considerations
--------------------------

- Materialized views improve query performance by pre-computing aggregations
- Views are stored as regular tables in SurrealDB
- Live updates may have a small performance impact on write operations
- For very large datasets, consider partitioning data or using time-based views
- Use ``omit()`` and field selection to minimize data transfer

Migration from Older Versions
------------------------------

If you're upgrading from versions < 0.5.0:

.. code-block:: python

    # OLD (< v0.5.0)
    await ProductStats.create()
    await ProductStats.refresh()  # Manually refresh

    # NEW (v0.5.0+)
    await ProductStats.create(if_not_exists=True)
    # No refresh needed - views are live!
    stats = await ProductStats.objects.all()  # Always current
