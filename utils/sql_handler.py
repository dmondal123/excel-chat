import sqlite3
import pandas as pd
from typing import Optional, Dict, Any
import streamlit as st

class SimpleSQLHandler:
    """Simple text-to-SQL handler for Excel data analysis"""
    
    def __init__(self):
        self.connection = None
        self.df = None
        self.table_name = "data"
    
    def load_data(self, df: pd.DataFrame):
        """Load DataFrame into SQLite for querying"""
        try:
            self.df = df
            # Create in-memory SQLite connection
            self.connection = sqlite3.connect(":memory:")
            
            # Load DataFrame into SQLite
            df.to_sql(self.table_name, self.connection, index=False, if_exists='replace')
            
            return True
        except Exception as e:
            st.error(f"Error loading data into SQL: {str(e)}")
            return False
    
    def is_analytical_query(self, query: str) -> bool:
        """Simple check if query needs SQL analysis"""
        analytical_keywords = [
            # Basic analytics
            'average', 'avg', 'sum', 'count', 'max', 'min', 'total',
            'group', 'filter', 'where', 'top', 'bottom', 'highest', 'lowest',
            'trend', 'compare', 'between', 'greater', 'less', 'most', 'least',
            # Accounting-specific terms
            'balance', 'outstanding', 'overdue', 'due', 'paid', 'unpaid',
            'vendor', 'account', 'document', 'amount', 'currency',
            'aging', 'reconcile', 'clearing', 'posting', 'by month', 'by date',
            'net due', 'terms', 'payment terms', 'invoice', 'credit', 'debit'
        ]
        
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in analytical_keywords)
    
    def get_table_schema(self) -> str:
        """Get simple table schema for SQL generation"""
        if self.df is None:
            return ""
        
        columns_info = []
        for col in self.df.columns:
            dtype = str(self.df[col].dtype)
            sample_vals = self.df[col].dropna().head(2).tolist()
            # Use square brackets to properly quote column names with spaces
            quoted_col = f"[{col}]" if ' ' in str(col) else str(col)
            columns_info.append(f"  {quoted_col} ({dtype}) - examples: {sample_vals}")
        
        schema = f"""
Table: {self.table_name}
Columns:
{chr(10).join(columns_info)}

Total rows: {len(self.df)}

IMPORTANT: Column names with spaces must be enclosed in square brackets like [Column Name].
"""
        return schema
    
    def generate_sql_prompt(self, user_query: str) -> str:
        """Create prompt for SQL generation"""
        schema = self.get_table_schema()
        
        prompt = f"""
Convert this natural language question to a simple SQL query.

{schema}

Question: {user_query}

Rules:
- Use table name: {self.table_name}
- Keep query simple and safe
- Use LIMIT 100 for large results
- Only use SELECT statements
- Column names with spaces MUST be in square brackets: [Column Name]
- Return ONLY the raw SQL query with NO additional text, explanations, or formatting

"""
        return prompt
    
    def execute_sql_query(self, sql_query: str) -> Optional[pd.DataFrame]:
        """Execute SQL query and return results"""
        try:
            if not self.connection:
                return None
            
            # Basic safety check
            sql_upper = sql_query.upper().strip()
            if not sql_upper.startswith('SELECT'):
                st.error("Only SELECT queries are allowed")
                return None
            
            # Execute query
            result_df = pd.read_sql_query(sql_query, self.connection)
            return result_df
            
        except Exception as e:
            st.error(f"SQL execution error: {str(e)}")
            return None
    
    def format_results_for_llm(self, results_df: pd.DataFrame, original_query: str) -> str:
        """Format SQL results for LLM interpretation"""
        if results_df is None or results_df.empty:
            return "No results found for your query."
        
        # Limit size for token efficiency
        if len(results_df) > 50:
            sample_note = f"\n(Showing first 50 of {len(results_df)} results)"
            display_df = results_df.head(50)
        else:
            sample_note = ""
            display_df = results_df
        
        formatted = f"""
Query: {original_query}

Results:{sample_note}
{display_df.to_string(index=False)}

Summary: {len(results_df)} total rows returned
"""
        return formatted
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.connection = None 