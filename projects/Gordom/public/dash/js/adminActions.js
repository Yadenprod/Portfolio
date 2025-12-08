$(document).ready(function() {
	$.post('/admin/getMerchant', function(data) {
		$('#fkBal').text(data);
	});
	$(document).on('click', '.versionUpdate', function () {
		$.post('/admin/versionUpdate')
		.then(e => {
			if(e.success) {
				$.notify({
	                type: 'success',
	                message: e.msg
	            });
			}
		})
		.fail(() => {
			$.notify({
	            type: 'error',
	            message: 'Ошибка на стороне сервера'
	        });
		})
	})
});