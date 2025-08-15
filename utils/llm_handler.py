from groq import Groq
from typing import List, Dict, Any
import streamlit as st
from config import Config
from utils.prompt_templates import PromptTemplates

class LLMHandler:
    """Handle LLM interactions for chat and analysis"""
    
    def __init__(self):
        self.client = None
        self.conversation_history = []
        self.excel_context = ""
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Groq client"""
        try:
            if Config.GROQ_API_KEY:
                self.client = Groq(api_key=Config.GROQ_API_KEY)
            else:
                st.error("Groq API key not found. Please set GROQ_API_KEY environment variable.")
        except Exception as e:
            st.error(f"Error initializing LLM client: {str(e)}")
    
    def set_excel_context(self, context: str):
        """Set Excel data context for the conversation"""
        self.excel_context = context
    
    def add_to_conversation(self, role: str, content: str):
        """Add message to conversation history"""
        self.conversation_history.append({"role": role, "content": content})
        
        # Keep only last 10 messages to avoid token limits
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]
    
    def generate_chat_response(self, user_query: str) -> str:
        """Generate response for general chat about Excel data"""
        try:
            if not self.client:
                return "LLM client not initialized. Please check your API key."
            
            # Prepare system prompt
            system_prompt = PromptTemplates.get_general_chat_prompt(self.excel_context)
            
            # Prepare messages
            messages = [{"role": "system", "content": system_prompt}]
            messages.extend(self.conversation_history)
            messages.append({"role": "user", "content": user_query})
            
            # Make API call
            response = self.client.chat.completions.create(
                model=Config.DEFAULT_MODEL,
                messages=messages,
                max_tokens=Config.MAX_TOKENS,
                temperature=Config.TEMPERATURE
            )
            
            assistant_response = response.choices[0].message.content
            
            # Add to conversation history
            self.add_to_conversation("user", user_query)
            self.add_to_conversation("assistant", assistant_response)
            
            return assistant_response
            
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def generate_payment_summary(self, payment_data: str, payment_number: str) -> str:
        """Generate summary for specific payment number using dedicated prompt"""
        try:
            if not self.client:
                return "LLM client not initialized. Please check your API key."
            
            # Use dedicated payment summary prompt
            system_prompt = PromptTemplates.get_payment_summary_prompt()
            
            user_message = f"""
            Payment Number: {payment_number}
            
            Data for this payment:
            {payment_data}
            
            Please generate a comprehensive summary table for this payment.
            """
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
            
            response = self.client.chat.completions.create(
                model=Config.DEFAULT_MODEL,
                messages=messages,
                max_tokens=Config.MAX_TOKENS,
                temperature=0.3  # Lower temperature for more consistent summaries
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error generating payment summary: {str(e)}"
    
    def generate_plot_suggestion(self, user_request: str, data_context: str) -> Dict[str, Any]:
        """Generate plot suggestions based on user request"""
        try:
            if not self.client:
                return {"error": "LLM client not initialized"}
            
            system_prompt = PromptTemplates.get_plot_suggestion_prompt(data_context)
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_request}
            ]
            
            response = self.client.chat.completions.create(
                model=Config.DEFAULT_MODEL,
                messages=messages,
                max_tokens=800,
                temperature=0.5
            )
            
            # Parse response to extract plot configuration
            plot_response = response.choices[0].message.content
            
            return {
                "suggestion": plot_response,
                "success": True
            }
            
        except Exception as e:
            return {
                "error": f"Error generating plot suggestion: {str(e)}",
                "success": False
            }
    
    def clear_conversation(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def generate_sql_query(self, sql_prompt: str) -> str:
        """Generate SQL query from natural language using LLM"""
        try:
            if not self.client:
                return "Error: LLM client not initialized"
            
            messages = [
                {"role": "system", "content": "You are a SQL expert. Generate only valid SQL queries."},
                {"role": "user", "content": sql_prompt}
            ]
            
            response = self.client.chat.completions.create(
                model=Config.DEFAULT_MODEL,
                messages=messages,
                max_tokens=300,
                temperature=0.1  # Low temperature for precise SQL
            )
            
            sql_query = response.choices[0].message.content.strip()
            
            # Clean up the response - remove markdown formatting if present
            if sql_query.startswith('```'):
                sql_query = sql_query.split('\n')[1:-1]
                sql_query = '\n'.join(sql_query)
            
            return sql_query
            
        except Exception as e:
            return f"Error generating SQL: {str(e)}"
    
    def interpret_sql_results(self, results_text: str) -> str:
        """Interpret SQL query results using LLM"""
        try:
            if not self.client:
                return "Error: LLM client not initialized"
            
            messages = [
                {"role": "system", "content": "You are a data analyst. Interpret these SQL query results in a clear, concise way."},
                {"role": "user", "content": f"Please interpret these query results:\n\n{results_text}"}
            ]
            
            response = self.client.chat.completions.create(
                model=Config.DEFAULT_MODEL,
                messages=messages,
                max_tokens=Config.MAX_TOKENS,
                temperature=0.5
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error interpreting results: {str(e)}"
    
    def get_conversation_summary(self) -> str:
        """Get a summary of the current conversation"""
        if not self.conversation_history:
            return "No conversation history."
        
        try:
            # Create a summary prompt
            conversation_text = "\n".join([
                f"{msg['role']}: {msg['content']}" 
                for msg in self.conversation_history
            ])
            
            messages = [
                {"role": "system", "content": "Summarize this conversation in 2-3 sentences."},
                {"role": "user", "content": conversation_text}
            ]
            
            response = self.client.chat.completions.create(
                model=Config.DEFAULT_MODEL,
                messages=messages,
                max_tokens=150,
                temperature=0.3
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error generating summary: {str(e)}" 