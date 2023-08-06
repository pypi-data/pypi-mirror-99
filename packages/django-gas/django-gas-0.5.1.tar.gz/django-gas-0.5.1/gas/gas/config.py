from django.utils.translation import gettext_lazy as _

from gas.sites import site


site.register_role('staff', _('Users with access to gas control panel.'))
site.register_role('admins', _('Users with access to everithing inside control panel.'))

site.register_urls('', 'gas.gas.core.urls')

site.register_urls('users', 'gas.gas.users.urls')
site.register_menu(
    name='users',
    label=_("Users"),
    icon="",
    url="gas:user_list",
    roles=('admins',),
)
