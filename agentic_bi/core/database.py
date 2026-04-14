"""Database management module."""

import logging
from typing import Any, Dict, List, Optional, Tuple
from contextlib import contextmanager
from sqlalchemy import create_engine, text, MetaData, inspect, Table
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from agentic_bi.config import settings

logger = logging.getLogger(__name__)


class Database:
    """PostgreSQL database connection manager."""

    def __init__(self) -> None:
        """Initialize database connection pool."""
        try:
            self.engine = create_engine(
                settings.database_url,
                poolclass=QueuePool,
                pool_size=5,
                max_overflow=10,
                pool_recycle=3600,
                echo=settings.DEBUG_MODE,
            )
            self.SessionLocal = sessionmaker(bind=self.engine)
            self.metadata = MetaData()
            logger.info("✅ Database connection pool initialized")
        except Exception as e:
            logger.error(f"❌ Database initialization failed: {e}")
            raise

    @contextmanager
    def get_session(self) -> Session:
        """Context manager for database sessions."""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Session error: {e}")
            raise
        finally:
            session.close()

    def execute_query(
        self, query: str, timeout: Optional[int] = None
    ) -> List[Tuple[Any, ...]]:
        """
        Execute raw SQL query.

        Args:
            query: SQL query string
            timeout: Query timeout in seconds

        Returns:
            List of result tuples

        Raises:
            Exception: If query execution fails
        """
        timeout = timeout or settings.QUERY_TIMEOUT
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(query))
                return result.fetchall()
        except Exception as e:
            logger.error(f"Query execution failed: {query} | Error: {e}")
            raise

    def execute_query_dict(
        self, query: str, timeout: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Execute query and return results as list of dicts.

        Args:
            query: SQL query string
            timeout: Query timeout in seconds

        Returns:
            List of result dictionaries
        """
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(query))
                columns = result.keys()
                return [dict(zip(columns, row)) for row in result.fetchall()]
        except Exception as e:
            logger.error(f"Query execution failed: {query} | Error: {e}")
            raise

    def get_table_schema(self, table_name: str) -> Dict[str, str]:
        """
        Get table schema with column names and types.

        Args:
            table_name: Name of the table

        Returns:
            Dictionary mapping column names to data types
        """
        try:
            inspector = inspect(self.engine)
            columns = inspector.get_columns(table_name)
            return {col["name"]: str(col["type"]) for col in columns}
        except Exception as e:
            logger.error(f"Failed to get schema for {table_name}: {e}")
            return {}

    def get_all_tables(self) -> List[str]:
        """
        Get list of all tables in database.

        Returns:
            List of table names
        """
        try:
            inspector = inspect(self.engine)
            return inspector.get_table_names()
        except Exception as e:
            logger.error(f"Failed to get table list: {e}")
            return []

    def get_table_row_count(self, table_name: str) -> int:
        """
        Get number of rows in a table.

        Args:
            table_name: Name of the table

        Returns:
            Row count
        """
        try:
            query = f"SELECT COUNT(*) FROM {table_name}"
            result = self.execute_query(query)
            return result[0][0] if result else 0
        except Exception as e:
            logger.error(f"Failed to get row count for {table_name}: {e}")
            return 0

    def get_table_sample(
        self, table_name: str, limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Get sample data from table.

        Args:
            table_name: Name of the table
            limit: Number of rows to retrieve

        Returns:
            List of sample rows as dictionaries
        """
        try:
            query = f"SELECT * FROM {table_name} LIMIT {limit}"
            return self.execute_query_dict(query)
        except Exception as e:
            logger.error(f"Failed to get sample from {table_name}: {e}")
            return []

    def test_connection(self) -> bool:
        """
        Test database connection.

        Returns:
            True if connection successful, False otherwise
        """
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info("✅ Database connection test passed")
            return True
        except Exception as e:
            logger.error(f"❌ Database connection test failed: {e}")
            return False

    def close(self) -> None:
        """Close database connection pool."""
        self.engine.dispose()
        logger.info("Database connection pool closed")


# Global database instance
_db_instance: Optional[Database] = None


def get_db() -> Database:
    """Get or create global database instance."""
    global _db_instance
    if _db_instance is None:
        _db_instance = Database()
    return _db_instance
