import pipeline
from gi.repository import Gst
from sap import SAP

class Sender(pipeline.Pipeline):
	def make_pipeline(self):
		launch = (("%s !" % self.options.input) +
			"audioconvert ! audio/x-raw, format=S24BE, channels=2, rate=48000 ! "
			"rtpL24pay name=rtppay min-ptime=1000000 max-ptime=1000000 ! "
			"application/x-rtp, clock-rate=48000, channels=2, payload=98 ! "
			"udpsink host=%s port=5004 qos=true qos-dscp=34 multicast-iface=%s" % (self.options.host, self.options.net))

		self.pipeline = Gst.parse_launch(launch)

		self.sap = SAP(self.options)
		self.sap.start()

	def activate(self):
		self.pipeline.get_by_name('rtppay').set_property('timestamp-offset', self.get_rtp_offset())
		self.pipeline.set_state(Gst.State.PLAYING)


