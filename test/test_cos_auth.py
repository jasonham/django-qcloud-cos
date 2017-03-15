from qcloudcos import cos_auth
import unittest


class cos_auth_TestCase(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.get_xml_api = cos_auth.Auth(
            appid='125000000',
            SecretID='QmFzZTY0IGlzIGEgZ2VuZXJp',
            SecretKey='AKIDZfbOA78asKUYBcXFrJD0a1ICvR98JM',
            bucket='testbucket',
            region='cn-north',
            method='get',
            objectName='/testfile',
            head="Range:bytes=0-3",
            sign_time="1480932292",
            key_time="1481012292"
        )
        self.put_xml_api = cos_auth.Auth(
            appid='125000000',
            SecretID='QmFzZTY0IGlzIGEgZ2VuZXJp',
            SecretKey='AKIDZfbOA78asKUYBcXFrJD0a1ICvR98JM',
            bucket='testbucket',
            region='cn-north',
            method='put',
            objectName='/testfile2',
            head="x-cos-content-sha1:db8ac1c259eb89d4a131b253bacfca5f319d54f2&x-cos-stroage-class:nearline",
            sign_time="1480932292",
            key_time="1481012292"
        )

    def test_get_xml_api_SignKey(self):
        self.assertEqual(self.get_xml_api.get_signkey(),'95d110a8ead64cac52083100db75b7e3f369e72f')

    def test_get_xml_api_FormatString(self):
        b = "get\n/testfile\n\nhost=testbucket-125000000.cn-north.myqcloud.com&range=bytes%3d0-3\n"
        self.assertEqual(self.get_xml_api.get_formatstring(),b
                         )

    def test_get_xml_api_StringToSign(self):
        a = self.get_xml_api.get_stringtosign()
        b = 'sha1\n1480932292;1481012292\nc92f7246e3f922fe4abae5d6d5ebcd2397dc88cb\n'
        self.assertEqual(a,b)

    def test_get_xml_api_Signature(self):
        a = self.get_xml_api.get_signature()
        b = '29b2f454bb9d8a629e7cad61227bd5fd0dd11a2d'
        self.assertEqual(a, b)

    def test_get_xml_api_Authorization(self):
        a = self.get_xml_api.get_authorization()
        b = 'q-sign-algorithm=sha1&q-ak=QmFzZTY0IGlzIGEgZ2VuZXJp&q-sign-time=1480932292;1481012292&q-key-time=1480932292;1481012292&q-header-list=host;range&q-url-param-list=&q-signature=29b2f454bb9d8a629e7cad61227bd5fd0dd11a2d'
        self.assertEqual(
            a,
            b
        )



    def test_put_xml_api_Authorization(self):
        a = self.put_xml_api.get_authorization()
        b = 'q-sign-algorithm=sha1&q-ak=QmFzZTY0IGlzIGEgZ2VuZXJp&q-sign-time=1480932292;1481012292&q-key-time=1480932292;1481012292&q-header-list=host;x-cos-content-sha1;x-cos-stroage-class&q-url-param-list=&q-signature=b237c36c5495b048519b82b17a200840594c0339'
        self.assertEqual(
            a,
            b
        )
    #     self.multi = cos_auth.Auth(appid='200001',
    #                            SecretID='AKIDUfLUEUigQiXqm7CVSspKJnuaiIKtxqAv',
    #                            SecretKey='bLcPnl88WU30VY57ipRhSePfPdOfSruK',
    #                            bucket='newbucket',
    #                            file='',
    #                            currentTime=1437995644,
    #                            expiredTime=1437995704,
    #                            rand=2081660421)
    #     self.once = cos_auth.Auth(appid='200001',
    #                                SecretID='AKIDUfLUEUigQiXqm7CVSspKJnuaiIKtxqAv',
    #                                SecretKey='bLcPnl88WU30VY57ipRhSePfPdOfSruK',
    #                                bucket='newbucket',
    #                                file='tencent_test.jpg',
    #                                currentTime=1437995644,
    #                                expiredTime=1437995704,
    #                                rand=2081660421)
    #
    #
    # def test_multi_effect_original(self):
    #     self.assertEqual(
    #         self.multi.get_original(),
    #         'a=200001&b=newbucket&k=AKIDUfLUEUigQiXqm7CVSspKJnuaiIKtxqAv&e=1437995704&t=1437995644&r=2081660421&f='
    #     )
    #
    # def test_multi_effect_signature(self):
    #     self.assertEqual(
    #         self.multi.get_sign(),
    #         'wHgvVkXpcZ3d+G0rOkAJml3R5NdhPTIwMDAwMSZiPW5ld2J1Y2tldCZrPUFLSURVZkxVRVVpZ1FpWHFtN0NWU3NwS0pudWFpSUt0eHFBdiZlPTE0Mzc5OTU3MDQmdD0xNDM3OTk1NjQ0JnI9MjA4MTY2MDQyMSZmPQ=='
    #     )
    #
    # def test_once_original(self):
    #     self.assertEqual(
    #         self.once.get_original(),
    #         'a=200001&b=newbucket&k=AKIDUfLUEUigQiXqm7CVSspKJnuaiIKtxqAv&e=0&t=1437995644&r=2081660421&f=/200001/newbucket/tencent_test.jpg'
    #     )
    #
    # def test_once_signature(self):
    #     self.assertEqual(
    #         self.once.get_sign(),
    #         'rUbXBVKcp4tdZKkm5wz6//DqLIdhPTIwMDAwMSZiPW5ld2J1Y2tldCZrPUFLSURVZkxVRVVpZ1FpWHFtN0NWU3NwS0pudWFpSUt0eHFBdiZlPTAmdD0xNDM3OTk1NjQ0JnI9MjA4MTY2MDQyMSZmPS8yMDAwMDEvbmV3YnVja2V0L3RlbmNlbnRfdGVzdC5qcGc='
    #     )
    #

    def tearDown(self):
        self.auth=None


if __name__ == '__main__':
    unittest.main()


