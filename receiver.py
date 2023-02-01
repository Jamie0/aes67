import pipeline
from gi.repository import Gst

class Receiver(pipeline.Pipeline):
	def make_pipeline(self):
		launch = ("udpsrc address=%s port=5004 multicast-iface=%s ! " % (self.options.host, self.options.net) +
			"application/x-rtp, clock-rate=48000, channels=2 ! "
			"rtpjitterbuffer ! "
			"rtpL24depay ! "
			"audioconvert ! "
			"audioresample ! %s" % self.options.output)
			
		self.pipeline = Gst.parse_launch(launch)

	def activate(self):
		self.pipeline.get_by_name('rtpdepay').set_property('timestamp-offset', self.get_rtp_offset())
		self.pipeline.set_state(Gst.State.PLAYING)

