<?php

add_admin_dashboard('admin_dashboard_opencase');

function admin_dashboard_opencase() {
	$depositeContent = '
			<div class="box box-success">
				<div class="box-header with-border">
					<h3 class="box-title">Депозиты</h3>
				</div>
				<div class="box-body chart-responsive">
					<div class="chart" id="deposite-chart" style="height: 300px;"></div>
				</div>
			</div>
		';

	$depositeData = array();
	$depQuery = db()->query('SELECT sum(`sum`) as sm, DATE_FORMAT(`time_add`, \'%Y %m %d\') as dat FROM `opencase_deposite` GROUP BY dat ORDER BY dat DESC LIMIT 30');
	foreach ($depQuery as $dep) {
		$date = explode(' ', $dep['dat']);
		$date = $date[0] . '-' . $date[1] . '-' . $date[2];
		$depositeData[] = '{y: \'' . $date . '\', deposite: ' . $dep['sm'] . '}';
	}
	add_jscript('
			if ($("#deposite-chart").length) {
				var depLine = new Morris.Line({
				  element: \'deposite-chart\',
				  resize: true,
				  data: [
					' . implode(',', $depositeData) . '
				  ],
				  xkey: \'y\',
				  ykeys: [\'deposite\'],
				  labels: [\'Депозитов на сумму\'],
				  lineColors: [\'#00a65a\'],
				  hideHover: \'auto\'
				});
			}
		');

	$caseOpenContent = '
			<div class="box box-primary">
				<div class="box-header with-border">
					<h3 class="box-title">Открыто кейсов</h3>
				</div>
				<div class="box-body chart-responsive">
					<div class="chart" id="caseopen-chart" style="height: 300px;"></div>
				</div>
			</div>
		';

	$caseData = array();
	$caseQuery = db()->query('SELECT count(`id`) as coun, DATE_FORMAT(`time_open`, \'%Y %m %d\') as dat FROM `opencase_opencases` GROUP BY dat ORDER BY dat DESC LIMIT 30');
	foreach ($caseQuery as $cas) {
		$date = explode(' ', $cas['dat']);
		$date = $date[0] . '-' . $date[1] . '-' . $date[2];
		$caseData[] = '{y: \'' . $date . '\', cases: ' . $cas['coun'] . '}';
	}
	add_jscript('
			if ($("#caseopen-chart").length) {
				var caseLine = new Morris.Line({
				  element: \'caseopen-chart\',
				  resize: true,
				  data: [
					' . implode(',', $caseData) . '
				  ],
				  xkey: \'y\',
				  ykeys: [\'cases\'],
				  labels: [\'Открыто кейсов\'],
				  lineColors: [\'#3c8dbc\'],
				  hideHover: \'auto\'
				});
			}
		');

	$withDrowContent = '
			<div class="box box-danger">
				<div class="box-header with-border">
					<h3 class="box-title">Выводы</h3>
				</div>
				<div class="box-body chart-responsive">
					<div class="chart" id="withdraw-chart" style="height: 300px;"></div>
				</div>
			</div>
		';

	$drawData = array();
	$drawQuery = db()->query('SELECT sum(`price`) as sm, count(id) as cn, DATE_FORMAT(`time_drop`, \'%Y %m %d\') as dat FROM `opencase_droppeditems` where status = 2 GROUP BY dat ORDER BY dat DESC LIMIT 30');
	foreach ($drawQuery as $draw) {
		$date = explode(' ', $draw['dat']);
		$date = $date[0] . '-' . $date[1] . '-' . $date[2];
		$drawData[] = '{y: \'' . $date . '\', sum: ' . $draw['sm'] . ', count: ' . $draw['cn'] . '}';
	}
	add_jscript('
			if ($("#withdraw-chart").length) {
				var drawLine = new Morris.Line({
				  element: \'withdraw-chart\',
				  resize: true,
				  data: [
					' . implode(',', $drawData) . '
				  ],
				  xkey: \'y\',
				  ykeys: [\'sum\', \'count\'],
				  labels: [\'Сумма выводов\', \'Количество выводов\'],
				  lineColors: [\'#dd4b39\', \'#ecaa1d\'],
				  hideHover: \'auto\'
				});
			}
		');

	$profitContent = '
			<div class="box">
				<div class="box-header with-border">
					<h3 class="box-title">Профит</h3>
				</div>
				<div class="box-body chart-responsive">
					<div class="chart" id="profit-chart" style="height: 300px;"></div>
				</div>
			</div>
		';

	$profitArray = array();
	$profitData = array();
	foreach ($drawQuery as $draw) {
		$profitArray[$draw['dat']]['draw'] = $draw['sm'];
	}

	foreach ($depQuery as $dep) {
		$profitArray[$dep['dat']]['dep'] = $dep['sm'];
	}

	$tableData = [];
	foreach ($profitArray as $key => $profit) {
		$date = explode(' ', $key);
		$date = $date[0] . '-' . $date[1] . '-' . $date[2];
		$dep = (isset($profit['dep']) ? $profit['dep'] : 0);
		$draw = (isset($profit['draw']) ? $profit['draw'] : 0);
		$profitData[] = '{y: \'' . $date . '\', dep: ' . $dep . ', draw: ' . $draw . ', diff : ' . ($dep - $draw) . '}';
		$tableData[$date] = ['dep' => $dep, 'draw' => $draw];
	}

	add_jscript('
			if ($("#profit-chart").length) {
				var profitLine = new Morris.Line({
				  element: \'profit-chart\',
				  resize: true,
				  data: [
					' . implode(',', $profitData) . '
				  ],
				  xkey: \'y\',
				  ykeys: [\'diff\', \'draw\', \'dep\'],
				  labels: [\'Разница\', \'Сумма выводов\', \'Сумма Депозитов\'],
				  lineColors: [\'#3c8dbc\', \'#dd4b39\', \'#00a65a\'],
				  hideHover: \'auto\'
				});
			}
		');
	
	
	$tableContent = '<div class="box">
		<div class="box-body">
			<table class = "table table-bordered table-striped" id="FAQElements">
				<thead>
					<tr>
						<th>Дата</th>
						<th>Депозиты</th>
						<th>Выводы</th>
						<th>Разница</th>
					</tr>
				</thead>';
				foreach ($tableData as $date => $data) {
					$tableContent .= '<tr>
						<td>'.$date.'</td>
						<td>'.$data['dep'].'</td>
						<td>'.$data['draw'].'</td>
						<td>'.($data['dep'] - $data['draw']).'</td>';
				}
			$tableContent .= '<tbody>
				</tbody>
			</table>		
		</div>
	</div>';

	add_css(get_admin_template_folder() . '/plugins/morris/morris.css', 11);
	add_script('https://cdnjs.cloudflare.com/ajax/libs/raphael/2.1.0/raphael-min.js', 10, 'footer');
	add_script(get_admin_template_folder() . '/plugins/morris/morris.min.js', 10, 'footer');

	$dashboard = array(
		'position' => 1,
		'cols' => array(
			array(
				'size' => 'lg-6',
				'class' => '',
				'content' => $depositeContent
			),
			array(
				'size' => 'lg-6',
				'class' => '',
				'content' => $caseOpenContent
			),
			array(
				'size' => 'lg-6',
				'class' => '',
				'content' => $withDrowContent
			),
			array(
				'size' => 'lg-6',
				'class' => '',
				'content' => $profitContent
			),
			array(
				'size' => 'lg-12',
				'class' => '',
				'content' => $tableContent
			)
		)
	);
	return $dashboard;
}
