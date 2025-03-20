#### Warning
For "serial_test.sh" to work, a change has to be done in "/home/vscode/.local/lib/python3.12/site-packages/berluf_selen_2_ctrl/recup/serial.py".
Change line 19 from Serial_conf(com, 9600, 1, 8, "O") to "Serial_conf(com, 9600, 1, 8, "N")".
The reason is "socat" for some reasom won't work with "odd" parity, so it has to be changed to "none".

After the change, setup the integration with serial port = "/srv/pts/ttyV1".