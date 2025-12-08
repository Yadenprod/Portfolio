<div class="tab-pane" id="site_bot" role="tabpanel">
    <div class="kt-section">
        <h3 class="kt-section__title">
            Настройки Telegram-бота
        </h3>
        <div class="form-group row">
            <div class="col-lg-4">
                <label>ID канала:</label>
                <input type="text" class="form-control" placeholder="xxxxxx" value="{{$settings->telegram_chat_id}}" name="telegram_chat_id" />
            </div>
            <div class="col-lg-4">
                <label>Токен бота:</label>
                <input type="text" class="form-control" placeholder="xxxxxx" value="{{$settings->telegram_token}}" name="telegram_token" />
            </div>
        </div>
    </div>
</div>
