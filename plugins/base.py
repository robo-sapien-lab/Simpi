"""
Base plugin class and plugin management system.
"""
from typing import Dict, Type, Optional
import importlib
import pkgutil
import structlog
from abc import ABC, abstractmethod

logger = structlog.get_logger()

class BasePlugin(ABC):
    name: str = None  # Must be set by subclasses
    
    @abstractmethod
    async def handle_message(self, message: str) -> Optional[str]:
        """Process a message and return a response if applicable."""
        pass
        
    @abstractmethod
    async def can_handle(self, message: str) -> bool:
        """Check if this plugin can handle the given message."""
        pass
        
class PluginManager:
    def __init__(self):
        self.plugins: Dict[str, BasePlugin] = {}
        
    async def load_plugins(self):
        """Discover and load all plugins."""
        try:
            # Import all modules in the plugins package
            plugin_package = importlib.import_module('plugins')
            for _, name, _ in pkgutil.iter_modules(
                plugin_package.__path__
            ):
                if name != 'base':  # Skip base module
                    try:
                        module = importlib.import_module(
                            f'plugins.{name}'
                        )
                        
                        # Find plugin classes
                        for attr_name in dir(module):
                            attr = getattr(module, attr_name)
                            if (isinstance(attr, type) and 
                                issubclass(attr, BasePlugin) and 
                                attr != BasePlugin):
                                plugin = attr()
                                if plugin.name:
                                    self.plugins[plugin.name] = plugin
                                    logger.info(
                                        f"Loaded plugin: {plugin.name}"
                                    )
                                    
                    except Exception as e:
                        logger.error(
                            f"Error loading plugin {name}",
                            error=str(e)
                        )
                        
        except Exception as e:
            logger.error("Error loading plugins", error=str(e))
            
    async def get_handler(self, message: str) -> Optional[BasePlugin]:
        """Find the appropriate plugin to handle a message."""
        for plugin in self.plugins.values():
            if await plugin.can_handle(message):
                return plugin
        return None
