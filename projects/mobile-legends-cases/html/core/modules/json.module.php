<?php
	function render_json($elem) {
		header('Content-Type: application/json');
		echo json_encode($elem);
		disable_render();
		wsexit();
	}
	
	function echo_json($elem) {
		render_json($elem);
	}
?>