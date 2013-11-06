from Plugins.Plugin import PluginDescriptor
from Screens.InfoBarGenerics import InfoBarPlugins
from Screens.AudioSelection import AudioSelection
from Components.PluginComponent import plugins
from Components.VolumeControl import VolumeControl
from Components.config import config
import KeymapConfig, MonkeyPatch
import keymapparser

def main(session, *args, **kwargs):
	print "[Keymap Config]"
	try:
		session.open(KeymapConfig.KeymapConfig)
	except Exception, e:
		print "[Keymap Config] Error:", e

def menu(session, *args, **kwargs):
	print "KWARGS", kwargs
	if session == "system":
		return [
			(_("Keymap Config"), main, "keymap_config", None)
		]
	return [ ]

def Plugins(*args, **kwargs):
	name = _("Keymap Config")
	descr = _("Config custom remote control keymaps")

	return [
		PluginDescriptor(where = PluginDescriptor.WHERE_MENU, fnc = menu, needsRestart = True),
		PluginDescriptor(where = PluginDescriptor.WHERE_SESSIONSTART, fnc = MonkeyPatch.autostart, needsRestart = True, weight = 99999999999)
	]