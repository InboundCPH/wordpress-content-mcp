"""Data models for WordPress posts."""

from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class PostCreate(BaseModel):
    """Model for creating a new post."""
    title: str = Field(..., description="Post title")
    content: str = Field(..., description="Post content (HTML)")
    status: str = Field(default="draft", description="Post status (draft, publish, etc.)")
    excerpt: Optional[str] = Field(None, description="Post excerpt")
    categories: Optional[List[int]] = Field(None, description="Category IDs")
    tags: Optional[List[int]] = Field(None, description="Tag IDs")
    acf_fields: Optional[Dict[str, Any]] = Field(None, description="ACF custom fields")
    featured_media: Optional[int] = Field(None, description="Featured image media ID")


class PostUpdate(BaseModel):
    """Model for updating an existing post."""
    title: Optional[str] = Field(None, description="Post title")
    content: Optional[str] = Field(None, description="Post content (HTML)")
    status: Optional[str] = Field(None, description="Post status")
    excerpt: Optional[str] = Field(None, description="Post excerpt")
    categories: Optional[List[int]] = Field(None, description="Category IDs")
    tags: Optional[List[int]] = Field(None, description="Tag IDs")
    acf_fields: Optional[Dict[str, Any]] = Field(None, description="ACF custom fields")
    featured_media: Optional[int] = Field(None, description="Featured image media ID")


class Post(BaseModel):
    """Model for a WordPress post."""
    id: int
    title: str
    content: str
    excerpt: str
    status: str
    slug: str
    date: datetime
    modified: datetime
    author: int
    categories: List[int]
    tags: List[int]
    featured_media: Optional[int] = None
    link: str
    acf: Optional[Dict[str, Any]] = None
    
    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> "Post":
        """Create Post instance from WordPress API response."""
        return cls(
            id=data["id"],
            title=data["title"]["rendered"] if isinstance(data["title"], dict) else data["title"],
            content=data["content"]["rendered"] if isinstance(data["content"], dict) else data["content"],
            excerpt=data["excerpt"]["rendered"] if isinstance(data["excerpt"], dict) else data.get("excerpt", ""),
            status=data["status"],
            slug=data["slug"],
            date=datetime.fromisoformat(data["date"].replace("Z", "+00:00")),
            modified=datetime.fromisoformat(data["modified"].replace("Z", "+00:00")),
            author=data["author"],
            categories=data.get("categories", []),
            tags=data.get("tags", []),
            featured_media=data.get("featured_media"),
            link=data["link"],
            acf=data.get("acf")
        )


class ContentGenerationRequest(BaseModel):
    """Model for AI content generation request."""
    topic: str = Field(..., description="Topic or subject for the post")
    keywords: Optional[List[str]] = Field(None, description="SEO keywords to include")
    tone: str = Field(default="professional", description="Tone of voice (professional, casual, friendly, etc.)")
    length: str = Field(default="medium", description="Content length (short, medium, long)")
    language: str = Field(default="da", description="Content language (da, en, sv, etc.)")
    save_as_draft: bool = Field(default=True, description="Save generated content as draft post")


class ContentImprovementRequest(BaseModel):
    """Model for content improvement request."""
    post_id: int = Field(..., description="Post ID to improve")
    improvements: Optional[List[str]] = Field(
        default=["seo", "readability", "structure"],
        description="Types of improvements (seo, readability, structure, grammar)"
    )
    save_changes: bool = Field(default=False, description="Save changes directly to post")

