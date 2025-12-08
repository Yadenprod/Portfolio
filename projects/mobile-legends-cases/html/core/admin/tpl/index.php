<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<title>Панель администрирования | <?php echo get_title();?></title>
		<meta content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no" name="viewport">
		<link rel="stylesheet" href="<?php echo get_admin_template_folder();?>/bootstrap/css/bootstrap.min.css">
		<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.5.0/css/font-awesome.min.css">
		<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/ionicons/2.0.1/css/ionicons.min.css">
		<link rel="stylesheet" href="<?php echo get_admin_template_folder();?>/dist/css/skins/_all-skins.min.css">
		<link rel="stylesheet" href="<?php echo get_admin_template_folder();?>/plugins/iCheck/flat/blue.css">
		<link rel="stylesheet" href="<?php echo get_admin_template_folder();?>/plugins/morris/morris.css">
		<link rel="stylesheet" href="<?php echo get_admin_template_folder();?>/plugins/jvectormap/jquery-jvectormap-1.2.2.css">
		<link rel="stylesheet" href="<?php echo get_admin_template_folder();?>/plugins/daterangepicker/daterangepicker.css">
		<link rel="stylesheet" href="<?php echo get_admin_template_folder();?>/plugins/bootstrap-wysihtml5/bootstrap3-wysihtml5.min.css">
		<link rel="stylesheet" href="<?php echo get_admin_template_folder();?>/plugins/datatables/dataTables.bootstrap.css">
		<link rel="stylesheet" href="<?php echo get_admin_template_folder();?>/plugins/iCheck/all.css">
		<link rel="stylesheet" href="<?php echo get_admin_template_folder();?>/plugins/datetimepicker/jquery.datetimepicker.min.css">
		<!--[if lt IE 9]>
		<script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>
		<script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
		<![endif]-->
		<?php head(); ?>
		<link rel="stylesheet" href="<?php echo get_admin_template_folder();?>/dist/css/AdminLTE.css">
	</head>
	<body class="hold-transition skin-black sidebar-mini">
		<div class="wrapper">
			<header class="main-header">
				<a href="<?php echo ADMINURL; ?>/" class="logo">
					<span class="logo-mini"><b>A</b>P</span>
					<span class="logo-lg"><b>Admin</b> Panel</span>
				</a>
				<nav class="navbar navbar-static-top">
					<a href="#" class="sidebar-toggle" data-toggle="offcanvas" role="button">
					<span class="sr-only">Переключение навигации</span>
					</a>
					<div class="navbar-custom-menu">
						<ul class="nav navbar-nav">
							<?php the_admin_navbar(); ?>
							<li class="dropdown user user-menu">
								<a href="#" class="dropdown-toggle" data-toggle="dropdown">
								<img src="<?php echo get_admin_template_folder();?>/dist/img/default-50x50.gif" class="user-image" alt="<?php echo get_admin_name(); ?>">
								<span class="hidden-xs"><?php echo get_admin_name(); ?></span>
								</a>
								<ul class="dropdown-menu">
									<li class="user-header">
										<img src="<?php echo get_admin_template_folder();?>/dist/img/default-50x50.gif" class="img-circle" alt="<?php echo get_admin_name(); ?>">
										<p>
											<?php echo get_admin_name(); ?>
											<small>Главный администратор</small>
										</p>
									</li>
									<li class="user-footer">
										<div class="pull-left">
											<a href="<?php echo ADMINURL; ?>/admins/" class="btn btn-default btn-flat">Профиль</a>
										</div>
										<div class="pull-right">
											<a href="<?php echo ADMINURL; ?>/logout/" class="btn btn-default btn-flat">Выход</a>
										</div>
									</li>
								</ul>
							</li>
						</ul>
					</div>
				</nav>
			</header>
			<aside class="main-sidebar">
				<section class="sidebar">
					<div class="user-panel">
						<div class="pull-left image">
							<img src="<?php echo get_admin_template_folder();?>/dist/img/default-50x50.gif" class="img-circle" alt="<?php echo get_admin_name(); ?>">
						</div>
						<div class="pull-left info">
							<p><?php echo get_admin_name(); ?></p>
							<a href="#"><i class="fa fa-circle text-success"></i> Online</a>
						</div>
					</div>
					<form action="#" method="get" class="sidebar-form">
						<div class="input-group">
							<input type="text" name="nav-search" id = "navSearch" class="form-control" placeholder="Поиск...">
							<span class="input-group-btn">
							<button type="submit" name="search" id="search-btn" class="btn btn-flat"><i class="fa fa-search"></i>
							</button>
							</span>
						</div>
					</form>
					<ul class="sidebar-menu" id = "sideBarMenu">
						<li class="header">Навигация</li>
						<?php echo get_admin_menu(); ?>
					</ul>
					<ul class="sidebar-menu" id = "sideBarSearch" style = "display: none;">
						<li class="header">Поиск</li>
						<li class="treeview active">
							<ul class="treeview-menu menu-open">
							</ul>
						</li>
					</ul>
				</section>
			</aside>
			<div class="content-wrapper">
				<section class="content-header">
					<h1>
						<?php echo get_title(); ?>
					</h1>
					<ol class="breadcrumb">
						<li><a href="<?php echo ADMINURL; ?>/dashboard/"><i class="fa fa-dashboard"></i> Главная</a></li>
						<?php breadcrumbs(); ?>
						<li class="active"><?php echo get_title();?></li>
					</ol>
				</section>
				<section class="content">
					<?php echo get_cms_msg(); ?>
					<?php echo get_content(); ?>
				</section>
			</div>
			<footer class="main-footer">
				<div class="pull-right hidden-xs">
					<b>Версия</b> <?php echo get_setval('cms_version'); ?>
				</div>
				<strong>&copy; 2019.</strong> Все права защищены.
			</footer>
			<div class="control-sidebar-bg"></div>
		</div>
		<script src="<?php echo get_admin_template_folder();?>/plugins/jQuery/jquery-2.2.3.min.js"></script>
		<script src="https://code.jquery.com/ui/1.11.4/jquery-ui.min.js"></script>
		<script>
			$.widget.bridge('uibutton', $.ui.button);
		</script>
		<script src="<?php echo get_admin_template_folder();?>/bootstrap/js/bootstrap.min.js"></script>
		<script src="https://cdnjs.cloudflare.com/ajax/libs/raphael/2.1.0/raphael-min.js"></script>
		<script src="<?php echo get_admin_template_folder();?>/plugins/morris/morris.min.js"></script>
		<script src="<?php echo get_admin_template_folder();?>/plugins/sparkline/jquery.sparkline.min.js"></script>
		<script src="<?php echo get_admin_template_folder();?>/plugins/jvectormap/jquery-jvectormap-1.2.2.min.js"></script>
		<script src="<?php echo get_admin_template_folder();?>/plugins/jvectormap/jquery-jvectormap-world-mill-en.js"></script>
		<script src="<?php echo get_admin_template_folder();?>/plugins/knob/jquery.knob.js"></script>
		<script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.11.2/moment.min.js"></script>
		<script src="<?php echo get_admin_template_folder();?>/plugins/daterangepicker/daterangepicker.js"></script>
		<script src="<?php echo get_admin_template_folder();?>/plugins/datepicker/bootstrap-datepicker.js"></script>
		<script src="<?php echo get_admin_template_folder();?>/plugins/bootstrap-wysihtml5/bootstrap3-wysihtml5.all.min.js"></script>
		<script src="<?php echo get_admin_template_folder();?>/plugins/slimScroll/jquery.slimscroll.min.js"></script>
		<script src="<?php echo get_admin_template_folder();?>/plugins/fastclick/fastclick.js"></script>
		<script src="<?php echo get_admin_template_folder();?>/dist/js/app.min.js"></script>
		<script src="<?php echo get_admin_template_folder();?>/dist/js/demo.js"></script>
		<script src="<?php echo get_admin_template_folder();?>/plugins/datatables/jquery.dataTables.min.js"></script>
		<script src="<?php echo get_admin_template_folder();?>/plugins/datatables/dataTables.bootstrap.min.js"></script>
		<script src="<?php echo get_admin_template_folder();?>/plugins/fastclick/fastclick.js"></script>
		<script src="<?php echo get_admin_template_folder();?>/plugins/iCheck/icheck.min.js"></script>
		<script src="<?php echo get_admin_template_folder();?>/plugins/navSearch/navSearch.js"></script>
		<script src="<?php echo get_admin_template_folder();?>/plugins/datetimepicker/jquery.datetimepicker.full.min.js"></script>
		<script>
			$('input[type="checkbox"].minimal, input[type="radio"].minimal').iCheck({
				checkboxClass: 'icheckbox_minimal-blue',
				radioClass: 'iradio_minimal-blue'
			});
		</script>
		<?php footer(); ?>
	</body>
</html>