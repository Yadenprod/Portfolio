const SteamCommunity = require('steamcommunity')
const EventEmitter = require('events')

class PromiseSteamCommunity extends EventEmitter {
    constructor(options) {
        super();
        this.SteamCommunity = new SteamCommunity(options)
        this.setupEvents()
    }

    getCommunity() {
        return this.SteamCommunity;
    }

    login(details) {
        return new Promise((resolve, reject) => {
            this.SteamCommunity.login(details, (err, sessionID, cookies, steamguard, oAuthToken) => {
                if (err) {
                    reject(err)
                    return false
                }
                resolve({sessionID, cookies, steamguard, oAuthToken})
            });
        })
    }

    oAuthLogin(steamguard, oAuthToken) {
        return new Promise((resolve, reject) => {
            this.SteamCommunity.oAuthLogin(steamguard, oAuthToken, (err, sessionID, cookies) => {
                if (err) {
                    reject(err)
                    return false
                }
                resolve({sessionID, cookies})
            })
        })
    }

    loggedIn() {
        return new Promise((resolve, reject) => {
            this.SteamCommunity.loggedIn((err, loggedIn, familyView) => {
                if (err) {
                    reject(err)
                    return false
                }
                resolve({loggedIn, familyView})
            })
        })
    }
    
    logged() {
        return new Promise((resolve, reject) => {
            this.SteamCommunity.loggedIn((err, loggedIn, familyView) => {
                if (err) {
                    reject(err)
                    return false
                }
                resolve(loggedIn)
            })
        })
    }

    setCookies(cookies) {
        return this.SteamCommunity.setCookies(cookies)
    }

    getSessionID() {
        return this.SteamCommunity.getSessionID()
    }

    getWebApiKey(domain) {
        return new Promise((resolve, reject) => {
            this.SteamCommunity.getWebApiKey(domain, (err, key) => {
                if (err) {
                    reject(err)
                    return false
                }
                resolve(key)
            })
        })
    }

    getWebApiOauthToken() {
        return new Promise((resolve, reject) => {
            this.SteamCommunity.getWebApiOauthToken((err, token) => {
                if (err) {
                    reject(err)
                    return false
                }
                resolve(token)
            })
        })
    }

    getClientLogonToken() {
        return new Promise((resolve, reject) => {
            this.SteamCommunity.getClientLogonToken((err, details) => {
                if (err) {
                    reject(err)
                    return false
                }
                resolve(details)
            })
        })
    }

    parentalUnlock(pin) {
        return new Promise((resolve, reject) => {
            this.SteamCommunity.parentalUnlock(pin, (err) => {
                if (err) {
                    reject(err)
                    return false
                }
                resolve(true)
            })
        })
    }

    getNotifications() {
        return new Promise((resolve, reject) => {
            this.SteamCommunity.getNotifications((err, notifications) => {
                if (err) {
                    reject(err)
                    return false
                }
                resolve(notifications)
            })
        })
    }

    resetItemNotifications() {
        return new Promise((resolve, reject) => {
            this.SteamCommunity.resetItemNotifications((err) => {
                if (err) {
                    reject(err)
                    return false
                }
                resolve(true)
            })
        })
    }

    getTradeURL() {
        return new Promise((resolve, reject) => {
            this.SteamCommunity.getTradeURL((err, url, token) => {
                if (err) {
                    reject(err)
                    return false
                }
                resolve({url, token})
            })
        })
    }

    changeTradeURL() {
        return new Promise((resolve, reject) => {
            this.SteamCommunity.changeTradeURL((err, url, token) => {
                if (err) {
                    reject(err)
                    return false
                }
                resolve({url, token})
            })
        })
    }

    clearPersonaNameHistory() {
        return new Promise((resolve, reject) => {
            this.SteamCommunity.clearPersonaNameHistory((err) => {
                if (err) {
                    reject(err)
                    return false
                }
                resolve(true)
            })
        })
    }

    getSteamUser(id) {
        return new Promise((resolve, reject) => {
            this.SteamCommunity.getSteamUser(id, (err, user) => {
                if (err) {
                    reject(err)
                    return false
                }
                resolve(user)
            })
        })
    }

    getSteamGroup(id) {
        return new Promise((resolve, reject) => {
            this.SteamCommunity.getSteamGroup(id, (err, group) => {
                if (err) {
                    reject(err)
                    return false
                }
                resolve(group)
            })
        })
    }

    getMarketApps() {
        return new Promise((resolve, reject) => {
            this.SteamCommunity.getMarketApps((err, apps) => {
                if (err) {
                    reject(err)
                    return false
                }
                resolve(apps)
            })
        })
    }

    getMarketItem(appid, hashName) {
        return new Promise((resolve, reject) => {
            this.SteamCommunity.getMarketItem(appid, hashName, (err, item) => {
                if (err) {
                    reject(err)
                    return false
                }
                resolve(item)
            })
        })
    }

    marketSearch(options) {
        return new Promise((resolve, reject) => {
            this.SteamCommunity.getMarketItem(options, (err, items) => {
                if (err) {
                    reject(err)
                    return false
                }
                resolve(items)
            })
        })
    }

