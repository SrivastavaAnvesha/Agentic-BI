"""Natural Language Query Processing module."""

import logging
import re
from typing import List, Dict, Any, Optional
from agentic_bi.core.database import get_db

logger = logging.getLogger(__name__)


class NLQProcessor:
    """Process and validate natural language queries."""

    # Common Hinglish/Hindi terms mapping to SQL
    HINDI_KEYWORDS = {
        "कुल": "SUM",
        "total": "SUM",
        "sum": "SUM",
        "गिनती": "COUNT",
        "count": "COUNT",
        "औसत": "AVG",
        "average": "AVG",
        "avg": "AVG",
        "अधिकतम": "MAX",
        "maximum": "MAX",
        "max": "MAX",
        "न्यूनतम": "MIN",
        "minimum": "MIN",
        "min": "MIN",
    }

    def __init__(self) -> None:
        """Initialize NLQ processor."""
        self.db = get_db()
        self.tables = self.db.get_all_tables()
        self.table_schemas = {
            table: self.db.get_table_schema(table) for table in self.tables
        }

    def extract_intent(self, query: str) -> str:
        """
        Extract query intent (SELECT, AGGREGATE, JOIN, etc).

        Args:
            query: User's natural language query

        Returns:
            Query intent type
        """
        query_lower = query.lower()

        if any(word in query_lower for word in ["how many", "गिनती", "count"]):
            return "COUNT"
        elif any(word in query_lower for word in ["total", "sum", "कुल"]):
            return "SUM"
        elif any(word in query_lower for word in ["average", "avg", "औसत"]):
            return "AVG"
        elif any(word in query_lower for word in ["top", "highest", "maximum", "max"]):
            return "MAX"
        elif any(word in query_lower for word in ["lowest", "minimum", "min"]):
            return "MIN"
        elif any(word in query_lower for word in ["by", "group", "category", "region"]):
            return "GROUP_BY"
        elif any(word in query_lower for word in ["trend", "over time", "timeline"]):
            return "TIME_SERIES"
        else:
            return "SELECT"

    def sanitize_input(self, query: str) -> str:
        """
        Sanitize user input to prevent SQL injection.

        Args:
            query: Raw user query

        Returns:
            Sanitized query
        """
        # Remove potential SQL injection patterns
        dangerous_patterns = [
            r";\s*(DROP|DELETE|INSERT|UPDATE|ALTER|TRUNCATE)",
            r"(DROP|DELETE|INSERT|UPDATE|ALTER|TRUNCATE)\s+TABLE",
            r"--\s*",
            r"/\*.*?\*/",
        ]

        sanitized = query
        for pattern in dangerous_patterns:
            sanitized = re.sub(pattern, "", sanitized, flags=re.IGNORECASE)

        return sanitized.strip()

    def get_column_suggestions(
        self, table_name: str, search_term: Optional[str] = None
    ) -> List[str]:
        """
        Get column suggestions for a table.

        Args:
            table_name: Name of the table
            search_term: Optional search term to filter columns

        Returns:
            List of matching column names
        """
        if table_name not in self.table_schemas:
            return []

        columns = list(self.table_schemas[table_name].keys())

        if search_term:
            search_term_lower = search_term.lower()
            columns = [
                col for col in columns if search_term_lower in col.lower()
            ]

        return columns

    def validate_query_safety(self, sql_query: str) -> bool:
        """
        Validate SQL query for safety.

        Args:
            sql_query: Generated SQL query

        Returns:
            True if query is safe, False otherwise
        """
        dangerous_keywords = ["DROP", "DELETE", "TRUNCATE", "ALTER", "CREATE"]
        sql_upper = sql_query.upper()

        for keyword in dangerous_keywords:
            if re.search(rf"\b{keyword}\b", sql_upper):
                logger.warning(f"Dangerous keyword detected: {keyword}")
                return False

        return True

    def suggest_queries(self, table_name: str) -> List[Dict[str, str]]:
        """
        Generate suggested queries based on table structure.

        Args:
            table_name: Name of the table

        Returns:
            List of suggested query templates
        """
        if table_name not in self.table_schemas:
            return []

        schema = self.table_schemas[table_name]
        numeric_cols = [col for col, dtype in schema.items() if "numeric" in dtype or "int" in dtype]
        string_cols = [col for col, dtype in schema.items() if "varchar" in dtype or "text" in dtype]

        suggestions = [
            {"title": f"Total Records", "query": f"How many records in {table_name}?"},
        ]

        if numeric_cols:
            col = numeric_cols[0]
            suggestions.append({
                "title": f"Total {col.replace('_', ' ').title()}",
                "query": f"What is the sum of {col}?",
            })
            suggestions.append({
                "title": f"Average {col.replace('_', ' ').title()}",
                "query": f"What is the average {col}?",
            })

        if string_cols:
            col = string_cols[0]
            suggestions.append({
                "title": f"Group by {col.replace('_', ' ').title()}",
                "query": f"Show me the breakdown by {col}",
            })

        return suggestions

    def extract_entities(self, query: str) -> Dict[str, Any]:
        """
        Extract entities from natural language query.

        Args:
            query: User's natural language query

        Returns:
            Dictionary of extracted entities
        """
        entities = {
            "intent": self.extract_intent(query),
            "tables": [],
            "columns": [],
            "conditions": [],
            "raw_query": query,
        }

        # Find potential table names
        for table in self.tables:
            if table.lower() in query.lower():
                entities["tables"].append(table)

        # Find potential columns
        for table in entities["tables"]:
            for column in self.get_column_suggestions(table):
                if column.lower() in query.lower():
                    entities["columns"].append(column)

        return entities
