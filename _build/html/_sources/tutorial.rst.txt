Tutorial: Building a Blog Application
======================================

This tutorial will guide you through building a complete blog application with SurrealEngine,
covering documents, relationships, queries, and real-time updates.

What You'll Build
-----------------

A blog platform with:

- User authentication and profiles
- Blog posts with categories and tags
- Comments on posts
- Real-time notifications for new comments
- User following/followers (graph relationships)

Project Setup
-------------

Create a new project:

.. code-block:: bash

    mkdir blog-app
    cd blog-app
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install surrealengine

Start SurrealDB:

.. code-block:: bash

    docker run --rm -p 8000:8000 surrealdb/surrealdb:latest \
        start --user root --pass root

Step 1: Define Document Models
-------------------------------

Create ``models.py``:

.. code-block:: python

    from surrealengine import (
        Document, RelationDocument,
        StringField, IntField, BoolField, DateTimeField,
        ListField, ReferenceField, RelationField,
        EmailField
    )

    class User(Document):
        """User model with profile information."""
        username = StringField(required=True, unique=True, max_length=50)
        email = EmailField(required=True, unique=True)
        password_hash = StringField(required=True)
        bio = StringField(max_length=500)
        avatar_url = StringField()
        created_at = DateTimeField(auto_now_add=True)

        # Graph relationships
        following = RelationField("Follows", out_ref=True)
        followers = RelationField("Follows", in_ref=True)

        class Meta:
            collection = "users"
            schemafull = True
            indexes = [
                {"fields": ["username"], "unique": True},
                {"fields": ["email"], "unique": True}
            ]

    class Category(Document):
        """Blog post category."""
        name = StringField(required=True, unique=True)
        slug = StringField(required=True, unique=True)
        description = StringField()

        class Meta:
            collection = "categories"

    class Post(Document):
        """Blog post."""
        title = StringField(required=True, max_length=200)
        slug = StringField(required=True, unique=True)
        content = StringField(required=True)
        excerpt = StringField(max_length=300)
        author = ReferenceField("User", required=True)
        category = ReferenceField("Category")
        tags = ListField(StringField())
        published = BoolField(default=False)
        views = IntField(default=0)
        created_at = DateTimeField(auto_now_add=True)
        updated_at = DateTimeField(auto_now=True)

        class Meta:
            collection = "posts"
            schemafull = True
            indexes = [
                {"fields": ["slug"], "unique": True},
                {"fields": ["author"]},
                {"fields": ["category"]},
                {"fields": ["published"]},
                {"fields": ["created_at"]}
            ]

    class Comment(Document):
        """Comment on a blog post."""
        content = StringField(required=True, max_length=1000)
        author = ReferenceField("User", required=True)
        post = ReferenceField("Post", required=True)
        created_at = DateTimeField(auto_now_add=True)
        edited = BoolField(default=False)

        class Meta:
            collection = "comments"
            indexes = [
                {"fields": ["post"]},
                {"fields": ["author"]},
                {"fields": ["created_at"]}
            ]

    class Follows(RelationDocument):
        """Graph relationship: User follows User."""
        followed_at = DateTimeField(auto_now_add=True)

        class Meta:
            collection = "follows"
            in_doc = "User"
            out_doc = "User"

Step 2: Initialize Database
----------------------------

Create ``database.py``:

.. code-block:: python

    import asyncio
    from surrealengine import create_connection
    from models import User, Category, Post, Comment, Follows

    async def init_database():
        """Initialize database connection and create tables."""
        connection = create_connection(
            url="ws://localhost:8000/rpc",
            namespace="blog",
            database="production",
            username="root",
            password="root",
            async_mode=True,
            use_pool=True,
            pool_size=20,
            make_default=True
        )

        await connection.connect()
        print("✓ Connected to SurrealDB")

        # Create tables
        await User.create_table()
        await Category.create_table()
        await Post.create_table()
        await Comment.create_table()
        await Follows.create_table()
        print("✓ Created tables")

        # Create indexes
        await User.create_indexes()
        await Post.create_indexes()
        await Comment.create_indexes()
        print("✓ Created indexes")

        return connection

    if __name__ == "__main__":
        asyncio.run(init_database())

Run the initialization:

.. code-block:: bash

    python database.py

Step 3: User Management
-----------------------

Create ``users.py``:

