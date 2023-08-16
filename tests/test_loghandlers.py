import unittest
from unittest.mock import patch, Mock
from service.common import log_handlers
from flask import Flask
import logging

class LogHandlersTests(unittest.TestCase):
    def setUp(self):
        """Runs before every test"""
        self.app = Flask(__name__)
        self.app.logger = Mock()  # Modify this line to mock the entire logger object
        self.app.logger.handlers = []

    @patch('logging.getLogger')
    @patch('logging.Formatter', autospec=True)
    def test_init_logging(self, mock_formatter_class, mock_get_logger):
        """Test that log handlers are properly set"""

        # Mock the gunicorn logger to simulate its behavior
        mock_gunicorn_logger = Mock(spec=logging.Logger)
        mock_handler1 = Mock(spec=logging.Handler)
        mock_handler2 = Mock(spec=logging.Handler)
        mock_gunicorn_logger.handlers = [mock_handler1, mock_handler2]
        mock_gunicorn_logger.level = logging.INFO  # This line should work now since we're mocking the app.logger object
        mock_get_logger.return_value = mock_gunicorn_logger

        # Mock the formatter
        mock_formatter = Mock(spec=logging.Formatter)
        mock_formatter_class.return_value = mock_formatter

        # Call the function
        log_handlers.init_logging(self.app, "mock-logger-name")

        # Assert the formatter was created with the right format string
        mock_formatter_class.assert_called_once_with("[%(asctime)s] [%(levelname)s] [%(module)s] %(message)s", "%Y-%m-%d %H:%M:%S %z")

        # Assert that the format has been set for both handlers
        mock_handler1.setFormatter.assert_called_once_with(mock_formatter)
        mock_handler2.setFormatter.assert_called_once_with(mock_formatter)

if __name__ == "__main__":
    unittest.main()

