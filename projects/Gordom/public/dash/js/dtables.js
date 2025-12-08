"use strict";
function getFormattedDate(today) 
{
    // var week = new Array('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday');
    // var day  = week[today.getDay()];
    var dd   = today.getDate();
    var mm   = today.getMonth()+1; //January is 0!
    var yyyy = today.getFullYear();
    var hour = today.getHours();
    var minu = today.getMinutes();
	var sec = today.getSeconds();

    if(dd<10)  { dd='0'+dd } 
    if(mm<10)  { mm='0'+mm } 
    if(minu<10){ minu='0'+minu } 
	if(sec<10){ sec='0'+sec } 
    return dd+'-'+mm+'-'+yyyy+' '+hour+':'+minu+':'+sec;
}
var KTDatatablesData = function() {

	var users = function() {
		var table = $('#users');

		table.DataTable({
			responsive: true,
			searchDelay: 500,
			processing: true,
			serverSide: true,
			ajax: {
				url: "/admin/load",
				type: "POST",
				data: {
					type: 'users'
				}
			},
			columns: [
				{ data: "id", searchable: true },
				{ data: "username", searchable: true, orderable: false,
					render: function (data, type, row) {
						return '<a href="/admin/users/edit/' + row.id + '" target="_blank">' + data + '</a>';
					}
				},
				{ data: "balance", searchable: false,
					render: function (data, type, row) {
						return data.toFixed(2) + ' р.';
					}
				},
				{
					data: null, searchable: false, orderable: false,
					render: function (data, type, row) {
						return '<a href="https://vk.com/id' + row.vk_id + '" target="_blank">Перейти</a>'
					}
				},
				{ data: "is_admin", searchable: true, orderable: true,
					render: function (data, type, row) {
						var privilege = "";
						if(row.is_admin) privilege += '<span class="kt-badge kt-badge--unified-danger kt-badge--inline kt-badge--pill">Администратор</span>';
						if(row.is_youtuber) privilege += '<span class="kt-badge kt-badge--unified-warning kt-badge--inline kt-badge--pill">Ютубер</span>';
						if(row.is_worker) privilege += '<span class="kt-badge kt-badge--unified-success kt-badge--inline kt-badge--pill">Сотрудник</span>';
						if(row.is_bot) privilege += '<span class="kt-badge kt-badge--unified-brand kt-badge--inline kt-badge--pill">Бот</span>';
						if(privilege.length == 0) privilege += '<span class="kt-badge kt-badge--unified-primary kt-badge--inline kt-badge--pill">Пользователь</span>';
						return privilege;
					}
				},
				{ data: "created_ip", searchable: true, orderable: false },
				{ data: "used_ip", searchable: true, orderable: false },
				{ 
					data: "ban", searchable: true, orderable: true,
					render: function (data, type, row) {
						return row.ban 
							? '<span class="kt-badge kt-badge--danger kt-badge--inline kt-badge--pill">Да</span>'
							: '<span class="kt-badge kt-badge--success kt-badge--inline kt-badge--pill">Нет</span>'
					}
				},
				{ data: null, searchable: false, orderable: false,
					render: function (data, type, row) {
						return '<a href="/admin/users/edit/'+ row.id +'" class="btn btn-sm btn-clean btn-icon btn-icon-md" title="Редактировать"><i class="la la-edit"></i></a>';
					}
				}
			],
			"language": {
				  "processing": "Подождите...",
				  "search": "Поиск:",
				  "lengthMenu": "Показать _MENU_ записей",
				  "info": "Записи с _START_ по _END_ из _TOTAL_ записей",
				  "infoEmpty": "Записи с 0 до 0 из 0 записей",
				  "infoFiltered": "(отфильтровано из _MAX_ записей)",
				  "infoPostFix": "",
				  "loadingRecords": "Загрузка записей...",
				  "zeroRecords": "Записи отсутствуют.",
				  "emptyTable": "В таблице отсутствуют данные",
				  "paginate": {
					"first": "Первая",
					"previous": "Предыдущая",
					"next": "Следующая",
					"last": "Последняя"
				  },
				  "aria": {
					"sortAscending": ": активировать для сортировки столбца по возрастанию",
					"sortDescending": ": активировать для сортировки столбца по убыванию"
				  }
			}
		});
	};

	var bots = function() {
		var table = $('#bots');

		table.DataTable({
			responsive: true,
			searchDelay: 500,
			processing: true,
			serverSide: true,
			ajax: {
				url: "/admin/load",
				type: "POST",
				data: {
					type: 'bots'
				}
			},
			columns: [
				{ data: "id", searchable: true },
				{ data: "username", searchable: true },
				{ data: null, searchable: false, orderable: false,
					render: function (data, type, row) {
						return '\
						<a href="/admin/bots/edit/'+ row.id +'" class="btn btn-sm btn-clean btn-icon btn-icon-md" title="Редактировать"><i class="la la-edit"></i></a>\
						<a href="/admin/bots/delete/'+ row.id +'" class="btn btn-sm btn-clean btn-icon btn-icon-md" title="Удалить"><i class="la la-trash"></i></a>\
						';
					}
				}
			],
			"language": {
				  "processing": "Подождите...",
				  "search": "Поиск:",
				  "lengthMenu": "Показать _MENU_ записей",
				  "info": "Записи с _START_ по _END_ из _TOTAL_ записей",
				  "infoEmpty": "Записи с 0 до 0 из 0 записей",
				  "infoFiltered": "(отфильтровано из _MAX_ записей)",
				  "infoPostFix": "",
				  "loadingRecords": "Загрузка записей...",
				  "zeroRecords": "Записи отсутствуют.",
				  "emptyTable": "В таблице отсутствуют данные",
				  "paginate": {
					"first": "Первая",
					"previous": "Предыдущая",
					"next": "Следующая",
					"last": "Последняя"
				  },
				  "aria": {
					"sortAscending": ": активировать для сортировки столбца по возрастанию",
					"sortDescending": ": активировать для сортировки столбца по убыванию"
				  }
			}
		});
	};

	var promocodes = function() {
		var table = $('#promocodes');

		table.DataTable({
			responsive: true,
			searchDelay: 500,
			processing: true,
			serverSide: true,
			ajax: {
				url: "/admin/load",
				type: "POST",
				data: {
					type: 'promocodes'
				}
			},
			columns: [
				{ data: "id", searchable: true },
				{ data: "name", searchable: true },
				{ data: "sum", searchable: true },
				{ data: "activation", searchable: true },
				{ data: null, searchable: true, 
					render: function (data, type, row) {
						return Number(row.activation) - Number(row.activated);
					}
				},
				{ data: "type", searchable: true, 
					render: function (data, type, row) {
						return data == 'balance' ? 'Баланс' : 'Депозит';
					}
				},
				{ data: null, searchable: false, orderable: false,
					render: function (data, type, row) {
						return '<a href="/admin/promocodes/delete/'+ row.id +'" class="btn btn-sm btn-clean btn-icon btn-icon-md" title="Удалить"><i class="la la-trash"></i></a>';
					}
				}
			],
			"language": {
				  "processing": "Подождите...",
				  "search": "Поиск:",
				  "lengthMenu": "Показать _MENU_ записей",
				  "info": "Записи с _START_ по _END_ из _TOTAL_ записей",
				  "infoEmpty": "Записи с 0 до 0 из 0 записей",
				  "infoFiltered": "(отфильтровано из _MAX_ записей)",
				  "infoPostFix": "",
				  "loadingRecords": "Загрузка записей...",
				  "zeroRecords": "Записи отсутствуют.",
				  "emptyTable": "В таблице отсутствуют данные",
				  "paginate": {
					"first": "Первая",
					"previous": "Предыдущая",
					"next": "Следующая",
					"last": "Последняя"
				  },
				  "aria": {
					"sortAscending": ": активировать для сортировки столбца по возрастанию",
					"sortDescending": ": активировать для сортировки столбца по убыванию"
				  }
			}
		});
	};

	var bonuses = function() {
		var table = $('#bonuses');

		table.DataTable({
			responsive: true,
			searchDelay: 500,
			processing: true,
			serverSide: true,
			ajax: {
				url: "/admin/load",
				type: "POST",
				data: {
					type: 'bonus'
				}
			},
			columns: [
				{ data: "id", searchable: true },
				{ data: "title", searchable: true },
				{ data: "goal", searchable: true },
				{ data: "reward", searchable: true },
				{ data: "background", searchable: true,
					render: function (data, type, row) {
						return `${data} <div style="min-height:18px;border-radius:999;background: ${data}"></div>`
					}
				},
				{ data: null, searchable: false, orderable: false,
					render: function (data, type, row) {
						return '\
						<a href="/admin/bonus/delete/'+ row.id +'" class="btn btn-sm btn-clean btn-icon btn-icon-md" title="Удалить"><i class="la la-trash"></i></a>\
						';
					}
				}
			],
			"language": {
				  "processing": "Подождите...",
				  "search": "Поиск:",
				  "lengthMenu": "Показать _MENU_ записей",
				  "info": "Записи с _START_ по _END_ из _TOTAL_ записей",
				  "infoEmpty": "Записи с 0 до 0 из 0 записей",
				  "infoFiltered": "(отфильтровано из _MAX_ записей)",
				  "infoPostFix": "",
				  "loadingRecords": "Загрузка записей...",
				  "zeroRecords": "Записи отсутствуют.",
				  "emptyTable": "В таблице отсутствуют данные",
				  "paginate": {
					"first": "Первая",
					"previous": "Предыдущая",
					"next": "Следующая",
					"last": "Последняя"
				  },
				  "aria": {
					"sortAscending": ": активировать для сортировки столбца по возрастанию",
					"sortDescending": ": активировать для сортировки столбца по убыванию"
				  }
			}
		});
	};

	var active_withdraws = function() {
		var table = $('#active_withdraws');

		table.DataTable({
			responsive: true,
			searchDelay: 500,
			processing: true,
			serverSide: true,
			ajax: {
				url: "/admin/load",
				type: "POST",
				data: {
					type: 'withdraws',
					status: 0
				}
			},
			columns: [
				{ data: "id", searchable: true },
				{ data: "username", searchable: true,
					render: function (data, type, row) {
						return '<a href="/admin/users/edit/' + row.user_id + '" target="_blank">' + data + '</a>';
					}
				},
				{ data: "sum", searchable: false },
				{ data: "wallet", searchable: true, orderable: false },
				{ data: "system", searchable: true, orderable: false, 
					render: function(data, type, row) {
						return `<img style="width: 92px!important" src="/assets/image/${data}.png">`
					} 
				},
				{ data: "created_at", searchable: true, orderable: true,
					render: function (data, type, row) {
						return getFormattedDate(new Date(data))
					}
				},
				{ data: null, searchable: false, orderable: false,
					render: function (data, type, row) {
						return `
							<a href="javascript://" onclick="acceptWithdraw(${row.id})" class="btn btn-sm btn-success btn-sm btn-icon btn-icon-md" title="Подтвердить"><i class="la la-send"></i></a>
							<a href="javascript://" onclick="declineWithdraw(${row.id})" class="btn btn-sm btn-danger btn-sm btn-icon btn-icon-md" title="Удалить"><i class="la la-trash"></i></a>
							<a href="javascript://" onclick="multiChecker(${row.user_id})" class="btn btn-sm btn-primary btn-sm btn-icon btn-icon-md" title="Инфо"><i class="la la-info"></i></a>
						`;
					}
				}
			],
			"language": {
				  "processing": "Подождите...",
				  "search": "Поиск:",
				  "lengthMenu": "Показать _MENU_ записей",
				  "info": "Записи с _START_ по _END_ из _TOTAL_ записей",
				  "infoEmpty": "Записи с 0 до 0 из 0 записей",
				  "infoFiltered": "(отфильтровано из _MAX_ записей)",
				  "infoPostFix": "",
				  "loadingRecords": "Загрузка записей...",
				  "zeroRecords": "Записи отсутствуют.",
				  "emptyTable": "В таблице отсутствуют данные",
				  "paginate": {
					"first": "Первая",
					"previous": "Предыдущая",
					"next": "Следующая",
					"last": "Последняя"
				  },
				  "aria": {
					"sortAscending": ": активировать для сортировки столбца по возрастанию",
					"sortDescending": ": активировать для сортировки столбца по убыванию"
				  }
			}
		});
	};

	var process_withdraws = function() {
		var table = $('#process_withdraws');

		table.DataTable({
			responsive: true,
			searchDelay: 500,
			processing: true,
			serverSide: true,
			ajax: {
				url: "/admin/load",
				type: "POST",
				data: {
					type: 'withdraws',
					status: 3
				}
			},
			columns: [
				{ data: "id", searchable: true },
				{ data: "username", searchable: true,
					render: function (data, type, row) {
						return '<a href="/admin/users/edit/' + row.user_id + '" target="_blank">' + data + '</a>';
					}
				},
				{ data: "sum", searchable: false },
				{ data: "wallet", searchable: true, orderable: false },
				{ data: "system", searchable: true, orderable: false, 
					render: function(data, type, row) {
						return `<img style="width: 92px!important" src="/assets/image/${data}.png">`
					} 
				},
				{ data: "created_at", searchable: true, orderable: true,
					render: function (data, type, row) {
						return getFormattedDate(new Date(data))
					}
				},
			],
			"language": {
				  "processing": "Подождите...",
				  "search": "Поиск:",
				  "lengthMenu": "Показать _MENU_ записей",
				  "info": "Записи с _START_ по _END_ из _TOTAL_ записей",
				  "infoEmpty": "Записи с 0 до 0 из 0 записей",
				  "infoFiltered": "(отфильтровано из _MAX_ записей)",
				  "infoPostFix": "",
				  "loadingRecords": "Загрузка записей...",
				  "zeroRecords": "Записи отсутствуют.",
				  "emptyTable": "В таблице отсутствуют данные",
				  "paginate": {
					"first": "Первая",
					"previous": "Предыдущая",
					"next": "Следующая",
					"last": "Последняя"
				  },
				  "aria": {
					"sortAscending": ": активировать для сортировки столбца по возрастанию",
					"sortDescending": ": активировать для сортировки столбца по убыванию"
				  }
			}
		});
	};

	var sended_withdraws = function() {
		var table = $('#sended_withdraws');

		table.DataTable({
			responsive: true,
			searchDelay: 500,
			processing: true,
			serverSide: true,
			ajax: {
				url: "/admin/load",
				type: "POST",
				data: {
					type: 'withdraws',
					status: 1
				}
			},
			columns: [
				{ data: "id", searchable: true },
				{ data: "username", searchable: true,
					render: function (data, type, row) {
						return '<a href="/admin/users/edit/' + row.user_id + '" target="_blank">' + data + '</a>';
					}
				},
				{ data: "sum", searchable: false },
				{ data: "wallet", searchable: true, orderable: false },
				{ data: "system", searchable: true, orderable: false, 
					render: function(data, type, row) {
						return `<img style="width: 92px!important" src="/assets/image/${data}.png">`
					} 
				},
				{ data: "created_at", searchable: true, orderable: true,
					render: function (data, type, row) {
						return getFormattedDate(new Date(data))
					}
				},
			],
			"language": {
				  "processing": "Подождите...",
				  "search": "Поиск:",
				  "lengthMenu": "Показать _MENU_ записей",
				  "info": "Записи с _START_ по _END_ из _TOTAL_ записей",
				  "infoEmpty": "Записи с 0 до 0 из 0 записей",
				  "infoFiltered": "(отфильтровано из _MAX_ записей)",
				  "infoPostFix": "",
				  "loadingRecords": "Загрузка записей...",
				  "zeroRecords": "Записи отсутствуют.",
				  "emptyTable": "В таблице отсутствуют данные",
				  "paginate": {
					"first": "Первая",
					"previous": "Предыдущая",
					"next": "Следующая",
					"last": "Последняя"
				  },
				  "aria": {
					"sortAscending": ": активировать для сортировки столбца по возрастанию",
					"sortDescending": ": активировать для сортировки столбца по убыванию"
				  }
			}
		});
	};

	var deposits = function() {
		var table = $('#deposits');

		table.DataTable({
			responsive: true,
			searchDelay: 500,
			processing: true,
			serverSide: true,
			ajax: {
				url: "/admin/load",
				type: "POST",
				data: {
					type: 'deposits'
				}
			},
			columns: [
				{ data: "id", searchable: true },
				{ data: "username", searchable: true,
					render: function (data, type, row) {
						return '<a href="/admin/users/edit/' + row.user_id + '" target="_blank">' + data + '</a>';
					}
				},
				{ data: "sum", searchable: false },
				{ data: "bonus", searchable: true, orderable: false },
				{ data: "created_at", searchable: true, orderable: true,
					render: function (data, type, row) {
						return getFormattedDate(new Date(data))
					}
				},
			],
			"language": {
				  "processing": "Подождите...",
				  "search": "Поиск:",
				  "lengthMenu": "Показать _MENU_ записей",
				  "info": "Записи с _START_ по _END_ из _TOTAL_ записей",
				  "infoEmpty": "Записи с 0 до 0 из 0 записей",
				  "infoFiltered": "(отфильтровано из _MAX_ записей)",
				  "infoPostFix": "",
				  "loadingRecords": "Загрузка записей...",
				  "zeroRecords": "Записи отсутствуют.",
				  "emptyTable": "В таблице отсутствуют данные",
				  "paginate": {
					"first": "Первая",
					"previous": "Предыдущая",
					"next": "Следующая",
					"last": "Последняя"
				  },
				  "aria": {
					"sortAscending": ": активировать для сортировки столбца по возрастанию",
					"sortDescending": ": активировать для сортировки столбца по убыванию"
				  }
			}
		});
	};


	var initTable1 = function() {
		var table = $('#dtable');

		// begin first table
		table.DataTable({
			responsive: true,
			searchDelay: 500,
			"language": {
				  "processing": "Подождите...",
				  "search": "Поиск:",
				  "lengthMenu": "Показать _MENU_ записей",
				  "info": "Записи с _START_ по _END_ из _TOTAL_ записей",
				  "infoEmpty": "Записи с 0 до 0 из 0 записей",
				  "infoFiltered": "(отфильтровано из _MAX_ записей)",
				  "infoPostFix": "",
				  "loadingRecords": "Загрузка записей...",
				  "zeroRecords": "Записи отсутствуют.",
				  "emptyTable": "В таблице отсутствуют данные",
				  "paginate": {
					"first": "Первая",
					"previous": "Предыдущая",
					"next": "Следующая",
					"last": "Последняя"
				  },
				  "aria": {
					"sortAscending": ": активировать для сортировки столбца по возрастанию",
					"sortDescending": ": активировать для сортировки столбца по убыванию"
				  }
			}
		});
	};

	var initTable2 = function() {
		var table = $('#dtable2');

		// begin first table
		table.DataTable({
			responsive: true,
			searchDelay: 500,
			"language": {
				  "processing": "Подождите...",
				  "search": "Поиск:",
				  "lengthMenu": "Показать _MENU_ записей",
				  "info": "Записи с _START_ по _END_ из _TOTAL_ записей",
				  "infoEmpty": "Записи с 0 до 0 из 0 записей",
				  "infoFiltered": "(отфильтровано из _MAX_ записей)",
				  "infoPostFix": "",
				  "loadingRecords": "Загрузка записей...",
				  "zeroRecords": "Записи отсутствуют.",
				  "emptyTable": "В таблице отсутствуют данные",
				  "paginate": {
					"first": "Первая",
					"previous": "Предыдущая",
					"next": "Следующая",
					"last": "Последняя"
				  },
				  "aria": {
					"sortAscending": ": активировать для сортировки столбца по возрастанию",
					"sortDescending": ": активировать для сортировки столбца по убыванию"
				  }
			}
		});
	};

	var initTable3 = function() {
		var table = $('#dtable3');

		// begin first table
		table.DataTable({
			responsive: true,
			searchDelay: 500,
			"language": {
				  "processing": "Подождите...",
				  "search": "Поиск:",
				  "lengthMenu": "Показать _MENU_ записей",
				  "info": "Записи с _START_ по _END_ из _TOTAL_ записей",
				  "infoEmpty": "Записи с 0 до 0 из 0 записей",
				  "infoFiltered": "(отфильтровано из _MAX_ записей)",
				  "infoPostFix": "",
				  "loadingRecords": "Загрузка записей...",
				  "zeroRecords": "Записи отсутствуют.",
				  "emptyTable": "В таблице отсутствуют данные",
				  "paginate": {
					"first": "Первая",
					"previous": "Предыдущая",
					"next": "Следующая",
					"last": "Последняя"
				  },
				  "aria": {
					"sortAscending": ": активировать для сортировки столбца по возрастанию",
					"sortDescending": ": активировать для сортировки столбца по убыванию"
				  }
			}
		});
	};

	return {
		init: function() {
			users();
			bots();
			promocodes();
			bonuses();
			active_withdraws();
			process_withdraws();
			sended_withdraws();
			deposits();
			initTable1();
			initTable2();
			initTable3();
		},

	};

}();

jQuery(document).ready(function() {
	KTDatatablesData.init();
});