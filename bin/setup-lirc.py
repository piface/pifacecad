def setup_lirc():
    # setup /etc/modules
    # check if lines are already there
    write_lirc_dev = write_lirc_rpi = True
    with open('/etc/modules', 'r') as modfile:
        for line in modfile:
            if "lirc_dev" in line:
                write_lirc_dev = False
            if "lirc_rpi gpio_in_pin=23" in line:
                write_lirc_rpi = False
    # write them
    if write_lirc_dev or write_lirc_rpi:
        with open('/etc/modules', 'a') as modfile:
            if write_lirc_dev:
                modfile.write("lirc_dev\n")
            if write_lirc_rpi:
                modfile.write("lirc_rpi gpio_in_pin=23\n")

    # setup /etc/lirc/hardware.conf
    shutil.copyfile(
        "/etc/lirc/hardware.conf", "/etc/lirc/hardware.conf.backup")
    # TODO make this grab the file from the web
    shutil.copyfile("lirc_hardware.conf", "/etc/lirc/hardware.conf")
    os.chmod(
        "/etc/lirc/hardware.conf",
        stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR |
        stat.S_IRGRP | stat.S_IXGRP |
        stat.S_IROTH | stat.S_IXOTH)

    # install lirc
    run_cmd(INSTALL_LIRC_CMD, "Failed to install lirc.")

    # point to documentation
    print(
        "\n\n\tYou will need to generate a key map for your remote.\n"
        "\tSee: {}\n\n".format(KEY_MAP_INSTRUCTIONS))


if __name__ == '__main__':
    setup_lirc()
