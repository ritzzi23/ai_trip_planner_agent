import os
import requests
import json
from dotenv import load_dotenv
from typing import Literal, Optional, Any, List, Dict
from pydantic import BaseModel, Field
from utils.config_loader import load_config
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_core.outputs import ChatResult, ChatGeneration


class OllamaLLM(BaseChatModel):
    """Custom LLM class for Ollama API"""
    
    base_url: str = "https://ollama-gemma-549370391494.europe-west1.run.app"
    model_name: str = "gemma3:1b"
    tools: Optional[List] = None
    
    def bind_tools(self, tools):
        """Bind tools to the model - required for LangChain compatibility"""
        # Store tools for manual tool calling
        self.tools = tools
        return self
    
    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[Any] = None,
        **kwargs: Any,
    ) -> ChatResult:
        """Generate a response from the Ollama API"""
        
        # Convert messages to prompt format
        prompt = self._format_messages_to_prompt(messages)
        
        # Prepare the request payload
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            # Make request to Ollama API
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=60
            )
            response.raise_for_status()
            
            # Parse the response
            result = response.json()
            ai_message = AIMessage(content=result.get("response", ""))
            
            return ChatResult(generations=[ChatGeneration(message=ai_message)])
            
        except Exception as e:
            print(f"Error calling Ollama API: {e}")
            # Fallback response
            ai_message = AIMessage(content="I apologize, but I'm having trouble processing your request right now.")
            return ChatResult(generations=[ChatGeneration(message=ai_message)])
    
    def _format_messages_to_prompt(self, messages: List[BaseMessage]) -> str:
        """Convert LangChain messages to a single prompt string"""
        formatted_parts = []
        
        for message in messages:
            if isinstance(message, SystemMessage):
                formatted_parts.append(f"System: {message.content}")
            elif isinstance(message, HumanMessage):
                formatted_parts.append(f"Human: {message.content}")
            elif isinstance(message, AIMessage):
                formatted_parts.append(f"Assistant: {message.content}")
        
        return "\n".join(formatted_parts)
    
    @property
    def _llm_type(self) -> str:
        return "ollama"


class ConfigLoader:
    def __init__(self):
        print(f"Loaded config.....")
        self.config = load_config()
    
    def __getitem__(self, key):
        return self.config[key]

class ModelLoader(BaseModel):
    model_provider: Literal["groq", "openai", "ollama"] = "groq"
    config: Optional[ConfigLoader] = Field(default=None, exclude=True)

    def model_post_init(self, __context: Any) -> None:
        self.config = ConfigLoader()
    
    class Config:
        arbitrary_types_allowed = True
    
    def load_llm(self):
        """
        Load and return the LLM model.
        """
        print("LLM loading...")
        print(f"Loading model from provider: {self.model_provider}")
        
        if self.model_provider == "ollama":
            print("Loading self-hosted Gemma 3 1B from Ollama..............")
            llm = OllamaLLM()
        elif self.model_provider == "groq":
            print("Loading LLM from Groq..............")
            groq_api_key = os.getenv("GROQ_API_KEY")
            model_name = self.config["llm"]["groq"]["model_name"]
            llm=ChatGroq(model=model_name, api_key=groq_api_key)
        elif self.model_provider == "openai":
            print("Loading LLM from OpenAI..............")
            openai_api_key = os.getenv("OPENAI_API_KEY")
            model_name = self.config["llm"]["openai"]["model_name"]
            llm = ChatOpenAI(model_name="o4-mini", api_key=openai_api_key)
        
        return llm
    