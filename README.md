# Chat to Excel 📊

A powerful Streamlit application that lets you chat with your Excel data using Large Language Models (LLMs). Upload an Excel file, ask questions about your data, generate visualizations, and get AI-powered insights.

**Powered by Groq** for lightning-fast inference and cost-effective analysis.

## ✨ Features

### 🔄 Core Functionality
- **Excel File Upload**: Support for `.xlsx` and `.xls` files
- **Interactive Chat**: Natural language queries about your data
- **Payment Analysis**: Dedicated payment number selection and summary generation
- **Data Visualization**: AI-suggested plots and charts
- **Business Insights**: Automated analysis and recommendations

### 📊 Visualization Types
- Bar Charts
- Line Charts
- Scatter Plots
- Histograms
- Box Plots
- Heatmaps
- Pie Charts
- Area Charts

### 💳 Payment Features
- Payment number extraction and selection
- Dedicated payment summary generation using specialized prompts
- Financial analysis and risk assessment
- Transaction pattern identification

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Groq API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd chat-to-excel
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your Groq API key
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

The application will open in your browser at `http://localhost:8501`

## 📁 Project Structure

```
chat-to-excel/
├── app.py                    # Main Streamlit application
├── config.py                 # Configuration management
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── README.md                # This file
├── utils/                   # Core utilities
│   ├── __init__.py
│   ├── excel_handler.py     # Excel file processing
│   ├── llm_handler.py       # LLM integration and chat
│   ├── plot_generator.py    # Visualization generation
│   └── prompt_templates.py  # System prompts
├── prompts/                 # Specialized prompts
│   └── summary_prompt.txt   # Payment summary prompt
└── data/                    # Temporary file storage (auto-created)
```

## 🛠️ Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Required
GROQ_API_KEY=your_groq_api_key_here

