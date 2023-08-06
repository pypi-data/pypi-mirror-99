from unittest import TestCase
from mock import patch
from nose.tools import raises
import os, glob, logging


class TestProfile(TestCase):

    # Remove *.log files before each test
    @classmethod
    def setup_class(cls):
        for filename in os.listdir(os.curdir):
            if filename.endswith('.log'):
                os.remove(filename)

    @raises(AttributeError)
    def test_profile_with_wrong_appid_1(self):
        from eikon.Profile import get_profile, set_app_key
        get_profile().set_app_key([])

    @raises(AttributeError)
    def test_profile_with_wrong_appid_2(self):
        from eikon.Profile import get_profile, set_app_key
        get_profile().set_app_key({'a': 'b'})

    @raises(AttributeError)
    def test_profile_with_wrong_appid_3(self):
        from eikon.Profile import get_profile, set_app_key
        get_profile().set_app_key(12345)

    @patch('os.path.exists')
    @patch('eikon.Profile.read_firstline_in_file')
    @patch('eikon.Profile.check_port')
    def test_get_scripting_proxy_port(self, mock_check_port, read_firstline_in_file, mock_os_path_exits):
        from eikon.Profile import identify_scripting_proxy_port
        mock_os_path_exits.return_value = True

        from requests_async import Session
        session = Session()

        # test when .portInUse file is empty or doesn't exist
        read_firstline_in_file.return_value = ''
        mock_check_port.return_value = False
        self.assertEqual(None, identify_scripting_proxy_port(session, 'app_key'))

        # test when .portInUse file exists, contains validated '123' port number
        read_firstline_in_file.return_value = '123'
        mock_check_port.return_value = True
        self.assertEqual('123', identify_scripting_proxy_port(session, 'app_key'))

        # test when .portInUse file exists, contains '123' port number, but Proxy is listening on 9000 port
        read_firstline_in_file.return_value = '123'
        def fake_check_port(session, application_key, port, timeout=1.0):
            return True if port == '9000' else False
        mock_check_port.side_effect = fake_check_port
        result = identify_scripting_proxy_port(session, 'app_key')
        self.assertEqual('9000', result)

        # test when .portInUse file is empty or doesn't exist and Proxy is listening on 36036 port
        read_firstline_in_file.return_value = ''
        def fake_check_port(session, application_key, port, timeout=1.0):
            return True if port == '36036' else False
        mock_check_port.side_effect = fake_check_port
        self.assertEqual('36036', identify_scripting_proxy_port(session, 'app_key'))

    def test_log_path(self):
        import logging
        import glob

        # clean old pyeikon.*.log files in TEMP directory
        file_pattern = os.path.join(os.environ.get('TEMP'), 'pyeikon*.log')
        for filename in glob.glob(file_pattern):
            os.remove(filename)

        # check no pyeikon.*.log file is in TEMP directory
        self.assertFalse(glob.glob(file_pattern))
        from eikon.Profile import Profile
        profile = Profile()
        profile.set_log_path(os.environ.get('TEMP'))
        profile.set_log_level(logging.INFO)
        profile.set_app_key('123')

        # check that a pyeikon.*.log was created
        self.assertTrue(glob.glob(file_pattern))

    def test_logger(self):
        import logging

        # clean old pyeikon.*.log files in current directory
        file_pattern = os.path.join(os.curdir, 'pyeikon*.log')
        for filename in glob.glob(file_pattern):
            os.remove(filename)

        # check that no pyeikon.*.log is in current directory
        filenames = os.listdir(os.curdir)
        self.assertFalse(any((filename.endswith('.log')) for filename in filenames))

        from eikon.Profile import Profile
        profile = Profile()
        profile.set_log_path(os.curdir)
        profile.set_log_level(logging.INFO)
        profile.set_app_key('123')

        # check that a pyeikon.*.log was created
        filenames = os.listdir(os.curdir)
        self.assertTrue(any((filename.endswith('.log')) for filename in filenames))
