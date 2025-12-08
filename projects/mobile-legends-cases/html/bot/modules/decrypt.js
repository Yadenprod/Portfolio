const RSA = require('node-rsa')
const fs = require('fs')
const pkey = fs.readFileSync('./bot.key', 'utf8')
let key = new RSA(pkey, {encryptionScheme: {scheme: 'pkcs1', hash: 'sha256'}})

module.exports = (str) => {
    return key.decrypt(str, 'utf8')
}

