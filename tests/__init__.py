from unittest.mock import patch
from service import models, app
import logging
from unittest import TestCase


class TestDBInit(TestCase):
    @patch.object(models, 'init_db')
    @patch.object(app.logger, 'critical')
    def test_db_init_error(self, mock_critical, mock_init_db):
        """Test DB initialization error handling"""
        mock_init_db.side_effect = Exception("DB error")  # Make init_db raise an exception
        try:
            models.init_db(app)
        except Exception as error:
            mock_critical.assert_called_once_with("%s: Cannot continue", error)
