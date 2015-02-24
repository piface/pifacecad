#!/bin/bash
#: Description: Configures Raspberry Pi for the IR Recevier on
#:              PiFace Control and Display.

MODULES_FILE="/etc/modules"
HARDWARECONF_FILE="/etc/lirc/hardware.conf"
LIRCD_FILE="/etc/lirc/lircd.conf"
BOOTCONFIG="/boot/config.txt"

#=======================================================================
# NAME: version less than or equal to
# DESCRIPTION: True if version in first arg <= version in second arg
#=======================================================================
verlte() {
    [  "$1" = "`echo -e "$1\n$2" | sort -V | head -n1`" ]
}

#=======================================================================
# NAME: version less than
# DESCRIPTION: True if version in first arg < version in second arg
#=======================================================================
verlt() {
    [ "$1" = "$2" ] && return 1 || verlte $1 $2
}

#=======================================================================
# NAME: issue_warning
# DESCRIPTION: Issues a warning about running this script.
#=======================================================================
issue_warning() {
    echo "This script will overwrite the following files:"
    echo $HARDWARECONF_FILE
    if [ verlt $(uname -r) 3.18 ]; then
        echo $MODULES_FILE
    else
        echo $BOOTCONFIG
    fi
    echo "Do you wish to continue?"
    select yn in "Yes" "No"; do
        case $yn in
            Yes ) break;;
            No ) exit;;
        esac
    done
}

#=======================================================================
# NAME: backup_file
# DESCRIPTION: Creates a backup of a file.
#=======================================================================
backup_file() {
    echo "Backing up $1."
    cp $1 $1.setup_pifacecad_lirc.backup
}

#=======================================================================
# NAME: install_lirc
# DESCRIPTION: Install LIRC.
#=======================================================================
install_lirc() {
    echo "Installing LIRC."
    apt-get install --assume-yes lirc || \
        { echo 'Installing LIRC failed.' ; exit 1; }
}

#=======================================================================
# NAME: setup_modules
# DESCRIPTION: Add appropriate kernel modules.
#=======================================================================
setup_modules() {
    if [ verlt $(uname -r) 3.18 ]; then
        # old way for enable modules
        echo "Configuring modules."
        backup_file $MODULES_FILE
        # add "lirc_dev" and "lirc_rpi gpio_in_pin=23" to $MODULES_FILE
        for line in "lirc_dev" "lirc_rpi gpio_in_pin=23"; do
            if ! grep -q "$line" $MODULES_FILE; then
                echo "$line" >> $MODULES_FILE
            fi
        done
    else
        # new way to enable IR (kernel v3.18+)
        line="dtoverlay=lirc-rpi,gpio_in_pin=23,gpio_in_pull=high"
        backup_file $BOOTCONFIG
        if ! grep -q "$line" $BOOTCONFIG; then
            echo "$line" >> $BOOTCONFIG
        fi
    fi
}

#=======================================================================
# NAME: setup_hardwareconf
# DESCRIPTION: Copies hardware conf
#=======================================================================
setup_hardwareconf() {
    echo "Configuring hardware."
    backup_file $HARDWARECONF_FILE

    # write to the hardware conf
    cat << EOF > $HARDWARECONF_FILE
# /etc/lirc/hardware.conf
#
# Arguments which will be used when launching lircd
LIRCD_ARGS="--uinput"
#
#Don't start lircmd even if there seems to be a good config file
#START_LIRCMD=false
#
#Don't start irexec, even if a good config file seems to exist.
#START_IREXEC=false
#
#Try to load appropriate kernel modules
LOAD_MODULES=true
#
# Run "lircd --driver=help" for a list of supported drivers.
DRIVER="default"
# usually /dev/lirc0 is the correct setting for systems using udev
DEVICE="/dev/lirc0"
MODULES="lirc_rpi"
#
# Default configuration files for your hardware if any
LIRCD_CONF=""
LIRCMD_CONF=""
EOF
}

#=======================================================================
# NAME: final_message
# DESCRIPTION: Install
#=======================================================================
final_message() {
    printf "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Now you must create an $LIRCD_FILE for your remote control.
Either download one from here:

    http://lirc.sourceforge.net/remotes/

Or generate one yourself with the following command:

    sudo irrecord -f -d /dev/lirc0 /etc/lirc/lircd.conf

For more information go to:

    http://piface.github.io/pifacecad/lirc.html#configuring-lirc

You will need to reboot.
"
}

#=======================================================================
# MAIN
#=======================================================================
# check if the script is being run as root
if [[ $EUID -ne 0 ]]
then
    printf 'This script must be run as root.\nExiting..\n'
    exit 1
fi

issue_warning
install_lirc
setup_modules
setup_hardwareconf
final_message
