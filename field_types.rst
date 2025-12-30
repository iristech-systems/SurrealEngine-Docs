Field Types
===========

SurrealEngine provides a comprehensive set of field types for defining document schemas.
Fields handle validation, type conversion, and serialization between Python and SurrealDB.

Basic Field Types
-----------------

StringField
~~~~~~~~~~~

Store text data:

.. code-block:: python

    from surrealengine import StringField

    class User(Document):
        name = StringField(required=True, max_length=100)
        bio = StringField(max_length=500)
        status = StringField(choices=["active", "inactive", "pending"])

IntField
~~~~~~~~

Store integer numbers:

.. code-block:: python

    from surrealengine import IntField

    class Product(Document):
        quantity = IntField(min_value=0)
        stock_level = IntField(min_value=0, max_value=10000)

FloatField
~~~~~~~~~~

Store floating-point numbers:

.. code-block:: python

    from surrealengine import FloatField

    class Product(Document):
        price = FloatField(min_value=0.0, required=True)
        rating = FloatField(min_value=0.0, max_value=5.0)

BoolField
~~~~~~~~~

Store boolean values:

.. code-block:: python

    from surrealengine import BoolField

    class User(Document):
        is_active = BoolField(default=True)
        email_verified = BoolField(default=False)

Date and Time Fields
--------------------

DateTimeField
~~~~~~~~~~~~~

Store date and time:

.. code-block:: python

    from surrealengine import DateTimeField
    from datetime import datetime

    class Post(Document):
        created_at = DateTimeField(auto_now_add=True)
        updated_at = DateTimeField(auto_now=True)
        published_at = DateTimeField()

Options:
- ``auto_now_add=True``: Set to current time on creation
- ``auto_now=True``: Update to current time on each save

DurationField (v0.4.1+)
~~~~~~~~~~~~~~~~~~~~~~~

Store time durations using native SurrealDB Duration objects:

.. code-block:: python

    from surrealengine import DurationField
    from datetime import timedelta
    from surrealdb import Duration

    class Task(Document):
        estimated_time = DurationField()
        actual_time = DurationField()

    # Use with timedelta
    task = Task(estimated_time=timedelta(hours=2, minutes=30))
    await task.save()

    # Or use SurrealDB Duration objects directly
    task = Task(estimated_time=Duration(hours=2, minutes=30))
    await task.save()

.. note::

    **SDK Type Compliance (v0.4.1+)**

    DurationField now natively supports ``surrealdb.Duration`` objects for improved
    type safety and better integration with the SurrealDB SDK.

SurrealDB-Specific Fields
--------------------------

RecordIDField (v0.4.1+)
~~~~~~~~~~~~~~~~~~~~~~~

Store record identifiers with native RecordID support:

.. code-block:: python

    from surrealengine import RecordIDField
    from surrealdb import RecordID

    class Reference(Document):
        target = RecordIDField(table_name="users")  # Optional table validation

    # Use with strings
    ref = Reference(target="user:alice")
    await ref.save()

    # Or use RecordID objects directly
    ref = Reference(target=RecordID("user", "alice"))
    await ref.save()

    # The field returns RecordID objects
    ref = await Reference.objects.get(id=ref.id)
    print(type(ref.target))  # <class 'surrealdb.RecordID'>

.. note::

    **Breaking Change (v0.4.1+)**

    RecordIDField now returns ``surrealdb.RecordID`` objects instead of strings
    for improved type safety. Use ``str(record_id)`` if you need the string form.

TableField (v0.4.1+)
~~~~~~~~~~~~~~~~~~~~

Store table names with native Table object support:

.. code-block:: python

    from surrealengine import TableField
    from surrealdb import Table

    class Schema(Document):
        table_name = TableField()

    # Use with strings
    schema = Schema(table_name="users")
    await schema.save()

    # Or use Table objects
    schema = Schema(table_name=Table("users"))
    await schema.save()

.. note::

    **SDK Type Compliance (v0.4.1+)**

    TableField now natively supports ``surrealdb.Table`` objects.

RangeField (v0.4.1+)
~~~~~~~~~~~~~~~~~~~~

Store value ranges with native Range support:

