# -*- coding: utf-8 -*-

"""
Test for cmemcache module.
Gijsbert de Haan <gijsbert.de.haan@gmail.com>
http://gijsbert.org/cmemcache/index.html
Based on revision 283
"""

from __future__ import print_function
from Testing import ZopeTestCase

import os
import signal
import socket
import subprocess


# -----------------------------------------------------------------------------------------
#
def to_s(val):
    """
    Convert val to string.
    """
    if not isinstance(val, str):
        return "%s (%s)" % (val, type(val))
    return val


# -----------------------------------------------------------------------------------------
#
def test_setget(mc, key, val, checkf):
    """
    test set and get in one go
    """
    mc.set(key, val)
    newval = mc.get(key)
    checkf(val, newval)


# -------------------------------------------------------------------------------
#
class TestCmemcache(ZopeTestCase.ZopeTestCase):

    servers = ["127.0.0.1:11211"]
    servers_unknown = ["127.0.0.1:52345"]
    servers_weighted = [("127.0.0.1:11211", 2)]

    def _test_cmemcache(self, mcm):
        """
        Test cmemcache specifics.
        """
        mc = mcm.StringClient(self.servers)
        mc.set("blo", "blu", 0, 12)
        self.assertEqual(mc.get("blo"), "blu")
        self.assertEqual(mc.getflags("blo"), ("blu", 12))

        self.assertEqual(mc.incr("nonexistantnumber"), None)
        self.assertEqual(mc.decr("nonexistantnumber"), None)

        # try weird server formats
        # number is not a server
        with self.assertRaises(TypeError):
            mc.set_servers([12])
        # forget port
        with self.assertRaises(TypeError):
            mc.set_servers(["12"])

    def _test_memcache(self, mcm):
        """
        Test memcache specifics.
        """
        mc = mcm.Client(self.servers)
        mc.set("blo", "blu")
        self.assertEqual(mc.get("blo"), "blu")
        with self.assertRaises(ValueError):
            mc.decr("nonexistantnumber")
        with self.assertRaises(ValueError):
            mc.incr("nonexistantnumber")

    def _test_sgra(self, mc, val, repval, norepval, ok):
        """
        Test set, get, replace, add api.
        """
        self.assertEqual(mc.set("blo", val), ok)
        self.assertEqual(mc.get("blo"), val)
        mc.replace("blo", repval)
        self.assertEqual(mc.get("blo"), repval)
        mc.add("blo", norepval)
        self.assertEqual(mc.get("blo"), repval)

        mc.delete("blo")
        self.assertEqual(mc.get("blo"), None)
        mc.replace("blo", norepval)
        self.assertEqual(mc.get("blo"), None)
        mc.add("blo", repval)
        self.assertEqual(mc.get("blo"), repval)

    def _test_base(self, mcm, mc, ok):
        """
        The base test, uses string values only.

        The return codes are not compatible between memcache and cmemcache.  memcache
        return 1 for any reply from memcached, and cmemcache returns the return code
        returned by memcached.

        Actually the return codes from libmemcache for replace and add do not seem to be
        logical either. So ignore them and tests through get() if the appropriate action
        was done.

        """

        print("testing", mc, "\n\tfrom", mcm)

        self._test_sgra(mc, "blu", "replace", "will not be set", ok)

        mc.delete("blo")
        self.assertEqual(mc.get("blo"), None)

        mc.set("number", "5")
        self.assertEqual(mc.get("number"), "5")
        self.assertEqual(mc.incr("number", 3), 8)
        self.assertEqual(mc.decr("number", 2), 6)
        self.assertEqual(mc.get("number"), "6")
        self.assertEqual(mc.incr("number"), 7)
        self.assertEqual(mc.decr("number"), 6)

        mc.set("blo", "bli")
        self.assertEqual(mc.get("blo"), "bli")
        d = mc.get_multi(["blo", "number", "doesnotexist"])
        self.assertEqual(d, {"blo": "bli", "number": "6"})

        # make sure zero delimitation characters are ignored in values.
        test_setget(mc, "blabla", "bli\000bli", self.assertEqual)

        # get stats
        stats = mc.get_stats()
        self.assertEqual(len(stats), 1)
        self.assertTrue(self.servers[0] in stats[0][0])
        self.assertTrue("total_items" in stats[0][1])
        self.assertTrue("bytes_read" in stats[0][1])
        self.assertTrue("bytes_written" in stats[0][1])

        # set_servers to none
        mc.set_servers([])
        try:
            # memcache does not support the 0 server case
            mc.set("bli", "bla")
        except ZeroDivisionError:
            pass
        else:
            self.assertEqual(mc.get("bli"), None)

        # set unknown server
        # mc.set_servers(self.servers_unknown)
        # test_setget(mc, 'bla', 'bli', self.assertFalseEqual)

        # set servers with weight syntax
        mc.set_servers(self.servers_weighted)
        test_setget(mc, "bla", "bli", self.assertEqual)
        test_setget(mc, "blo", "blu", self.assertEqual)

        # set servers again
        mc.set_servers(self.servers)
        test_setget(mc, "bla", "bli", self.assertEqual)
        test_setget(mc, "blo", "blu", self.assertEqual)

        # test unicode
        test_setget(mc, "blo", "© 2006", self.assertEqual)

        # flush_all
        # fixme: how to test this?
        # fixme: after doing flush_all() one can not start new Client(), do not know why
        # since I know no good way to test it we ignore it for now
        # mc.flush_all()

        mc.disconnect_all()

    def _test_client(self, mcm, ok):
        """
        Test Client, only need to test the set, get, add, replace, rest is
        implemented by test_memcache().
        """
        mc = mcm.Client(self.servers)

        self._test_sgra(mc, "blu", "replace", "will not be set", ok)

        val = {"bla": "bli", "blo": 12}
        repval = {"bla": "blo", "blo": 12}
        norepval = {"blo": 12}
        self._test_sgra(mc, val, repval, norepval, ok)

    def test_memcache(self):
        # quick check if memcached is running
        ip, port = self.servers[0].split(":")
        print("ip", ip, "port", port)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        memcached = None
        try:
            s.connect((ip, int(port)))
        except socket.error as e:
            # not running, start one
            memcached = subprocess.Popen("memcached -m 10", shell=True)
            print("memcached not running, starting one (pid %d)" % (memcached.pid,))
            # give it some time to start
            import time

            time.sleep(0.5)
        s.close()

        # use memcache as the reference
        try:
            from Products.MemcachedManager.tests import memcache
        except ImportError:
            pass
        else:
            self._test_memcache(memcache)
            self._test_base(memcache, memcache.Client(self.servers), ok=1)
            self._test_client(memcache, ok=1)

        # test extension
        try:
            from cmemcache import StringClient  # Only in cmemcache

            del StringClient
            import cmemcache
        except ImportError:
            pass
        else:
            self._test_cmemcache(cmemcache)
            self._test_base(cmemcache, cmemcache.StringClient(self.servers), ok=0)
            self._test_base(cmemcache, cmemcache.Client(self.servers), ok=0)
            self._test_client(cmemcache, ok=0)

        # if we created memcached for our test, then shut it down
        if memcached:
            os.kill(memcached.pid, signal.SIGINT)


def test_suite():
    from unittest import makeSuite
    from unittest import TestSuite

    suite = TestSuite()
    suite.addTest(makeSuite(TestCmemcache))
    return suite
