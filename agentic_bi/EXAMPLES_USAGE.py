"""
Agentic BI Usage Examples
Comprehensive examples showing how to use the platform
"""

from agentic_bi.core import AIAgent, Database, NLQProcessor, SelfHealer
from agentic_bi.utils import Visualizer, format_currency
import pandas as pd
import time
import json
from datetime import datetime


# ============= EXAMPLE 1: Basic Query Execution =============
def example_1_basic_query():
    """Execute a basic natural language query"""
    print("\n" + "="*60)
    print("[EXAMPLE 1] Basic Natural Language Query")
    print("="*60)
    
    ai_agent = AIAgent()
    user_query = "What are the top 10 customers by revenue?"
    
    print(f"\n🔍 Query: {user_query}")
    
    result = ai_agent.execute_query(user_query)
    
    print(f"📝 Generated SQL: {result['sql']}")
    print(f"✅ Success: {result['success']}")
    print(f"📊 Rows: {result['metrics']['row_count']}")
    print(f"⚡ Time: {result['metrics']['execution_time']:.2f}s")
    
    if result['data']:
        df = pd.DataFrame(result['data'])
        print(f"\n{df.to_string()}")


# ============= EXAMPLE 2: SQL Generation =============
def example_2_sql_generation():
    """Show SQL generation process"""
    print("\n" + "="*60)
    print("[EXAMPLE 2] AI-Powered SQL Generation")
    print("="*60)
    
    ai_agent = AIAgent()
    queries = [
        "Total sales this month",
        "Top 5 regions by revenue",
        "Average order value by category"
    ]
    
    for query in queries:
        print(f"\n📌 Natural Language: {query}")
        sql, success, error = ai_agent.generate_sql(query)
        if success:
            print(f"✅ Generated SQL: {sql}")
        else:
            print(f"❌ Error: {error}")


# ============= EXAMPLE 3: Visualization =============
def example_3_visualization():
    """Create interactive Plotly visualizations"""
    print("\n" + "="*60)
    print("[EXAMPLE 3] Interactive Visualizations")
    print("="*60)
    
    ai_agent = AIAgent()
    result = ai_agent.execute_query("Show me sales by category")
    
    if result['success'] and result['data']:
        print(f"\n✅ Query returned {len(result['data'])} rows")
        
        # Create different chart types
        charts = {
            'bar': "Bar Chart",
            'pie': "Pie Chart",
            'line': "Line Chart"
        }
        
        for chart_type, name in charts.items():
            print(f"\n📊 Creating {name}...")
            if chart_type == 'bar':
                fig = Visualizer.create_bar_chart(
                    result['data'],
                    x_col=list(result['data'][0].keys())[0],
                    y_col=list(result['data'][0].keys())[1] if len(result['data'][0]) > 1 else list(result['data'][0].keys())[0],
                    title=name
                )
            print(f"✅ {name} created successfully")


# ============= EXAMPLE 4: Error Handling & Self-Healing =============
def example_4_error_handling():
    """Demonstrate error handling and self-healing"""
    print("\n" + "="*60)
    print("[EXAMPLE 4] Error Handling & Self-Healing")
    print("="*60)
    
    db = Database()
    self_healer = SelfHealer()
    
    # Try an invalid query
    invalid_query = "SELECT * FROM non_existent_table LIMIT 1"
    
    print(f"\n🔴 Testing invalid query: {invalid_query}")
    
    try:
        db.execute_query(invalid_query)
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Error: {error_msg}")
        
        # Attempt to fix
        print(f"\n🔧 Attempting to heal...")
        fixed_query, success, explanation = self_healer.attempt_fix(
            original_query=invalid_query,
            error_msg=error_msg
        )
        
        if success:
            print(f"✅ Fixed! Query: {fixed_query}")
        else:
            print(f"⚠️ Could not auto-fix: {explanation}")


# ============= EXAMPLE 5: Query Suggestions =============
def example_5_query_suggestions():
    """Get AI-powered query suggestions"""
    print("\n" + "="*60)
    print("[EXAMPLE 5] Smart Query Suggestions")
    print("="*60)
    
    db = Database()
    nlq = NLQProcessor()
    
    tables = db.get_all_tables()
    
    if tables:
        table_name = tables[0]
        print(f"\n📚 Analyzing table: {table_name}")
        
        suggestions = nlq.suggest_queries(table_name)
        
        print(f"\n💡 AI-Suggested Queries:")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"{i}. {suggestion['title']}")
            print(f"   → {suggestion['query']}")


