"""WordPress REST API client."""

import requests
import logging
from typing import Dict, List, Optional, Any
from requests.auth import HTTPBasicAuth
from ..config.settings import settings

logger = logging.getLogger(__name__)


class WordPressAPIError(Exception):
    """Custom exception for WordPress API errors."""
    pass


class WordPressClient:
    """Client for interacting with WordPress REST API."""
    
    def __init__(self):
        """Initialize WordPress API client."""
        self.base_url = settings.get_wordpress_api_url()
        self.auth = HTTPBasicAuth(
            settings.WORDPRESS_USERNAME,
            settings.WORDPRESS_APP_PASSWORD
        )
        self.timeout = settings.REQUEST_TIMEOUT
        self.session = requests.Session()
        self.session.auth = self.auth
        
        logger.info(f"WordPress client initialized for {settings.WORDPRESS_URL}")
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Make HTTP request to WordPress API."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.HTTPError as e:
            error_msg = f"WordPress API error: {e.response.status_code}"
            try:
                error_data = e.response.json()
                error_msg += f" - {error_data.get('message', '')}"
            except:
                pass
            logger.error(error_msg)
            raise WordPressAPIError(error_msg)
        
        except requests.exceptions.RequestException as e:
            error_msg = f"Request failed: {str(e)}"
            logger.error(error_msg)
            raise WordPressAPIError(error_msg)
    
    # Posts endpoints
    
    def get_posts(
        self,
        per_page: int = 10,
        page: int = 1,
        status: str = "publish",
        search: Optional[str] = None,
        categories: Optional[List[int]] = None
    ) -> List[Dict[str, Any]]:
        """Get list of posts."""
        params = {
            "per_page": per_page,
            "page": page,
            "status": status
        }
        
        if search:
            params["search"] = search
        
        if categories:
            params["categories"] = ",".join(map(str, categories))
        
        return self._make_request("GET", "posts", params=params)
    
    def get_post(self, post_id: int) -> Dict[str, Any]:
        """Get a specific post by ID."""
        return self._make_request("GET", f"posts/{post_id}")
    
    def create_post(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new post."""
        return self._make_request("POST", "posts", data=data)
    
    def update_post(self, post_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing post."""
        return self._make_request("POST", f"posts/{post_id}", data=data)
    
    def delete_post(self, post_id: int, force: bool = False) -> Dict[str, Any]:
        """Delete a post."""
        params = {"force": force}
        return self._make_request("DELETE", f"posts/{post_id}", params=params)
    
    # Categories and Tags
    
    def get_categories(self) -> List[Dict[str, Any]]:
        """Get all categories."""
        return self._make_request("GET", "categories", params={"per_page": 100})
    
    def get_tags(self) -> List[Dict[str, Any]]:
        """Get all tags."""
        return self._make_request("GET", "tags", params={"per_page": 100})
    
    # Media
    
    def upload_media(self, file_path: str, alt_text: Optional[str] = None) -> Dict[str, Any]:
        """Upload media file to WordPress."""
        url = f"{self.base_url}/media"
        
        with open(file_path, 'rb') as f:
            files = {'file': f}
            headers = {}
            if alt_text:
                headers['Content-Disposition'] = f'attachment; filename="{file_path}"'
            
            response = self.session.post(
                url,
                files=files,
                headers=headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
    
    def search_posts(
        self,
        query: str,
        search_columns: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """Search for posts."""
        params = {
            "search": query,
            "per_page": 20
        }
        
        if search_columns:
            params["search_columns"] = search_columns
        
        return self._make_request("GET", "posts", params=params)

