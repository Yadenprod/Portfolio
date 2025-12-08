const api = require('./modules/api')
const request = require('request-promise')
const xml = require('xml2js')

const uris = [
    {
        method: '/currencies/rates/update/',
        params: {},
        interval: 60 * 60000,
        func: async function() {
            api(this.method, await updateFiatRates())
        }
    },
    /*{
        method: '/botinventories/update/',
        interval: 300000
    },*/
    /*{
        method: '/qiwi/check/',
        interval: 30000
    },*/
    {
        method: '/itemlist/update/',
        interval: 20 * 60000
    },
    {
        method: '/market/tick/',
        interval: 10000
    }
];

(async () => {
    for(let i in uris) {
        let uri = uris[i]
        setInterval(() => {
            if (typeof uri.func == 'function') {
                uri.func()
            } else {
                api(uri.method, uri.params)
            }
        }, uri.interval)
        if (typeof uri.func == 'function') {
            uri.func()
        } else {
            await api(uri.method, uri.params)
        }
    }
})()

async function updateFiatRates() {
    const data = await request({uri: 'https://www.cbr.ru/scripts/XML_daily.asp'})
    const parser = new xml.Parser()
    let json = await parser.parseStringPromise(data)
    let rates = {}
    json.ValCurs.Valute.forEach(valut => {
        if (~['USD', 'EUR'].indexOf(valut.CharCode['0'])) {
            rates[valut.CharCode['0'].toLowerCase()] = Math.floor(parseFloat(valut.Value['0'].replace(',', '.')) * 100) / 100
        }
    })
    return rates
}