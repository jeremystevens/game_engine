
"""
Logging system for the game engine
Provides debug, info, warning, and error logging with configurable output
"""
import sys
import time
from enum import Enum
from typing import Optional, TextIO


class LogLevel(Enum):
    """Log level enumeration"""
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3


class Logger:
    """Game engine logger with multiple levels and formatting"""
    
    def __init__(self, name: str = "GameEngine", min_level: LogLevel = LogLevel.INFO):
        """Initialize logger"""
        self.name = name
        self.min_level = min_level
        self.output_stream: TextIO = sys.stdout
        self.error_stream: TextIO = sys.stderr
        self.show_timestamps = True
        self.show_level = True
        self.show_logger_name = True
        
        # Color codes for terminal output
        self.colors = {
            LogLevel.DEBUG: '\033[90m',     # Gray
            LogLevel.INFO: '\033[94m',      # Blue
            LogLevel.WARNING: '\033[93m',   # Yellow
            LogLevel.ERROR: '\033[91m',     # Red
        }
        self.reset_color = '\033[0m'
        
    def set_level(self, level: LogLevel):
        """Set minimum logging level"""
        self.min_level = level
    
    def set_output_stream(self, stream: TextIO):
        """Set output stream for info/debug messages"""
        self.output_stream = stream
    
    def set_error_stream(self, stream: TextIO):
        """Set output stream for warning/error messages"""
        self.error_stream = stream
    
    def enable_colors(self, enabled: bool = True):
        """Enable or disable colored output"""
        if not enabled:
            for level in self.colors:
                self.colors[level] = ''
            self.reset_color = ''
    
    def _format_message(self, level: LogLevel, message: str) -> str:
        """Format a log message"""
        parts = []
        
        # Timestamp
        if self.show_timestamps:
            timestamp = time.strftime("%H:%M:%S", time.localtime())
            parts.append(f"[{timestamp}]")
        
        # Logger name
        if self.show_logger_name:
            parts.append(f"[{self.name}]")
        
        # Log level
        if self.show_level:
            level_name = level.name
            parts.append(f"[{level_name}]")
        
        # Message
        formatted = " ".join(parts) + f" {message}"
        
        # Add color
        color = self.colors.get(level, '')
        return f"{color}{formatted}{self.reset_color}"
    
    def _should_log(self, level: LogLevel) -> bool:
        """Check if message should be logged based on level"""
        return level.value >= self.min_level.value
    
    def _write_message(self, level: LogLevel, message: str):
        """Write message to appropriate stream"""
        if not self._should_log(level):
            return
        
        formatted = self._format_message(level, message)
        
        # Use error stream for warnings and errors
        if level in (LogLevel.WARNING, LogLevel.ERROR):
            stream = self.error_stream
        else:
            stream = self.output_stream
        
        stream.write(formatted + '\n')
        stream.flush()
    
    def debug(self, message: str):
        """Log debug message"""
        self._write_message(LogLevel.DEBUG, message)
    
    def info(self, message: str):
        """Log info message"""
        self._write_message(LogLevel.INFO, message)
    
    def warning(self, message: str):
        """Log warning message"""
        self._write_message(LogLevel.WARNING, message)
    
    def error(self, message: str):
        """Log error message"""
        self._write_message(LogLevel.ERROR, message)
    
    def log(self, level: LogLevel, message: str):
        """Log message at specified level"""
        self._write_message(level, message)


class LoggerManager:
    """Manages multiple loggers for different systems"""
    
    def __init__(self):
        """Initialize logger manager"""
        self.loggers = {}
        self.default_level = LogLevel.INFO
        
        # Create default engine logger
        self.engine_logger = Logger("Engine", self.default_level)
        self.loggers["Engine"] = self.engine_logger
    
    def get_logger(self, name: str) -> Logger:
        """Get or create a logger with the given name"""
        if name not in self.loggers:
            self.loggers[name] = Logger(name, self.default_level)
        return self.loggers[name]
    
    def set_global_level(self, level: LogLevel):
        """Set logging level for all loggers"""
        self.default_level = level
        for logger in self.loggers.values():
            logger.set_level(level)
    
    def enable_colors_globally(self, enabled: bool = True):
        """Enable or disable colors for all loggers"""
        for logger in self.loggers.values():
            logger.enable_colors(enabled)
    
    def configure_timestamps(self, enabled: bool = True):
        """Enable or disable timestamps for all loggers"""
        for logger in self.loggers.values():
            logger.show_timestamps = enabled


# Global logger manager instance
_logger_manager = LoggerManager()

def get_logger(name: str = "Engine") -> Logger:
    """Get a logger instance"""
    return _logger_manager.get_logger(name)

def set_global_log_level(level: LogLevel):
    """Set global logging level"""
    _logger_manager.set_global_level(level)

def enable_colors(enabled: bool = True):
    """Enable or disable colored logging globally"""
    _logger_manager.enable_colors_globally(enabled)

def configure_timestamps(enabled: bool = True):
    """Enable or disable timestamps globally"""
    _logger_manager.configure_timestamps(enabled)
