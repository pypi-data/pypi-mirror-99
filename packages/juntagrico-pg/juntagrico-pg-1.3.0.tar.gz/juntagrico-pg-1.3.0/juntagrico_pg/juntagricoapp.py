from juntagrico.util import addons

import juntagrico_pg

addons.config.register_admin_menu('jpg/menu.html')
addons.config.register_version(juntagrico_pg.name, juntagrico_pg.version)
