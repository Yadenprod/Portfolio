<template>
    <div class="container">
        <main class="content">
            <div class="page-title">
                <h1>Mobile Legends Bang Bang Cases</h1>
                <div class="subtitle">Открывай кейсы и получай скины, героев и другие предметы!</div>
            </div>
            
            <div class="cases-wrapper" v-if="cases">
                <div class="case-item" v-for="item in cases" :key="item.id" @click="openCase(item)">
                    <div class="case-image">
                        <img :src="item.image_url" :alt="item.name">
                    </div>
                    <div class="case-info">
                        <div class="case-name">{{ item.name }}</div>
                        <div class="case-price">{{ item.price }} руб.</div>
                    </div>
                </div>
            </div>
            <div class="loading" v-else>
                Загрузка кейсов...
            </div>
            
            <!-- Модальное окно для открытия кейса -->
            <div class="modal" v-if="showModal">
                <div class="modal-overlay" @click="showModal = false"></div>
                <div class="modal-container">
                    <div class="modal-header">
                        <h3>{{ selectedCase ? selectedCase.name : 'Открытие кейса' }}</h3>
                        <span class="close-btn" @click="showModal = false">&times;</span>
                    </div>
                    <div class="modal-body">
                        <div class="case-opening" v-if="openingInProgress">
                            <div class="spinner"></div>
                            <div class="opening-text">Открываем кейс...</div>
                        </div>
                        <div class="case-result" v-else-if="openedItem">
                            <div class="won-item">
                                <img :src="openedItem.image_url" :alt="openedItem.name">
                                <div class="item-name" :class="'rarity-'+openedItem.rarity">{{ openedItem.name }}</div>
                                <div class="item-type">{{ openedItem.type_name }}</div>
                                <div class="item-price">{{ openedItem.price }} руб.</div>
                            </div>
                            <div class="result-actions">
                                <button class="btn btn-primary" @click="showModal = false">Закрыть</button>
                                <button class="btn btn-success" @click="openCase(selectedCase)">Открыть еще</button>
                            </div>
                        </div>
                        <div class="case-preview" v-else>
                            <img :src="selectedCase ? selectedCase.image_url : ''" :alt="selectedCase ? selectedCase.name : ''">
                            <p>{{ selectedCase ? selectedCase.description : '' }}</p>
                            <div class="case-price">Стоимость: {{ selectedCase ? selectedCase.price : 0 }} руб.</div>
                            <button class="btn btn-primary open-btn" @click="confirmOpenCase">Открыть кейс</button>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    </div>
</template>

<script>
export default {
    data: () => ({
        cases: null,
        showModal: false,
        selectedCase: null,
        openingInProgress: false,
        openedItem: null
    }),
    mounted() {
        Utils.setTitle("Mobile Legends Cases");
        this.getCases();
    },
    methods: {
        getCases() {
            Utils.apiPostCall("/api/mobilelegends/getcases/")
                .then(resp => {
                    if (resp.data.success) {
                        this.cases = resp.data.cases;
                    }
                })
                .catch(err => {
                    Utils.userAlert('Ошибка загрузки', 'Не удалось загрузить кейсы', 'error');
                });
        },
        openCase(caseItem) {
            this.selectedCase = caseItem;
            this.openedItem = null;
            this.showModal = true;
        },
        confirmOpenCase() {
            if (!this.isLogin) {
                Utils.userAlert('Необходима авторизация', 'Пожалуйста, авторизуйтесь для открытия кейса', 'error');
                return;
            }
            
            if (this.userData.balance < this.selectedCase.price) {
                Utils.userAlert('Недостаточно средств', 'Пополните баланс для открытия кейса', 'error');
                return;
            }
            
            this.openingInProgress = true;
            
            Utils.apiPostCall("/api/mobilelegends/opencase/", {
                case_id: this.selectedCase.id
            })
                .then(resp => {
                    if (resp.data.success) {
                        setTimeout(() => {
                            this.openedItem = resp.data.item;
                            this.openingInProgress = false;
                            this.$root.$emit('balanceUpdated', resp.data.balance);
                            Utils.playSound('case_opened');
                        }, 2000); // Искусственная задержка для анимации
                    } else {
                        this.openingInProgress = false;
                        Utils.userAlert('Ошибка', resp.data.error, 'error');
                    }
                })
                .catch(err => {
                    this.openingInProgress = false;
                    Utils.userAlert('Ошибка открытия', 'Не удалось открыть кейс', 'error');
                });
        }
    },
    computed: {
        isLogin() {
            return this.$root.isLogin;
        },
        userData() {
            return this.$root.userData;
        }
    }
}
</script>

<style scoped>
.cases-wrapper {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 20px;
    margin-top: 30px;
}

.case-item {
    width: 220px;
    border-radius: 10px;
    background: rgba(0, 0, 0, 0.6);
    overflow: hidden;
    cursor: pointer;
    transition: transform 0.3s;
}

.case-item:hover {
    transform: translateY(-5px);
}

.case-image {
    height: 180px;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
}

.case-image img {
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
}

.case-info {
    padding: 15px;
    text-align: center;
}

.case-name {
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 5px;
}

.case-price {
    font-size: 16px;
    color: #ffc107;
}

.modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 1000;
    display: flex;
    justify-content: center;
    align-items: center;
}

.modal-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.7);
}

.modal-container {
    position: relative;
    width: 90%;
    max-width: 600px;
    background: #1a1a1a;
    border-radius: 15px;
    overflow: hidden;
    z-index: 1001;
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 20px;
    background: #2d2d2d;
}

.close-btn {
    font-size: 24px;
    cursor: pointer;
}

.modal-body {
    padding: 20px;
    min-height: 300px;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.case-preview {
    text-align: center;
}

.case-preview img {
    max-width: 200px;
    margin-bottom: 15px;
}

.open-btn {
    margin-top: 20px;
    padding: 10px 30px;
    font-size: 18px;
}

.case-opening {
    text-align: center;
}

.spinner {
    width: 80px;
    height: 80px;
    border: 6px solid rgba(255, 255, 255, 0.1);
    border-top: 6px solid #ffc107;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin: 0 auto 20px;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.opening-text {
    font-size: 18px;
}

.case-result {
    text-align: center;
}

.won-item {
    margin: 20px 0;
}

.won-item img {
    max-width: 200px;
    max-height: 200px;
    margin-bottom: 15px;
}

.item-name {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 5px;
}

.item-type {
    font-size: 16px;
    margin-bottom: 5px;
}

.item-price {
    font-size: 18px;
    color: #ffc107;
}

.result-actions {
    margin-top: 20px;
    display: flex;
    justify-content: center;
    gap: 15px;
}

.rarity-common { color: #c0c0c0; }
.rarity-uncommon { color: #4e9bd7; }
.rarity-rare { color: #4a80d9; }
.rarity-epic { color: #a64df5; }
.rarity-legendary { color: #d95b09; }
.rarity-mythic { color: #e6c532; }
</style> 