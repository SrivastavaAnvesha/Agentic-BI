"""AI Agent module using Google Gemini."""

import logging
import time
import json
from typing import List, Dict, Any, Optional, Tuple
from google import genai
from agentic_bi.config import settings
from agentic_bi.core.database import get_db
from agentic_bi.core.nlq_processor import NLQProcessor

logger = logging.getLogger(__name__)


class AIAgent:
    """AI Agent for natural language to SQL conversion and data analysis."""

    def __init__(self) -> None:
        """Initialize AI Agent with Gemini client."""
        try:
            self.client = genai.Client(api_key=settings.GOOGLE_API_KEY)
            self.model_id = settings.GEMINI_MODEL
            self.temperature = settings.GEMINI_TEMPERATURE
            self.db = get_db()
            self.nlq_processor = NLQProcessor()
            self.query_cache: Dict[str, Any] = {}
            logger.info(f"✅ AI Agent initialized with model: {self.model_id}")
        except Exception as e:
            logger.error(f"❌ AI Agent initialization failed: {e}")
            raise

    def _build_context(self) -> str:
        """
        Build comprehensive database context for the AI model.

        Returns:
            Context string with database information
        """
        tables = self.db.get_all_tables()
        context = "You are a SQL expert assistant for business intelligence.\n\n"
        context += "DATABASE SCHEMA:\n"
        context += "=" * 50 + "\n\n"

        for table in tables:
            schema = self.db.get_table_schema(table)
            row_count = self.db.get_table_row_count(table)

            context += f"Table: {table}\n"
            context += f"Rows: {row_count}\n"
            context += "Columns:\n"

            for col_name, col_type in schema.items():
                context += f"  - {col_name} ({col_type})\n"

            # Add sample data
            sample = self.db.get_table_sample(table, limit=2)
            if sample:
                context += "Sample Data:\n"
                for i, row in enumerate(sample[:2], 1):
                    context += f"  Row {i}: {row}\n"

            context += "\n"

        context += "=" * 50 + "\n\n"
        context += "INSTRUCTIONS:\n"
        context += "1. Generate ONLY valid PostgreSQL queries\n"
        context += "2. Do NOT include markdown formatting or backticks\n"
        context += "3. Return the raw SQL query only\n"
        context += "4. If you need multiple queries, return them separated by semicolons\n"
        context += "5. Use column names exactly as shown above\n"
        context += "6. For aggregations, always include GROUP BY when needed\n"
        context += "7. Add LIMIT 100 to prevent large result sets\n\n"

        return context

    def generate_sql(self, user_query: str, max_attempts: int = 3) -> Tuple[str, bool, str]:
        """
        Generate SQL query from natural language using AI with retry logic.

        Args:
            user_query: Natural language query from user
            max_attempts: Maximum retry attempts on quota errors

        Returns:
            Tuple of (SQL query, success bool, error message if any)
        """
        # Check cache
        cache_key = user_query.lower().strip()
        if cache_key in self.query_cache and settings.CACHE_ENABLED:
            logger.info(f"📦 Cache hit for query: {user_query}")
            return self.query_cache[cache_key]["sql"], True, ""

        context = self._build_context()
        full_prompt = f"{context}\nUser Question: {user_query}\n\nGenerate the SQL query:"

        for attempt in range(max_attempts):
            try:
                logger.info(f"🧠 Generating SQL (attempt {attempt + 1}/{max_attempts})...")

                response = self.client.models.generate_content(
                    model=self.model_id,
                    contents=full_prompt,
                    config={
                        "temperature": self.temperature,
                        "top_p": 0.95,
                        "top_k": 40,
                        "max_output_tokens": 500,
                    },
                )

                sql_query = response.text.strip()
                # Remove markdown formatting if present
                sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

                # Validate safety
                if not self.nlq_processor.validate_query_safety(sql_query):
                    return "", False, "Generated query failed safety validation"

                logger.info(f"✅ SQL generated successfully: {sql_query[:100]}...")

                # Cache the result
                if settings.CACHE_ENABLED:
                    self.query_cache[cache_key] = {
                        "sql": sql_query,
                        "timestamp": time.time(),
                    }

                return sql_query, True, ""

            except Exception as e:
                error_msg = str(e)
                if "429" in error_msg:  # Quota exceeded
                    if attempt < max_attempts - 1:
                        wait_time = 10 * (attempt + 1)
                        logger.warning(
                            f"⚠️ API quota exceeded. Retrying in {wait_time}s..."
                        )
                        time.sleep(wait_time)
                        continue
                    else:
                        return "", False, "API quota limit exceeded after retries"
                else:
                    logger.error(f"❌ SQL generation error: {error_msg}")
                    return "", False, error_msg

        return "", False, "Failed to generate SQL after maximum attempts"

    def execute_query(
        self, user_query: str, include_reasoning: bool = False
    ) -> Dict[str, Any]:
        """
        Execute full pipeline: NLQ -> SQL -> Database Query.

        Args:
            user_query: Natural language query from user
            include_reasoning: Include AI reasoning in response

        Returns:
            Dictionary with results, metadata, and optional reasoning
        """
        result = {
            "success": False,
            "query": user_query,
            "sql": "",
            "data": [],
            "error": "",
            "reasoning": None,
            "metrics": {
                "execution_time": 0,
                "row_count": 0,
            },
        }

        start_time = time.time()

        try:
            # Generate SQL
            sql_query, success, error = self.generate_sql(user_query)

            if not success:
                result["error"] = error
                result["success"] = False
                return result

            result["sql"] = sql_query

            # Execute query
            logger.info(f"📊 Executing query: {sql_query}")
            data = self.db.execute_query_dict(sql_query)

            result["data"] = data
            result["success"] = True
            result["metrics"]["row_count"] = len(data)
            result["metrics"]["execution_time"] = time.time() - start_time

            logger.info(
                f"✅ Query executed successfully. Returned {len(data)} rows in "
                f"{result['metrics']['execution_time']:.2f}s"
            )

        except Exception as e:
            logger.error(f"❌ Query execution failed: {e}")
            result["error"] = str(e)
            result["success"] = False

        result["metrics"]["execution_time"] = time.time() - start_time
        return result

    def analyze_data(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze data results and provide insights.

        Args:
            data: Query result data

        Returns:
            Dictionary with analysis insights
        """
        if not data:
            return {"summary": "No data to analyze", "insights": []}

        analysis = {
            "summary": f"Analyzed {len(data)} records",
            "insights": [],
            "statistics": {},
        }

        # Extract numeric columns and calculate stats
        numeric_values: Dict[str, List[float]] = {}

        for row in data:
            for key, value in row.items():
                if isinstance(value, (int, float)):
                    if key not in numeric_values:
                        numeric_values[key] = []
                    numeric_values[key].append(float(value))

        # Calculate statistics
        for col_name, values in numeric_values.items():
            if values:
                analysis["statistics"][col_name] = {
                    "sum": sum(values),
                    "avg": sum(values) / len(values),
                    "min": min(values),
                    "max": max(values),
                    "count": len(values),
                }

                # Generate insights
                if len(values) > 1:
                    trend = "increasing" if values[-1] > values[0] else "decreasing"
                    analysis["insights"].append(
                        f"{col_name} shows a {trend} trend"
                    )

        return analysis

    def suggest_follow_up_queries(self, data: List[Dict[str, Any]]) -> List[str]:
        """
        Suggest follow-up queries based on current data.

        Args:
            data: Query result data

        Returns:
            List of suggested follow-up questions
        """
        suggestions = []

        if not data:
            return suggestions

        # Analyze data structure
        first_row = data[0]
        columns = list(first_row.keys())

        # Generate suggestions
        suggestions.append(f"Show me the top 10 records by {columns[0]}")

        # Check for numeric columns
        for col in columns:
            if isinstance(first_row[col], (int, float)):
                suggestions.append(f"What is the average {col}?")
                suggestions.append(f"What is the maximum {col}?")
                break

        return suggestions[:3]  # Return top 3 suggestions