# Optional (defaults provided)
MAX_FILE_SIZE_MB=50
DEFAULT_MODEL=llama3-8b-8192
MAX_TOKENS=1500
TEMPERATURE=0.7
```

### Customization

You can customize the application by modifying:

- **`config.py`**: Application settings and defaults
- **`utils/prompt_templates.py`**: System prompts for different tasks
- **`prompts/summary_prompt.txt`**: Dedicated payment summary prompt

## 📖 Usage Guide

### 1. Upload Excel File
- Click "Browse files" or drag and drop your Excel file
- Supported formats: `.xlsx`, `.xls`
- Maximum file size: 50MB (configurable)

### 2. Data Overview
- View data preview in the main interface
- Check column information in the sidebar
- Review basic statistics and data quality

### 3. Chat with Your Data
- Type natural language questions in the chat interface
- Examples:
  - "What are the trends in payment amounts?"
  - "Show me a chart of monthly transactions"
  - "Which payment method is most common?"

### 4. Generate Visualizations
- Request plots using natural language
- Choose from multiple chart types
- Export plots as HTML or PNG files

### 5. Payment Analysis
- Select a payment number from the dropdown
- Click "Generate Summary" for detailed analysis
- View structured payment information and insights

### 6. Quick Actions
- **Show Statistics**: Display descriptive statistics
- **Data Quality Check**: Identify missing values and data issues
- **Generate Insights**: Get AI-powered business recommendations

## 🎯 Excel File Requirements

For optimal results, ensure your Excel file has:

### ✅ Recommended Structure
- **Headers in the first row**
- **Clean data** without merged cells or formatting issues
- **Payment column** (payment_id, payment_number, etc.) for payment analysis
- **Numerical columns** for statistical analysis
- **Date columns** in standard format (YYYY-MM-DD or similar)

### 📋 Example Column Names
- Payment-related: `payment_id`, `payment_number`, `transaction_id`
- Financial: `amount`, `fee`, `total`, `balance`
- Temporal: `date`, `timestamp`, `created_at`
- Categorical: `status`, `method`, `category`, `type`

## 🔧 Advanced Features

### Custom Prompts
Modify `utils/prompt_templates.py` to customize AI behavior for:
- General chat responses
- Payment summary generation
- Plot suggestions
- Business insights

### Plot Configuration
Extend `utils/plot_generator.py` to add new visualization types or customize existing ones.

### Data Processing
Enhance `utils/excel_handler.py` to add custom data validation or preprocessing logic.

## 🐛 Troubleshooting

### Common Issues

1. **"Groq API key not found"**
   - Ensure your `.env` file contains `GROQ_API_KEY=your_key_here`
   - Restart the application after adding the key

2. **File upload errors**
   - Check file size (default limit: 50MB)
   - Ensure file format is `.xlsx` or `.xls`
   - Verify the file isn't corrupted

3. **No payment numbers detected**
   - Ensure your Excel file has a column with "payment" or "pay" in the name
   - Check that the payment column contains valid data

4. **Plot generation fails**
   - Verify the selected columns contain appropriate data types
   - Check for missing values in the selected columns

### Getting Help

If you encounter issues:
1. Check the Streamlit error messages in the browser
2. Review the terminal/console for detailed error logs
3. Verify your Excel file structure matches the requirements

## 📈 Roadmap

- [ ] Support for CSV files
- [ ] Multiple file upload and comparison
- [ ] Advanced statistical analysis
- [ ] Custom dashboard creation
- [ ] Data export functionality
- [ ] Integration with additional LLM providers
- [ ] Real-time data refresh
- [ ] Advanced payment analytics

## 🤝 Contributing

Contributions are welcome! Please feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [Groq](https://groq.com/)
- Visualizations by [Plotly](https://plotly.com/)
- Data processing with [Pandas](https://pandas.pydata.org/)

---

## **Updated User Flow Diagram**

```
┌─────────────────────────────────────────────────────────────────┐
│                        START APPLICATION                        │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                   UPLOAD EXCEL FILE                            │
│  • Drag & drop or browse                                       │
│  • Validate file format (.xlsx, .xls)                         │
│  • Display file info (size, sheets, etc.)                     │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│            PROCESS & LOAD DATA (Enhanced)                      │
│  • Load data with pandas (handles object columns)             │
│  • Load into SQLite in-memory database                        │
│  • Show data preview (first 10 rows)                          │
│  • Display column names, types, and sample values             │
│  • Generate enhanced statistics                               │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│               MAIN APPLICATION INTERFACE                       │
│                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   PAYMENT       │  │   SMART CHAT    │  │     PLOT        │ │
│  │   SUMMARY       │  │   (HYBRID)      │  │  GENERATION     │ │
│  │                 │  │                 │  │                 │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────┬───────────────────┬───────────────────┬───┘
                      │                   │                   │
          ┌───────────┘                   │                   └───────────┐
          │                               │                               │
          ▼                               ▼                               ▼
