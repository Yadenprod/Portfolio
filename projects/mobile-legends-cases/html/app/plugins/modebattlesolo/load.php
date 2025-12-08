<?php

add_loader('modebattle_loader');

const DROPPED_ITEM_FROM_BATTLE = -2;

function modebattle_loader() {
	droppedItem::addSourceInfoClass(DROPPED_ITEM_FROM_BATTLE, battleItemDataSource::class);
	stats::addAditionalStat('count_battles', 'opencase_count_battles');
	stats::addAditionalUserStat('battle', 'get_user_count_battles');
}
