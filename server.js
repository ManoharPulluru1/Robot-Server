const express = require("express");
const cors = require("cors");
const http = require("http");
const socketIo = require("socket.io");

const app = express();
app.use(cors());

const server = http.createServer(app);
const io = socketIo(server, { cors: { origin: "*" } });

const PORT = process.env.PORT || 4000;

io.on("connection", (socket) => {
    console.log(`Client connected: ${socket.id}`);
    
    socket.on("press", (direction) => {
        console.log(`Press: ${direction}`);
        io.emit("press_new", { direction1: direction });  // Broadcasting to all clients
    });
    
    socket.on("release", (direction) => {
        console.log(`Release: ${direction}`);
        io.emit("release_new", { direction1: direction });  // Broadcasting to all clients
    });
    
    socket.on("disconnect", () => {
        console.log(`Client disconnected: ${socket.id}`);
    });
});

server.listen(PORT, () => {
    console.log(`Server listening on port ${PORT}`);
});
