import argparse

parser = argparse.ArgumentParser(description="AES67 Utility")
subparsers = parser.add_subparsers(help="sub-command help", dest="mode")

parser.add_argument("--host", type=str, help="The broadcast address (239.69.0.0/16) for AES67 data", required=True)
parser.add_argument("--net", type=str, help="The network interface name", default="eth0", required=False)


parser_tx = subparsers.add_parser("tx", help="Transmit mode")
parser_tx.add_argument("--input", type=str, help="GStreamer audio source string", default="autoaudiosrc")

parser_rx = subparsers.add_parser("rx", help="Transmit mode")
parser_rx.add_argument("--output", type=str, help="GStreamer audio sink string", default="autoaudiosink")

args = parser.parse_args()
print(args)

if args.mode == "tx":
	from sender import Sender
	sender = Sender(args)
	sender.start()
	sender.join()
elif args.mode == "rx":
	from receiver import Receiver
	receiver = Receiver(args)
	receiver.start()
	receiver.join()
