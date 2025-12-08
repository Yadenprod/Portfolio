<!DOCTYPE html>
<html>
	<head>
		<title><?php echo get_setval('site_name'); ?></title>
		<meta charset="utf-8">
		<meta name="viewport" content="width=1915, minimum-scale=0.1, maximum-scale=1.0">
		<meta name="description" content="<?php echo get_meta_des(); ?>">
		<meta name="keywords" content="<?php echo get_meta_key(); ?>">
		<link href="<?php the_template_folder(); ?>/css/style1.css" rel="stylesheet" type="text/css">
		<link href="<?php the_template_folder(); ?>/css/mobile1.css" rel="stylesheet" type="text/css">
		<?php $games = array('570' => 'Dota2', '730' => 'CS:GO', '252490' => 'Rust', 'ml_bang' => 'Mobile Legends Bang Bang'); ?>
		<script>
			var SITE_URL = '<?php echo get_site_url() ?>';
			var SITE_NAME = '<?php echo get_setval('site_name'); ?>';
			var GAME_NAME = '<?php echo $games[get_setval('opencase_gameid')]; ?>';
		</script>
		<script type="text/javascript" src="https://vk.com/js/api/openapi.js?168"></script>
<!--		<script type="text/javascript">
			VK.init({apiId: 0, onlyWidgets: true});
		</script>-->
	</head>
	<body>
		<div id="app">
			<header-layout></header-layout>
			<router-view></router-view>
			<footer-layout></footer-layout>
			<notifications position="top right"></notifications>
		</div>		
		<script src="<?php the_template_folder(); ?>/js/app.js?v=3" type="text/javascript"></script>
	</body>
</html>