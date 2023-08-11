msg = vehicle.message_factory.command_long_encode(
0, 0,    # target_system, target_component
mavutil.mavlink.MAV_CMD_DO_SET_SERVO, #command
0, #confirmation
1,    # servo number
1500,          # servo position between 1000 and 2000
0, 0, 0, 0, 0)    # param 3 ~ 7 not used

# send command to vehicle
vehicle.send_mavlink(msg)