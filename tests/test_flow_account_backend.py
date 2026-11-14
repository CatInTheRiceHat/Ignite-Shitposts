"""Account summaries marked as the retired Labs backend must not generate."""
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from google_flow import FlowClient


class AccountBackendTests(unittest.TestCase):
    def test_legacy_backend_is_not_selected(self):
        with patch.dict('os.environ',{'USEAPI_TOKEN':'test-token'}):
            client=FlowClient()
        with patch.object(client,'request',return_value={'legacy@example.com':{'health':'OK','backend':'labs'}}) as request:
            with self.assertRaisesRegex(RuntimeError,'healthy'):
                client.healthy_account()
            request.assert_called_once_with('GET','/accounts')

    def test_explicit_legacy_backend_is_rejected(self):
        with patch.dict('os.environ',{'USEAPI_TOKEN':'test-token'}):
            client=FlowClient()
        with patch.object(client,'request',return_value={'legacy@example.com':{'health':'OK','backend':'labs'}}):
            with self.assertRaisesRegex(RuntimeError,'unhealthy'):
                client.healthy_account('legacy@example.com')


if __name__=='__main__':
    unittest.main()
