This plugin aims to fix some remote control usability issues that probably will never be addresed by the oficial E2 core images managers, offering the ability to choose between customized keymaps and some extended events.

After you install the package, is recommended to restart your E2 to make it work properly.

You can choose your desired keymap under Setup > System > Keymap Config. Choose your desired keymap with OK. Activate it and save your selection using the green button. Exit or red button will cancel any changes you made.

It was developed using OpenPLi 3 (by OpenRSI), and may not work properly on other or older images.

Attention: If you are using my older plugin "keymap by pingflood", you are encouraged to uninstall that plugin and use this one (if this one works for you). The previous keymap plugin is deprecated and will not be updated anymore, and will conflicts with this one if you use both together.

Included with this plugin you will find four basic keymaps for the AzBox HD and Me series, one of them using regular AzBox zap mode and other using the legacy DM mode zap.

You are free (and encouraged) to create (and share) your own keymaps in order to meet your needs.

You can save your own keymaps in the same base path you use for picons, this way your custom files will be retained even if you upgrade or delete this plugin.

The paths scanned by this plugin are: "/media/hdd/keymap/", "/media/cf/keymap/", "/media/mmc1/keymap/", "/media/usb/keymap/". 

Store your keymap with a short but descriptive name (.xml extension). In the filename, preferably use plain ASCII text, without special characters. The name of the file will be used to list your keymap inside the plugin.

If you need some inspiration, you can start copying your original image keymap, usually found at "/usr/share/enigma2/keymap.xml", or edit any of the bundled keymaps found in "/usr/lib/enigma2/python/Plugins/Extensions/KeymapConfig/keymap/". Don't forget to always have a backup of any file you edit, in order to be able to revert if anything go wrong.

New events (considering the original keymap):
"showGraphEPG": Open Graphical EPG plugin,
"showSoftcam": Open Softcam manager plugin,
"showYouTube": Open myTube plugin,
"showMediaCenter": Open MediaCenter / MediaPlayer plugin,
"volumeUp": Audio volume up,
"volumeDown": Audio volume down,
"switchRadioTV": Toggles between Radio and TV mode,
"subtitleSelection": Open subtitle selection screen,
"instantRecordIndefinitely": Instantly start an indefinitely recording (no menu is shown) with a short press on recording button. Instant record menu is shown with a long press on recording button.

This events (and the regular ones) are mapped in a manner that it should be intuitive and easy to find in your remote control. It could be better than currently is, but unfortunately some buttons (AzBox Premium RC) was never mapped on kernel, so this is what we can have for now. I'll not document every key action here because I don't think is really necessary, but I'm sure you will find the function you need while using it.


DISCLAIMER

This plugin is distributed as is. It may not work on some setups and may stop working at any moment if the E2 core images managers change something this plugin relies (key names mapped on kernel, classes and function names, other plugins that conflicts with this one, etc.)

This plugin is open source and you are free to use it for non commercial purposes. Code thieves, closed images and any one that you have to "donate" to use (payment disguised) are NOT welcome to use any part of this code.
