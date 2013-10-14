from Plugins.Plugin import PluginDescriptor
import keymapparser
from Screens.InfoBarGenerics import InfoBarPlugins, InfoBarEPG, InfoBarSubtitleSupport
from Components.PluginComponent import plugins
from Components.VolumeControl import VolumeControl
from Components.config import config
import KeymapConfig, MonkeyPatch

def autostart(reason, **kwargs):
	if "session" in kwargs:
		session = kwargs["session"]
		if MonkeyPatch.baseInfoBarPlugins__init__ is None:
			MonkeyPatch.baseInfoBarPlugins__init__ = InfoBarPlugins.__init__

		print "[Keymap Config] Monkeypatching InfoBarPlugins"
		InfoBarPlugins.__init__ = MonkeyPatch.InfoBarPlugins__init__
		InfoBarPlugins.showGraphEPG = MonkeyPatch.showGraphEPG
		InfoBarPlugins.showYouTube = MonkeyPatch.showYouTube
		InfoBarPlugins.showSoftcam = MonkeyPatch.showSoftcam
		InfoBarPlugins.showMediaCenter = MonkeyPatch.showMediaCenter
		InfoBarPlugins.volumeUp = MonkeyPatch.volumeUp
		InfoBarPlugins.volumeDown = MonkeyPatch.volumeDown
		InfoBarPlugins.switchRadioTV = MonkeyPatch.switchRadioTV
		InfoBarPlugins.subtitleSelectionAlt = MonkeyPatch.subtitleSelectionAlt
		InfoBarPlugins.instantRecordIndefinitely = MonkeyPatch.instantRecordIndefinitely

def main(session, **kwargs):
	print "[Keymap Config]"
	try:
		session.open(KeymapConfig.KeymapConfig)
	except Exception, e:
		print "[Keymap Config] Error:", e

def menu(session, **kwargs):
	if session == "system":
		return [
			(_("Keymap Config"), main, "keymap_config", None)
		]
	return [ ]

def Plugins(**kwargs):
	name = _("Keymap Config")
	descr = _("Config custom remote control keymaps")

	return [
		PluginDescriptor(where = PluginDescriptor.WHERE_MENU, fnc = menu, needsRestart = True),
		PluginDescriptor(where = PluginDescriptor.WHERE_SESSIONSTART, fnc = autostart, needsRestart = True, weight = 99999999999)
	]