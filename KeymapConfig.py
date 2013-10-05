from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.Sources.List import List
from Components.Sources.StaticText import StaticText
from Tools.LoadPixmap import LoadPixmap
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_CURRENT_SKIN
import keymapparser
import os

from Components.config import config, ConfigSubsection, ConfigText

config.plugins.keymap = ConfigSubsection()
config.plugins.keymap.selected = ConfigText()

def load_keymap(keymap, keymaplist = []):
	if os.path.isfile(keymap):
		keymaplist.append(("/usr/share/enigma2/keymap.xml", None, None))
		keymaplist.append(("/usr/lib/enigma2/python/Plugins/Extensions/CutListEditor/keymap.xml", None, None))
		keymaplist.append(("/usr/lib/enigma2/python/Plugins/Extensions/setupGlass16/keymap.xml", None, None))

		keymaplist = set(k[0] for k in keymaplist)

		for k in keymaplist:
			if not os.path.isfile(k) or k == keymap: continue

			try:
				keymapparser.removeKeymap(k)
			except:
				pass

		try:
			print "[KEYMAP CONFIG] Loading '%s'" % keymap
			keymapparser.readKeymap(keymap)
			return True

		except:
			print "[KEYMAP CONFIG] Could not load keymap file '%s'" % keymap
			print "[KEYMAP CONFIG] This plugin will not work properly..."

	return False



class KeymapConfig(Screen):
	skin = """
<screen position="fill" title="Keymap Config" flags="wfNoBorder" >
	<panel name="PigTemplate"/>
	<!--panel name="ButtonTemplate_2S"/-->
	<panel name="ButtonTemplate_RGS"/>

	<widget source="config" render="Listbox" position="590,110" size="600,512" scrollbarMode="showOnDemand" enableWrapAround="1"  selectionDisabled="1">
		<convert type="TemplatedMultiContent">
			{"template": [
				MultiContentEntryPixmapAlphaBlend(pos = (4, 2), size = (24, 24), png = 3),
				MultiContentEntryText(pos = (32, 0), size = (1000, 32), font=0, flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 1),
			],
			"fonts": [gFont("Regular", 20)],
			"itemHeight": 32
			}
		</convert>
	</widget>
</screen>"""

	def __init__(self, session):
		Screen.__init__(self, session)

		self["shortcuts"] = ActionMap(["WizardActions", "DirectionActions", "ColorActions"],
		{
			"ok": self.ok,
			"back": self.exit,
			"cancel": self.exit,
			"red": self.exit,
			"green": self.save,
		})

		self.keymap_paths = [
			"/usr/lib/enigma2/python/Plugins/Extensions/KeymapConfig/keymap/",
			"/media/hdd/keymap/",
			"/media/cf/keymap/",
			"/media/mmc1/keymap/",
			"/media/usb/keymap/"
		]

		self.list = []
		self["config"] = List(self.list)

		self["key_red"] = StaticText(_("Cancel"))
		self["key_green"] = StaticText(_("Save"))

		self.selected = 0

		self.onShow.append(self.on_load)

	def on_load(self):
		self.update_list()

	def exit(self):
		self.close()

	def ok(self):
		self.selected = self["config"].getIndex()
		self.set_selected()

	def set_selected(self):
		for k, item in enumerate(self.list):
			item = list(item)
			item[3] = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, "skin_default/icons/lock_off.png"))
			self["config"].modifyEntry(k, tuple(item))

		item = list(self.list[self.selected])
		item[3] = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, "skin_default/icons/lock_on.png"))
		self["config"].modifyEntry(self.selected, tuple(item))
		self["config"].setIndex(self.selected)

	def save(self):
		current = self.list[self.selected]

		if load_keymap(current[0], self.list):
			config.plugins.keymap.selected.value = current[0]
			config.plugins.keymap.save()
			self.exit()

	def update_list(self):
		self.list = []
		selected = 0

		self.list.append((
			"/usr/share/enigma2/keymap.xml",
			_("Default"),
			"/usr/share/enigma2/keymap.xml",
			LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, "skin_default/icons/lock_off.png")),
		))

		for path_item in self.keymap_paths:
			path = os.path.normpath(path_item)

			for root, dirnames, filenames in os.walk(path):
				for filename in sorted(filenames):
					if filename[0] == ".": continue
					title, ext = os.path.splitext(filename)
					ext = ext.strip().lower()

					if ext == ".xml":
						keymap_path = "%s/%s" % (root, filename)

						if keymap_path == config.plugins.keymap.selected.value:
							self.selected = len(self.list)

						self.list.append((
							keymap_path,
							title,
							keymap_path.replace('/usr/lib/enigma2/python/Plugins/', './'), # description
							LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, "skin_default/icons/lock_off.png")),
						))
				break

		self["config"].setList(self.list)
		self.set_selected()
