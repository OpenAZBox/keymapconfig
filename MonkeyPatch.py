from Plugins.Plugin import PluginDescriptor
from Components.ActionMap import ActionMap
from Screens.InfoBarGenerics import InfoBarPlugins, InfoBarEPG, InfoBarSubtitleSupport, InfoBarInstantRecord #InfoBarAudioSelection
from Components.PluginComponent import plugins
from Components.VolumeControl import VolumeControl
from KeymapConfig import KeymapConfig.load_keymap
from Components.config import config

def InfoBarPlugins__init__(self):
	KeymapConfig.load_keymap(config.plugins.keymap.selected.value)

	if isinstance(self, InfoBarEPG):
		self.vol = VolumeControl(self.session)
		
		self["EPGActions"] = ActionMap(["InfobarEPGActions", "InfobarChannelSelection"],
		{
			"showGraphEPG": self.showGraphEPG,
			"showSoftcam": self.showSoftcam,
			"showYouTube": self.showYouTube,
			"showMediaCenter": self.showMediaCenter,
			"volumeUp": self.volumeUp,
			"volumeDown": self.volumeDown,
			"showEventInfo": self.openEventView,
			"switchRadioTV": self.switchRadioTV,
		})

	if isinstance(self, InfoBarSubtitleSupport):
		self["SubtitleSelectionAction"] = ActionMap(["InfobarSubtitleSelectionActions"],
		{
			"subtitleSelection": self.subtitleSelectionAlt,
		})

	if isinstance(self, InfoBarInstantRecord):
		self["InstantRecordActions"] = ActionMap(["InfobarInstantRecord"],
		{
			"instantRecord": self.instantRecord,
			"instantRecordIndefinitely": self.instantRecordIndefinitely,
		})

	baseInfoBarPlugins__init__(self)

def showGraphEPG(self):
	for p in plugins.getPlugins(where = PluginDescriptor.WHERE_EXTENSIONSMENU):
		if p.name == _("Graphical Multi EPG"):
			self.runPlugin(p)
			break

def showYouTube(self):
	for p in plugins.getPlugins(where = PluginDescriptor.WHERE_EXTENSIONSMENU):
		if p.name == _("My TubePlayer"):
			self.runPlugin(p)
			break

def showMediaCenter(self):
	try:
		from Plugins.Extensions.MediaCenter.plugin import DMC_MainMenu
		self.session.open(DMC_MainMenu)
	except:
		try:
			from RTiTeam.Panel import Panel
			self.session.open(Panel)
		except:
			try:
				from Plugins.Extensions.MediaPlayer.plugin import MediaPlayer
				self.session.open(MediaPlayer)
			except:
				pass

def subtitleSelectionAlt(self):
	try:
		from Screens.AudioSelection import SubtitleSelection
		self.session.open(SubtitleSelection, self)
	except:
		pass

def instantRecordIndefinitely(self):
	if self.isInstantRecordRunning():
		self.instantRecord()
	else:
		self.startInstantRecording()

def volumeUp(self):
	self.vol.volUp()

def volumeDown(self):
	self.vol.volDown()

RADIO_MODE = False
def switchRadioTV(self):
	global RADIO_MODE

	if RADIO_MODE:
		RADIO_MODE = False
		self.showTv()
	else:
		if config.usage.e1like_radio_mode.value:
			RADIO_MODE = True
		self.showRadio()

def showSoftcam(self):
	try:
		try:
			from Plugins.PLi.SoftcamSetup.Sc import ScSelection
			self.session.open(ScSelection)
		except:
			from Plugins.Extensions.CAMDManager.plugin import CAMDManager
			self.session.open(CAMDManager)
	except:
		from Screens.PluginBrowser import PluginBrowser
		self.session.open(PluginBrowser)

baseInfoBarPlugins__init__ = None