.. code-block:: python

    import hashlib
    from models import User, Follows

    def hash_password(password: str) -> str:
        """Simple password hashing (use proper hashing in production!)."""
        return hashlib.sha256(password.encode()).hexdigest()

    async def create_user(username: str, email: str, password: str, bio: str = ""):
        """Create a new user."""
        user = User(
            username=username,
            email=email,
            password_hash=hash_password(password),
            bio=bio
        )
        await user.save()
        print(f"✓ Created user: {user.username} ({user.id})")
        return user

    async def follow_user(follower_id: str, followed_id: str):
        """Create a follow relationship."""
        follow = Follows(in_doc=followed_id, out_doc=follower_id)
        await follow.save()
        print(f"✓ {follower_id} is now following {followed_id}")
        return follow

    async def get_user_followers(user_id: str):
        """Get all followers of a user."""
        from surrealengine import QuerySet
        followers = await QuerySet(Follows, None).filter(in_doc=user_id).all()
        return followers

    async def get_user_following(user_id: str):
        """Get all users that a user is following."""
        from surrealengine import QuerySet
        following = await QuerySet(Follows, None).filter(out_doc=user_id).all()
        return following

Step 4: Blog Post Operations
-----------------------------

Create ``posts.py``:

.. code-block:: python

    from models import Post, Category, Comment

    async def create_category(name: str, slug: str, description: str = ""):
        """Create a blog category."""
        category = Category(name=name, slug=slug, description=description)
        await category.save()
        return category

    async def create_post(title: str, slug: str, content: str,
                         author_id: str, category_id: str = None,
                         tags: list = None, published: bool = False):
        """Create a new blog post."""
        post = Post(
            title=title,
            slug=slug,
            content=content,
            excerpt=content[:300],
            author=author_id,
            category=category_id,
            tags=tags or [],
            published=published
        )
        await post.save()
        print(f"✓ Created post: {post.title} ({post.id})")
        return post

    async def publish_post(post_id: str):
        """Publish a draft post."""
        post = await Post.objects.get(id=post_id)
        await post.update(published=True)
        print(f"✓ Published post: {post.title}")
        return post

    async def increment_views(post_id: str):
        """Increment post view count."""
        post = await Post.objects.get(id=post_id)
        await post.update(views=post.views + 1)
        return post

    async def add_comment(post_id: str, author_id: str, content: str):
        """Add a comment to a post."""
        comment = Comment(
            content=content,
            author=author_id,
            post=post_id
        )
        await comment.save()
        print(f"✓ Added comment to post {post_id}")
        return comment

    async def get_post_with_comments(post_id: str):
        """Get a post with all its comments and related data."""
        # Fetch post with author and category
        post = await Post.objects.fetch("author", "category").get(id=post_id)

        # Get comments with authors
        comments = await Comment.objects.filter(post=post_id).fetch("author").all()

        return post, comments

Step 5: Advanced Queries
-------------------------

Create ``queries.py``:

.. code-block:: python

    from surrealengine import Q
    from models import Post, User, Comment

    async def search_posts(keyword: str):
        """Search posts by keyword in title or content."""
        posts = await Post.objects.filter(
            Q(title__contains=keyword) | Q(content__contains=keyword)
        ).filter(published=True).order_by("-created_at")
        return posts

    async def get_popular_posts(limit: int = 10):
        """Get most viewed published posts."""
        posts = await (Post.objects
            .filter(published=True)
            .order_by("-views")
            .limit(limit)
            .fetch("author", "category")
        )
        return posts

    async def get_user_feed(user_id: str, page: int = 1, page_size: int = 20):
        """Get paginated feed of posts from followed users."""
        from surrealengine import QuerySet
        from models import Follows

        # Get IDs of users that user is following
        following = await QuerySet(Follows, None).filter(out_doc=user_id).all()
        following_ids = [f.in_doc for f in following]

        # Get posts from followed users
        posts = await (Post.objects
            .filter(author__inside=following_ids)
            .filter(published=True)
            .order_by("-created_at")
            .page(page, page_size)
            .fetch("author")
        )
        return posts

    async def get_trending_tags(limit: int = 10):
        """Get most used tags across published posts."""
        from surrealengine import AggregationPipeline

        pipeline = AggregationPipeline(Post.objects.filter(published=True))
        # Note: This is a simplified example
        # In production, you'd use proper aggregation
        posts = await Post.objects.filter(published=True).all()
        tag_counts = {}
        for post in posts:
            for tag in post.tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1

        sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
        return sorted_tags[:limit]

Step 6: Real-Time Comments with LIVE Queries
---------------------------------------------

Create ``live_comments.py``:

