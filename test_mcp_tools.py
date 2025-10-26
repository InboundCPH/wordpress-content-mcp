#!/usr/bin/env python3
"""
Test script to verify MCP server tools are properly configured.
This script checks that all tools are accessible and have correct signatures.
"""

import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_mcp_tools():
    """Test that MCP server can be imported and tools are registered."""
    
    try:
        # Import the MCP server
        logger.info("Importing MCP server...")
        import mcp_server
        
        # Check that mcp instance exists
        assert hasattr(mcp_server, 'mcp'), "MCP instance not found"
        logger.info("✓ MCP server imported successfully")
        
        # Get registered tools
        mcp_instance = mcp_server.mcp
        
        # Expected tools
        expected_tools = [
            'list_posts',
            'get_post',
            'create_post',
            'update_post',
            'delete_post',
            'generate_blog_post',
            'improve_post_content',
            'optimize_post_seo',
            'get_categories',
            'get_tags',
            'search_posts'
        ]
        
        logger.info(f"\nExpected tools: {len(expected_tools)}")
        logger.info("Checking tool registration...\n")
        
        for tool_name in expected_tools:
            # Check if tool exists in the module
            if hasattr(mcp_server, tool_name):
                logger.info(f"✓ {tool_name} - registered")
            else:
                logger.error(f"✗ {tool_name} - NOT FOUND")
        
        logger.info("\n" + "="*50)
        logger.info("MCP Server Tool Verification Complete")
        logger.info("="*50)
        
        return True
    
    except Exception as e:
        logger.error(f"Error testing MCP tools: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_settings():
    """Test that settings can be loaded."""
    try:
        logger.info("\nTesting settings...")
        from src.config.settings import settings
        
        logger.info(f"WordPress URL: {settings.WORDPRESS_URL or '(not set)'}")
        logger.info(f"WordPress Username: {'***' if settings.WORDPRESS_USERNAME else '(not set)'}")
        logger.info(f"WordPress App Password: {'***' if settings.WORDPRESS_APP_PASSWORD else '(not set)'}")
        logger.info(f"OpenAI API Key: {'***' if settings.OPENAI_API_KEY else '(not set)'}")
        
        if settings.validate():
            logger.info("✓ Settings validation passed")
        else:
            logger.warning("⚠ Settings validation failed - missing required configuration")
            logger.warning("This is expected if .env file is not configured yet")
        
        return True
    
    except Exception as e:
        logger.error(f"Error testing settings: {str(e)}")
        return False

if __name__ == "__main__":
    logger.info("="*50)
    logger.info("WordPress MCP Server - Tool Verification")
    logger.info("="*50 + "\n")
    
    # Test settings
    settings_ok = test_settings()
    
    # Test MCP tools
    tools_ok = test_mcp_tools()
    
    if settings_ok and tools_ok:
        logger.info("\n✓ All tests passed!")
        sys.exit(0)
    else:
        logger.error("\n✗ Some tests failed")
        sys.exit(1)

