import socket
import threading

class SAP(threading.Thread)
	def __init__(self, options):
		threading.Thread.__init__(self)
		self.options = options

	def generate_sdp(self):
		return "\r\n".join([
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
			"a=mediaclk:direct=0",
			"a=ts-refclk:ptp=IEEE1588-2008:%s" % self.ptp_mac,
			"a=recvonly"
		])


