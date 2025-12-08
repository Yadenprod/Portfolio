<?php

add_loader('modeupgarde_loader');

function modeupgarde_loader() {
	droppedItem::addItemStatus(DROPPED_ITEM_STATUS_UPGRADED, 'Апгрейд', 'default');
	droppedItem::addSourceInfoClass(DROPPED_ITEM_FROM_UPGRADE, upgradeItemDataSource::class);
	stats::addAditionalStat('count_upgrade', 'opencase_count_upgrades');
	stats::addAditionalUserStat('upgrade', 'get_user_count_upgrades');
}
