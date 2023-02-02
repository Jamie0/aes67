# aes67

An experimental Python/GStreamer tool that can send and receive AES67 streams. 

## Usage

```
usage: aes67 [-h] --host HOST [--net NET] {tx,rx} ...

AES67 Utility

positional arguments:
    tx         transmit mode
    rx         receive mode

options:
  -h, --help       show this help message and exit
  --host HOST      the broadcast address (239.69.0.0/16) for AES67 data
  --net NET        the network interface name

TX options:
  --input INPUT    GStreamer audio source string

RX options:
  --output OUTPUT  GStreamer audio sink string

```

## Planned Features

A future version will be able to discover and dump a list of devices on the network.
