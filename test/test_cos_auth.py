from QcloudCos import cos_auth
import unittest


class cos_auth_TestCase(unittest.TestCase):
    def setUp(self):
        self.multi = cos_auth.Auth(appid='200001',
                               SecretID='AKIDUfLUEUigQiXqm7CVSspKJnuaiIKtxqAv',
                               SecretKey='bLcPnl88WU30VY57ipRhSePfPdOfSruK',
                               bucket='newbucket',
                               file='',
                               currentTime=1437995644,
                               expiredTime=1437995704,
                               rand=2081660421)

    def test_multi_effect_original(self):
        self.assertEqual(
            self.multi.get_original(),
            'a=200001&b=newbucket&k=AKIDUfLUEUigQiXqm7CVSspKJnuaiIKtxqAv&e=1437995704&t=1437995644&r=2081660421&f='
        )

    def test_multi_effect_signature(self):
        self.assertEqual(
            self.multi.get_sign(),
            'wHgvVkXpcZ3d+G0rOkAJml3R5NdhPTIwMDAwMSZiPW5ld2J1Y2tldCZrPUFLSURVZkxVRVVpZ1FpWHFtN0NWU3NwS0pudWFpSUt0eHFBdiZlPTE0Mzc5OTU3MDQmdD0xNDM3OTk1NjQ0JnI9MjA4MTY2MDQyMSZmPQ=='
        )

    def tearDown(self):
        self.auth=None


if __name__ == '__main__':
    unittest.main()

