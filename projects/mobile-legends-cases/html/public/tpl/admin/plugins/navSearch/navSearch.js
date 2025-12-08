$('#navSearch').keyup(function() {
	$('#sideBarSearch').show().find('.treeview-menu').html('');
	if ($('#navSearch').val() != '') {
		$('#sideBarMenu').hide();
		$('#sideBarSearch').show();
		$('#sideBarMenu .treeview-menu li').each(function() {
			if ($(this).text().toLowerCase().indexOf($('#navSearch').val().toLowerCase().trim()) > -1) {
				let $clone = $(this).clone();
				$('#sideBarSearch').show().find('.treeview-menu').append($clone);
			}
		});
	} else {
		$('#sideBarMenu').show();
		$('#sideBarSearch').hide();
	}
	
});