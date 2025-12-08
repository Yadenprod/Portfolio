const app = require('express')()
const server = require('http').createServer(app)
const io = require('socket.io')(server, {
    cors: {
        origin: "*",
        methods: ["GET", "POST"]
    }
})

server.listen(8443)

console.log('🎉 WebSocket server started on port 8443')

// ростое хранилище для чата
let chatMessages = []
let onlineUsers = 0

// WebSocket обработчики
io.on('connection', (socket) => {
    console.log('✅ User connected:', socket.id)
    onlineUsers++

    // тправляем последние сообщения при подключении
    socket.emit('chat_history', chatMessages.slice(-50))

    // бновляем количество онлайн пользователей
    io.emit('online_users', onlineUsers)

    // бработчик сообщений чата
    socket.on('chat_message', (data) => {
        const message = {
            id: Date.now(),
            user: data.user || 'Anonymous',
            text: data.text,
            timestamp: new Date().toISOString()
        }

        chatMessages.push(message)

        // граничиваем историю до 100 сообщений
        if (chatMessages.length > 100) {
            chatMessages = chatMessages.slice(-100)
        }

        // тправляем сообщение всем клиентам
        io.emit('chat_message', message)
    })

    // бработчик отключения
    socket.on('disconnect', () => {
        console.log('❌ User disconnected:', socket.id)
        onlineUsers = Math.max(0, onlineUsers - 1)
        io.emit('online_users', onlineUsers)
    })
})

// HTTP endpoints
app.get('/health', (req, res) => {
    res.json({
        status: 'ok',
        online_users: onlineUsers,
        messages_count: chatMessages.length,
        timestamp: new Date().toISOString()
    })
})

app.get('/online', (req, res) => {
    res.json({ count: onlineUsers })
})

console.log('🚀 WebSocket server ready for connections')