.. code-block:: python

    from surrealengine import RangeField, IntField, FloatField
    from surrealdb import Range

    class PriceRange(Document):
        price_range = RangeField(
            min_type=FloatField(),
            max_type=FloatField()
        )
        age_range = RangeField(
            min_type=IntField(),
            max_type=IntField()
        )

    # Use with dictionaries
    product = PriceRange(
        price_range={"min": 10.0, "max": 50.0},
        age_range={"min": 18, "max": 65}
    )
    await product.save()

    # Or use Range objects
    product = PriceRange(
        price_range=Range(10.0, 50.0),
        age_range=Range(18, 65)
    )
    await product.save()

.. note::

    **SDK Type Compliance (v0.4.1+)**

    RangeField now natively supports ``surrealdb.Range`` objects for robust
    validation and serialization.

GeometryField (v0.4.1+)
~~~~~~~~~~~~~~~~~~~~~~~

Store geometric data with native Geometry support:

.. code-block:: python

    from surrealengine import GeometryField
    from surrealdb import Geometry

    class Location(Document):
        position = GeometryField()

    # Use with dictionaries (GeoJSON format)
    location = Location(position={
        "type": "Point",
        "coordinates": [-122.4194, 37.7749]
    })
    await location.save()

    # Or use Geometry objects
    location = Location(position=Geometry.Point([-122.4194, 37.7749]))
    await location.save()

Supported geometry types:
- Point
- LineString
- Polygon
- MultiPoint
- MultiLineString
- MultiPolygon

.. note::

    **SDK Type Compliance (v0.4.1+)**

    GeometryField now natively supports ``surrealdb.Geometry`` objects and
    strictly validates closed linear rings for Polygons.

Collection Fields
-----------------

ListField
~~~~~~~~~

Store lists of values:

.. code-block:: python

    from surrealengine import ListField, StringField, IntField

    class Article(Document):
        tags = ListField(StringField())
        scores = ListField(IntField())

    article = Article(
        tags=["python", "surrealdb", "orm"],
        scores=[5, 4, 5, 3]
    )
    await article.save()

SetField
~~~~~~~~

Store unique values (automatically removes duplicates):

.. code-block:: python

    from surrealengine import SetField, StringField

    class User(Document):
        interests = SetField(StringField())

    user = User(interests=["python", "rust", "python"])  # Duplicate removed
    await user.save()
    print(user.interests)  # {"python", "rust"}

DictField
~~~~~~~~~

Store nested dictionaries:

.. code-block:: python

    from surrealengine import DictField

    class User(Document):
        settings = DictField()
        metadata = DictField()

    user = User(settings={
        "theme": "dark",
        "language": "en",
        "notifications": True
    })
    await user.save()

    # Query nested fields
    users = await User.objects.filter(settings__theme="dark")

Specialized Fields
------------------

EmailField
~~~~~~~~~~

Store and validate email addresses:

.. code-block:: python

    from surrealengine import EmailField

    class User(Document):
        email = EmailField(required=True)

    # Automatically validates email format
    user = User(email="alice@example.com")
    await user.save()

URLField
~~~~~~~~

Store and validate URLs:

.. code-block:: python

    from surrealengine import URLField

    class Website(Document):
        url = URLField(required=True)

    website = Website(url="https://example.com")
    await website.save()

IPAddressField
~~~~~~~~~~~~~~

Store and validate IP addresses:

.. code-block:: python

    from surrealengine import IPAddressField

    class Connection(Document):
        ip_address = IPAddressField(version=4)  # IPv4 only
        ipv6_address = IPAddressField(version=6)  # IPv6 only
        any_ip = IPAddressField()  # Both IPv4 and IPv6

SlugField
~~~~~~~~~

Store URL-friendly strings:

.. code-block:: python

    from surrealengine import SlugField

    class Article(Document):
        title = StringField(required=True)
        slug = SlugField(required=True)

    article = Article(title="My Article", slug="my-article")
    await article.save()

ChoiceField
~~~~~~~~~~~

Restrict values to a predefined set:

.. code-block:: python

    from surrealengine import ChoiceField

    class Task(Document):
        status = ChoiceField(choices=[
            ("pending", "Pending"),
            ("in_progress", "In Progress"),
            ("completed", "Completed"),
            ("cancelled", "Cancelled")
        ])

    task = Task(status="pending")
    await task.save()

Reference Fields
----------------

ReferenceField
~~~~~~~~~~~~~~

Create references to other documents:

