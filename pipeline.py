import gi
import sys
import threading

gi.require_version('Gst', '1.0')
gi.require_version('GstNet', '1.0')

from gi.repository import Gst, GstNet, GObject, GLib

Gst.init()

class Pipeline(threading.Thread):
	def __init__(self, options):
		threading.Thread.__init__(self)
		self.options = options

	def make_pipeline(self):
		pass

	def make_clock(self):
		if not GstNet.ptp_init(GstNet.PTP_CLOCK_ID_NONE, [self.options.net]):
			raise Exception("Could not initialise PTP")

		self.clock = GstNet.PtpClock.new('PTP-Master', 0)
		self.clock.wait_for_sync(Gst.CLOCK_TIME_NONE)

	def reset_time(self):
		self.pipeline.set_start_time(Gst.CLOCK_TIME_NONE)
		self.pipeline.set_base_time(self.clock.get_time())

	def get_rtp_offset(self):
		return round((self.clock.get_time()) * (48000 / 1000000000)) & 0xffffffff

	def activate(self):
		pass

	def run(self):
		try:
			self.make_clock()
			self.make_pipeline()
			self.reset_time()
			self.activate()

			self.loop = GLib.MainLoop()
			self.loop.run()
		except:
			traceback.print_exc()
			sys.exit(1)	
