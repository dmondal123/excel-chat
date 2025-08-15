import pandas as pd
import streamlit as st
from typing import Dict, List, Any, Optional
import os
from config import Config

class ExcelHandler:
    """Handle Excel file operations and data processing"""
    
    def __init__(self):
        self.data = None
        self.filename = None
        self.columns = []
        self.payment_numbers = []
        
    def upload_and_process_file(self, uploaded_file) -> bool:
        """
        Upload and process Excel file
        Returns True if successful, False otherwise
        """
        try:
            if uploaded_file is None:
                return False
                
            # Validate file extension
            if not self._validate_file_extension(uploaded_file.name):
                st.error("Please upload a valid Excel file (.xlsx or .xls)")
                return False
                
            # Validate file size
            if not self._validate_file_size(uploaded_file):
                st.error(f"File size too large. Maximum size: {Config.MAX_FILE_SIZE_MB}MB")
                return False
                
            # Read Excel file
            self.data = pd.read_excel(uploaded_file)
            self.filename = uploaded_file.name
            self.columns = list(self.data.columns)
            
            # Extract payment numbers (assuming there's a payment column)
            self._extract_payment_numbers()
            
            st.success(f"Successfully loaded {self.filename}")
            return True
            
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
            return False
    
    def _validate_file_extension(self, filename: str) -> bool:
        """Validate file extension"""
        return any(filename.lower().endswith(ext) for ext in Config.ALLOWED_EXTENSIONS)
    
    def _validate_file_size(self, uploaded_file) -> bool:
        """Validate file size"""
        return uploaded_file.size <= Config.MAX_FILE_SIZE_MB * 1024 * 1024
    
    def _extract_payment_numbers(self):
        """Extract unique payment numbers from the data"""
        # Look for payment-related columns
        payment_columns = [col for col in self.columns if 'payment' in col.lower() or 'pay' in col.lower()]
        
        if payment_columns:
            # Use the first payment column found
            payment_col = payment_columns[0]
            self.payment_numbers = sorted(self.data[payment_col].dropna().unique().tolist())
        else:
            # If no payment column found, use index as payment numbers
            self.payment_numbers = list(range(1, len(self.data) + 1))
    
    def get_data_preview(self, rows: int = 10) -> pd.DataFrame:
        """Get data preview with specified number of rows"""
        if self.data is not None:
            return self.data.head(rows)
        return pd.DataFrame()
    
    def get_data_info(self) -> Dict[str, Any]:
        """Get basic information about the dataset"""
        if self.data is None:
            return {}
        
        return {
            "shape": self.data.shape,
            "columns": self.columns,
            "dtypes": dict(self.data.dtypes),
            "missing_values": dict(self.data.isnull().sum()),
            "memory_usage": self.data.memory_usage(deep=True).sum(),
        }
    
    def get_statistics(self) -> pd.DataFrame:
        """Get descriptive statistics for numerical columns"""
        if self.data is None:
            return pd.DataFrame()
        
        return self.data.describe()
    
    def filter_by_payment_number(self, payment_number) -> pd.DataFrame:
        """Filter data by payment number"""
        if self.data is None:
            return pd.DataFrame()
        
        # Find payment column
        payment_columns = [col for col in self.columns if 'payment' in col.lower() or 'pay' in col.lower()]
        
        if payment_columns:
            payment_col = payment_columns[0]
            return self.data[self.data[payment_col] == payment_number]
        else:
            # If no payment column, return row by index
            try:
                return self.data.iloc[[payment_number - 1]]
            except IndexError:
                return pd.DataFrame()
    
    def get_context_for_llm(self) -> str:
        """Generate context string for LLM about the Excel data"""
        if self.data is None:
            return "No data loaded."
        
        info = self.get_data_info()
        
        context = f"""
        Excel File: {self.filename}
        Dataset Shape: {info['shape']}
        Columns: {', '.join(self.columns)}
        
        Column Types:
        {chr(10).join([f"- {col}: {dtype}" for col, dtype in info['dtypes'].items()])}
        
        Summary Statistics:
        {self.get_statistics().to_string()}
        
        Sample Data (first 3 rows):
        {self.data.head(3).to_string()}
        """
        
        return context
    
    def save_processed_data(self, filepath: str):
        """Save processed data to file"""
        if self.data is not None:
            self.data.to_csv(filepath, index=False) 