<?php

function get_reviews($where = '', $order = '', $limit = '') {
	return review::get_reviews($where, $order, $limit);
}