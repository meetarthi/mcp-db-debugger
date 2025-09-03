import openai
import json
import logging
from typing import Dict, List, Any
from config.settings import Config

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self):
        self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)

    def analyze_database_error(self, user_input: str, db_type: str = "postgresql") -> Dict[str, Any]:
        """
        This is the CORE function that sends your error to OpenAI
        """
        prompt = f"""
        You are a database debugging expert. Analyze this error:

        Database Type: {db_type}
        User Error: {user_input}

        Respond in JSON format:
        {{
            "error_category": "connection|query|performance|permissions|other",
            "severity": "low|medium|high|critical",
            "analysis": "Detailed explanation of what's wrong",
            "diagnostic_queries": [
                "SELECT query to investigate the issue",
                "SHOW command to check system status"
            ],
            "potential_causes": ["cause1", "cause2"],
            "recommended_fixes": ["fix1", "fix2"]
        }}
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a database expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            # Return fallback response
            return {
                "error_category": "other",
                "severity": "medium", 
                "analysis": f"Could not analyze: {user_input}",
                "diagnostic_queries": ["SELECT 1 as health_check"],
                "potential_causes": ["Analysis unavailable"],
                "recommended_fixes": ["Manual investigation needed"]
            }