import threading
import os

from yandextank.common.util import get_test_path
from yandextank.core.tankcore import TankCore
from yandextank.core.tankworker import TankInfo
from yandextank.plugins.Telegraf import Plugin as TelegrafPlugin


class TestTelegrafPlugin(object):
    def test_plugin_configuration(self):
        """ testing telegraf plugin configuration """
        cfg = {
            'core': {'skip_generator_check': True},
            'telegraf': {
                'package': 'yandextank.plugins.Telegraf',
                'enabled': True,
                'ssh_key_path': '/some/path',
                'config': os.path.join(get_test_path(), 'yandextank/plugins/Telegraf/tests/telegraf_mon.xml')
            }
        }
        core = TankCore(cfg, threading.Event(), TankInfo({}))
        telegraf_plugin = core.get_plugin_of_type(TelegrafPlugin)
        telegraf_plugin.configure()
        assert telegraf_plugin.detected_conf == 'telegraf'
        assert telegraf_plugin.monitoring.ssh_key_path == '/some/path'

    def test_legacy_plugin_configuration(self):
        """ testing legacy plugin configuration, old-style monitoring """
        cfg = {
            'core': {'skip_generator_check': True},
            'monitoring': {
                'package': 'yandextank.plugins.Telegraf',
                'enabled': True,
                'config': os.path.join(get_test_path(), 'yandextank/plugins/Telegraf/tests/old_mon.xml')
            }
        }
        core = TankCore(cfg, threading.Event(), TankInfo({}))
        telegraf_plugin = core.get_plugin_of_type(TelegrafPlugin)
        telegraf_plugin.configure()
        assert telegraf_plugin.detected_conf == 'monitoring'
