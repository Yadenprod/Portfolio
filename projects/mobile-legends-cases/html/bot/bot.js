const Bot = require('./class/Bot')
const decrypt = require('./modules/decrypt')
const api = require('./modules/api')

/*let bot = new Bot({logon: {
    'accountName': 'maria18219',
	'password': 'CLNJQog1996z1',
	'sharedSecret': 'stGSDdr4pVnyvLUvyJKAKlyZHzs='
}})*/
const bots = []

(async () => {
    let responce = api('bots/get')
    if (!responce) throw new Error('Can\'t load bots')
    responce.bots.forEach(loadBot => {
        
    })
})()