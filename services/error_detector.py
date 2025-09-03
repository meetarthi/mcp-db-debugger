import logging
from typing import Dict, Any
from services.openai_service import OpenAIService
from services.mcp_service import MCPService

logger = logging.getLogger(__name__)

class ErrorDetector:
    """
    This is the MAIN ENGINE that combines everything
    """
    
    def __init__(self):
        self.openai_service = OpenAIService()
        self.mcp_service = MCPService()
    
    async def diagnose_error(self, user_input: str, db_type: str = "postgresql") -> Dict[str, Any]:
        """
        MAIN PIPELINE:
        1. Send to OpenAI for analysis
        2. Execute diagnostic queries via MCP
        3. Combine results
        4. Return recommendations
        """
        try:
            # Step 1: Get AI analysis
            logger.info("🤖 Getting OpenAI analysis...")
            ai_analysis = self.openai_service.analyze_database_error(user_input, db_type)
            
            # Step 2: Execute diagnostic queries
            logger.info("🔍 Executing diagnostic queries...")
            query_results = await self.mcp_service.execute_diagnostic_queries(
                ai_analysis.get('diagnostic_queries', [])
            )
            
            # Step 3: Check database health
            health_check = await self._check_database_health()
            
            # Step 4: Combine everything
            final_result = {
                "success": True,
                "user_input": user_input,
                "ai_analysis": ai_analysis,
                "database_investigation": {
                    "queries_executed": len(query_results),
                    "successful_queries": sum(1 for r in query_results if r.get('success')),
                    "failed_queries": sum(1 for r in query_results if not r.get('success')),
                    "query_results": query_results,
                    "health_check": health_check
                },
                "recommendations": ai_analysis.get('recommended_fixes', []),
                "prevention_tips": ai_analysis.get('prevention_tips', [])
            }
            
            return final_result
            
        except Exception as e:
            logger.error(f"Error in diagnosis: {e}")
            return {
                "success": False,
                "error": str(e),
                "recommendations": ["Please check your setup and try again"]
            }
    
    async def _check_database_health(self) -> Dict[str, Any]:
        """Simple database health check"""
        health_query = "SELECT 1 as health_check"
        result = await self.mcp_service.execute_single_query(health_query)
        
        return {
            "connection_healthy": result.get('success', False)
        }