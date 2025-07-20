import streamlit as st
import requests
import datetime
import json

# from exception.exceptions import TradingBotException
import sys

BASE_URL = "http://localhost:8000"  # Backend endpoint

st.set_page_config(
    page_title="🌍 AI Travel Planner Agent",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        font-size: 2.5rem;
        margin-bottom: 2rem;
    }
    .query-template {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        cursor: pointer;
        border-left: 4px solid #1f77b4;
    }
    .query-template:hover {
        background-color: #e1e5e9;
    }
    .tool-indicator {
        display: inline-block;
        background-color: #28a745;
        color: white;
        padding: 0.2rem 0.5rem;
        border-radius: 0.3rem;
        font-size: 0.8rem;
        margin: 0.1rem;
    }
    .comprehensive-plan {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🌍 AI Travel Planner Agent</h1>', unsafe_allow_html=True)

# Sidebar with query templates
with st.sidebar:
    st.header("🚀 Quick Start Templates")
    st.markdown("Click any template to get started:")
    
    # Comprehensive travel planning templates
    st.subheader("📋 Comprehensive Travel Plans")
    
    templates = [
        "Plan a 3-day trip to Paris with budget breakdown",
        "Create a 5-day itinerary for Tokyo including all activities",
        "Plan a weekend getaway to Barcelona with restaurant recommendations",
        "Design a 7-day vacation to New York with cost estimates",
        "Plan a 4-day trip to Amsterdam with transportation options"
    ]
    
    for template in templates:
        if st.button(template, key=f"template_{template[:20]}"):
            st.session_state.selected_template = template
            st.rerun()
    
    st.subheader("🔍 Specific Queries")
    specific_templates = [
        "Find restaurants in London",
        "What's the weather in Rome?",
        "Convert 100 USD to EUR",
        "Find attractions in Tokyo",
        "Search for activities in Paris"
    ]
    
    for template in specific_templates:
        if st.button(template, key=f"specific_{template[:20]}"):
            st.session_state.selected_template = template
            st.rerun()

# Main content area
st.header("🎯 How can I help you plan your perfect trip?")

# Show selected template if any
if hasattr(st.session_state, 'selected_template') and st.session_state.selected_template:
    st.info(f"📝 Selected: {st.session_state.selected_template}")
    user_input = st.text_input("Modify the query or use as is:", value=st.session_state.selected_template)
    del st.session_state.selected_template
else:
    user_input = st.text_input("Enter your travel query:", placeholder="e.g., Plan a 3-day trip to Paris with budget breakdown")

# Comprehensive planning guide
if user_input and any(keyword in user_input.lower() for keyword in ['plan', 'trip', 'itinerary', 'vacation']):
    st.markdown("""
    <div class="comprehensive-plan">
        <h4>🎯 For the most comprehensive travel plan, try including:</h4>
        <ul>
            <li>📍 Specific destination and duration</li>
            <li>💰 Budget requirements or preferences</li>
            <li>🍽️ Food preferences or dietary restrictions</li>
            <li>🎭 Activities you're interested in</li>
            <li>🏨 Accommodation preferences</li>
        </ul>
        <p><strong>Example:</strong> "Plan a 5-day luxury trip to Tokyo with sushi restaurants, cultural activities, and budget under $3000"</p>
    </div>
    """, unsafe_allow_html=True)

# Submit button
if st.button("🚀 Generate Travel Plan", type="primary"):
    if user_input.strip():
        try:
            # Show processing status
            with st.spinner("🤖 AI Agent is analyzing your request and gathering comprehensive travel data..."):
                payload = {"question": user_input}
                response = requests.post(f"{BASE_URL}/query", json=payload)

            if response.status_code == 200:
                answer = response.json().get("answer", "No answer returned.")
                
                # Enhanced markdown content with better formatting
                markdown_content = f"""
                # 🌍 AI Travel Plan

                **Generated:** {datetime.datetime.now().strftime('%Y-%m-%d at %H:%M')}  
                **Created by:** AI Travel Planner Agent

                ---

                {answer}

                ---

                ### 🔧 Tools Used in This Plan:
                <span class="tool-indicator">🌤️ Weather Data</span>
                <span class="tool-indicator">🏛️ Attractions</span>
                <span class="tool-indicator">🍽️ Restaurants</span>
                <span class="tool-indicator">🎭 Activities</span>
                <span class="tool-indicator">🚇 Transportation</span>
                <span class="tool-indicator">💰 Cost Calculator</span>
                <span class="tool-indicator">💱 Currency Converter</span>

                ---

                ⚠️ **Important:** This travel plan was generated by AI. Please verify all information, especially prices, operating hours, and travel requirements before your trip.
                """
                
                st.markdown(markdown_content, unsafe_allow_html=True)
                
                # Add download button for the plan
                st.download_button(
                    label="📥 Download Travel Plan",
                    data=markdown_content,
                    file_name=f"travel_plan_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.md",
                    mime="text/markdown"
                )
                
            else:
                st.error(f"❌ Bot failed to respond: {response.text}")

        except Exception as e:
            st.error(f"❌ The response failed due to: {str(e)}")
    else:
        st.warning("⚠️ Please enter a travel query to get started.")

# Footer with information
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>🌍 Powered by AI Agentic Workflow | Real-time data from multiple APIs | Comprehensive travel planning</p>
</div>
""", unsafe_allow_html=True)