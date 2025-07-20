
from utils.model_loader import ModelLoader
from prompt_library.prompt import SYSTEM_PROMPT
from langgraph.graph import StateGraph, MessagesState, END, START
from langgraph.prebuilt import ToolNode, tools_condition
from tools.weather_info_tool import WeatherInfoTool
from tools.place_search_tool import PlaceSearchTool
from tools.expense_calculator_tool import CalculatorTool
from tools.currency_conversion_tool import CurrencyConverterTool

class GraphBuilder():
    def __init__(self,model_provider: str = "ollama"):
        self.model_loader = ModelLoader(model_provider=model_provider)
        self.llm = self.model_loader.load_llm()
        
        self.tools = []
        
        self.weather_tools = WeatherInfoTool()
        self.place_search_tools = PlaceSearchTool()
        self.calculator_tools = CalculatorTool()
        self.currency_converter_tools = CurrencyConverterTool()
        
        self.tools.extend([* self.weather_tools.weather_tool_list, 
                           * self.place_search_tools.place_search_tool_list,
                           * self.calculator_tools.calculator_tool_list,
                           * self.currency_converter_tools.currency_converter_tool_list])
        
        self.llm_with_tools = self.llm.bind_tools(tools=self.tools)
        
        self.graph = None
        
        self.system_prompt = SYSTEM_PROMPT
    
    
    def agent_function(self,state: MessagesState):
        """Main agent function"""
        user_question = state["messages"]
        
        # Check if this is a travel planning query
        last_message = user_question[-1].content if user_question else ""
        is_travel_planning = any(keyword in last_message.lower() for keyword in ['plan', 'trip', 'itinerary', 'vacation', 'travel'])
        
        # Enhanced system prompt for travel planning
        if is_travel_planning:
            # Create enhanced system message for travel planning
            from langchain_core.messages import SystemMessage
            enhanced_content = self.system_prompt.content + "\n\nIMPORTANT: For travel planning queries, you MUST call multiple tools to provide comprehensive information. Call weather, attractions, restaurants, activities, transportation, and cost calculation tools."
            enhanced_prompt = SystemMessage(content=enhanced_content)
        else:
            enhanced_prompt = self.system_prompt
            
        input_question = [enhanced_prompt] + user_question
        response = self.llm_with_tools.invoke(input_question)
        
        # For Ollama/Gemma models, we need to manually detect tool calls from the response
        response_content = response.content if hasattr(response, 'content') else str(response)
        
        # Check if the response contains tool call patterns
        if 'tool_code' in response_content or any(tool.name in response_content for tool in self.tools):
            print(f"🔧 Agent detected tool call in response")
            
            # Extract tool calls from the response
            tool_calls = []
            for tool in self.tools:
                if tool.name in response_content:
                    # Simple pattern matching to extract parameters
                    import re
                    pattern = rf"{tool.name}\(([^)]*)\)"
                    matches = re.findall(pattern, response_content)
                    if matches:
                        tool_calls.append({
                            'name': tool.name,
                            'args': matches[0]
                        })
            
            if tool_calls:
                print(f"🔧 Agent calling tools: {[tc['name'] for tc in tool_calls]}")
                # Execute tools manually
                results = []
                for tool_call in tool_calls:
                    try:
                        tool = next(t for t in self.tools if t.name == tool_call['name'])
                        # Parse arguments (simplified)
                        args_str = tool_call['args']
                        if 'city=' in args_str or 'place=' in args_str:
                            # Extract city/place name
                            import re
                            city_match = re.search(r'["\']([^"\']+)["\']', args_str)
                            if city_match:
                                city = city_match.group(1)
                                result = tool.invoke({"city": city} if 'city' in tool_call['name'] else {"place": city})
                                results.append(f"{tool_call['name']} result: {result}")
                    except Exception as e:
                        print(f"Error executing tool {tool_call['name']}: {e}")
                
                # Create a new response with tool results
                from langchain_core.messages import AIMessage
                combined_response = response_content + "\n\n" + "\n".join(results)
                return {"messages": [AIMessage(content=combined_response)]}
        
        print(f"✅ Agent providing final answer (no tool calls)")
        # If no tool calls, this is the final answer
        return {"messages": [response]}
    def build_graph(self):
        graph_builder=StateGraph(MessagesState)
        graph_builder.add_node("agent", self.agent_function)
        graph_builder.add_node("tools", ToolNode(tools=self.tools))
        graph_builder.add_edge(START,"agent")
        graph_builder.add_conditional_edges("agent",tools_condition)
        graph_builder.add_edge("tools","agent")
        graph_builder.add_edge("agent",END)
        self.graph = graph_builder.compile()
        return self.graph
        
    def __call__(self):
        return self.build_graph()