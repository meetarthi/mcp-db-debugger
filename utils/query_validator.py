import re
from typing import Set

class QueryValidator:
    """
    CRITICAL: This prevents dangerous SQL from being executed
    """
    
    def __init__(self):
        # Only these commands are allowed
        self.allowed_commands = {'SELECT', 'SHOW', 'DESCRIBE', 'EXPLAIN', 'PRAGMA'}
        
        # These are NEVER allowed
        self.dangerous_keywords = {
            'DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER', 'TRUNCATE', 'CREATE'
        }
    
    def is_safe_query(self, query: str) -> bool:
        """Check if query is safe to execute"""
        if not query:
            return False
            
        query_upper = query.strip().upper()
        first_word = query_upper.split()[0] if query_upper.split() else ''
        
        # Must start with allowed command
        if first_word not in self.allowed_commands:
            return False
            
        # Must not contain dangerous keywords
        for keyword in self.dangerous_keywords:
            if keyword in query_upper:
                return False
                
        return True