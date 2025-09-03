import logging
from typing import Dict, List, Any
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from config.settings import Config
from utils.query_validator import QueryValidator

logger = logging.getLogger(__name__)

class MCPService:
    """
    This handles SAFE database interactions
    """
    
    def __init__(self):
        self.engine = create_engine(Config.DATABASE_URL)
        self.query_validator = QueryValidator()
    
    async def execute_diagnostic_queries(self, queries: List[str]) -> List[Dict[str, Any]]:
        """
        Execute multiple diagnostic queries safely
        """
        results = []
        for query in queries:
            result = await self.execute_single_query(query)
            results.append(result)
        return results
    
    async def execute_single_query(self, query: str) -> Dict[str, Any]:
        """
        Execute ONE query with safety checks
        """
        # SAFETY CHECK: Validate query first
        if not self.query_validator.is_safe_query(query):
            return {
                "query": query,
                "success": False,
                "error": "Unsafe query - only SELECT/SHOW/DESCRIBE allowed",
                "data": None
            }
        
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text(query))
                
                if result.returns_rows:
                    rows = result.fetchmany(Config.MAX_QUERY_RESULTS)
                    columns = result.keys()
                    data = [dict(zip(columns, row)) for row in rows]
                else:
                    data = {"message": "Query executed successfully"}
                
                return {
                    "query": query,
                    "success": True,
                    "error": None,
                    "data": data
                }
                
        except SQLAlchemyError as e:
            return {
                "query": query,
                "success": False,
                "error": str(e),
                "data": None
            }