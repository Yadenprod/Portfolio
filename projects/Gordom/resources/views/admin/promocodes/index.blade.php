@extends('admin/layout')

@section('content')
<script src="/dash/js/dtables.js?v={{time()}}" type="text/javascript"></script>
<div class="kt-subheader kt-grid__item" id="kt_subheader">
    <div class="kt-subheader__main">
        <h3 class="kt-subheader__title">Промокоды</h3>
    </div>
</div>

<div class="kt-content kt-grid__item kt-grid__item--fluid" id="kt_content">
    <div class="kt-portlet kt-portlet--mobile">
        <div class="kt-portlet__head kt-portlet__head--lg">
            <div class="kt-portlet__head-label">
                <span class="kt-portlet__head-icon">
                    <i class="kt-font-brand flaticon2-menu-2"></i>
                </span>
                <h3 class="kt-portlet__head-title">
                    Список промокодов
                </h3>
            </div>
            <div class="kt-portlet__head-toolbar">
                <div class="kt-portlet__head-wrapper">
                    <div class="kt-portlet__head-actions">
                        <a data-toggle="modal" href="#new" class="btn btn-success btn-elevate btn-icon-sm">
                            <i class="la la-plus"></i>
                            Добавить
                        </a>
                    </div>  
                </div>
            </div>
        </div>
        <div class="kt-portlet__body">

            <!--begin: Datatable -->
            <table class="table table-striped- table-bordered table-hover table-checkable" id="promocodes">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Название</th>
                        <th>Сумма</th>
                        <td>Активаций</td>
                        <td>Активаций осталось</td>
                        <td>Тип</td>
                        <th>Действия</th>
                    </tr>
                </thead>
            </table>

            <!--end: Datatable -->
        </div>
    </div>
</div>
<div class="modal fade" id="new" tabindex="-1" role="dialog" aria-labelledby="newLabel" style="display: none;" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered" role="document">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="exampleModalLongTitle">Добавление промокода</h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close"></button>
            </div>
            <form class="kt-form-new" method="post" action="{{ route('admin.promocodes.create') }}" id="save">
                <div class="modal-body">
                    <div class="form-group">
                        <label for="name">Название: <span class="generateStr" onclick="generatePromo()">Сгенерировать</span></label>
                        <input type="text" class="form-control" placeholder="" name="name" id="name" required>
                    </div>
                    <div class="form-group">
                        <label for="name">Сумма (Если к пополнению - %):</label>
                        <input type="number" class="form-control" placeholder="" name="sum" required>
                    </div>
                    <div class="form-group">
                        <label for="name">Активаций:</label>
                        <input type="text" class="form-control" placeholder="" name="activation" required>
                    </div>
                    <div class="form-group">
                        <label for="type">Тип:</label>
                        <select class="form-control" name="type">
                            <option value="balance" selected>Баланс</option>
                            <option value="deposit">Депозит</option>
                        </select>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Закрыть</button>
                    <button type="submit" class="btn btn-primary">Добавить</button>
                </div>
            </form>
        </div>
    </div>
</div>
<style>
    .generateStr {
        color: #5867dd;
        cursor: pointer;
        user-select: none
    }
</style>
<script>
    function pass_gen(len) {
        chrs = 'abdehkmnpswxzABDEFGHKMNPQRSTWXZ123456789';
        var str = '';
        for (var i = 0; i < len; i++) {
            var pos = Math.floor(Math.random() * chrs.length);
            str += chrs.substring(pos,pos+1);
        }
        return str;
    }
    function generatePromo() {
        $('#name').val(pass_gen(8));
    }
</script>
@endsection
