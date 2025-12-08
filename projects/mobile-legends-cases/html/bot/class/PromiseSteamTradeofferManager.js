const TradeOfferManager = require('steam-tradeoffer-manager')
const PromiseTradeOffer = require('./PromiseTradeOffer');
const EventEmitter = require('events')

class PromiseTradeOfferManager extends EventEmitter {
    constructor(options) {
        super();
        this.TradeOfferManager = new TradeOfferManager(options)
        this.setupEvents()
    }

    getTradeOfferManager() {
        return this.TradeOfferManager;
    }
    
    setCookies(cookies, familyViewPin) {
        return new Promise((resolve, reject) => {
            this.TradeOfferManager.setCookies(cookies, familyViewPin, (err) => {
                if (err) {
                    reject(err)
                    return false
                }
                resolve(true)
            })
        })
    }

    shutdown() {
        return this.TradeOfferManager.shutdown()
    }

    parentalUnlock(pin) {
        return new Promise((resolve, reject) => {
            this.TradeOfferManager.parentalUnlock(pin, (err) => {
                if (err) {
                    reject(err)
                    return false
                }
                resolve(true)
            })
        })
    }

    createOffer(partner, token) {
        return new PromiseTradeOffer(this.TradeOfferManager.createOffer(partner, token))
    }

    getOffer(id) {
        return new Promise((resolve, reject) => {
            this.TradeOfferManager.getOffer(id, (err, offer) => {
                if (err) {
                    reject(err)
                    return false
                }
                resolve(new PromiseTradeOffer(offer))
            })
        })
    }

    getOffers(filter, historicalCutoff) {
        return new Promise((resolve, reject) => {
            this.TradeOfferManager.getOffers(filter, historicalCutoff, (err, sent, received) => {
                if (err) {
                    reject(err)
                    return false
                }
                sent.forEach((offer, index) => {
                    sent[index] = new PromiseTradeOffer(offer)
                })
                received.forEach((offer, index) => {
                    received[index] = new PromiseTradeOffer(offer)
                })
                resolve({sent, received})
            })
        })
    }

    getInventoryContents(appid, contextid, tradableOnly) {
        return new Promise((resolve, reject) => {
            this.TradeOfferManager.getInventoryContents(appid, contextid, tradableOnly, (err, inventory, currencies) => {
                if (err) {
                    reject(err)
                    return false
                }
                resolve({inventory, currencies})
            })
        })
    }

    getUserInventoryContents(steamID, appid, contextid, tradableOnly) {
        return new Promise((resolve, reject) => {
            this.TradeOfferManager.getInventoryContents(steamID, appid, contextid, tradableOnly, (err, inventory, currencies) => {
                if (err) {
                    reject(err)
                    return false
                }
                resolve({inventory, currencies})
            })
        })
    }

    loadInventory(appid, contextid, tradableOnly) {
        return new Promise((resolve, reject) => {
            this.TradeOfferManager.loadInventory(appid, contextid, tradableOnly, (err, inventory, currencies) => {
                if (err) {
                    reject(err)
                    return false
                }
                resolve({inventory, currencies})
            })
        })
    }

    loadUserInventory(steamID, appid, contextid, tradableOnly) {
        return new Promise((resolve, reject) => {
            this.TradeOfferManager.loadUserInventory(steamID, appid, contextid, tradableOnly, (err, inventory, currencies) => {
                if (err) {
                    reject(err)
                    return false
                }
                resolve({inventory, currencies})
            })
        })
    }

    getOfferToken() {
        return new Promise((resolve, reject) => {
            this.TradeOfferManager.getOfferToken((err, token) => {
                if (err) {
                    reject(err)
                    return false
                }
                resolve(token)
            })
        })
    }

    getOffersContainingItems(items, includeInactive) {
        return new Promise((resolve, reject) => {
            this.TradeOfferManager.getOffersContainingItems(items, includeInactive, (err, sent, received) => {
                if (err) {
                    reject(err)
                    return false
                }
                resolve({sent, received})
            })
        })
    }

    doPoll() {
        return this.TradeOfferManager.doPoll()
    }

    setupEvents() {
        this.TradeOfferManager.on('newOffer', (offer) => {
            this.emit('newOffer', new PromiseTradeOffer(offer))
        })

        this.TradeOfferManager.on('sentOfferChanged', (offer, oldState) => {
            this.emit('sentOfferChanged', new PromiseTradeOffer(offer), oldState)
        })

        this.TradeOfferManager.on('sentOfferCanceled', (offer, reason) => {
            this.emit('sentOfferCanceled', new PromiseTradeOffer(offer), reason)
        })

        this.TradeOfferManager.on('sentPendingOfferCanceled', (offer) => {
            this.emit('sentPendingOfferCanceled', new PromiseTradeOffer(offer))
        })

        this.TradeOfferManager.on('unknownOfferSent', (offer) => {
            this.emit('unknownOfferSent', new PromiseTradeOffer(offer))
        })

        this.TradeOfferManager.on('receivedOfferChanged', (offer, oldState) => {
            this.emit('receivedOfferChanged', new PromiseTradeOffer(offer), oldState)
        })

        this.TradeOfferManager.on('realTimeTradeConfirmationRequired', (offer) => {
            this.emit('realTimeTradeConfirmationRequired', new PromiseTradeOffer(offer))
        })

        this.TradeOfferManager.on('realTimeTradeCompleted', (offer) => {
            this.emit('realTimeTradeCompleted', new PromiseTradeOffer(offer))
        })

        this.TradeOfferManager.on('pollFailure', (err) => {
            this.emit('pollFailure', err)
        })

        this.TradeOfferManager.on('pollSuccess', () => {
            this.emit('pollSuccess')
        })

        this.TradeOfferManager.on('pollData', (pollData) => {
            this.emit('pollData', pollData)
        })

        this.TradeOfferManager.on('offerList', (filter, sent, received) => {
            sent.forEach((offer, index) => {
                sent[index] = new PromiseTradeOffer(offer)
            })
            received.forEach((offer, index) => {
                received[index] = new PromiseTradeOffer(offer)
            })
            this.emit('offerList', filter, sent, received)
        })
    }
}

module.exports = PromiseTradeOfferManager;