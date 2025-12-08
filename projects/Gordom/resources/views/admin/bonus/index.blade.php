@extends('admin/layout')

@section('content')

<script src="/dash/js/dtables.js?v={{time()}}" type="text/javascript"></script>
<div class="kt-subheader kt-grid__item" id="kt_subheader">
    <div class="kt-subheader__main">
        <h3 class="kt-subheader__title">Настройка бонусов</h3>
    </div>
</div>

<div class="kt-content kt-grid__item kt-grid__item--fluid" id="kt_content">
    <div class="kt-portlet kt-portlet--mobile">
        <div class="kt-portlet__head kt-portlet__head--lg">
            <div class="kt-portlet__head-label">
                <span class="kt-portlet__head-icon">
                    <i class="kt-font-brand flaticon2-gift"></i>
                </span>
                <h3 class="kt-portlet__head-title">
                    Список уровней
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
            <table class="table table-striped- table-bordered table-hover table-checkable" id="bonuses">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Название</th>
                        <th>Для достижения</th>
                        <th>Награда за пост</th>
                        <th>Цвет</th>
                        <th>Действие</th>
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
                <h5 class="modal-title" id="exampleModalLongTitle">Добавление уровня</h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close"></button>
            </div>
            <form class="kt-form-new" method="post" action="{{ route('admin.bonus.create') }}" id="save">
                <div class="modal-body">
                    <div class="form-group">
                        <label for="name">Название уровня:</label>
                        <input type="text" class="form-control" placeholder="" name="title" minlength="3" required>
                    </div>
                    <div class="form-group">
                        <label for="name">Кол-во репостов:</label>
                        <input type="number" class="form-control" min="1" name="goal" required>
                    </div>
                    <div class="form-group">
                        <label for="name">Награда:</label>
                        <input type="number" class="form-control" min="0" step="0.01" name="reward" required>                    </div>
                    <div class="form-group">
                        <label for="name">Цвет:</label>
                        <input type="color" class="form-control" placeholder="" name="background" minlength="1" required>
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
@endsection
