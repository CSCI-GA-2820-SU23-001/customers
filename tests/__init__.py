# """
# Test initialization of the database

# """

# from unittest.mock import patch
# from unittest import TestCase
# import logging
# from service import models, app


# ######################################################################
# #  Customer   M O D E L   I N I T   T E S T
# ######################################################################
# class TestDBInit(TestCase):
#     """ Test Cases for Customer Model Initialization"""
#     @patch.object(models, 'init_db')
#     @patch.object(app.logger, 'critical')
#     def test_db_init_error(self, mock_critical, mock_init_db):
#         """Test DB initialization error handling"""
#         mock_init_db.side_effect = AssertionError("DB error")  # Make init_db raise an exception
#         try:
#             models.init_db(app)
#         except AssertionError as error:
#             mock_critical.assert_called_once_with("%s: Cannot continue", error)