.. code-block:: python

    import asyncio
    from models import Comment

    async def watch_post_comments(post_id: str):
        """Watch for new comments on a post in real-time."""
        print(f"Watching for comments on post: {post_id}")

        async for event in Comment.objects.live(
            where={"post": post_id},
            action="CREATE"
        ):
            if event.is_create:
                comment_data = event.data
                print(f"New comment: {comment_data.get('content')[:50]}...")
                # Here you could:
                # - Send notification to post author
                # - Update real-time dashboard
                # - Trigger webhooks
                # etc.

    async def watch_user_mentions(user_id: str):
        """Watch for mentions of a user in comments."""
        async for event in Comment.objects.live(action=["CREATE", "UPDATE"]):
            content = event.data.get("content", "")
            if f"@{user_id}" in content:
                print(f"You were mentioned in a comment!")
                # Send notification

Step 7: Putting It All Together
--------------------------------

Create ``app.py``:

.. code-block:: python

    import asyncio
    from database import init_database
    from users import create_user, follow_user
    from posts import (
        create_category, create_post, publish_post,
        add_comment, get_post_with_comments
    )
    from queries import get_popular_posts, search_posts

    async def main():
        # Initialize database
        await init_database()

        # Create users
        alice = await create_user(
            "alice",
            "alice@example.com",
            "password123",
            "Tech blogger and Python enthusiast"
        )
        bob = await create_user(
            "bob",
            "bob@example.com",
            "password456",
            "Full-stack developer"
        )

        # Bob follows Alice
        await follow_user(bob.id, alice.id)

        # Create categories
        tech = await create_category(
            "Technology",
            "technology",
            "All about tech"
        )
        python = await create_category(
            "Python",
            "python",
            "Python programming"
        )

        # Alice creates posts
        post1 = await create_post(
            "Getting Started with SurrealDB",
            "getting-started-surrealdb",
            "SurrealDB is an amazing database...",
            alice.id,
            tech.id,
            tags=["surrealdb", "database", "nosql"],
            published=False
        )

        # Publish the post
        await publish_post(post1.id)

        # Bob adds a comment
        comment = await add_comment(
            post1.id,
            bob.id,
            "Great post! Very helpful."
        )

        # Get post with all comments
        post, comments = await get_post_with_comments(post1.id)
        print(f"\nPost: {post.title}")
        print(f"Author: {post.author.username}")
        print(f"Category: {post.category.name if post.category else 'None'}")
        print(f"Comments: {len(comments)}")
        for c in comments:
            print(f"  - {c.author.username}: {c.content}")

        # Search posts
        results = await search_posts("SurrealDB")
        print(f"\nSearch results: {len(results)} posts")

        # Get popular posts
        popular = await get_popular_posts(limit=5)
        print(f"\nPopular posts: {len(popular)}")

    if __name__ == "__main__":
        asyncio.run(main())

Run the application:

.. code-block:: bash

    python app.py

Expected Output
---------------

.. code-block:: text

    ✓ Connected to SurrealDB
    ✓ Created tables
    ✓ Created indexes
    ✓ Created user: alice (user:alice_id)
    ✓ Created user: bob (user:bob_id)
    ✓ bob_id is now following alice_id
    ✓ Created post: Getting Started with SurrealDB (post:post_id)
    ✓ Published post: Getting Started with SurrealDB
    ✓ Added comment to post post_id

    Post: Getting Started with SurrealDB
    Author: alice
    Category: Technology
    Comments: 1
      - bob: Great post! Very helpful.

    Search results: 1 posts

    Popular posts: 1

Next Steps
----------

Enhance your blog application:

1. **Add authentication**: Implement JWT tokens for user authentication
2. **Add pagination**: Use ``.page()`` for all list views
3. **Add caching**: Cache popular posts and categories
4. **Add search**: Implement full-text search with indexes
5. **Add notifications**: Use LIVE queries for real-time notifications
6. **Add moderation**: Flag and moderate comments
7. **Add analytics**: Track user engagement with materialized views
8. **Add file uploads**: Store and serve images for posts

Additional Resources
--------------------

- :doc:`document_models` - Learn more about document models
- :doc:`querying` - Advanced querying techniques
- :doc:`relationships` - Graph relationships in depth
- :doc:`live` - Real-time LIVE queries
- :doc:`materialized_views` - Analytics and aggregations
- :doc:`performance` - Optimization tips

Complete Example
----------------

The complete working example is available in the repository at
``example_scripts/`` directory.
