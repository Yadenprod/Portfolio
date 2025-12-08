<div class="tab-pane" id="site_payments" role="tabpanel">
    <div class="kt-section">
        <h3 class="kt-section__title">
            Настройки платежной системы FreeKassa:
        </h3>
        <div class="form-group row">
            <div class="col-lg-3">
                <label>ID Магазина:</label>
                <input type="text" class="form-control" placeholder="xxxxxx" value="{{$settings->kassa_id}}" name="kassa_id" />
            </div>
            <div class="col-lg-3">
                <label>Секрет 1:</label>
                <input type="text" class="form-control" placeholder="xxxxxxx" value="{{$settings->kassa_secret1}}" name="kassa_secret1" />
            </div>
            <div class="col-lg-3">
                <label>Секрет 2:</label>
                <input type="text" class="form-control" placeholder="xxxxxxx" value="{{$settings->kassa_secret2}}" name="kassa_secret2" />
            </div>
            <div class="col-lg-3">
                <label>API ключ:</label>
                <input type="text" class="form-control" placeholder="xxxxxxx" value="{{$settings->kassa_key}}" name="kassa_key" />
            </div>
        </div>
    </div>
    <div class="kt-section">
        <h3 class="kt-section__title">
            Настройки выплат через FkWallet:
        </h3>
        <div class="form-group row">
            <div class="col-lg-4">
                <label>Кошелек FkWallet:</label>
                <input type="text" class="form-control" placeholder="xxxxxx" value="{{$settings->wallet_id}}" name="wallet_id" />
            </div>
            <div class="col-lg-4">
                <label>Ключ кошелька:</label>
                <input type="text" class="form-control" placeholder="xxxxxxx" value="{{$settings->wallet_secret}}" name="wallet_secret" />
            </div>
            <div class="col-lg-4">
                <label>Примечание:</label>
                <input type="text" class="form-control" placeholder="xxxxxxx" value="{{$settings->wallet_desc}}" name="wallet_desc" />
            </div>
        </div>
    </div>
    <!-- <div class="kt-section">
        <h3 class="kt-section__title">
            Настройки автовыплат:
        </h3>
        <div class="form-group row">
            <div class="col-lg-4">
                <label>Состояние</label>
                <select class="form-control" name="">
                    <option value="1" selected="">Включены</option>
                    <option value="0">Выключены</option>
                </select>
            </div>
            <div class="col-lg-4">
                <label>Система автовыплат</label>
                <select class="form-control" name="">
                    <option value="1" selected="">XMPay</option>
                    <option value="0">GetPay</option>
                </select>
            </div>
        </div>
    </div> -->
    <!-- <div class="kt-section">
        <h3 class="kt-section__title">
            Разделение выплат
        </h3>
        <div class="form-group row">
            <div class="col-lg-4">
                <label>Если сумма выплат больше N</label>
                <input type="text" class="form-control" placeholder="xxxxxxx" value="1000" name="" />
            </div>
            <div class="col-lg-4">
                <label>Разделяем на платежи по ... (РУБ)</label>
                <input type="text" class="form-control" placeholder="xxxxxxx" value="500" name="" />
            </div>
        </div>
    </div> -->
</div>