.. code-block:: python

    from surrealengine import ReferenceField

    class Comment(Document):
        content = StringField(required=True)
        author = ReferenceField("User", required=True)
        post = ReferenceField("Post", required=True)

    # Create with references
    comment = Comment(
        content="Great post!",
        author="user:alice",
        post="post:123"
    )
    await comment.save()

    # Fetch referenced documents
    comments = await Comment.objects.fetch("author", "post").all()
    print(comments[0].author.name)  # Access author's name

RelationField
~~~~~~~~~~~~~

Define graph relationships:

.. code-block:: python

    from surrealengine import RelationField, RelationDocument

    class User(Document):
        name = StringField(required=True)
        following = RelationField("Follows", out_ref=True)
        followers = RelationField("Follows", in_ref=True)

    class Follows(RelationDocument):
        since = DateTimeField(auto_now_add=True)

        class Meta:
            collection = "follows"
            in_doc = "User"
            out_doc = "User"

Field Options
-------------

Common Options
~~~~~~~~~~~~~~

All fields support these options:

.. code-block:: python

    field = StringField(
        required=True,           # Field must have a value
        default="draft",         # Default value if not provided
        null=False,              # Allow None values
        unique=False,            # Enforce uniqueness
        indexed=False,           # Create database index
        help_text="Field help"   # Documentation
    )

Validation Options
~~~~~~~~~~~~~~~~~~

Numeric fields (IntField, FloatField):

.. code-block:: python

    age = IntField(min_value=0, max_value=150)
    price = FloatField(min_value=0.0)

String fields:

.. code-block:: python

    name = StringField(
        min_length=2,
        max_length=100,
        regex=r'^[A-Za-z\s]+$'
    )

SDK Type Compliance Summary (v0.4.1+)
--------------------------------------

The following fields now natively support SurrealDB SDK types:

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Field Type
     - Python Type
     - SurrealDB SDK Type
   * - DurationField
     - ``timedelta``
     - ``surrealdb.Duration``
   * - RangeField
     - ``dict``
     - ``surrealdb.Range``
   * - GeometryField
     - ``dict`` (GeoJSON)
     - ``surrealdb.Geometry``
   * - TableField
     - ``str``
     - ``surrealdb.Table``
   * - RecordIDField
     - ``str``
     - ``surrealdb.RecordID``

Benefits:
- Type safety with proper type hints
- Better integration with SurrealDB SDK
- Robust validation and serialization
- Fixes CBOR serialization errors

Custom Fields
-------------

Create custom field types by extending the base Field class:

.. code-block:: python

    from surrealengine.fields import Field

    class UpperCaseField(Field):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.py_type = str

        def validate(self, value):
            if not isinstance(value, str):
                raise ValueError("Value must be a string")
            return value.upper()

    class User(Document):
        code = UpperCaseField()

    user = User(code="abc123")
    await user.save()
    print(user.code)  # "ABC123"

Best Practices
--------------

1. **Use appropriate field types**:

   .. code-block:: python

       # Good
       email = EmailField()
       age = IntField(min_value=0)

       # Avoid
       email = StringField()  # No validation
       age = StringField()    # Wrong type

2. **Set sensible defaults**:

   .. code-block:: python

       status = StringField(default="draft")
       created_at = DateTimeField(auto_now_add=True)

3. **Use SDK types for better integration (v0.4.1+)**:

   .. code-block:: python

       from surrealdb import RecordID, Duration

       # Good - native SDK type
       target = RecordID("user", "alice")

       # Also works - string form
       target = "user:alice"

4. **Validate at field level**:

   .. code-block:: python

       age = IntField(min_value=0, max_value=150)
       # Better than validating in business logic

5. **Use references for relationships**:

   .. code-block:: python

       author = ReferenceField("User", required=True)
       # Better than storing user ID as string

Migration Guide
---------------

If upgrading from versions before v0.4.1:

.. code-block:: python

    # OLD - RecordIDField returned strings
    ref = await Reference.objects.get(id=ref_id)
    table, id = ref.target.split(":")  # Parse string

    # NEW (v0.4.1+) - Returns RecordID objects
    ref = await Reference.objects.get(id=ref_id)
    table = ref.target.table
    id = ref.target.id
    string_form = str(ref.target)  # Get string if needed

The same applies to DurationField, RangeField, GeometryField, and TableField - they now
return native SurrealDB SDK objects instead of dictionaries or strings.
