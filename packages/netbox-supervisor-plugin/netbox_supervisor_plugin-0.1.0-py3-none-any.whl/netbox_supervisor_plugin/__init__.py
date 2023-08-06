from extras.plugins import PluginConfig


class SupervisorConfig(PluginConfig):
    """This class defines attributes for the NetBox Virtual Circuit Plugin."""

    name = 'netbox_supervisor_plugin'
    verbose_name = 'Supervisors'
    description = 'Netbox Supervisor Plugin'
    version = '0.1'
    base_url = 'supervisor'
    author = 'Zakharov Ilya'
    author_email = 'axe-ska@bk.ru'
    required_settings = []
    default_settings = {}
    caching_config = {}


config = SupervisorConfig
