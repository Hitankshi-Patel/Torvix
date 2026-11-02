"""
AI Provider integrations for Torvix
"""

import requests
import json
from typing import Dict, Optional, Any
from abc import ABC, abstractmethod
from rich.console import Console
from .logger import logger, log_api_request, log_error

console = Console()

class AIProvider(ABC):
    """Abstract base class for AI providers."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        # Ensure api key is clean (avoid accidental spaces/newlines)
        raw_key = config.get('api_key')
        self.api_key = raw_key.strip() if isinstance(raw_key, str) else raw_key
        self.base_url = config.get('base_url')
        self.model = config.get('model')
    
    @abstractmethod
    def query(self, prompt: str) -> Optional[str]:
        """Send a query to the AI provider and return the response."""
        pass
    
    def _make_request(self, url: str, headers: Dict[str, str], data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Make HTTP request to AI provider with better error diagnostics."""
        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            # Try to surface provider error body
            status = e.response.status_code if e.response is not None else 'N/A'
            body = None
            try:
                body = e.response.json()
            except Exception:
                body = e.response.text if e.response is not None else ''
            console.print(f"[red]API request failed ({status}): {body}[/red]")
            return None
        except requests.exceptions.RequestException as e:
            console.print(f"[red]API request failed: {e}[/red]")
            return None

class OpenAIProvider(AIProvider):
    """OpenAI ChatGPT provider."""
    
    def query(self, prompt: str) -> Optional[str]:
        if not self.api_key:
            console.print("[red]OpenAI API key is missing or empty[/red]")
            return None
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        system_prompt = """You are Torvix, an AI terminal assistant. When users ask you to perform tasks, respond with:
1. A brief explanation of what you'll do
2. The specific terminal commands needed, each prefixed with 'RUN: '
3. Any warnings or considerations

Example:
I'll help you push your code to GitHub. Here are the commands:

RUN: git add .
RUN: git commit -m "Update code"
RUN: git push origin main

Make sure you have a remote repository configured."""
        
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 1000,
            "temperature": 0.7
        }
        
        response = self._make_request(url, headers, data)
        if response and 'choices' in response:
            return response['choices'][0]['message']['content']
        return None

class GeminiProvider(AIProvider):
    """Google Gemini provider."""
    
    def query(self, prompt: str) -> Optional[str]:
        if not self.api_key or not isinstance(self.api_key, str) or len(self.api_key.strip()) < 10:
            console.print("[red]Gemini API key is missing or empty[/red]")
            return None
        
        url = f"{self.base_url}/models/{self.model}:generateContent?key={self.api_key}"
        headers = {
            "Content-Type": "application/json"
        }

        system_prompt = """You are Torvix, an AI terminal assistant. When users ask you to perform tasks, respond with:
1. A brief explanation of what you'll do
2. The specific terminal commands needed, each prefixed with 'RUN: '
3. Any warnings or considerations"""

        data = {
            "contents": [{
                "parts": [{
                    "text": f"{system_prompt}\n\nUser request: {prompt}"
                }]
            }],
            "generationConfig": {
                "maxOutputTokens": 1000,
                "temperature": 0.7
            }
        }

        response = self._make_request(url, headers, data)
        if response and 'candidates' in response and len(response['candidates']) > 0:
            content = response['candidates'][0].get('content', {})
            parts = content.get('parts', [])
            if parts and len(parts) > 0:
                return parts[0].get('text', '')
        return None

class AnthropicProvider(AIProvider):
    """Anthropic Claude provider."""
    
    def query(self, prompt: str) -> Optional[str]:
        url = f"{self.base_url}/messages"
        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        system_prompt = """You are Torvix, an AI terminal assistant. When users ask you to perform tasks, respond with:
1. A brief explanation of what you'll do
2. The specific terminal commands needed, each prefixed with 'RUN: '
3. Any warnings or considerations"""
        
        data = {
            "model": self.model,
            "max_tokens": 1000,
            "system": system_prompt,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        
        response = self._make_request(url, headers, data)
        if response and 'content' in response:
            return response['content'][0]['text']
        return None

class GenericProvider(AIProvider):
    """Generic provider for OpenAI-compatible APIs (DeepSeek, Perplexity, Grok, etc.)."""
    
    def query(self, prompt: str) -> Optional[str]:
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        system_prompt = """You are Torvix, an AI terminal assistant. When users ask you to perform tasks, respond with:
1. A brief explanation of what you'll do
2. The specific terminal commands needed, each prefixed with 'RUN: '
3. Any warnings or considerations

Example:
I'll help you push your code to GitHub. Here are the commands:

RUN: git add .
RUN: git commit -m "Update code"
RUN: git push origin main

Make sure you have a remote repository configured."""
        
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 1000,
            "temperature": 0.7
        }
        
        response = self._make_request(url, headers, data)
        if response and 'choices' in response:
            return response['choices'][0]['message']['content']
        return None

class AIProviderManager:
    """Manages AI provider instances and routing."""
    
    PROVIDER_CLASSES = {
        'chatgpt': OpenAIProvider,
        'gemini': GeminiProvider,
        'claude': AnthropicProvider,
        'deepseek': GenericProvider,
        'perplexity': GenericProvider,
        'grok': GenericProvider,
        'torvix': GenericProvider
    }
    
    def __init__(self, config_manager):
        self.config_manager = config_manager
    
    def query(self, prompt: str, provider_id: Optional[str] = None) -> Optional[str]:
        """Send a query to the specified or default AI provider."""
        config = self.config_manager.get_provider_config(provider_id)

        if not config:
            if provider_id:
                console.print(f"[red]Provider '{provider_id}' not configured or no API key found[/red]")
                logger.warning(f"Provider '{provider_id}' not configured")
            else:
                console.print("[red]No default provider configured. Run 'torvix setup' first.[/red]")
                logger.warning("No default provider configured")
            return None

        provider_class = self.PROVIDER_CLASSES.get(config['provider_id'])
        if not provider_class:
            console.print(f"[red]Unsupported provider: {config['provider_id']}[/red]")
            logger.error(f"Unsupported provider: {config['provider_id']}")
            return None

        provider = provider_class(config)

        try:
            logger.debug(f"Querying {config['name']} with prompt: {prompt[:50]}...")
            response = provider.query(prompt)
            log_api_request(config['name'], prompt, response is not None)
            return response
        except Exception as e:
            console.print(f"[red]Error querying {config['name']}: {e}[/red]")
            log_error(e, f"querying {config['name']}")
            return None
