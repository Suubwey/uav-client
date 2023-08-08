const { SerialPort } = require("serialport");
const {
  MavLinkPacketSplitter,
  MavLinkPacketParser,
  minimal,
  common,
  ardupilotmega,
  MavLinkProtocolV2,
  send,
} = require("node-mavlink");

// substitute with your serial port!
const port = new SerialPort({
  path: "/dev/tty.usbserial-D30EZNZF",
  baudRate: 57600,
});

// console.log(port);

// constructing a reader that will emit each packet separately
const reader = port
  .pipe(new MavLinkPacketSplitter())
  .pipe(new MavLinkPacketParser());

// create a registry of mappings between a message id and a data class
const REGISTRY = {
  ...minimal.REGISTRY,
  ...common.REGISTRY,
  ...ardupilotmega.REGISTRY,
};

reader.on("data", (packet) => {
  const clazz = REGISTRY[packet.header.msgid];
  if (clazz) {
    const data = packet.protocol.data(packet.payload, clazz);

    // console.log(data.constructor.name);
    if (data.constructor.name == "CommandAck")
      console.log("Received packet: CommandAck", data);
    if (data.constructor.name == "GlobalPositionInt")
      console.log("Position:", data.lat / 1e7, data.lon / 1e7, data.alt / 1000);
    if (data.constructor.name == "MissionAck")
      console.log("Received packet: MissionAck", data);
  }
});

// command.targetSystem = 254;
// command.targetComponent = 1;

// // arm check
// const command = new common.RunPrearmChecksCommand();

// arm
const command = new common.ComponentArmDisarmCommand();
command.arm = 1;
command.force = 21196;

// takeoff
const command1 = new common.NavTakeoffCommand();
command1.pitch = 0;
command1.yaw = 0;

command1.altitude = 1168;
command1.latitude = 51.0868047;
command1.longitude = -114.0596604;

// // flight information message
// const command = new common.RequestMessageCommand();
// command.messageId = 264;
// command.responseTarget = 0;

// // system status message
// const command = new common.RequestMessageCommand();
// command.messageId = 1;
// command.responseTarget = 0;

// // system time  message
// const command = new common.RequestMessageCommand();
// command.messageId = 2;
// command.responseTarget = 0;

port.on("open", async () => {
  let res1 = await send(port, command, new MavLinkProtocolV2());
  let res2 = await send(port, command1, new MavLinkProtocolV2());
});
