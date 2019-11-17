echo -e "Hello, $USER! \n*** MAKE SURE YOU ARE EXECUTING THIS SCRIPT FROM PYTHON_REPO DIRECTORY ***\nThis script will install all the necessary libraries and modules essential for a Linux system.... I realise this is a fresh installation... Pls co-operate with me and all this will be over soon... Have fun!\n"

sudo apt-get install dkms python3 python3-dev python3-pip python3-setuptools python3-tk vnstat vim espeak pacman portaudio19-dev speedtest-cli openssh-server magic-wormhole mpv chromium-browser qbittorrent youtube-dl dos2unix wakeonlan tlp vlc acpi git binwalk adb fastboot;

echo -e "\nInstalling essential python libraries, actually all the python libraries I have ever worked with!\n"

python3 -m pip install --user -r requirements.txt
