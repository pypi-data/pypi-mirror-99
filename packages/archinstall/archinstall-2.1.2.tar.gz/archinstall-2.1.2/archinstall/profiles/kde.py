# A desktop environement using "KDE".

import archinstall, os

# TODO: Remove hard dependency of bash (due to .bash_profile)

def _prep_function(*args, **kwargs):
	"""
	Magic function called by the importing installer
	before continuing any further. It also avoids executing any
	other code in this stage. So it's a safe way to ask the user
	for more input before any other installer steps start.
	"""

	# KDE requires a functioning Xorg installation.
	profile = archinstall.Profile(None, 'xorg')
	with profile.load_instructions(namespace='xorg.py') as imported:
		if hasattr(imported, '_prep_function'):
			return imported._prep_function()
		else:
			print('Deprecated (??): xorg profile has no _prep_function() anymore')

# Ensures that this code only gets executed if executed
# through importlib.util.spec_from_file_location("kde", "/somewhere/kde.py")
# or through conventional import kde
if __name__ == 'kde':
	# Install dependency profiles
	installation.install_profile('xorg')

	# Install the application kde from the template under /applications/
	kde = archinstall.Application(installation, 'kde')
	kde.install()

	# Enable autostart of KDE for all users
	installation.enable_service('sddm')
