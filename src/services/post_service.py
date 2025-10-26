"""Service for managing WordPress posts."""

import logging
from typing import List, Optional, Dict, Any
from ..api.wordpress_client import WordPressClient
from ..models.post import Post, PostCreate, PostUpdate
from .content_generator import ContentGenerator

logger = logging.getLogger(__name__)


class PostService:
    """Service for post management operations."""
    
    def __init__(self):
        """Initialize post service."""
        self.wp_client = WordPressClient()
        self.content_generator = ContentGenerator()
    
    def list_posts(
        self,
        per_page: int = 10,
        page: int = 1,
        status: str = "publish",
        search: Optional[str] = None,
        categories: Optional[List[int]] = None
    ) -> List[Dict[str, Any]]:
        """List posts with filtering."""
        try:
            posts = self.wp_client.get_posts(
                per_page=per_page,
                page=page,
                status=status,
                search=search,
                categories=categories
            )
            
            # Return simplified post data
            return [
                {
                    "id": post["id"],
                    "title": post["title"]["rendered"] if isinstance(post["title"], dict) else post["title"],
                    "status": post["status"],
                    "date": post["date"],
                    "link": post["link"],
                    "excerpt": post["excerpt"]["rendered"] if isinstance(post["excerpt"], dict) else post.get("excerpt", "")
                }
                for post in posts
            ]
        
        except Exception as e:
            logger.error(f"Error listing posts: {str(e)}")
            raise
    
    def get_post(self, post_id: int) -> Post:
        """Get a specific post with full details."""
        try:
            post_data = self.wp_client.get_post(post_id)
            return Post.from_api_response(post_data)
        
        except Exception as e:
            logger.error(f"Error getting post {post_id}: {str(e)}")
            raise
    
    def create_post(self, post_data: PostCreate) -> Post:
        """Create a new post."""
        try:
            # Prepare data for WordPress API
            wp_data = {
                "title": post_data.title,
                "content": post_data.content,
                "status": post_data.status,
            }
            
            if post_data.excerpt:
                wp_data["excerpt"] = post_data.excerpt
            
            if post_data.categories:
                wp_data["categories"] = post_data.categories
            
            if post_data.tags:
                wp_data["tags"] = post_data.tags
            
            if post_data.featured_media:
                wp_data["featured_media"] = post_data.featured_media
            
            if post_data.acf_fields:
                wp_data["acf"] = post_data.acf_fields
            
            # Create post
            created_post = self.wp_client.create_post(wp_data)
            
            logger.info(f"Created post: {created_post['id']} - {created_post['title']['rendered']}")
            
            return Post.from_api_response(created_post)
        
        except Exception as e:
            logger.error(f"Error creating post: {str(e)}")
            raise
    
    def update_post(self, post_id: int, post_data: PostUpdate) -> Post:
        """Update an existing post."""
        try:
            # Prepare data for WordPress API (only include non-None fields)
            wp_data = {}
            
            if post_data.title is not None:
                wp_data["title"] = post_data.title
            
            if post_data.content is not None:
                wp_data["content"] = post_data.content
            
            if post_data.status is not None:
                wp_data["status"] = post_data.status
            
            if post_data.excerpt is not None:
                wp_data["excerpt"] = post_data.excerpt
            
            if post_data.categories is not None:
                wp_data["categories"] = post_data.categories
            
            if post_data.tags is not None:
                wp_data["tags"] = post_data.tags
            
            if post_data.featured_media is not None:
                wp_data["featured_media"] = post_data.featured_media
            
            if post_data.acf_fields is not None:
                wp_data["acf"] = post_data.acf_fields
            
            # Update post
            updated_post = self.wp_client.update_post(post_id, wp_data)
            
            logger.info(f"Updated post: {post_id}")
            
            return Post.from_api_response(updated_post)
        
        except Exception as e:
            logger.error(f"Error updating post {post_id}: {str(e)}")
            raise
    
    def delete_post(self, post_id: int, force: bool = False) -> Dict[str, Any]:
        """Delete a post."""
        try:
            result = self.wp_client.delete_post(post_id, force=force)
            logger.info(f"Deleted post: {post_id} (force={force})")
            return result
        
        except Exception as e:
            logger.error(f"Error deleting post {post_id}: {str(e)}")
            raise
    
    def search_posts(
        self,
        query: str,
        search_in: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """Search for posts."""
        try:
            posts = self.wp_client.search_posts(query, search_columns=search_in)
            
            return [
                {
                    "id": post["id"],
                    "title": post["title"]["rendered"] if isinstance(post["title"], dict) else post["title"],
                    "excerpt": post["excerpt"]["rendered"] if isinstance(post["excerpt"], dict) else post.get("excerpt", ""),
                    "link": post["link"]
                }
                for post in posts
            ]
        
        except Exception as e:
            logger.error(f"Error searching posts: {str(e)}")
            raise
    
    def generate_post(
        self,
        topic: str,
        keywords: Optional[List[str]] = None,
        tone: str = "professional",
        length: str = "medium",
        language: str = "da",
        save_as_draft: bool = True
    ) -> Dict[str, Any]:
        """Generate a blog post using AI."""
        try:
            # Generate content
            generated = self.content_generator.generate_blog_post(
                topic=topic,
                keywords=keywords,
                tone=tone,
                length=length,
                language=language
            )
            
            if save_as_draft:
                # Create post as draft
                post_data = PostCreate(
                    title=generated["title"],
                    content=generated["content"],
                    excerpt=generated["excerpt"],
                    status="draft"
                )
                
                post = self.create_post(post_data)
                
                return {
                    "post_id": post.id,
                    "title": post.title,
                    "link": post.link,
                    "status": post.status,
                    "content": generated["content"],
                    "excerpt": generated["excerpt"]
                }
            else:
                # Return generated content without saving
                return generated
        
        except Exception as e:
            logger.error(f"Error generating post: {str(e)}")
            raise
    
    def improve_post(
        self,
        post_id: int,
        improvements: List[str],
        save_changes: bool = False
    ) -> Dict[str, Any]:
        """Improve existing post content."""
        try:
            # Get current post
            post = self.get_post(post_id)
            
            # Improve content
            improved_content = self.content_generator.improve_content(
                content=post.content,
                improvements=improvements,
                language="da"  # Could be detected or passed as parameter
            )
            
            if save_changes:
                # Update post with improved content
                post_data = PostUpdate(content=improved_content)
                updated_post = self.update_post(post_id, post_data)
                
                return {
                    "post_id": updated_post.id,
                    "title": updated_post.title,
                    "improved_content": improved_content,
                    "saved": True
                }
            else:
                # Return improved content without saving
                return {
                    "post_id": post_id,
                    "title": post.title,
                    "original_content": post.content,
                    "improved_content": improved_content,
                    "saved": False
                }
        
        except Exception as e:
            logger.error(f"Error improving post {post_id}: {str(e)}")
            raise
    
    def optimize_post_seo(
        self,
        post_id: int,
        target_keywords: Optional[List[str]] = None,
        save_changes: bool = False
    ) -> Dict[str, Any]:
        """Optimize post for SEO."""
        try:
            # Get current post
            post = self.get_post(post_id)
            
            # Get SEO optimization suggestions
            seo_data = self.content_generator.optimize_for_seo(
                title=post.title,
                content=post.content,
                target_keywords=target_keywords,
                language="da"
            )
            
            if save_changes:
                # Update post with optimized title
                post_data = PostUpdate(title=seo_data["title"])
                updated_post = self.update_post(post_id, post_data)
                
                return {
                    "post_id": updated_post.id,
                    "optimized_title": seo_data["title"],
                    "meta_description": seo_data["meta_description"],
                    "content_suggestions": seo_data.get("content_suggestions", []),
                    "saved": True
                }
            else:
                return {
                    "post_id": post_id,
                    "current_title": post.title,
                    "optimized_title": seo_data["title"],
                    "meta_description": seo_data["meta_description"],
                    "content_suggestions": seo_data.get("content_suggestions", []),
                    "saved": False
                }
        
        except Exception as e:
            logger.error(f"Error optimizing post {post_id} for SEO: {str(e)}")
            raise

