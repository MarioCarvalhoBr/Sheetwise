"""
Internationalization (i18n) Manager
Manages language loading and switching for the application
"""

import json
import os
from typing import Dict, Any, Optional


class I18nManager:
    """Manages internationalization for the application"""
    
    def __init__(self, default_language: str = 'pt'):
        """
        Initialize the I18n Manager
        
        Args:
            default_language: Default language code ('pt' or 'en')
        """
        self.current_language = default_language
        self.translations: Dict[str, Any] = {}
        self.base_path = os.path.join(os.path.dirname(__file__), '..', 'static', 'i18n')
        self.available_languages = ['pt', 'en']
        
        # Load default language
        self.load_language(default_language)
    
    def load_language(self, language_code: str) -> bool:
        """
        Load translations for specified language
        
        Args:
            language_code: Language code to load ('pt' or 'en')
            
        Returns:
            bool: True if language loaded successfully, False otherwise
        """
        if language_code not in self.available_languages:
            print(f"Language '{language_code}' not available. Using default.")
            language_code = 'pt'
        
        try:
            file_path = os.path.join(self.base_path, f'{language_code}.json')
            
            with open(file_path, 'r', encoding='utf-8') as file:
                self.translations = json.load(file)
                self.current_language = language_code
                print(f"Language '{language_code}' loaded successfully")
                return True
                
        except FileNotFoundError:
            print(f"Translation file not found: {file_path}")
            # Try to load default language as fallback
            if language_code != 'pt':
                return self.load_language('pt')
            return False
            
        except json.JSONDecodeError as e:
            print(f"Error parsing translation file: {e}")
            return False
            
        except Exception as e:
            print(f"Unexpected error loading translations: {e}")
            return False
    
    def get_text(self, key_path: str, **kwargs) -> str:
        """
        Get translated text by key path
        
        Args:
            key_path: Dot-separated path to translation key (e.g., 'login.username')
            **kwargs: Variables for string formatting
            
        Returns:
            str: Translated text or key_path if not found
        """
        try:
            # Split the key path and navigate through the dictionary
            keys = key_path.split('.')
            current = self.translations
            
            for key in keys:
                if isinstance(current, dict) and key in current:
                    current = current[key]
                else:
                    print(f"Translation key not found: {key_path}")
                    return key_path  # Return the key path if not found
            
            # If we have a string, format it with provided kwargs
            if isinstance(current, str):
                try:
                    return current.format(**kwargs)
                except KeyError as e:
                    print(f"Missing format variable {e} for key: {key_path}")
                    return current
            else:
                print(f"Translation key does not point to a string: {key_path}")
                return key_path
                
        except Exception as e:
            print(f"Error getting translation for '{key_path}': {e}")
            return key_path
    
    def change_language(self, language_code: str) -> bool:
        """
        Change the current language
        
        Args:
            language_code: New language code
            
        Returns:
            bool: True if language changed successfully
        """
        if language_code == self.current_language:
            return True
            
        return self.load_language(language_code)
    
    def get_available_languages(self) -> Dict[str, str]:
        """
        Get available languages with their display names
        
        Returns:
            dict: Language codes mapped to display names
        """
        return {
            'pt': self.get_text('main.settings.languages.pt'),
            'en': self.get_text('main.settings.languages.en')
        }
    
    def get_current_language(self) -> str:
        """
        Get current language code
        
        Returns:
            str: Current language code
        """
        return self.current_language


# Global i18n instance
_i18n_instance: Optional[I18nManager] = None


def get_i18n() -> I18nManager:
    """
    Get global i18n instance (singleton pattern)
    
    Returns:
        I18nManager: Global i18n instance
    """
    global _i18n_instance
    if _i18n_instance is None:
        _i18n_instance = I18nManager()
    return _i18n_instance


def init_i18n(language: str = 'pt') -> I18nManager:
    """
    Initialize global i18n instance with specific language
    
    Args:
        language: Language code to initialize with
        
    Returns:
        I18nManager: Initialized i18n instance
    """
    global _i18n_instance
    _i18n_instance = I18nManager(language)
    return _i18n_instance


def _(key_path: str, **kwargs) -> str:
    """
    Shorthand function for getting translated text
    
    Args:
        key_path: Dot-separated path to translation key
        **kwargs: Variables for string formatting
        
    Returns:
        str: Translated text
    """
    return get_i18n().get_text(key_path, **kwargs)


# Example usage:
# from src.utils.i18n_manager import _, get_i18n
# 
# # Get translated text
# title = _('app.title')
# welcome = _('main.welcome', username='John')
# 
# # Change language
# get_i18n().change_language('en')