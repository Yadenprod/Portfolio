require('dotenv').config({path: __dirname+'/./../.env'});

module.exports = {
    https: (process.env.APP_HTTPS == 'true') || false,
    domain: process.env.APP_URL,
    ssl: {
        key: process.env.SSL_KEY_PATH || null,
        cert: process.env.SSL_CERT_PATH || ''
    },
    database: {
        host: process.env.DB_HOST,
        user: process.env.DB_USERNAME,
        database: process.env.DB_DATABASE,
        password: process.env.DB_PASSWORD
    }
}