# How to Gracefully Shutdown an OrangePi

1. Find the IP address of the OrangePi.
2. ssh in: `ssh pi@$IP_ADDR` replacing `$IP_ADDR` with the correct IP.
3. Type the password (`raspberry`). It will not show up as you type, so you have to type it blind.
4. Shut it down: `sudo shutdown now`
5. Your ssh session should disconnect, indicating the OrangePi has shut down.

NOTE: to turn the OrangePi back on, disconnect and reconnect the power cable,
or power cycle the robot.