┌─────────────────────┐      ┌─────────────────────┐      ┌─────────────────────┐
│  PAYMENT SUMMARY    │      │    SMART CHAT       │      │   PLOT GENERATION   │
│  WORKFLOW           │      │    (NEW HYBRID)     │      │   WORKFLOW          │
│                     │      │                     │      │                     │
│ 1. Select payment # │      │ 1. Query analysis   │      │ 1. User requests    │
│ 2. Apply filters    │      │ 2. Route decision:  │      │    visualization    │
│ 3. Generate summary │      │    • Analytical →   │      │ 2. Analyze request  │
│    with dedicated   │      │      SQL Path       │      │ 3. Generate plot    │
│    system prompt    │      │    • Regular →      │      │ 4. Display chart    │
│ 4. Display table    │      │      Context Path   │      │ 5. Allow download   │
│                     │      │    • Plot →         │      │                     │
│                     │      │      Visualization  │      │                     │
│                     │      │ 3. Generate         │      │                     │
│                     │      │    response         │      │                     │
└─────────────────────┘      └─────────────────────┘      └─────────────────────┘
```

## **Updated System Architecture Flow**

```
                          ┌─────────────────┐
                          │   STREAMLIT     │
                          │   FRONTEND      │
                          │   (app.py)      │
                          └────────┬────────┘
                                   │
              ┌────────────────────┼────────────────────┐
              │                    │                    │
              ▼                    ▼                    ▼
    ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
    │ EXCEL_HANDLER   │  │  LLM_HANDLER    │  │ PLOT_GENERATOR  │
    │                 │  │   (GROQ API)    │  │                 │
    │ • Upload file   │  │ • Process chat  │  │ • Create charts │
    │ • Parse data    │  │ • Generate SQL  │  │ • Handle types  │
    │ • Validate      │  │ • Interpret     │  │ • Export plots  │
    │ • Extract info  │  │ • Responses     │  │ • Interactive   │
    └─────────┬───────┘  └─────────┬───────┘  └─────────┬───────┘
              │                    │                    │
              │                    │                    │
              └────────────┬───────┘                    │
                           │                            │
                           ▼                            │
                ┌─────────────────┐                     │
                │ SQL_HANDLER     │                     │
                │  (NEW)          │                     │
                │ • SQLite DB     │                     │
                │ • Query routing │                     │
                │ • Execute SQL   │                     │
                │ • Format results│                     │
                └─────────┬───────┘                     │
                          │                             │
                          └─────────────────────────────┘
                                   │
                                   ▼
                        ┌─────────────────┐
                        │ PROMPT_TEMPLATES│
                        │                 │
                        │ • General chat  │
                        │ • Payment       │
                        │   summary       │
                        │ • SQL generation│
                        │ • Plot requests │
                        └─────────────────┘
```

## **Enhanced Query Routing Flow**

```
USER INPUT
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│                    QUERY CLASSIFICATION                     │
│                                                             │
│  🔍 Check Keywords:                                        │
│  • Plot: 'chart', 'graph', 'visualize', 'plot', 'show'   │
│  • Analytical: 'average', 'sum', 'count', 'filter',      │
│    'group', 'compare', 'trend', 'max', 'min'             │
│  • Regular: Everything else                                │
└─────────────────────┬───────────────────────────────────────┘
                      │
         ┌────────────┼────────────┐
         │            │            │
         ▼            ▼            ▼
    ┌─────────┐  ┌─────────┐  ┌─────────┐
    │  PLOT   │  │   SQL   │  │REGULAR  │
    │  PATH   │  │  PATH   │  │  CHAT   │
    └─────────┘  └─────────┘  └─────────┘
         │            │            │
         │            ▼            │
         │    ┌─────────────────┐  │
         │    │ 1. Generate SQL │  │
         │    │ 2. Execute Query│  │
         │    │ 3. Format Results│  │
         │    │ 4. LLM Interpret│  │
         │    │ 5. Show Data    │  │
         │    └─────────────────┘  │
         │            │            │
         └────────────┼────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ DISPLAY RESPONSE│
              │ • Text response │
              │ • Data tables   │
              │ • Visualizations│
              │ • SQL queries   │
              └─────────────────┘
