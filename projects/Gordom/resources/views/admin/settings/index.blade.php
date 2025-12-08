@extends('admin/layout')

@section('content')
<div class="kt-subheader kt-grid__item" id="kt_subheader">
    <div class="kt-subheader__main">
        <h3 class="kt-subheader__title">Настройки</h3>
    </div>
</div>

<div class="kt-content  kt-grid__item kt-grid__item--fluid" id="kt_content">
    <div class="kt-portlet kt-portlet--tabs">
        <div class="kt-portlet__head">
            <div class="kt-portlet__head-toolbar">
                <ul class="nav nav-tabs nav-tabs-line nav-tabs-line-danger nav-tabs-line-2x nav-tabs-line-right" role="tablist">
                    <li class="nav-item">
                        <a class="nav-link active" data-toggle="tab" href="#site" role="tab" aria-selected="true">
                            Настройки сайта
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" data-toggle="tab" href="#site_payments" role="tab" aria-selected="true">
                            Платёжные системы
                        </a>
                    </li>
                    <!-- <li class="nav-item">
                        <a class="nav-link" data-toggle="tab" href="#site_bot" role="tab" aria-selected="true">
                            Telegram-бот
                        </a>
                    </li> -->
                    <li class="nav-item">
                        <a class="nav-link" data-toggle="tab" href="#site_bonus" role="tab" aria-selected="true">
                            Раздача
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" data-toggle="tab" href="#site_slots" role="tab" aria-selected="true">
                            Слоты
                        </a>
                    </li>
                </ul>
            </div>
        </div>
        <form class="kt-form" method="post" action="{{ route('admin.settings') }}">
            <div class="kt-portlet__body">
                <div class="tab-content">
                    @include('admin.settings.sections.main')
                    @include('admin.settings.sections.payments')
                    @include('admin.settings.sections.bot')
                    @include('admin.settings.sections.bonus')
                    @include('admin.settings.sections.slot')
                </div>
            </div>
            <div class="kt-portlet__foot">
                <div class="kt-form__actions">
                    <button type="submit" class="btn btn-primary">Сохранить</button>
                </div>
            </div>
        </form>
    </div>
</div>
<style>
    @media (max-width:1100px) {
        .col-lg-4 {
            margin-top: 20px;
        }
    }
</style>
@endsection
