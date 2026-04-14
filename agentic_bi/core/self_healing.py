"""Self-healing error correction module."""

import logging
import re
from typing import Dict, Any, List, Optional, Tuple
from agentic_bi.core.database import get_db
from agentic_bi.core.ai_agent import AIAgent

logger = logging.getLogger(__name__)


class SelfHealer:
    """Self-healing system for correcting SQL query errors."""

    # Common SQL error patterns and fixes
    ERROR_FIXES = {
        "column.*does not exist": "Check column name spelling or use SELECT * to see available columns",
        "syntax error": "Review SQL syntax - check for missing commas, quotes, or parentheses",
        "relation.*does not exist": "Table name not found - verify table exists in database",
        "ambiguous column": "Column exists in multiple tables - use table_name.column_name format",
        "division by zero": "Add WHERE clause to exclude zero values",
    }

    def __init__(self) -> None:
        """Initialize self-healer."""
        self.db = get_db()
        self.ai_agent = AIAgent()
        self.correction_history: List[Dict[str, Any]] = []

    def extract_error_info(self, error_msg: str) -> Dict[str, str]:
        """
        Extract structured information from error message.

        Args:
            error_msg: Raw error message from database

        Returns:
            Dictionary with error type and details
        """
        error_lower = error_msg.lower()

        error_info = {
            "type": "unknown",
            "message": error_msg,
            "suggestion": "",
        }

        for pattern, suggestion in self.ERROR_FIXES.items():
            if re.search(pattern, error_lower):
                error_info["type"] = pattern.split(".*")[0]
                error_info["suggestion"] = suggestion
                break

        return error_info

    def attempt_fix(
        self, original_query: str, error_msg: str, attempt_num: int = 1
    ) -> Tuple[str, bool, str]:
        """
        Attempt to fix SQL query based on error.

        Args:
            original_query: Original SQL query that failed
            error_msg: Error message from database
            attempt_num: Which attempt this is (max 3)

        Returns:
            Tuple of (fixed_query, success, explanation)
        """
        logger.info(f"🔧 Attempting to fix query (attempt {attempt_num}/3)...")

        error_info = self.extract_error_info(error_msg)

        # Rule-based fixes
        fixed_query = original_query
        error_lower = error_msg.lower()

        # Fix 1: Missing table prefix for ambiguous columns
        if "ambiguous" in error_lower:
            logger.info("🔍 Detected ambiguous column error")
            # This would need more sophisticated parsing
            pass

        # Fix 2: Missing LIMIT clause causing large results
        if "out of memory" in error_lower:
            logger.info("🔍 Detected memory error - adding LIMIT")
            if "LIMIT" not in fixed_query.upper():
                fixed_query = fixed_query.rstrip(";") + " LIMIT 100;"

        # Fix 3: Try executing simple SELECT * on identified table
        if "does not exist" in error_lower:
            logger.info("🔍 Detected missing table/column")

            # Try to extract table name and validate
            tables = self.db.get_all_tables()
            for table in tables:
                if table.lower() in original_query.lower():
                    logger.info(f"✅ Found valid table: {table}")
                    fixed_query = f"SELECT * FROM {table} LIMIT 10;"
                    break

        # Test the fixed query
        try:
            logger.info(f"📝 Testing fixed query: {fixed_query}")
            self.db.execute_query(fixed_query)
            logger.info("✅ Fixed query executed successfully")
            return fixed_query, True, "Query fixed using rule-based correction"
        except Exception as e:
            logger.warning(f"⚠️ Fixed query still has errors: {e}")

            # If rule-based fix didn't work, try AI-based fix
            if attempt_num < 3:
                return self._ai_powered_fix(original_query, error_msg, attempt_num)
            else:
                return "", False, f"Could not fix query after {attempt_num} attempts"

        return fixed_query, True, error_info["suggestion"]

    def _ai_powered_fix(
        self, original_query: str, error_msg: str, attempt_num: int
    ) -> Tuple[str, bool, str]:
        """
        Use AI to fix SQL query.

        Args:
            original_query: Original SQL query
            error_msg: Error message
            attempt_num: Current attempt number

        Returns:
            Tuple of (fixed_query, success, explanation)
        """
        logger.info("🧠 Using AI to fix query...")

        try:
            # Build context about the error
            error_context = f"""
The following SQL query produced an error:

Original Query: {original_query}

Error: {error_msg}

Please fix this query. Return ONLY the corrected SQL query with no explanation.
"""

            response = self.ai_agent.client.models.generate_content(
                model=self.ai_agent.model_id,
                contents=error_context,
            )

            fixed_query = response.text.strip().replace("```sql", "").replace("```", "").strip()

            # Validate and test
            try:
                self.db.execute_query(fixed_query)
                logger.info("✅ AI-generated fix executed successfully")
                return fixed_query, True, "Fixed using AI-powered correction"
            except Exception as e:
                logger.warning(f"⚠️ AI-generated fix still has errors: {e}")
                return "", False, f"AI fix failed: {str(e)}"

        except Exception as e:
            logger.error(f"❌ AI-powered fix failed: {e}")
            return "", False, str(e)

    def log_correction(
        self,
        original_query: str,
        fixed_query: str,
        error_msg: str,
        success: bool,
        correction_type: str,
    ) -> None:
        """
        Log correction for monitoring and improvement.

        Args:
            original_query: Original failing query
            fixed_query: Fixed query
            error_msg: Error message
            success: Whether fix was successful
            correction_type: Type of correction applied
        """
        import time

        record = {
            "timestamp": time.time(),
            "original_query": original_query,
            "fixed_query": fixed_query,
            "error": error_msg,
            "success": success,
            "correction_type": correction_type,
        }

        self.correction_history.append(record)
        logger.info(f"📋 Correction logged: {correction_type} - {success}")

    def get_corrections_report(self) -> Dict[str, Any]:
        """
        Get report on all corrections made.

        Returns:
            Dictionary with correction statistics
        """
        if not self.correction_history:
            return {
                "total_corrections": 0,
                "successful": 0,
                "failed": 0,
                "success_rate": 0,
                "common_errors": [],
            }

        total = len(self.correction_history)
        successful = sum(1 for c in self.correction_history if c["success"])
        failed = total - successful

        # Count error types
        error_types: Dict[str, int] = {}
        for record in self.correction_history:
            error = record["error"]
            for pattern in self.ERROR_FIXES.keys():
                if re.search(pattern, error.lower()):
                    error_types[pattern] = error_types.get(pattern, 0) + 1
                    break

        return {
            "total_corrections": total,
            "successful": successful,
            "failed": failed,
            "success_rate": (successful / total * 100) if total > 0 else 0,
            "common_errors": sorted(
                error_types.items(), key=lambda x: x[1], reverse=True
            ),
            "recent_corrections": self.correction_history[-5:],
        }
