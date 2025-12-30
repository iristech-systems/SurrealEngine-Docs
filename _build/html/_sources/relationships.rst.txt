Relationships
=============

SurrealEngine supports graph relationships, allowing you to model complex connections
between documents. This guide covers reference fields, graph relations, and traversals.

For complete examples, see: ``example_scripts/relationships_example.py``

Reference Fields
----------------

Simple one-to-many relationships:

.. code-block:: python

    from surrealengine import Document, StringField, ReferenceField

    class Author(Document):
        name = StringField(required=True)
        
        class Meta:
            collection = "authors"

    class Book(Document):
        title = StringField(required=True)
        author = ReferenceField("Author", required=True)
        
        class Meta:
            collection = "books"

    # Create relationships
    author = Author(name="Alice")
    await author.save()
    
    book = Book(title="Python Guide", author=author.id)
    await book.save()
    
    # Fetch with references
    books = await Book.objects.fetch("author").all()
    print(books[0].author.name)  # "Alice"

Graph Relationships
-------------------

Many-to-many relationships using RelationDocument:

.. code-block:: python

    from surrealengine import RelationDocument, RelationField, DateTimeField

    class User(Document):
        name = StringField(required=True)
        following = RelationField("Follows", out_ref=True)
        followers = RelationField("Follows", in_ref=True)
        
        class Meta:
            collection = "users"

    class Follows(RelationDocument):
        since = DateTimeField(auto_now_add=True)
        
        class Meta:
            collection = "follows"
            in_doc = "User"
            out_doc = "User"

    # Create relationship
    alice = await User(name="Alice").save()
    bob = await User(name="Bob").save()
    
    follow = Follows(in_doc=bob.id, out_doc=alice.id)
    await follow.save()
    
    # Query relationships
    followers = await Follows.objects.filter(in_doc=bob.id).all()

Graph Traversals
----------------

Traverse graph relationships:

.. code-block:: python

    # Traverse one level
    query = User.objects.traverse("->follows->user")
    users = await query.all()
    
    # Multi-level traversal with depth
    query = User.objects.traverse("->follows->user", max_depth=3)
    users = await query.all()

Bidirectional Relations
-----------------------

Navigate relationships in both directions:

.. code-block:: python

    # Get followers
    async def get_followers(user_id: str):
        return await Follows.objects.filter(in_doc=user_id).fetch("out_doc").all()
    
    # Get following
    async def get_following(user_id: str):
        return await Follows.objects.filter(out_doc=user_id).fetch("in_doc").all()

Complex Relationship Queries
----------------------------

.. code-block:: python

    from surrealengine import Q
    
    # Users following bob and alice
    common_followers = await Follows.objects.filter(
        Q(in_doc=bob.id) | Q(in_doc=alice.id)
    ).all()
    
    # Recent followers
    recent = await Follows.objects.filter(
        in_doc=bob.id
    ).order_by("-since").limit(10).all()

For more examples, see :doc:`tutorial` and ``example_scripts/relationships_example.py``
