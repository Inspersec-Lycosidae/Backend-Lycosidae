# logger.py
import logging
import re
from datetime import datetime

"""

Sistema de logging personalizado para o Dashboard

"""

class BracketLevelFormatter(logging.Formatter):
    """

    Formatter that shows: "YYYY-MM-DD HH:MM:SS | [LEVEL] Message"
    with colors for INFO, WARNING, ERROR and CRITICAL.

    """

    COLOR_RESET = "\033[0m"
    COLORS = {
        logging.DEBUG: "\033[35m",      # Magenta
        logging.INFO: "\033[36m",       # Cyan
        logging.WARNING: "\033[33m",    # Yellow
        logging.ERROR: "\033[31m",      # Red
        logging.CRITICAL: "\033[1;31m"  # Bright Red
    }
    
    # Link's color (green)
    LINK_COLOR = "\033[32m"

    def __init__(self, fmt=None, datefmt=None, use_color=True):
        super().__init__(fmt=fmt, datefmt=datefmt)
        self.use_color = use_color

    def format(self, record: logging.LogRecord) -> str:
        level_tag = f"[{record.levelname}]"
        if self.use_color:
            color = self.COLORS.get(record.levelno)
            if color:
                level_tag = f"{color}{level_tag}{self.COLOR_RESET}"
        
        # Process message to color links
        if self.use_color:
            record.msg = self._colorize_links(str(record.msg))
        
        # Injeta campo customizado para uso no fmt
        setattr(record, "levelname_br", level_tag)
        return super().format(record)
    
    def _colorize_links(self, message: str) -> str:
        """
        
        Color links (http/https) on messages
        
        """
        url_pattern = r'https?://[^\s]+'
        
        def replace_url(match):
            url = match.group(0)
            return f"{self.LINK_COLOR}{url}{self.COLOR_RESET}"
        
        # Substituir URLs encontradas
        colored_message = re.sub(url_pattern, replace_url, message)
        return colored_message

def setup_logging(level: int = logging.INFO) -> logging.Logger:
    """
    
    Cofigure global logging with standardized formatter and colors
    
    """
    root = logging.getLogger()

    # Avoid duped handlers on hot-reload
    if root.handlers:
        for h in list(root.handlers):
            root.removeHandler(h)

    handler = logging.StreamHandler()
    formatter = BracketLevelFormatter(
        fmt="%(levelname_br)s | %(asctime)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        use_color=True,
    )
    handler.setFormatter(formatter)
    handler.setLevel(level)

    root.setLevel(level)
    root.addHandler(handler)

    # Reduce verbose from external libraries
    logging.getLogger('apscheduler').setLevel(logging.WARNING)
    logging.getLogger('apscheduler.executors.default').setLevel(logging.WARNING)

    return root

def get_logger(name: str) -> logging.Logger:
    """
    
    Retorn a configured logger to the specified module
    
    """
    return logging.getLogger(name) 