# ============= EXAMPLE 6: Data Analysis & Insights =============
def example_6_data_analysis():
    """Analyze data and generate insights"""
    print("\n" + "="*60)
    print("[EXAMPLE 6] Data Analysis & Insights")
    print("="*60)
    
    ai_agent = AIAgent()
    result = ai_agent.execute_query("What are the sales by region?")
    
    if result['success']:
        print(f"\n📊 Analyzing {len(result['data'])} records...")
        
        analysis = ai_agent.analyze_data(result['data'])
        
        print(f"\n📈 {analysis['summary']}")
        
        if analysis['statistics']:
            print("\n📊 Statistics:")
            for col_name, stats in analysis['statistics'].items():
                print(f"\n  {col_name}:")
                print(f"    • Sum: {stats.get('sum', 0):,.2f}")
                print(f"    • Average: {stats.get('avg', 0):,.2f}")
                print(f"    • Min: {stats.get('min', 0):,.2f}")
                print(f"    • Max: {stats.get('max', 0):,.2f}")
        
        if analysis['insights']:
            print("\n💭 Insights:")
            for insight in analysis['insights']:
                print(f"  • {insight}")


# ============= EXAMPLE 7: Custom SQL Query =============
def example_7_custom_sql():
    """Execute custom SQL queries"""
    print("\n" + "="*60)
    print("[EXAMPLE 7] Custom SQL Queries")
    print("="*60)
    
    db = Database()
    
    # Get database stats
    tables = db.get_all_tables()
    print(f"\n📊 Available tables: {len(tables)}")
    for table in tables:
        row_count = db.get_table_row_count(table)
        print(f"  • {table}: {row_count:,} rows")
    
    # Execute sample query
    if 'raw_sales_data' in tables:
        print("\n🔍 Executing custom SQL...")
        query = """
        SELECT 
            category,
            COUNT(*) as total_sales,
            SUM(sales_amount) as revenue
        FROM raw_sales_data
        GROUP BY category
        ORDER BY revenue DESC
        LIMIT 5
        """
        
        results = db.execute_query_dict(query)
        
        print("\n📋 Top 5 Categories:")
        for result in results:
            print(f"  • {result.get('category', 'N/A')}: ₹{result.get('revenue', 0):,.2f}")


# ============= EXAMPLE 8: Performance Monitoring =============
def example_8_performance():
    """Monitor query performance"""
    print("\n" + "="*60)
    print("[EXAMPLE 8] Performance Monitoring")
    print("="*60)
    
    ai_agent = AIAgent()
    
    print("\n⚡ Performance Metrics:")
    
    # SQL Generation time
    start = time.time()
    sql, success, _ = ai_agent.generate_sql("Show top products")
    gen_time = (time.time() - start) * 1000
    print(f"  SQL Generation: {gen_time:.2f}ms")
    
    # Full execution
    start = time.time()
    result = ai_agent.execute_query("Show top products")
    exec_time = (time.time() - start) * 1000
    print(f"  Total Execution: {exec_time:.2f}ms")
    
    if result['success']:
        print(f"  Query Execution: {result['metrics']['execution_time']*1000:.2f}ms")
        print(f"  Rows Returned: {result['metrics']['row_count']}")


# ============= EXAMPLE 9: Export Results =============
def example_9_export():
    """Export results in multiple formats"""
    print("\n" + "="*60)
    print("[EXAMPLE 9] Export Results")
    print("="*60)
    
    ai_agent = AIAgent()
    result = ai_agent.execute_query("What are the top 5 customers?")
    
    if result['success'] and result['data']:
        df = pd.DataFrame(result['data'])
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # CSV
        csv_file = f"export_{timestamp}.csv"
        df.to_csv(csv_file, index=False)
        print(f"✅ Exported to CSV: {csv_file}")
        
        # JSON
        json_file = f"export_{timestamp}.json"
        with open(json_file, 'w') as f:
            json.dump(result['data'], f, indent=2)
        print(f"✅ Exported to JSON: {json_file}")


# ============= EXAMPLE 10: Follow-up Questions =============
def example_10_followup():
    """Get AI-suggested follow-up questions"""
    print("\n" + "="*60)
    print("[EXAMPLE 10] Follow-up Question Suggestions")
    print("="*60)
    
    ai_agent = AIAgent()
    result = ai_agent.execute_query("What are the top customers?")
    
    if result['success']:
        print(f"\n💭 AI-Suggested Follow-up Questions:")
        
        suggestions = ai_agent.suggest_follow_up_queries(result['data'])
        for i, suggestion in enumerate(suggestions, 1):
            print(f"{i}. {suggestion}")


# ============= MAIN EXECUTION =============
if __name__ == "__main__":
    print("\n" + "🎯"*30)
    print("AGENTIC BI - COMPREHENSIVE EXAMPLES")
    print("🎯"*30)
    
    examples = [
        ("Basic Query", example_1_basic_query),
        ("SQL Generation", example_2_sql_generation),
        ("Visualization", example_3_visualization),
        ("Error Handling", example_4_error_handling),
        ("Query Suggestions", example_5_query_suggestions),
        ("Data Analysis", example_6_data_analysis),
        ("Custom SQL", example_7_custom_sql),
        ("Performance", example_8_performance),
        ("Export", example_9_export),
        ("Follow-up", example_10_followup),
    ]
    
    for name, example_func in examples:
        try:
            example_func()
        except Exception as e:
            print(f"\n❌ Error in {name}: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*60)
    print("✅ All examples completed!")
    print("="*60 + "\n")
