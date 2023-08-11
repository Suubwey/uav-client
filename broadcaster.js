const express = require("express");
const http = require("http");
const socketIo = require("socket.io");
const { spawn } = require("child_process");

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

// Broadcast camera feed using raspivid
io.on("connection", (socket) => {
  const videoStream = spawn("raspivid", [
    "-t",
    "0",
    "-w",
    "640",
    "-h",
    "480",
    "-fps",
    "30",
    "-o",
    "-",
  ]);
  videoStream.stdout.on("data", (data) => {
    socket.emit("video", data);
  });
});

server.listen(3000, () => {
  console.log("Server is running on port 3000");
});
