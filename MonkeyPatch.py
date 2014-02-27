from Plugins.Plugin import PluginDescriptor
from Components.ActionMap import ActionMap
from Screens.InfoBarGenerics import InfoBarPlugins, InfoBarEPG, InfoBarSubtitleSupport, InfoBarInstantRecord, isStandardInfoBar
from Components.PluginComponent import plugins
from Components.VolumeControl import VolumeControl
from Screens.AudioSelection import AudioSelection, SubtitleSelection
from KeymapConfig import load_keymap
from Components.config import config

def InfoBarPlugins__init__(self):
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
		self.session.open(SubtitleSelection, self)
	except:
		pass

def openAutoLanguageSetup(self):
	from Screens.Setup import Setup
	if self.settings.menupage.getValue() == "subtitles": # PAGE_SUBTITLES
		self.session.open(Setup, "subtitlesetup")
	else:
		self.session.open(Setup, "autolanguagesetup")

def instantRecordIndefinitely(self):
	if isStandardInfoBar(self):
		ts = self.getTimeshift()
		if self.isInstantRecordRunning() or self.isTimerRecordRunning() or not ts is None and ts.isTimeshiftActive():
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

def autostart(reason, *args, **kwargs):
	global baseInfoBarPlugins__init__

	load_keymap(config.plugins.keymap.selected.value)

	if "session" in kwargs:
		if baseInfoBarPlugins__init__ is None:
			baseInfoBarPlugins__init__ = InfoBarPlugins.__init__

		print "[Keymap Config] Monkeypatching InfoBarPlugins"
		InfoBarPlugins.__init__ = InfoBarPlugins__init__
		InfoBarPlugins.showGraphEPG = showGraphEPG
		InfoBarPlugins.showYouTube = showYouTube
		InfoBarPlugins.showSoftcam = showSoftcam
		InfoBarPlugins.showMediaCenter = showMediaCenter
		InfoBarPlugins.volumeUp = volumeUp
		InfoBarPlugins.volumeDown = volumeDown
		InfoBarPlugins.switchRadioTV = switchRadioTV
		InfoBarPlugins.subtitleSelectionAlt = subtitleSelectionAlt
		InfoBarPlugins.instantRecordIndefinitely = instantRecordIndefinitely
		AudioSelection.openAutoLanguageSetup = openAutoLanguageSetup
