import os
import logging
from unittest import TestCase
from unittest.mock import MagicMock, patch
from service import app
from service.models import db, init_db, Customer
from service.common import status  # HTTP Status Codes
from tests.factories import CustomerFactory
from service.common import log_handlers

class TestLogging(TestCase):
    def test_logging_format(self):
        """Test that log messages get formatted as expected"""
        log_msg = "This is a test log message"
        app.logger.info(log_msg)

        with open('path_to_your_log_file.log', 'r') as log_file:
            log_file_content = log_file.read()

        self.assertIn(log_msg, log_file_content)
        # Further checks could be added here to test the format of the log message
