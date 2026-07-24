"""
Rate limiting to prevent spam and abuse.
"""

import logging
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)

class RateLimiter:
    """
    Simple in-memory rate limiter for contact form submissions.
    Tracks requests by IP address and enforces limits.
    """
    
    def __init__(self, max_requests: int = 5, window_seconds: int = 3600):
        """
        Initialize rate limiter.
        
        Args:
            max_requests: Maximum requests allowed per window
            window_seconds: Time window in seconds (default: 1 hour)
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, List[datetime]] = defaultdict(list)
    
    def is_allowed(self, identifier: str) -> bool:
        """
        Check if a request from the given identifier is allowed.
        
        Args:
            identifier: IP address or other unique identifier
        
        Returns:
            True if request is allowed, False if rate limit exceeded
        """
        now = datetime.utcnow()
        window_start = now - timedelta(seconds=self.window_seconds)
        
        # Clean old requests outside the window
        if identifier in self.requests:
            self.requests[identifier] = [
                req_time for req_time in self.requests[identifier]
                if req_time > window_start
            ]
        
        # Check if limit exceeded
        if len(self.requests[identifier]) >= self.max_requests:
            logger.warning(
                f"Rate limit exceeded for {identifier}: "
                f"{len(self.requests[identifier])} requests in {self.window_seconds}s"
            )
            return False
        
        # Record this request
        self.requests[identifier].append(now)
        return True
    
    def get_remaining(self, identifier: str) -> int:
        """
        Get remaining requests for an identifier.
        
        Args:
            identifier: IP address or other unique identifier
        
        Returns:
            Number of remaining requests in current window
        """
        now = datetime.utcnow()
        window_start = now - timedelta(seconds=self.window_seconds)
        
        if identifier not in self.requests:
            return self.max_requests
        
        # Count valid requests in window
        valid_requests = [
            req_time for req_time in self.requests[identifier]
            if req_time > window_start
        ]
        
        return max(0, self.max_requests - len(valid_requests))
    
    def reset(self, identifier: str = None):
        """
        Reset rate limit for an identifier or all identifiers.
        
        Args:
            identifier: IP address or identifier. If None, resets all.
        """
        if identifier:
            if identifier in self.requests:
                del self.requests[identifier]
                logger.info(f"Rate limit reset for {identifier}")
        else:
            self.requests.clear()
            logger.info("Rate limit reset for all identifiers")
