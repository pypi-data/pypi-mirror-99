# -*- coding: utf-8 -*-
'''
    :codeauthor: :email:`Daniel Wallace <dwallace@saltstack.com`
'''

# Import python libs
from __future__ import absolute_import, print_function, unicode_literals
import os
import shutil
import tempfile

# Import Salt Testing libs
from tests.support.runtests import RUNTIME_VARS
from tests.support.unit import skipIf, TestCase
from tests.support.case import ShellCase
from tests.support.mock import patch, MagicMock, call

# Import Salt libs
import salt.client.ssh.client
import salt.config
import salt.roster
import salt.utils.files
import salt.utils.path
import salt.utils.thin
import salt.utils.yaml

from salt.client import ssh

ROSTER = '''
localhost:
  host: 127.0.0.1
  port: 2827
self:
  host: 0.0.0.0
  port: 42
'''


@skipIf(not salt.utils.path.which('ssh'), "No ssh binary found in path")
class SSHPasswordTests(ShellCase):
    def test_password_failure(self):
        '''
        Check password failures when trying to deploy keys
        '''
        opts = salt.config.client_config(self.get_config_file_path('master'))
        opts['list_hosts'] = False
        opts['argv'] = ['test.ping']
        opts['selected_target_option'] = 'glob'
        opts['tgt'] = 'localhost'
        opts['arg'] = []
        roster = os.path.join(self.config_dir, 'roster')
        handle_ssh_ret = [
            {'localhost': {'retcode': 255, 'stderr': u'Permission denied (publickey).\r\n', 'stdout': ''}},
        ]
        expected = {'localhost': 'Permission denied (publickey)'}
        display_output = MagicMock()
        with patch('salt.roster.get_roster_file', MagicMock(return_value=roster)), \
                patch('salt.client.ssh.SSH.handle_ssh', MagicMock(return_value=handle_ssh_ret)), \
                patch('salt.client.ssh.SSH.key_deploy', MagicMock(return_value=expected)), \
                patch('salt.output.display_output', display_output):
            client = ssh.SSH(opts)
            ret = next(client.run_iter())
            with self.assertRaises(SystemExit):
                client.run()
        display_output.assert_called_once_with(expected, 'nested', opts)
        self.assertIs(ret, handle_ssh_ret[0])


class SSHRosterDefaults(TestCase):
    def test_roster_defaults_flat(self):
        '''
        Test Roster Defaults on the flat roster
        '''
        tempdir = tempfile.mkdtemp(dir=RUNTIME_VARS.TMP)
        expected = {
            'self': {
                'host': '0.0.0.0',
                'user': 'daniel',
                'port': 42,
            },
            'localhost': {
                'host': '127.0.0.1',
                'user': 'daniel',
                'port': 2827,
            },
        }
        try:
            root_dir = os.path.join(tempdir, 'foo', 'bar')
            os.makedirs(root_dir)
            fpath = os.path.join(root_dir, 'config')
            with salt.utils.files.fopen(fpath, 'w') as fp_:
                fp_.write(
                    '''
                    roster_defaults:
                      user: daniel
                    '''
                )
            opts = salt.config.master_config(fpath)
            with patch('salt.roster.get_roster_file', MagicMock(return_value=ROSTER)):
                with patch('salt.template.compile_template', MagicMock(return_value=salt.utils.yaml.safe_load(ROSTER))):
                    roster = salt.roster.Roster(opts=opts)
                    self.assertEqual(roster.targets('*', 'glob'), expected)
        finally:
            if os.path.isdir(tempdir):
                shutil.rmtree(tempdir)


class SSHSingleTests(TestCase):
    def setUp(self):
        self.tmp_cachedir = tempfile.mkdtemp(dir=RUNTIME_VARS.TMP)

    def test_single_opts(self):
        ''' Sanity check for ssh.Single options
        '''
        argv = ['ssh.set_auth_key', 'root', 'hobn+amNAXSBTiOXEqlBjGB...rsa root@master']
        opts = {
            'argv': argv,
            '__role': 'master',
            'cachedir': self.tmp_cachedir,
            'extension_modules': os.path.join(self.tmp_cachedir, 'extmods'),
        }
        target = {
            'passwd': 'abc123',
            'ssh_options': None,
            'sudo': False,
            'identities_only': False,
            'host': 'login1',
            'user': 'root',
            'timeout': 65,
            'remote_port_forwards': None,
            'sudo_user': '',
            'port': '22',
            'priv': '/etc/salt/pki/master/ssh/salt-ssh.rsa'
        }

        single = ssh.Single(
                opts,
                opts['argv'],
                'localhost',
                mods={},
                fsclient=None,
                thin=salt.utils.thin.thin_path(opts['cachedir']),
                mine=False,
                **target)

        self.assertEqual(single.shell._ssh_opts(), '')
        self.assertEqual(single.shell._cmd_str('date +%s'), 'ssh login1 '
                         '-o KbdInteractiveAuthentication=no -o '
                         'PasswordAuthentication=yes -o ConnectTimeout=65 -o Port=22 '
                         '-o IdentityFile=/etc/salt/pki/master/ssh/salt-ssh.rsa '
                         '-o User=root  date +%s')


