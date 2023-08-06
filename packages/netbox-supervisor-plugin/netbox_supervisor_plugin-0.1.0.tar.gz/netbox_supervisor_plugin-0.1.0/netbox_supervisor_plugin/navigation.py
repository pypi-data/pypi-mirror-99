from extras.plugins import PluginMenuButton, PluginMenuItem
from utilities.choices import ButtonColorChoices


menu_items = (
    PluginMenuItem(
        link='plugins:netbox_supervisor_plugin:supervisor_list',
        link_text='Ответственные',
        permissions=['netbox_supervisor_plugin.view_supervisor'],
        buttons=(
            PluginMenuButton(
                link='plugins:netbox_supervisor_plugin:supervisor_add',
                title='Add a new supervisor',
                icon_class='mdi mdi-plus-thick',
                color=ButtonColorChoices.GREEN,
                permissions=['netbox_supervisor_plugin.add_supervisor']
            ),
        )
    ),
    PluginMenuItem(
        link='plugins:netbox_supervisor_plugin:supervisor_tenant_list',
        link_text='Связи',
        permissions=['netbox_supervisor_plugin.view_supervisortenant'],
        buttons=(
            PluginMenuButton(
                link='plugins:netbox_supervisor_plugin:supervisor_tenant_add',
                title='Assign a Tenant to Supervisor',
                icon_class='mdi mdi-plus-thick',
                color=ButtonColorChoices.GREEN,
                permissions=['netbox_supervisor_plugin.add_supervisortenant']
            ),
        )
    ),
)
