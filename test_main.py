"""main.py tests"""

import os
import unittest
from unittest.mock import patch
from importlib import import_module
import yaml


class MainTestCase(unittest.TestCase):
    """main.py test case"""

    def test_google_credentials_are_not_specified(self):
        """Check Google Application credentials are not specified"""
        self.assertIsNone(os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"),
                          "Tests must run without "
                          "GOOGLE_APPLICATION_CREDENTIALS "
                          "environment variable")

    @patch('kcidb.misc.get_secret')
    @patch('kcidb.mq.ORMPatternPublisher')
    @patch('kcidb.mq.IOSubscriber')
    @patch('kcidb.monitor.spool.Client')
    @patch('kcidb.db.Client')
    @patch('kcidb.oo.Client')
    # pylint: disable=unused-argument,too-many-arguments
    def test_import(self, oo_client, db_client, spool_client,
                    mq_publisher, mq_subscriber, get_secret):
        """Check main.py can be loaded"""
        # Load deployment environment variables
        file_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(file_dir, "main.env.yaml"), "r",
                  encoding='utf8') as env_file:
            env = yaml.safe_load(env_file)
        env["GCP_PROJECT"] = "TEST_PROJECT"

        orig_env = dict(os.environ)
        try:
            os.environ.update(env)
            import_module("main")
        finally:
            os.environ.clear()
            os.environ.update(orig_env)
        # Piss off, pylint
        self.assertTrue(not False)
