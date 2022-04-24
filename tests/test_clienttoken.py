import os, sys
currDir = os.path.dirname(os.path.realpath(__file__))
rootDir = os.path.abspath(os.path.join(currDir, '..'))
if rootDir not in sys.path: # add parent dir to paths
    sys.path.append(rootDir)
from modules.clienttoken import ClientToken
import time
import unittest

class TestUser(unittest.TestCase):

    def test_is_expired_when_token_is_expired(self):
        auth_token = "atoken"
        auth_rtoken = "rtoken"
        expires_in = 1
        t = ClientToken(auth_token, auth_rtoken, expires_in)
        time.sleep(2)
        expired = t.is_expired()
        self.assertTrue(expired)

    def test_is_expired_when_token_is_not_expired(self):
        auth_token = "atoken"
        auth_rtoken = "rtoken"
        expires_in = 100
        t = ClientToken(auth_token, auth_rtoken, expires_in)
        time.sleep(1)
        expired = t.is_expired()
        self.assertFalse(expired)
    
    def test_is_refreshable_when_token_is_refreshable(self):
        auth_token = "atoken"
        auth_rtoken = "rtoken"
        expires_in = 1
        t = ClientToken(auth_token, auth_rtoken, expires_in)
        time.sleep(1)
        refreshable = t.is_refreshable()
        self.assertTrue(refreshable)
    
    def test_is_refreshable_when_token_is_not_refreshable(self):
        auth_token = "atoken"
        auth_rtoken = "rtoken"
        expires_in = 6000
        t = ClientToken(auth_token, auth_rtoken, expires_in)
        refreshable = t.is_refreshable()
        self.assertFalse(refreshable)

if __name__ == '__main__':
    unittest.main()