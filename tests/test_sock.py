# -*- coding: utf-8 -
#
# This file is part of gunicorn released under the MIT license.
# See the NOTICE for more information.

try:
    import unittest.mock as mock
except ImportError:
    import mock

from gunicorn import sock


@mock.patch('os.unlink')
def test_close_sockets(unlink):
    listener1 = mock.Mock()
    listener1.getsockname.return_value = ('127.0.0.1', '80')
    listener2 = mock.Mock()
    listener2.getsockname.return_value = '/var/run/test.sock'
    sock.close_sockets([listener1, listener2])
    listener1.close.assert_called_with()
    listener2.close.assert_called_with()
    unlink.assert_called_once_with('/var/run/test.sock')


@mock.patch('os.unlink')
def test_close_sockets_without_unlink(unlink):
    listener1 = mock.Mock()
    listener1.getsockname.return_value = '/var/run/test.sock'
    sock.close_sockets([listener1], False)
    listener1.close.assert_called_with()
    assert not unlink.called, 'unlink should not have been called'
