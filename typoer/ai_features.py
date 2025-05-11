import logging
from typing import Dict, Optional, Any
import google.generativeai as genai
import os

class TypoerAI:
    def __init__(self, api_key: Optional[str] = None):
        self.logger = logging.getLogger(__name__)
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY') or "AIzaSyALQq4cyKojcmdIrtU67jBXooD7OTdMEvc"
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            self.logger.info("Gemini API initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize Gemini API: {str(e)}")
            self.model = None

    def get_typing_suggestions(self, text: str, language: str = "plaintext") -> Dict[str, Any]:
        if not self.model:
            return {"error": "AI features not available"}
        try:
            prompt = f"""Analyze this {language} code/text and provide typing suggestions:\n1. Proper indentation\n2. Special character handling\n3. Line breaks\n4. Code formatting\n\nText: {text}\n\nProvide suggestions in a structured format."""
            response = self.model.generate_content(prompt)
            return {"suggestions": response.text, "status": "success"}
        except Exception as e:
            self.logger.error(f"Error getting typing suggestions: {str(e)}")
            return {"error": str(e)}

    def format_code(self, code: str, language: str) -> Dict[str, Any]:
        if not self.model:
            return {"error": "AI features not available"}
        try:
            prompt = f"""Format this {language} code with proper indentation and structure:\n\n{code}\n\nReturn only the formatted code."""
            response = self.model.generate_content(prompt)
            return {"formatted_code": response.text, "status": "success"}
        except Exception as e:
            self.logger.error(f"Error formatting code: {str(e)}")
            return {"error": str(e)}

    def is_available(self) -> bool:
        return self.model is not None

    def analyze_code(self, code: str, language: str) -> Dict:
        if not self.model:
            return {"error": "AI not loaded"}
        try:
            prompt = f"Analyze this {language} code and suggest improvements:\n{code}"
            result = self.model.generate_content(prompt)
            return {"suggestions": result.text, "status": "success"}
        except Exception as e:
            self.logger.error(f"Error analyzing code: {str(e)}")
            return {"error": str(e)}

    def generate_typing_pattern(self, text: str, style: str = "natural") -> Dict:
        if not self.model:
            return {"error": "AI not loaded"}
        try:
            prompt = f"Generate a natural typing pattern for this text in {style} style:\n{text}"
            result = self.model.generate_content(prompt)
            return {"pattern": result.text, "status": "success"}
        except Exception as e:
            self.logger.error(f"Error generating typing pattern: {str(e)}")
            return {"error": str(e)}

    def suggest_improvements(self, text: str, context: str = "general") -> Dict:
        if not self.model:
            return {"error": "AI not loaded"}
        try:
            prompt = f"Suggest improvements for this text in {context} context:\n{text}"
            result = self.model.generate_content(prompt)
            return {"suggestions": result.text, "status": "success"}
        except Exception as e:
            self.logger.error(f"Error suggesting improvements: {str(e)}")
            return {"error": str(e)}

    def auto_complete(self, partial_text: str, language: str) -> Dict:
        if not self.model:
            return {"error": "AI not loaded"}
        try:
            prompt = f"Complete this {language} code:\n{partial_text}"
            result = self.model.generate_content(prompt)
            return {"suggestions": result.text, "status": "success"}
        except Exception as e:
            self.logger.error(f"Error providing auto-completion: {str(e)}")
            return {"error": str(e)} 