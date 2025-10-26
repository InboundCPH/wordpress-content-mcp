#!/usr/bin/env python3
"""
WordPress Content Management MCP Server

This MCP server provides intelligent content management for WordPress sites,
with AI-powered content generation and optimization capabilities.
"""

import logging
import sys
from typing import List, Optional, Dict, Any
from fastmcp import FastMCP

# Add src to path
sys.path.insert(0, str(__file__).replace('mcp_server.py', ''))

from src.config.settings import settings
from src.services.post_service import PostService
from src.api.wordpress_client import WordPressClient

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger("wordpress-mcp")

# Validate settings
if not settings.validate():
    logger.error("Missing required configuration. Please check your .env file.")
    logger.error("Required: WORDPRESS_URL, WORDPRESS_USERNAME, WORDPRESS_APP_PASSWORD")
    sys.exit(1)

# Initialize FastMCP server
mcp = FastMCP("wordpress-content-management")

# Initialize services
post_service = PostService()
wp_client = WordPressClient()

logger.info(f"WordPress MCP Server initialized for {settings.WORDPRESS_URL}")


# ============================================================================
# Post Management Tools
# ============================================================================

@mcp.tool()
def list_posts(
    per_page: int = 10,
    page: int = 1,
    status: str = "publish",
    search: Optional[str] = None,
    categories: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    List WordPress posts with filtering options.
    
    Args:
        per_page: Number of posts per page (default: 10)
        page: Page number (default: 1)
        status: Post status - publish, draft, pending, private (default: publish)
        search: Search query to filter posts
        categories: Comma-separated category IDs to filter by
    
    Returns:
        List of posts with id, title, status, date, link, and excerpt
    """
    category_ids = None
    if categories:
        category_ids = [int(c.strip()) for c in categories.split(',')]
    
    return post_service.list_posts(
        per_page=per_page,
        page=page,
        status=status,
        search=search,
        categories=category_ids
    )


@mcp.tool()
def get_post(post_id: int) -> Dict[str, Any]:
    """
    Get a specific WordPress post with full details including ACF fields.
    
    Args:
        post_id: The WordPress post ID
    
    Returns:
        Complete post data including title, content, excerpt, categories, tags, ACF fields, etc.
    """
    post = post_service.get_post(post_id)
    return {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "excerpt": post.excerpt,
        "status": post.status,
        "slug": post.slug,
        "date": post.date.isoformat(),
        "modified": post.modified.isoformat(),
        "author": post.author,
        "categories": post.categories,
        "tags": post.tags,
        "featured_media": post.featured_media,
        "link": post.link,
        "acf": post.acf
    }


@mcp.tool()
def create_post(
    title: str,
    content: str,
    status: str = "draft",
    excerpt: Optional[str] = None,
    categories: Optional[str] = None,
    tags: Optional[str] = None,
    acf_fields: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a new WordPress post.
    
    Args:
        title: Post title
        content: Post content (HTML)
        status: Post status - draft, publish, pending, private (default: draft)
        excerpt: Post excerpt/summary
        categories: Comma-separated category IDs
        tags: Comma-separated tag IDs
        acf_fields: JSON string of ACF custom fields
    
    Returns:
        Created post data with id, title, link, and status
    """
    from src.models.post import PostCreate
    import json
    
    # Parse categories and tags
    category_ids = [int(c.strip()) for c in categories.split(',')] if categories else None
    tag_ids = [int(t.strip()) for t in tags.split(',')] if tags else None
    
    # Parse ACF fields
    acf_data = json.loads(acf_fields) if acf_fields else None
    
    post_data = PostCreate(
        title=title,
        content=content,
        status=status,
        excerpt=excerpt,
        categories=category_ids,
        tags=tag_ids,
        acf_fields=acf_data
    )
    
    post = post_service.create_post(post_data)
    
    return {
        "id": post.id,
        "title": post.title,
        "link": post.link,
        "status": post.status,
        "date": post.date.isoformat()
    }


@mcp.tool()
def update_post(
    post_id: int,
    title: Optional[str] = None,
    content: Optional[str] = None,
    status: Optional[str] = None,
    excerpt: Optional[str] = None,
    categories: Optional[str] = None,
    tags: Optional[str] = None,
    acf_fields: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update an existing WordPress post.
    
    Args:
        post_id: The WordPress post ID to update
        title: New post title (optional)
        content: New post content (optional)
        status: New post status (optional)
        excerpt: New post excerpt (optional)
        categories: Comma-separated category IDs (optional)
        tags: Comma-separated tag IDs (optional)
        acf_fields: JSON string of ACF custom fields (optional)
    
    Returns:
        Updated post data
    """
    from src.models.post import PostUpdate
    import json
    
    # Parse categories and tags
    category_ids = [int(c.strip()) for c in categories.split(',')] if categories else None
    tag_ids = [int(t.strip()) for t in tags.split(',')] if tags else None
    
    # Parse ACF fields
    acf_data = json.loads(acf_fields) if acf_fields else None
    
    post_data = PostUpdate(
        title=title,
        content=content,
        status=status,
        excerpt=excerpt,
        categories=category_ids,
        tags=tag_ids,
        acf_fields=acf_data
    )
    
    post = post_service.update_post(post_id, post_data)
    
    return {
        "id": post.id,
        "title": post.title,
        "link": post.link,
        "status": post.status,
        "modified": post.modified.isoformat()
    }


@mcp.tool()
def delete_post(post_id: int, force: bool = False) -> Dict[str, str]:
    """
    Delete a WordPress post (moves to trash by default).
    
    Args:
        post_id: The WordPress post ID to delete
        force: If true, permanently delete the post. If false, move to trash (default: false)
    
    Returns:
        Deletion status
    """
    result = post_service.delete_post(post_id, force=force)
    return {
        "status": "deleted" if force else "trashed",
        "post_id": str(post_id)
    }


# ============================================================================
# AI Content Generation Tools
# ============================================================================

@mcp.tool()
def generate_blog_post(
    topic: str,
    keywords: Optional[str] = None,
    tone: str = "professional",
    length: str = "medium",
    language: str = "da",
    save_as_draft: bool = True
) -> Dict[str, Any]:
    """
    Generate a complete blog post using AI.
    
    Args:
        topic: Topic or subject for the blog post
        keywords: Comma-separated SEO keywords to include
        tone: Tone of voice - professional, casual, friendly, etc. (default: professional)
        length: Content length - short (400-600 words), medium (800-1200 words), long (1500-2000 words) (default: medium)
        language: Content language - da (Danish), en (English), sv (Swedish), etc. (default: da)
        save_as_draft: Save generated post as draft in WordPress (default: true)
    
    Returns:
        Generated post with title, content, excerpt, and post ID if saved
    """
    keyword_list = [k.strip() for k in keywords.split(',')] if keywords else None
    
    return post_service.generate_post(
        topic=topic,
        keywords=keyword_list,
        tone=tone,
        length=length,
        language=language,
        save_as_draft=save_as_draft
    )


@mcp.tool()
def improve_post_content(
    post_id: int,
    improvements: Optional[str] = "seo,readability,structure",
    save_changes: bool = False
) -> Dict[str, Any]:
    """
    Improve existing post content using AI.
    
    Args:
        post_id: The WordPress post ID to improve
        improvements: Comma-separated list of improvements - seo, readability, structure, grammar (default: seo,readability,structure)
        save_changes: Save improved content directly to WordPress (default: false)
    
    Returns:
        Original and improved content, with post ID and save status
    """
    improvement_list = [i.strip() for i in improvements.split(',')]
    
    return post_service.improve_post(
        post_id=post_id,
        improvements=improvement_list,
        save_changes=save_changes
    )


@mcp.tool()
def optimize_post_seo(
    post_id: int,
    target_keywords: Optional[str] = None,
    save_changes: bool = False
) -> Dict[str, Any]:
    """
    Optimize post for SEO (title, meta description, content suggestions).
    
    Args:
        post_id: The WordPress post ID to optimize
        target_keywords: Comma-separated target keywords for SEO
        save_changes: Save optimized title directly to WordPress (default: false)
    
    Returns:
        Current and optimized title, meta description, and content suggestions
    """
    keyword_list = [k.strip() for k in target_keywords.split(',')] if target_keywords else None
    
    return post_service.optimize_post_seo(
        post_id=post_id,
        target_keywords=keyword_list,
        save_changes=save_changes
    )


# ============================================================================
# Utility Tools
# ============================================================================

@mcp.tool()
def get_categories() -> List[Dict[str, Any]]:
    """
    Get all WordPress categories.
    
    Returns:
        List of categories with id, name, slug, and count
    """
    categories = wp_client.get_categories()
    return [
        {
            "id": cat["id"],
            "name": cat["name"],
            "slug": cat["slug"],
            "count": cat["count"]
        }
        for cat in categories
    ]


@mcp.tool()
def get_tags() -> List[Dict[str, Any]]:
    """
    Get all WordPress tags.
    
    Returns:
        List of tags with id, name, slug, and count
    """
    tags = wp_client.get_tags()
    return [
        {
            "id": tag["id"],
            "name": tag["name"],
            "slug": tag["slug"],
            "count": tag["count"]
        }
        for tag in tags
    ]


@mcp.tool()
def search_posts(
    query: str,
    search_in: Optional[str] = "title,content"
) -> List[Dict[str, Any]]:
    """
    Search for posts by keyword.
    
    Args:
        query: Search query
        search_in: Comma-separated list of fields to search in - title, content, excerpt (default: title,content)
    
    Returns:
        List of matching posts with id, title, excerpt, and link
    """
    search_columns = [s.strip() for s in search_in.split(',')] if search_in else None
    
    return post_service.search_posts(
        query=query,
        search_in=search_columns
    )


# ============================================================================
# Run Server
# ============================================================================

if __name__ == "__main__":
    logger.info("Starting WordPress Content Management MCP Server...")
    logger.info(f"Connected to: {settings.WORDPRESS_URL}")
    logger.info("Available tools: 12")
    mcp.run()

