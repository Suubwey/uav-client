const express = require("express");
const http = require("http");
const socketIo = require("socket.io");
const socketIoClient = require("socket.io-client");

const app = express();
const server = http.createServer(app);
const io = socketIo(server, {
  cors: {
    origin: "http://localhost:3000",
  },
});

// Connect to Raspberry Pi
const raspberryPiSocket = socketIoClient.connect("http://:10.0.0.160:3000"); // Change to your Raspberry Pi's address

// Broadcast the video data to all connected clients
raspberryPiSocket.on("video", (data) => {
  io.sockets.emit("video", data);
});

// Serve static files (like the HTML client)
app.use(express.static("public"));

server.listen(5000, () => {
  console.log("Central Server is running on port 5000");
});