```

## **Enhanced Data Pipeline with Object Column Handling**

```
┌─────────────────────────────────────────────────────────────────┐
│                    ENHANCED DATA PIPELINE                       │
│                                                                 │
│  Excel File (200 rows × 22 columns)                           │
│      │                                                          │
│      ▼                                                          │
│  pandas.read_excel() ──► DataFrame ──► Data Validation         │
│      │                       │              │                  │
│      │                       ▼              ▼                  │
│      │              Column Analysis   Enhanced Statistics      │
│      │              • Numeric: int64,  • describe() for nums   │
│      │                float64          • value_counts() for    │
│      │              • Object: strings,   categorical          │
│      │                categories       • Missing values       │
│      │              • Datetime: dates  • Data quality        │
│      │                       │              │                  │
│      │                       └──────┬───────┘                  │
│      │                              │                          │
│      └──────────────┬─────────────────────────────────────────┤
│                     │                 │                       │
│                     ▼                 ▼                       │
│              Session State     Context for LLM               │
│              • DataFrame       • Schema info                 │
│              • Column info     • Sample data                 │
│              • Payment numbers • Statistics                   │
│                     │                 │                       │
│                     └─────────┬───────┘                       │
│                               │                               │
│                               ▼                               │
│                   ┌─────────────────────┐                    │
│                   │   SQLite Database   │                    │
│                   │   (In-Memory)       │                    │
│                   │ • All 200 rows      │                    │
│                   │ • Object columns    │                    │
│                   │   preserved         │                    │
│                   │ • Ready for SQL     │                    │
│                   └─────────────────────┘                    │
│                               │                               │
│                     ┌─────────┼─────────┐                     │
│                     │         │         │                     │
│                     ▼         ▼         ▼                     │
│              Context    SQL Analysis   Plot                   │
│              Based      (Full Dataset) Generation             │
│              Chat       • GROUP BY     • All data            │
│              • 3 rows   • WHERE        • Object cols         │
│              • Stats    • Object cols  • Relationships       │
│                         • Aggregations                       │
│                               │                               │
│                               ▼                               │
│                        User Interface                        │
│                     • Chat responses                          │
│                     • Data tables                             │
│                     • Visualizations                          │
│                     • SQL queries                             │
└─────────────────────────────────────────────────────────────────┘
```

## **Object Column Handling Details**

```
OBJECT COLUMNS IN YOUR 22-COLUMN DATASET
│
├── TEXT FIELDS
│   ├── Customer Names → GROUP BY customer_name
│   ├── Descriptions → LIKE '%keyword%' searches
│   └── Addresses → Geographic analysis
│
├── CATEGORICAL DATA
│   ├── Status → WHERE status = 'approved'
│   ├── Payment Method → GROUP BY payment_method
│   └── Product Type → COUNT(*) BY category
│
├── ID FIELDS
│   ├── Transaction IDs → Unique identifiers
│   ├── Customer IDs → JOIN operations
│   └── Reference Numbers → Exact matches
│
└── DATE STRINGS
    ├── If not datetime → String operations
    ├── Pattern matching → LIKE '2024%'
    └── LLM interpretation → Smart parsing
```

## **Groq API Integration Benefits**

```
┌─────────────────────────────────────────────────────────────────┐
│                      GROQ ADVANTAGES                            │
│                                                                 │
│  SPEED                     COST                 MODELS          │
│  ┌─────────────┐         ┌─────────────┐      ┌─────────────┐   │
│  │ SQL Query   │         │ 10x cheaper │      │ Llama3-8B   │   │
│  │ Generation: │         │ than OpenAI │      │ (Default)   │   │
│  │ 0.5 seconds │         │             │      │             │   │
│  │             │         │ Pay per use │      │ Mixtral-8x7B│   │
│  │ Result      │         │ No monthly  │      │ (Advanced)  │   │
│  │ Analysis:   │         │ minimums    │      │             │   │
│  │ 0.8 seconds │         │             │      │ Llama3-70B  │   │
│  │             │         │             │      │ (Premium)   │   │
│  └─────────────┘         └─────────────┘      └─────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## **Key Improvements in Updated Architecture:**

1. **Hybrid Intelligence**: Automatic routing between SQL and context-based analysis
2. **Object Column Support**: Full handling of text/categorical data in both paths  
3. **Groq Speed**: Lightning-fast responses for better user experience
4. **Enhanced Context**: Smarter sampling and statistics for LLM
5. **SQL Safety**: Only SELECT queries with proper validation
6. **Transparent Process**: Users can see generated SQL queries
7. **Fallback Mechanism**: If SQL fails, gracefully falls back to context chat

The system now intelligently chooses the best approach for each query while handling your mixed-datatype Excel files perfectly! 🚀