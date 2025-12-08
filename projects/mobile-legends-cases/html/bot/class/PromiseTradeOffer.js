class PromiseTradeOffer {
    constructor(TradeOffer) {
        this.TradeOffer = TradeOffer
    }

    getTradeOfeer() {
        return this.TradeOffer
    }

    isGlitched() {
        return this.TradeOffer.isGlitched()
    }

    data(key, value) {
        return this.TradeOffer.data(key, value)
    }

    getPartnerInventoryContents(appid, contextid) {
        return new Promise((resolve, reject) => {
            this.TradeOffer.getPartnerInventoryContents(appid, contextid, (err, inventory, currencies) => {
                if (err) {
                    reject(err)
                    return false
                }
                resolve({inventory, currencies})
            })
        })
    }

    loadPartnerInventory(appid, contextid) {
        return new Promise((resolve, reject) => {
            this.TradeOffer.loadPartnerInventory(appid, contextid, (err, inventory, currencies) => {
                if (err) {
                    reject(err)
                    return false
                }
                resolve({inventory, currencies})
            })
        })
    }

    addMyItem(item) {
        return this.TradeOffer.addMyItem(item)
    }

    addMyItems(items) {
        return this.TradeOffer.addMyItems(items)
    }

    removeMyItem(item) {
        return this.TradeOffer.removeMyItem(item)
    }

    removeMyItems(items) {
        return this.TradeOffer.removeMyItems(items)
    }

    addTheirItem(item) {
        return this.TradeOffer.addTheirItem(item)
    }

    addTheirItems(items) {
        return this.TradeOffer.addTheirItems(items)
    }

    removeTheirItem(item) {
        return this.TradeOffer.removeTheirItem(item)
    }

    removeTheirItems(items) {
        return this.TradeOffer.removeTheirItems(items)
    }

    containsItem(item) {
        return this.TradeOffer.containsItem(item)
    }

    setMessage(message) {
        return this.TradeOffer.setMessage(message)
    }

    setToken(token) {
        return this.TradeOffer.setToken(token)
    }

    getUserDetails() {
        return new Promise((resolve, reject) => {
            this.TradeOffer.getUserDetails((err, me, them) => {
                if (err) {
                    reject(err)
                    return false
                }
                resolve({me, them})
            })
        })
    }

    send() {
        return new Promise((resolve, reject) => {
            this.TradeOffer.send((err, status) => {
                if (err) {
                    reject(err)
                    return false
                }
                resolve(status)
            })
        })
    }

    cancel() {
        return new Promise((resolve, reject) => {
            this.TradeOffer.send((err) => {
                if (err) {
                    reject(err)
                    return false
                }
                resolve(true)
            })
        })
    }

    decline() {
        return new Promise((resolve, reject) => {
            this.TradeOffer.decline((err) => {
                if (err) {
                    reject(err)
                    return false
                }
                resolve(true)
            })
        })
    }

    accept(skipStateUpdate) {
        return new Promise((resolve, reject) => {
            this.TradeOffer.accept(skipStateUpdate, (err, status) => {
                if (err) {
                    reject(err)
                    return false
                }
                resolve(status)
            })
        })
    }

    duplicate() {
        return new PromiseTradeOffer(this.TradeOffer.duplicate());
    }

    counter() {
        return new PromiseTradeOffer(this.TradeOffer.counter());
    }

    update() {
        return new Promise((resolve, reject) => {
            this.TradeOffer.update((err) => {
                if (err) {
                    reject(err)
                    return false
                }
                resolve(true)
            })
        })
    }

    getReceivedItems(getActions) {
        return new Promise((resolve, reject) => {
            this.TradeOffer.getReceivedItems(getActions, (err, items) => {
                if (err) {
                    reject(err)
                    return false
                }
                resolve(items)
            })
        })
    }

    getExchangeDetails(getDetailsIfFailed) {
        return new Promise((resolve, reject) => {
            this.TradeOffer.getExchangeDetails(getDetailsIfFailed, (err, status, tradeInitTime, receivedItems, sentItems) => {
                if (err) {
                    reject(err)
                    return false
                }
                resolve({status, tradeInitTime, receivedItems, sentItems})
            })
        })
    }
}

module.exports = PromiseTradeOffer;