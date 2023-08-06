# Copyright 2019-2020 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

import csv
import os

import portmod.package
from portmod.globals import env


def execute(*args, **kwargs):
    return portmod.execute.execute(*args, **kwargs)


def create_file(path):
    """
    Returns the path to be used for redirection
    and adds it to the list of redirected paths
    """
    protect_dir = os.path.join(env.prefix().CONFIG_PROTECT_DIR)
    new_path = os.path.join(protect_dir, os.path.basename(path) + ".cfg_protect")
    if os.path.exists(new_path):
        num = 1
        new_path = new_path + "." + str(num)

        while os.path.exists(new_path):
            num += 1
            new_path, _ = os.path.splitext(new_path)
            new_path = new_path + "." + str(num)

    os.makedirs(protect_dir, exist_ok=True)
    csv_path = os.path.join(protect_dir, "cfg_protect.csv")
    if os.path.exists(csv_path):
        with open(csv_path, "r") as file:
            reader = csv.reader(file)

            if [path, new_path] not in reader:
                with open(csv_path, "a", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow([path, new_path])
    else:
        with open(csv_path, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([path, new_path])

    return new_path
