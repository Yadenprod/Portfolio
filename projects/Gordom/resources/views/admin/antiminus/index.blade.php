@extends('admin/layout')

@section('content')
<div class="kt-subheader kt-grid__item" id="kt_subheader">
    <div class="kt-subheader__main">
        <h3 class="kt-subheader__title">Антиминус</h3>
    </div>
</div>

<div class="kt-content  kt-grid__item kt-grid__item--fluid" id="kt_content">
    <div class="kt-portlet kt-portlet--tabs">
        <!-- <div class="kt-portlet__head">
            <div class="kt-portlet__head-toolbar">
                <ul class="nav nav-tabs nav-tabs-line nav-tabs-line-danger nav-tabs-line-2x nav-tabs-line-right" role="tablist">
                    <li class="nav-item">
                        <a class="nav-link active" data-toggle="tab" href="#site" role="tab" aria-selected="true">
                            Настройки сайта
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" data-toggle="tab" href="#site_payments" role="tab" aria-selected="true">
                            Настройка платежных систем
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" data-toggle="tab" href="#site_bot" role="tab" aria-selected="true">
                            Настройка Telegram-бота
                        </a>
                    </li>
                </ul>
            </div>
        </div> -->
        <form class="kt-form" method="post" action="{{ route('admin.antiminus') }}">
            <div class="kt-portlet__body">
                <div class="tab-content">
                    <div class="tab-pane active" id="site" role="tabpanel">
                        <div class="kt-section">
                            <h3 class="kt-section__title">
                                Настройки антиминуса:
                            </h3>
                            <div class="form-group row">
                                <div class="col-lg-4">
                                    <label>Антиминус:</label>
                                    <select class="form-control" name="antiminus">
                                        <option value="1" @if($settings->antiminus == 1) selected @endif>Включен</option>
                                        <option value="0" @if($settings->antiminus == 0) selected @endif>Отключен</option>
                                    </select>
                                </div>
                                <div class="col-lg-4">
                                    <label>Банк в Dice:</label>
                                    <input type="text" class="form-control" placeholder="" value="{{\App\Models\Profit::query()->find(1)->bank_dice}}" name="bank_dice" />
                                </div>
                                <div class="col-lg-4">
                                    <label>Банк в Mines:</label>
                                    <input type="text" class="form-control" placeholder="" value="{{\App\Models\Profit::query()->find(1)->bank_mines}}" name="bank_mines" />
                                </div>
                            </div>
                            <div class="form-group row">
                                <div class="col-lg-4">
                                    <label>Банк в Bubbles:</label>
                                    <input type="text" class="form-control" placeholder="" value="{{\App\Models\Profit::query()->find(1)->bank_bubbles}}" name="bank_bubbles" />
                                </div>
                                <div class="col-lg-4">
                                    <label>Комиссия в банк сайта:</label>
                                    <input type="text" class="form-control" placeholder="" value="{{\App\Models\Profit::query()->find(1)->comission}}" name="comission" />
                                </div>
                            </div>
                        </div>
                    </div>
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
