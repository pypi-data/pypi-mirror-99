# Copyright (C) 2012-2021 by the Free Software Foundation, Inc.
#
# This file is part of GNU Mailman.
#
# GNU Mailman is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# GNU Mailman is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# GNU Mailman.  If not, see <https://www.gnu.org/licenses/>.

"""Test the message API."""

import sys
import unittest

from email import message_from_binary_file
from email.header import Header
from email.parser import FeedParser
from email.utils import _has_surrogates
from importlib_resources import path
from mailman.app.lifecycle import create_list
from mailman.email.message import Message, UserNotification
from mailman.testing.helpers import get_queue_messages
from mailman.testing.layers import ConfigLayer


class TestMessage(unittest.TestCase):
    """Test the message API."""

    layer = ConfigLayer

    def setUp(self):
        self._mlist = create_list('test@example.com')
        self._msg = UserNotification(
            'aperson@example.com',
            'test@example.com',
            'Something you need to know',
            'I needed to tell you this.')

    def test_one_precedence_header(self):
        # Ensure that when the original message already has a Precedence:
        # header, UserNotification.send(..., add_precedence=True, ...) does
        # not add a second header.
        self.assertEqual(self._msg['precedence'], None)
        self._msg['Precedence'] = 'omg wtf bbq'
        self._msg.send(self._mlist)
        items = get_queue_messages('virgin', expected_count=1)
        self.assertEqual(items[0].msg.get_all('precedence'),
                         ['omg wtf bbq'])

    def test_reduced_rfc_2369_headers(self):
        # Notifications should get reduced List-* headers.
        self._msg.send(self._mlist)
        items = get_queue_messages('virgin', expected_count=1)
        self.assertTrue(items[0].msgdata.get('reduced_list_headers'))


class TestMessageSubclass(unittest.TestCase):
    layer = ConfigLayer

    def test_i18n_filenames(self):
        parser = FeedParser(_factory=Message)
        parser.feed("""\
Message-ID: <blah@example.com>
Content-Type: multipart/mixed; boundary="------------050607040206050605060208"

This is a multi-part message in MIME format.
--------------050607040206050605060208
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: quoted-printable

Test message containing an attachment with an accented filename

--------------050607040206050605060208
Content-Disposition: attachment;
    filename*=UTF-8''d%C3%A9jeuner.txt

Test content
--------------050607040206050605060208--
""")
        msg = parser.close()
        attachment = msg.get_payload(1)
        try:
            filename = attachment.get_filename()
        except TypeError as error:
            self.fail(error)
        self.assertEqual(filename, u'd\xe9jeuner.txt')

    def test_senders_header_instances(self):
        msg = Message()
        msg['From'] = Header('test@example.com')
        # Make sure the senders property does not fail
        self.assertEqual(msg.senders, ['test@example.com'])

    def test_user_notification_bad_charset(self):
        msg = UserNotification(
            'aperson@example.com',
            'test@example.com',
            'Something you need to know',
            'Non-ascii text é.')
        self.assertEqual(msg.get_payload(), 'Non-ascii text ?.')

    def test_as_string_python_bug_27321(self):
        # Bug 27321 is fixed in Python 3.8.7rc1, 3.9.1rc1 and later.
        with path('mailman.email.tests.data', 'bad_email.eml') as email_path:
            with open(str(email_path), 'rb') as fp:
                msg = message_from_binary_file(fp, Message)
                fp.seek(0)
                text = fp.read().decode('ascii', 'replace')
        if (sys.version_info.minor == 8 and sys.hexversion >= 0x030807C1 or
                sys.hexversion >= 0x030901C1):
            self.assertEqual(msg.as_string(), """\
To: <test@example.com>
Subject: =?koi8-r?B?UF9AX/NfQ1/5X+xfS1/p?=
From: =?koi8-r?B?8sXL0sXB1MnXzs/FIMHHxc7U09TXzw==?=
Content-Type: text/plain; charset="koi8-r"
Message-Id: <20160614102505.9OFQ19L1C>
Content-Transfer-Encoding: base64

/vTvIPTh6+/lIPLl6+zh7e7h8SDy4fPz+ezr4T8K68HLz8ogz9TLzMnLINbEwdTYIM/UINzUz8fP
IM3F1M/EwSDQz8nTy8Egy8zJxc7Uz9c/Cg==
""")
        else:
            self.assertEqual(msg.as_string(), text)

    def test_as_string_python_bug_32330(self):
        with path('mailman.email.tests.data', 'bad_email_2.eml') as email_path:
            with open(str(email_path), 'rb') as fp:
                msg = message_from_binary_file(fp, Message)
                fp.seek(0)
                text = fp.read().decode('ascii', 'replace')
        self.assertEqual(msg.as_string(), text)

    def test_as_string_unicode_surrogates(self):
        with path('mailman.email.tests.data', 'bad_email_4.eml') as email_path:
            with open(str(email_path), 'rb') as fp:
                msg = message_from_binary_file(fp, Message)
        self.assertFalse(_has_surrogates(msg.as_string()))

    def test_bogus_content_charset(self):
        with path('mailman.email.tests.data', 'bad_email_3.eml') as email_path:
            with open(str(email_path), 'rb') as fp:
                msg = message_from_binary_file(fp, Message)
                fp.seek(0)
                text = fp.read().decode('ascii', 'replace')
        self.assertEqual(msg.as_string(), text)
