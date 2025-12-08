$(document).on('click', '.invItem', function() {
	var checked = $(this).find('input').prop('checked');
	if (checked) {
		$(this).removeClass('checked');
		$(this).find('input').prop('checked', false);
	} else {
		$(this).addClass('checked');
		$(this).find('input').prop('checked', true);
	}
});