const SteamCommunity = require('./PromiseSteamCommunity')
const TradeOfferManager = require('./PromiseSteamTradeofferManager')
const SteamTotp = require('steam-totp')
const EventEmitter = require('events')
const fs = require('fs')

class Bot extends EventEmitter {
    constructor(options) {
        super()
        this.options = options
        this.logOnOptions = this.options.logon
        this.maFile = false
        this.community = new SteamCommunity(this.options.community)
        this.manager = new TradeOfferManager(this.options.manager)
        this.setupEvents()
    }

    getCommunity() {
        return this.community
    }

    getManager() {
        return this.manager
    }

    async login() {
        if (await this.community.logged()) return true
        if (fs.existsSync(`./steamguards/${this.logOnOptions.accountName}.grd`)) {
            this.logOnOptions.steamguard = fs.readFileSync(`./steamguards/${this.logOnOptions.accountName}.grd`, 'utf8')
        }
        if (fs.existsSync(`./mafiles/${this.logOnOptions.accountName}.mafile`)) {
            this.maFile = JSON.parse(fs.readFileSync(`./mafiles/${this.logOnOptions.accountName}.mafile`, 'utf8'))
            this.logOnOptions.sharedSecret = this.maFile.shared_secret
        }
        if (this.logOnOptions.sharedSecret) {
            this.logOnOptions.twoFactorCode = SteamTotp.getAuthCode(this.logOnOptions.sharedSecret)
        }
        let login = await this.community.login(this.logOnOptions)
        if (!login) return false
        fs.writeFileSync(`./steamguards/${this.logOnOptions.accountName}.grd`, login.steamguard, 'utf8')
        this.manager.setCookies(login.cookies)
        return true
    }

    setupEvents() {
        this.community.on('sessionExpired', (err) => {
            this.login()
            this.emit('sessionExpired', err)
        })

        this.manager.on('newOffer', (offer) => {
            this.emit('newOffer', offer)
        })

        this.manager.on('sentOfferChanged', (offer, oldState) => {
            this.emit('sentOfferChanged', offer, oldState)
        })

        this.manager.on('sentOfferCanceled', (offer, reason) => {
            this.emit('sentOfferCanceled', offer, reason)
        })

        this.manager.on('sentPendingOfferCanceled', (offer) => {
            this.emit('sentPendingOfferCanceled', offer)
        })

        this.manager.on('unknownOfferSent', (offer) => {
            this.emit('unknownOfferSent', offer)
        })

        this.manager.on('receivedOfferChanged', (offer, oldState) => {
            this.emit('receivedOfferChanged', offer)
        })

        this.manager.on('realTimeTradeConfirmationRequired', (offer) => {
            this.emit('realTimeTradeConfirmationRequired', offer)
        })

        this.manager.on('realTimeTradeCompleted', (offer) => {
            this.emit('realTimeTradeCompleted', offer)
        })

        this.manager.on('pollFailure', (err) => {
            this.emit('pollFailure', err)
        })

        this.manager.on('pollSuccess', () => {
            this.emit('pollSuccess')
        })

        this.manager.on('pollData', (pollData) => {
            this.emit('pollData', pollData)
        })

        this.manager.on('offerList', (filter, sent, received) => {
            this.emit('offerList', filter, sent, received)
        })
    }
}

module.exports = Bot