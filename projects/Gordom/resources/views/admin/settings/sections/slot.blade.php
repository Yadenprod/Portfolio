<div class="tab-pane" id="site_slots" role="tabpanel">
    <div class="kt-section">
        <h3 class="kt-section__title">
            Настройка TBS слотов:
        </h3>
        <div class="form-group row">
            <div class="col-lg-4">
                <label>Hall ID:</label>
                <input type="text" class="form-control" placeholder="" value="{{$settings->tbs_provider_id}}" name="tbs_provider_id" />
            </div>
            <div class="col-lg-4">
                <label>Hall Secret:</label>
                <input type="text" class="form-control" placeholder="" value="{{$settings->tbs_provider_secret}}" name="tbs_provider_secret" />
            </div>
        </div>
    </div>
</div>
