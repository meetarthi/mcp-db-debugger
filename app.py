import streamlit as st
import asyncio
from services.error_detector import ErrorDetector
from config.settings import Config

# Configure Streamlit page
st.set_page_config(
    page_title=Config.PAGE_TITLE,
    page_icon=Config.PAGE_ICON,
    layout="wide"
)

# Initialize the error detector (cached for performance)
@st.cache_resource
def get_error_detector():
    return ErrorDetector()

def main():
    # Header
    st.title("🔧 Database Error Debugger")
    st.write("AI-powered database error analysis")
    
    # Sidebar for settings
    with st.sidebar:
        st.header("⚙️ Settings")
        db_type = st.selectbox(
            "Database Type:", 
            ["postgresql", "mysql", "sqlite", "oracle", "sqlserver"]
        )
    
    # Main input area
    st.subheader("📝 Describe Your Error")
    error_description = st.text_area(
        "Error Description:",
        placeholder="Paste your error message or describe the issue...",
        height=150
    )
    
    # Analyze button
    if st.button("🔍 Analyze Error", type="primary", disabled=not error_description.strip()):
        
        # Show progress
        with st.spinner("🤖 Analyzing error..."):
            try:
                # Get the error detector
                error_detector = get_error_detector()
                
                # Run the analysis (handle async)
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                try:
                    result = loop.run_until_complete(
                        error_detector.diagnose_error(error_description, db_type)
                    )
                finally:
                    loop.close()
                
                # Display results
                display_results(result)
                
            except Exception as e:
                st.error(f"❌ Analysis failed: {str(e)}")

def display_results(result):
    """Display the analysis results"""
    
    if not result.get('success'):
        st.error(f"❌ Analysis failed: {result.get('error', 'Unknown error')}")
        return
    
    # Success message
    st.success("✅ Analysis complete!")
    
    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs(["📊 Summary", "🔍 Investigation", "💡 Recommendations"])
    
    with tab1:
        show_summary(result)
    
    with tab2:
        show_investigation(result)
        
    with tab3:
        show_recommendations(result)

def show_summary(result):
    """Show analysis summary"""
    ai_analysis = result.get('ai_analysis', {})
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        category = ai_analysis.get('error_category', 'unknown').title()
        st.metric("Error Category", category)
    
    with col2:
        severity = ai_analysis.get('severity', 'medium').upper()
        st.metric("Severity", severity)
        
    with col3:
        db_health = result.get('database_investigation', {}).get('health_check', {})
        health_status = "Healthy" if db_health.get('connection_healthy') else "Issues"
        st.metric("Database Health", health_status)
    
    # Analysis details
    st.subheader("📝 Analysis")
    st.write(ai_analysis.get('analysis', 'No analysis available'))

def show_investigation(result):
    """Show database investigation results"""
    db_investigation = result.get('database_investigation', {})
    
    # Query execution summary
    total_queries = db_investigation.get('queries_executed', 0)
    successful = db_investigation.get('successful_queries', 0)
    
    st.subheader("📊 Query Execution")
    st.write(f"Executed {successful}/{total_queries} queries successfully")
    
    # Show individual query results
    query_results = db_investigation.get('query_results', [])
    for i, query_result in enumerate(query_results, 1):
        with st.expander(f"Query {i}: {'✅' if query_result.get('success') else '❌'}"):
            st.code(query_result.get('query', ''), language='sql')
            
            if query_result.get('success'):
                data = query_result.get('data', [])
                if data and isinstance(data, list):
                    st.dataframe(data)
                else:
                    st.info("Query executed successfully")
            else:
                st.error(f"Error: {query_result.get('error', 'Unknown')}")

def show_recommendations(result):
    """Show recommendations"""
    recommendations = result.get('recommendations', [])
    
    if not recommendations:
        st.info("No recommendations available")
        return
    
    st.subheader("💡 Recommended Actions")
    
    for i, rec in enumerate(recommendations, 1):
        st.markdown(f"**{i}.** {rec}")

if __name__ == "__main__":
    main()