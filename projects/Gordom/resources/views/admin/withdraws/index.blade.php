@extends('admin/layout')

@section('content')
<script src="/dash/js/dtables.js?v={{time()}}" type="text/javascript"></script>
<div class="kt-subheader kt-grid__item" id="kt_subheader">
    <div class="kt-subheader__main">
        <h3 class="kt-subheader__title">Выплаты</h3>
    </div>
</div>

<div class="kt-content kt-grid__item kt-grid__item--fluid" id="kt_content">
    <div class="kt-portlet kt-portlet--mobile">
        <div class="kt-portlet__head kt-portlet__head--lg">
            <div class="kt-portlet__head-label">
                <span class="kt-portlet__head-icon">
                    <i class="kt-font-brand flaticon2-information"></i>
                </span>
                <h3 class="kt-portlet__head-title">
                    Активные
                </h3>
            </div>
        </div>
        <div class="kt-portlet__body">
            <table class="table table-striped- table-bordered table-hover table-checkable" id="active_withdraws">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Пользователь</th>
                        <th>Сумма</th>
                        <td>Кошелек</td>
                        <td>Система</td>
                        <td>Дата</td>
                        <th>Действие</th>
                    </tr>
                </thead>
            </table>
        </div>
    </div>
    <div class="kt-portlet kt-portlet--mobile">
        <div class="kt-portlet__head kt-portlet__head--lg">
            <div class="kt-portlet__head-label">
                <span class="kt-portlet__head-icon">
                    <i class="kt-font-brand flaticon2-information"></i>
                </span>
                <h3 class="kt-portlet__head-title">
                    В обработке
                </h3>
            </div>
        </div>
        <div class="kt-portlet__body">
            <table class="table table-striped- table-bordered table-hover table-checkable" id="process_withdraws">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Пользователь</th>
                        <th>Сумма</th>
                        <td>Кошелек</td>
                        <td>Система</td>
                        <td>Дата</td>
                    </tr>
                </thead>
            </table>
        </div>
    </div>
    <div class="kt-portlet kt-portlet--mobile">
        <div class="kt-portlet__head kt-portlet__head--lg">
            <div class="kt-portlet__head-label">
                <span class="kt-portlet__head-icon">
                    <i class="kt-font-brand flaticon2-information"></i>
                </span>
                <h3 class="kt-portlet__head-title">
                    Отправленные
                </h3>
            </div>
        </div>
        <div class="kt-portlet__body">
            <table class="table table-striped- table-bordered table-hover table-checkable" id="sended_withdraws">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Пользователь</th>
                        <th>Сумма</th>
                        <td>Кошелек</td>
                        <td>Система</td>
                        <td>Дата</td>
                    </tr>
                </thead>
            </table>
        </div>
    </div>
</div>
<div class="modal fade" id="declineWithdrawModal" tabindex="-1" role="dialog" aria-labelledby="newLabel" style="display: none;" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered" role="document">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="exampleModalLongTitle">Отмена выплаты</h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close"></button>
            </div>
            <form class="kt-form-new" action="#" id="save">
                <div class="modal-body">
                    <div class="form-group">
                        <label for="name">Логин:</label>
                        <input type="text" class="form-control" placeholder="" id="decline_login" disabled readonly />
                    </div>
                    <div class="form-group">
                        <label for="name">Кошелек:</label>
                        <input type="text" class="form-control" placeholder="" id="decline_wallet" disabled readonly />
                    </div>
                    <div class="form-group">
                        <label for="name">Сумма:</label>
                        <input type="text" class="form-control" placeholder="" id="decline_amount" disabled readonly />
                    </div>
                    <div class="form-group">
				        <label for="setMethod">Возвращать на баланс?</label>
				        <select id="returnBalance" class="form-control">
				            <option value="1">Да</option>
				            <option value="2">Нет</option>
				        </select>
				    </div>
                    <div class="form-group">
                        <label for="decline_reason">Причина отмены:</label>
                        <textarea type="text" class="form-control" id="decline_reason"></textarea>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Закрыть</button>
                    <button type="submit" class="btn btn-primary declineButton" onclick="saveDeclineReason()">Отменить выплату</button>
                </div>
            </form>
        </div>
    </div>
</div>
<script>
var showId = 0;
const declineWithdraw = id => {
    $('.btn-icon').css({pointerEvents: 'none'})

    $.post('/admin/withdraws/get', {
        id
    })
    .then(response => {
        showId = id;
        $('#declineWithdrawModal').modal('show');
        $('#decline_login').val(response.username)
        $('#decline_wallet').val(response.wallet)
        $('#decline_amount').val(response.sum)
        $('#returnBalance option[value=1]').attr('selected', 'selected')
        $('.btn-icon').css({pointerEvents: 'auto'})
    })
    .catch(err => {
        $.notify({
            type: 'error',
            message: "Произошла ошибка"
        });
    })
}
const saveDeclineReason = () => {
    var reason = $('#decline_reason').val();
    $('.declineButton').attr('disabled', true)
    $.post('/admin/withdraws/decline', {
        id: showId,
        status: 2,
        reason,
        returnBalance: $('#returnBalance').val()
    })
    .then(response => {
        if(response.error) {
            return $.notify({
                type: 'error',
                message: response.error
            });
        }

        $.notify({
            type: 'success',
            message: "Выплата отменена"
        });
        showId = 0;

        $('#decline_reason').val('');
        $('#declineWithdrawModal').modal('hide');
        $('#active_withdraws').DataTable().draw()
        $('.declineButton').attr('disabled', false)
    })
}
const acceptWithdraw = id => {
    $('.btn-icon').css({pointerEvents: 'none'})

    $.post('/admin/withdraws/send', {
        id
    })
    .then(response => {
        $('.btn-icon').css({pointerEvents: 'auto'})

        if(response.error) {
            if(response.reload) {
                $('#active_withdraws').DataTable().draw()
            }

            return $.notify({
                type: 'error',
                message: response.message
            });
        }

        $.notify({
            type: 'success',
            message: response.message
        });

        $('#active_withdraws').DataTable().draw()
        
        if(response.status == 1) $('#sended_withdraws').DataTable().draw()
        else $('#process_withdraws').DataTable().draw()
    })
}
</script>
<style>
    input.form-control:disabled {
        background: #f7f7f7!important
    }
</style>
@endsection
