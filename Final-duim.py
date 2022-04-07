#!/usr/bin/env python3

import subprocess, sys
import os
import argparse
from argparse import ArgumentTypeError as err


def parse_command_args():
    "Set up argparse here. Call this function inside main."
    parser = argparse.ArgumentParser(
        description="DU Improved -- See Disk Usage Report with bar charts",
        epilog="Copyright 2022",
    )
    parser.add_argument(
        "-l",
        "--length",
        type=int,
        default=20,
        help="Specify the length of the graph. Default is 20.",
    )

    # add argument for "human-readable". USE -H, don't use -h! -h is reserved for --help which is created automatically.
    parser.add_argument(
        "-H",
        "--human-readable",
        default="M",
        metavar="",
        help="print sizes in human readable format (e.g. 1K 23M 2G) ",
    )

    # check the docs for an argparse option to store this as a boolean.

    # add argument for "target". set number of args to 1.
    parser.add_argument("target", type=str, help="The directory to scan.")
    args = parser.parse_args()
    return args


def readable_dir(read_dir):
    if not os.path.isdir(
        read_dir
    ):  # Use the os function to check if path entered exists or not
        raise err(
            "readable_dir:{0} is not a valid path".format(read_dir)
        )  # raise error if path is wrong
    if os.access(read_dir, os.R_OK):
        call_du_sub(read_dir)  # call the call_du_sub function if the path is right
    else:
        raise err("readable_dir:{0} is not a readable dir".format(read_dir))


def percent_to_graph(percent, scale):
    "Will take two arguments and convert the percentage to a horizontal graph with default scale as 20 (100%)"
    ret = ""  # Creating an empty string
    if percent >= 0 or percent <= 100:  # Checking against any ValueError
        ret += (
            "'" + round(percent / 100 * scale) * "#"
        )  # Rounding Percentage and multiply with the '#' represent the used storage
        ret += (
            round((1 - percent / 100) * scale) * " " + "'"
        )  # Filling the remaining space with blank spaces
        return ret
    else:
        return "Error: Percent value error"


def call_du_sub(location):
    "Use subprocess to call `du -d 1 + location`, rtrn raw list"

    p = subprocess.Popen(
        ["du", "-d 1", location], stdout=subprocess.PIPE
    )  # Calling the Subprocess using Popen and putting it into variable p
    stdout = p.communicate()[0].decode("utf-8")  # Decode the output string
    stdout_arr = stdout.split(
        "\n"
    )  # Splitting the String into list with each argument having two values
    stdout_arr_split = [x.split("\t") for x in stdout_arr][
        :-1
    ]  # Splitting the List further having a list into list which will have two values seperated by commas.
    create_dir_dict(stdout_arr_split)


def create_dir_dict(raw_data):
    "get list from du_sub, return dict {'directory': 0} where 0 is size"

    size = int(
        raw_data[-1][0]
    )  # Passing the total size of the folder into a variable and removing it from the actual list
    raw_data = raw_data[:-1]
    location = x.target
    for (
        item
    ) in (
        raw_data
    ):  # Loop into the list with item_size =  size of the file and item_name = name of the file path
        item_size, item_name = item
        item_percentage = (
            int(item_size) / size * 100
        )  # Calculating the percentage and passing the value into percent_to_graph function
        graph = percent_to_graph(item_percentage, max)

        if hm == "K":  # Use Kb if secified by the user
            print(f"{int(item_percentage):>3}% {graph}\t{item_size:>7}kB\t{item_name}")
        elif hm == "M":  # Use Mb if secified by the user
            item_size = int(item_size) / 1000
            print(f"{int(item_percentage):>3}% {graph}\t{item_size:>7}MB\t{item_name}")
        else:  # Else use Gb
            item_size = int(item_size) / 1000000
            print(f"{int(item_percentage):>3}% {graph}\t{item_size:>7}GB\t{item_name}")

    if hm == "K":
        print("total folder size: ", size, "kB\t", "Selected directory: ", location)
    elif hm == "M":
        size = int(size) / 1000
        print("total folder size: ", size, "MB\t", "Selected directory: ", location)
    else:
        size = int(size) / 1000000
        print("total folder size: ", size, "GB\t", "Selected directory: ", location)


if __name__ == "__main__":
    x = parse_command_args()
    max = x.length
    hm = x.human_readable
    readable_dir(x.target)
