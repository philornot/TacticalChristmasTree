"""
Moduł zapewniający spójne i czytelne logowanie w aplikacji
"""
import logging
import sys
from datetime import datetime
from enum import IntEnum
from logging.handlers import RotatingFileHandler
from pathlib import Path

import coloredlogs

# Stała przechowująca nazwę projektu
PROJECT_NAME: str = "TacticalChristmasTree"


class LogLevel(IntEnum):
    """Enumeration dla poziomów logowania"""
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


class NiceLogger:
    """
    Klasa zarządzająca logowaniem w aplikacji
    """

    def __init__(self, logger_name: str = PROJECT_NAME):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)

        # Utworzenie katalogu na logi w Dokumentach
        documents_path = Path.home() / "Documents" / PROJECT_NAME
        log_dir = documents_path / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)

        # Format logów
        self.log_format = (
            '%(asctime)s.%(msecs)03d | '
            '%(levelname)-8s | '
            '%(name)s | '
            '%(filename)s:%(lineno)d | '
            '%(message)s'
        )

        self.date_format = '%Y-%m-%d %H:%M:%S'

        # Konfiguracja formattera
        formatter = logging.Formatter(self.log_format, self.date_format)

        # Handler dla plików logów
        current_time = datetime.now().strftime('%d-%m-%Y_%H-%M')
        log_file = log_dir / f"{PROJECT_NAME}_{current_time}.log"

        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)

        # Handler dla konsoli
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)

        # Konfiguracja kolorowych logów w konsoli
        coloredlogs.install(
            level='DEBUG',
            logger=self.logger,
            fmt=self.log_format,
            datefmt=self.date_format,
            level_styles={
                'debug': {'color': 'white'},
                'info': {'color': 'green'},
                'warning': {'color': 'yellow', 'bold': True},
                'error': {'color': 'red', 'bold': True},
                'critical': {'color': 'red', 'bold': True, 'background': 'white'}
            },
            field_styles={
                'asctime': {'color': 'cyan'},
                'levelname': {'color': 'white', 'bold': True},
                'filename': {'color': 'magenta'},
                'name': {'color': 'blue'},
            }
        )

        # Dodanie handlerów do loggera
        self.logger.addHandler(file_handler)

    def get_logger(self) -> logging.Logger:
        """Zwraca skonfigurowany logger"""
        return self.logger


# Przykład użycia
if __name__ == "__main__":
    logger = NiceLogger().get_logger()

    logger.debug("To jest debug message")
    logger.info("Aplikacja została uruchomiona")
    logger.warning("Uwaga! To jest ostrzeżenie")
    logger.error("Wystąpił błąd!")
    logger.critical("Krytyczny błąd aplikacji!")