@skipIf(not salt.utils.path.which("ssh"), "No ssh binary found in path")
class SSHTests(ShellCase):
    def setUp(self):
        self.tmp_cachedir = tempfile.mkdtemp(dir=RUNTIME_VARS.TMP)

        self.argv = [
            "ssh.set_auth_key",
            "root",
            "hobn+amNAXSBTiOXEqlBjGB...rsa root@master",
        ]
        self.target = {
            "passwd": "abc123",
            "ssh_options": None,
            "sudo": False,
            "identities_only": False,
            "host": "login1",
            "user": "root",
            "timeout": 65,
            "remote_port_forwards": None,
            "sudo_user": "",
            "port": "22",
            "priv": "/etc/salt/pki/master/ssh/salt-ssh.rsa",
        }
        self.opts = salt.config.client_config(self.get_config_file_path("master"))
        self.opts["selected_target_option"] = "glob"

    def test_shim_cmd(self):
        """
        test Single.shim_cmd()
        """
        opts = {
            "argv": self.argv,
            "__role": "master",
            "cachedir": self.tmp_cachedir,
            "extension_modules": os.path.join(self.tmp_cachedir, "extmods"),
        }

        single = ssh.Single(
            opts,
            opts["argv"],
            "localhost",
            mods={},
            fsclient=None,
            thin=salt.utils.thin.thin_path(opts["cachedir"]),
            mine=False,
            winrm=False,
            tty=True,
            **self.target
        )
        exp_ret = ("Success", "", 0)
        mock_cmd = MagicMock(return_value=exp_ret)
        patch_cmd = patch("salt.client.ssh.shell.Shell.exec_cmd", mock_cmd)
        patch_send = patch("salt.client.ssh.shell.Shell.send", return_value=("", "", 0))
        patch_rand = patch("os.urandom", return_value=b"5\xd9l\xca\xc2\xff")
        with patch_cmd, patch_rand, patch_send:
            ret = single.shim_cmd(cmd_str="echo test")
            assert ret == exp_ret
            assert [
                call("/bin/sh '.35d96ccac2ff.py'"),
                call("rm '.35d96ccac2ff.py'"),
            ] == mock_cmd.call_args_list

    def test_extra_filerefs(self):
        """
        test "extra_filerefs" are not excluded from kwargs
        when preparing the SSH opts
        """
        opts = {
            "eauth": "auto",
            "username": "test",
            "password": "test",
            "client": "ssh",
            "tgt": "localhost",
            "fun": "test.ping",
            "ssh_port": 22,
            "extra_filerefs": "salt://foobar",
        }
        roster = os.path.join(RUNTIME_VARS.TMP_CONF_DIR, "roster")
        client = salt.client.ssh.client.SSHClient(
            mopts=self.opts, disable_custom_roster=True
        )
        with patch("salt.roster.get_roster_file", MagicMock(return_value=roster)):
            ssh_obj = client._prep_ssh(**opts)
            assert ssh_obj.opts.get("extra_filerefs", None) == "salt://foobar"

    def test_ssh_kwargs(self):
        """
        test all ssh kwargs are not excluded from kwargs
        when preparing the SSH opts
        """
        test_opts = (
            ("extra_filerefs", "salt://foobar", True),
            ("host", "testhost", False),
            ("ssh_user", "testuser", True),
            ("ssh_passwd", "testpasswd", True),
            ("ssh_port", 23, False),
            ("ssh_sudo", True, True),
            ("ssh_sudo_user", "sudouser", False),
            ("ssh_priv", "test_priv", True),
            ("ssh_priv_passwd", "sshpasswd", True),
            ("ssh_identities_only", True, True),
            ("ssh_remote_port_forwards", "test", True),
            ("ssh_options", ["test1", "test2"], True),
            ("ssh_max_procs", 2, True),
            ("ssh_askpass", True, True),
            ("ssh_key_deploy", True, True),
            ("ssh_update_roster", True, True),
            ("ssh_scan_ports", "test", True),
            ("ssh_scan_timeout", 1.0, True),
            ("ssh_timeout", 1, False),
            ("ssh_log_file", "/tmp/test", True),
            ("raw_shell", True, True),
            ("refresh_cache", True, True),
            ("roster", "/test", True),
            ("roster_file", "/test1", True),
            ("rosters", ["test1"], False),
            ("ignore_host_keys", True, True),
            ("min_extra_mods", "test", True),
            ("thin_extra_mods", "test1", True),
            ("verbose", True, True),
            ("static", True, True),
            ("ssh_wipe", True, True),
            ("rand_thin_dir", True, True),
            ("regen_thin", True, True),
            ("python2_bin", "python2", True),
            ("python3_bin", "python3", True),
            ("no_host_keys", True, True),
            ("saltfile", "/tmp/test", True),
            ("doesnotexist", None, False),
        )

        for test_opt in test_opts:
            opt_key = test_opt[0]
            opt_value = test_opt[1]
            # Is the kwarg in salt.utils.parsers?
            in_parser = test_opt[2]

            opts = {
                "eauth": "auto",
                "username": "test",
                "password": "test",
                "client": "ssh",
                "tgt": "localhost",
                "fun": "test.ping",
                opt_key: opt_value,
            }
            roster = os.path.join(RUNTIME_VARS.TMP_CONF_DIR, "roster")
            client = salt.client.ssh.client.SSHClient(
                mopts=self.opts, disable_custom_roster=True
            )

            if in_parser:
                ssh_kwargs = salt.utils.parsers.SaltSSHOptionParser().defaults
                self.assertIn(opt_key, ssh_kwargs)

            with patch("salt.roster.get_roster_file", MagicMock(return_value=roster)):
                with patch("salt.client.ssh.shell.gen_key", MagicMock(return_value="")):
                    ssh_obj = client._prep_ssh(**opts)
                    self.assertEqual(ssh_obj.opts.get(opt_key, None), opt_value)