    setupProfile() {
        return new Promise((resolve, reject) => {
            this.SteamCommunity.setupProfile((err) => {
                if (err) {
                    reject(err)
                    return false
                }
                resolve(true)
            })
        })
    }

    editProfile(settings) {
        return new Promise((resolve, reject) => {
            this.SteamCommunity.editProfile(settings, (err) => {
                if (err) {
                    reject(err)
                    return false
                }
                resolve(true)
            })
        })
    }

    profileSettings(settings) {
        return new Promise((resolve, reject) => {
            this.SteamCommunity.profileSettings(settings, (err) => {
                if (err) {
                    reject(err)
                    return false
                }
                resolve(true)
            })
        })
    }

    uploadAvatar(image, format) {
        return new Promise((resolve, reject) => {
            this.SteamCommunity.uploadAvatar(image, format, (err, url) => {
                if (err) {
                    reject(err)
                    return false
                }
                resolve(url)
            })
        })
    }

    postProfileStatus(statusText, options) {
        return new Promise((resolve, reject) => {
            this.SteamCommunity.postProfileStatus(statusText, options, (err, postID) => {
                if (err) {
                    reject(err)
                    return false
                }
                resolve(postID)
            })
        })
    }

    deleteProfileStatus(postID) {
        return new Promise((resolve, reject) => {
            this.SteamCommunity.postProfileStatus(postID, (err) => {
                if (err) {
                    reject(err)
                    return false
                }
                resolve(true)
            })
        })
    }

    getInventoryHistory(options) {
        return new Promise((resolve, reject) => {
            this.SteamCommunity.getInventoryHistory(options, (err, history) => {
                if (err) {
                    reject(err)
                    return false
                }
                resolve(history)
            })
        })
    }

    enableTwoFactor() {
        return new Promise((resolve, reject) => {
            this.SteamCommunity.enableTwoFactor((err, response) => {
                if (err) {
                    reject(err)
                    return false
                }
                resolve(response)
            })
        })
    }

    finalizeTwoFactor(shared_secret, activationCode) {
        return new Promise((resolve, reject) => {
            this.SteamCommunity.finalizeTwoFactor(shared_secret, activationCode, (err) => {
                if (err) {
                    reject(err)
                    return false
                }
                resolve(true)
            })
        })
    }

    disableTwoFactor(revocationCode) {
        return new Promise((resolve, reject) => {
            this.SteamCommunity.disableTwoFactor(revocationCode, (err) => {
                if (err) {
                    reject(err)
                    return false
                }
                resolve(true)
            })
        })
    }

    getConfirmations(time, key,) {
        return new Promise((resolve, reject) => {
            this.SteamCommunity.getConfirmations(time, key, (err, confirmations) => {
                if (err) {
                    reject(err)
                    return false
                }
                resolve(confirmations)
            })
        })
    }

    getConfirmationOfferID(confID, time, key) {
        return new Promise((resolve, reject) => {
            this.SteamCommunity.getConfirmationOfferID(confID, time, key, (err, offerID) => {
                if (err) {
                    reject(err)
                    return false
                }
                resolve(offerID)
            })
        })
    }

    respondToConfirmation(confID, confKey, time, key, accept) {
        return new Promise((resolve, reject) => {
            this.SteamCommunity.getConfirmationOfferID(confID, confKey, time, key, accept, (err) => {
                if (err) {
                    reject(err)
                    return false
                }
                resolve(true)
            })
        })
    }

    acceptConfirmationForObject(identitySecret, objectID) {
        return new Promise((resolve, reject) => {
            this.SteamCommunity.acceptConfirmationForObject(identitySecret, objectID, (err) => {
                if (err) {
                    reject(err)
                    return false
                }
                resolve(true)
            })
        })
    }

    acceptAllConfirmations(time, confKey, allowKey) {
        return new Promise((resolve, reject) => {
            this.SteamCommunity.acceptConfirmationForObject(time, confKey, allowKey, (err, confs) => {
                if (err) {
                    reject(err)
                    return false
                }
                resolve(confs)
            })
        })
    }

    getGemValue(appid, assetid) {
        return new Promise((resolve, reject) => {
            this.SteamCommunity.getGemValue(appid, assetid, (err, res) => {
                if (err) {
                    reject(err)
                    return false
                }
                resolve(res)
            })
        })
    }

    turnItemIntoGems(appid, assetid, expectedGemsValue) {
        return new Promise((resolve, reject) => {
            this.SteamCommunity.turnItemIntoGems(appid, assetid, expectedGemsValue, (err, res) => {
                if (err) {
                    reject(err)
                    return false
                }
                resolve(res)
            })
        })
    }

    getGiftDetails(giftID) {
        return new Promise((resolve, reject) => {
            this.SteamCommunity.turnItemIntoGems(giftID, (err, res) => {
                if (err) {
                    reject(err)
                    return false
                }
                resolve(res)
            })
        })
    }

    redeemGift(giftID) {
        return new Promise((resolve, reject) => {
            this.SteamCommunity.turnItemIntoGems(giftID, (err) => {
                if (err) {
                    reject(err)
                    return false
                }
                resolve(true)
            })
        })
    }

    setupEvents() {
        this.SteamCommunity.on('sessionExpired', (err) => {
            this.emit('sessionExpired', err)
        })
    }
}

module.exports = PromiseSteamCommunity;