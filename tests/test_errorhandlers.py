import os
import logging
from unittest import TestCase
from unittest.mock import MagicMock, patch
from service import app
from service.models import db, init_db, Customer
from service.common import status  # HTTP Status Codes
from tests.factories import CustomerFactory
from service.common import error_handlers


