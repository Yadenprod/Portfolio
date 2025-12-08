$(document).ready(function() {
	$(document).on('click', 'a i.fa-trash', function() {
		return confirm('Вы уверены, что хотите выполнить это действие?');
	})
});