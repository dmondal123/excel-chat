import streamlit as st
import pandas as pd
from typing import Dict, Any
import os

# Import custom modules
from config import Config
from utils.excel_handler import ExcelHandler
from utils.llm_handler import LLMHandler
from utils.plot_generator import PlotGenerator
from utils.sql_handler import SimpleSQLHandler

# Page configuration
st.set_page_config(
    page_title=Config.PAGE_TITLE,
    page_icon=Config.PAGE_ICON,
    layout=Config.LAYOUT,
    initial_sidebar_state="expanded"
)

class ChatToExcelApp:
    """Main application class for Chat to Excel"""
    
    def __init__(self):
        self.excel_handler = ExcelHandler()
        self.llm_handler = LLMHandler()
        self.plot_generator = PlotGenerator()
        self.sql_handler = SimpleSQLHandler()
        
        # Initialize session state
        self._initialize_session_state()
    
    def _initialize_session_state(self):
        """Initialize Streamlit session state variables"""
        if 'data_loaded' not in st.session_state:
            st.session_state.data_loaded = False
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        if 'selected_payment' not in st.session_state:
            st.session_state.selected_payment = None
        if 'show_payment_summary' not in st.session_state:
            st.session_state.show_payment_summary = False
    
    def run(self):
        """Main application entry point"""
        try:
            # Validate configuration
            Config.validate_config()
            
            # Display header
            self._display_header()
            
            # Main application logic
            if not st.session_state.data_loaded:
                self._display_upload_section()
            else:
                self._display_main_interface()
                
        except Exception as e:
            st.error(f"Application error: {str(e)}")
            st.info("Please check your configuration and try again.")
    
    def _display_header(self):
        """Display application header"""
        st.title("📊 Chat to Excel")
        st.markdown("---")
        
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.markdown("**Upload your Excel file and start chatting with your data!**")
        with col2:
            if st.session_state.data_loaded:
                if st.button("🗑️ Clear Data"):
                    self._reset_application()
        with col3:
            if st.session_state.data_loaded:
                if st.button("💬 Clear Chat"):
                    st.session_state.chat_history = []
                    self.llm_handler.clear_conversation()
                    st.rerun()
    
    def _display_upload_section(self):
        """Display file upload interface"""
        st.header("📁 Upload Excel File")
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Choose an Excel file",
            type=['xlsx', 'xls'],
            help=f"Maximum file size: {Config.MAX_FILE_SIZE_MB}MB"
        )
        
        if uploaded_file is not None:
            with st.spinner("Processing your Excel file..."):
                if self.excel_handler.upload_and_process_file(uploaded_file):
                    # Set Excel context for LLM
                    excel_context = self.excel_handler.get_context_for_llm()
                    self.llm_handler.set_excel_context(excel_context)
                    
                    # Load data into SQL handler
                    self.sql_handler.load_data(self.excel_handler.data)
                    
                    st.session_state.data_loaded = True
                    st.rerun()
        
        # Display sample data format
        self._display_sample_format()
    
    def _display_sample_format(self):
        """Display expected Excel format"""
        st.markdown("### 📋 Expected Excel Format")
        st.info("""
        For best results, your Excel file should contain:
        - **Headers in the first row**
        - **Payment-related column** (payment_id, payment_number, etc.)
        - **Numerical data** for analysis
        - **Date columns** in standard format
        - **Clean data** without merged cells
        """)
    
    def _display_main_interface(self):
        """Display main application interface after data is loaded"""
        # Sidebar
        self._display_sidebar()
        
        # Main content area
        col1, col2 = st.columns([2, 1])
        
        with col1:
            self._display_chat_interface()
        
        with col2:
            self._display_data_info()
            self._display_payment_summary_section()
    
    def _display_sidebar(self):
        """Display sidebar with data information and controls"""
        with st.sidebar:
            st.header("📊 Data Overview")
            
            # Basic data info
            data_info = self.excel_handler.get_data_info()
            st.metric("Total Rows", data_info.get('shape', (0, 0))[0])
            st.metric("Total Columns", data_info.get('shape', (0, 0))[1])
            
            # Display columns
            st.subheader("📋 Available Columns")
            for col in self.excel_handler.columns:
                st.write(f"• {col}")
            
            st.markdown("---")
            
            # Quick actions
            st.subheader("⚡ Quick Actions")
            
            if st.button("📈 Show Statistics"):
                self._display_statistics()
            
            if st.button("🔍 Data Quality Check"):
                self._run_data_quality_check()
            
            if st.button("💡 Generate Insights"):
                self._generate_business_insights()
    
    def _display_chat_interface(self):
        """Display chat interface"""
        st.header("💬 Chat with Your Data")
        
        # Display chat history
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask a question about your Excel data..."):
            # Add user message to chat history
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            
            with st.chat_message("user"):
                st.write(prompt)
            
            # Generate response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    # Check if it's a plot request
                    if any(word in prompt.lower() for word in ['plot', 'chart', 'graph', 'visualize', 'show']):
                        self._handle_plot_request(prompt)
                    # Check if it's an analytical query that needs SQL
                    elif self.sql_handler.is_analytical_query(prompt):
                        self._handle_analytical_query(prompt)
                    else:
                        response = self.llm_handler.generate_chat_response(prompt)
                        st.write(response)
                        st.session_state.chat_history.append({"role": "assistant", "content": response})
    
    def _display_data_info(self):
        """Display data preview and information"""
        st.header("📋 Data Preview")
        
        # Data preview
        preview_data = self.excel_handler.get_data_preview()
        st.dataframe(preview_data, use_container_width=True)
        
        # Statistics
        if st.expander("📊 Basic Statistics"):
            stats = self.excel_handler.get_statistics()
            st.dataframe(stats)
    
    def _display_payment_summary_section(self):
        """Display payment summary section"""
        st.header("💳 Payment Summary")
        
        # Payment number selector
        if self.excel_handler.payment_numbers:
            selected_payment = st.selectbox(
                "Select Payment Number:",
                options=self.excel_handler.payment_numbers,
                key="payment_selector"
            )
            
            if st.button("Generate Summary", key="generate_summary"):
                self._generate_payment_summary(selected_payment)
            
            # Display summary if generated
            if st.session_state.get('payment_summary'):
                st.markdown("### Summary Report")
                st.markdown(st.session_state.payment_summary)
        else:
            st.info("No payment numbers detected. Please ensure your Excel file has a payment-related column.")
    
    def _handle_plot_request(self, user_request: str):
        """Handle user request for creating plots"""
        try:
            # Get plot suggestion from LLM
            data_context = self.excel_handler.get_context_for_llm()
            plot_suggestion = self.llm_handler.generate_plot_suggestion(user_request, data_context)
            
            if plot_suggestion.get('success'):
                st.write("**Plot Suggestion:**")
                st.write(plot_suggestion['suggestion'])
                
                # Simple plot generation interface
                st.write("**Create Plot:**")
                
                col1, col2 = st.columns(2)
                with col1:
                    plot_type = st.selectbox(
                        "Plot Type:",
                        options=self.plot_generator.supported_plot_types,
                        key="plot_type_selector"
                    )
                
                with col2:
                    x_column = st.selectbox(
                        "X-axis:",
                        options=self.excel_handler.columns,
                        key="x_axis_selector"
                    )
                
                # Additional options based on plot type
                y_column = None
                if plot_type not in ['histogram', 'pie']:
                    y_column = st.selectbox(
                        "Y-axis:",
                        options=[None] + self.excel_handler.columns,
                        key="y_axis_selector"
                    )
                
                if st.button("Create Plot", key="create_plot_btn"):
                    self._create_and_display_plot(plot_type, x_column, y_column)
            else:
                st.error(plot_suggestion.get('error', 'Error generating plot suggestion'))
                
        except Exception as e:
            st.error(f"Error handling plot request: {str(e)}")
    
    def _handle_analytical_query(self, user_query: str):
        """Handle analytical queries using SQL"""
        try:
            # Generate SQL query
            sql_prompt = self.sql_handler.generate_sql_prompt(user_query)
            sql_query = self.llm_handler.generate_sql_query(sql_prompt)
            
            # Show generated SQL (optional - can be removed)
            with st.expander("🔍 Generated SQL Query", expanded=False):
                st.code(sql_query, language="sql")
            
            # Execute SQL query
            results_df = self.sql_handler.execute_sql_query(sql_query)
            
            if results_df is not None and not results_df.empty:
                # Format results for LLM interpretation
                results_text = self.sql_handler.format_results_for_llm(results_df, user_query)
                
                # Get LLM interpretation
                interpretation = self.llm_handler.interpret_sql_results(results_text)
                
                st.write(interpretation)
                
                # Show data table
                with st.expander("📊 Query Results", expanded=False):
                    st.dataframe(results_df, use_container_width=True)
                
                # Add to conversation history
                full_response = f"{interpretation}\n\n[SQL Query executed successfully]"
                st.session_state.chat_history.append({"role": "assistant", "content": full_response})
            else:
                st.write("No results found for your query.")
                st.session_state.chat_history.append({"role": "assistant", "content": "No results found for your query."})
                
        except Exception as e:
            st.error(f"Error processing analytical query: {str(e)}")
            # Fall back to regular chat
            response = self.llm_handler.generate_chat_response(user_query)
            st.write(response)
            st.session_state.chat_history.append({"role": "assistant", "content": response})
    
    def _create_and_display_plot(self, plot_type: str, x_column: str, y_column: str = None):
        """Create and display plot"""
        try:
            # Prepare plot configuration
            plot_config = {
                'type': plot_type,
                'x': x_column,
                'y': y_column,
                'title': f'{plot_type.title()} Plot'
            }
            
            # Create plot
            fig = self.plot_generator.create_plot(self.excel_handler.data, plot_config)
            
            if fig:
                st.plotly_chart(fig, use_container_width=True)
                
                # Export options
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📄 Export as HTML", key="export_html"):
                        filepath = self.plot_generator.export_plot_as_html(fig)
                        st.success(f"Plot saved as {filepath}")
                
        except Exception as e:
            st.error(f"Error creating plot: {str(e)}")
    
    def _generate_payment_summary(self, payment_number):
        """Generate summary for selected payment"""
        try:
            # Filter data for selected payment
            payment_data = self.excel_handler.filter_by_payment_number(payment_number)
            
            if not payment_data.empty:
                # Convert to string for LLM processing
                payment_data_str = payment_data.to_string()
                
                # Generate summary using dedicated prompt
                summary = self.llm_handler.generate_payment_summary(
                    payment_data_str, 
                    str(payment_number)
                )
                
                st.session_state.payment_summary = summary
                st.session_state.selected_payment = payment_number
                st.rerun()
            else:
                st.error(f"No data found for payment number: {payment_number}")
                
        except Exception as e:
            st.error(f"Error generating payment summary: {str(e)}")
    
    def _display_statistics(self):
        """Display statistical analysis"""
        stats = self.excel_handler.get_statistics()
        st.subheader("📊 Statistical Summary")
        st.dataframe(stats)
    
    def _run_data_quality_check(self):
        """Run data quality analysis"""
        data_info = self.excel_handler.get_data_info()
        
        st.subheader("🔍 Data Quality Report")
        
        # Missing values
        missing_values = data_info.get('missing_values', {})
        if any(count > 0 for count in missing_values.values()):
            st.warning("Missing Values Detected:")
            for col, count in missing_values.items():
                if count > 0:
                    st.write(f"• {col}: {count} missing values")
        else:
            st.success("No missing values found!")
        
        # Data types
        st.info("Column Data Types:")
        for col, dtype in data_info.get('dtypes', {}).items():
            st.write(f"• {col}: {dtype}")
    
    def _generate_business_insights(self):
        """Generate business insights using LLM"""
        try:
            data_context = self.excel_handler.get_context_for_llm()
            
            # You would implement this method in LLMHandler
            st.subheader("💡 Business Insights")
            st.info("Business insights feature coming soon!")
            
        except Exception as e:
            st.error(f"Error generating insights: {str(e)}")
    
    def _reset_application(self):
        """Reset application state"""
        st.session_state.data_loaded = False
        st.session_state.chat_history = []
        st.session_state.selected_payment = None
        st.session_state.show_payment_summary = False
        if 'payment_summary' in st.session_state:
            del st.session_state.payment_summary
        
        # Reset handlers
        self.excel_handler = ExcelHandler()
        self.llm_handler = LLMHandler()
        self.plot_generator = PlotGenerator()
        if hasattr(self, 'sql_handler'):
            self.sql_handler.close()
        self.sql_handler = SimpleSQLHandler()
        
        st.rerun()

def main():
    """Main function to run the application"""
    app = ChatToExcelApp()
    app.run()

if __name__ == "__main__":
    main() 