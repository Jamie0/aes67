import netifaces
import random
import time
import socket
import struct
import threading

CONTENT_TYPE = b"application/sdp\0"

class SAP(threading.Thread):
	def __init__(self, options):
		threading.Thread.__init__(self)
		self.options = options

		self.session_id = random.randint(1, 65536)
		self.session_version = self.session_id
		self.addr = netifaces.ifaddresses(options.net)[2][0]['addr']

		self.description = options.desc

		self.encoding = 'L24'
		self.sample_rate = 48000
		self.channels = 2

		self.ptp_mac = '08-00-00-ff-fe-00-00-1f'
		self.ptp_domain = 0

	def run(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.socket.bind((self.addr, 9875))

		while True:
			self.socket.sendto(self.generate_sdp(), ("239.255.255.255", 9875))
			time.sleep(15)

		self.socket.close()

	def generate_sdp(self):
		ip = list(map(int, self.options.host.split('.')))

		header = struct.pack("<BxHBBBB", 0x20, 0xEFEF, ip[0], ip[1], ip[2], ip[3])

		return header + CONTENT_TYPE + str.encode("\r\n".join([
			"v=0"
			"o=- %s %s IN IP4 %s" % (self.session_id, self.session_version, self.addr),
			"s=%s" % self.description,
			"c=IN IP4 %s/32" % self.addr,
			"t=0 0",
			"a=clock-domain:PTPv2 0",
			"m=audio 5004 RTP/AVP 96",
			"a=rtpmap:96 %s/%s/%s" % (self.encoding, self.sample_rate, self.channels),
			"a=sync-time:0",
			"a=framecount:48",
			"a=ptime:1",
			"a=medialk:direct=0",
			"a=ts-refclk:ptp=IEEE1588-2008:%s:%s" % (self.ptp_mac, self.ptp_domain),
			"a=recvonly",
			""
		]))


