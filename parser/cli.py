#!/usr/bin/python3
import argparse

argparser = argparse.ArgumentParser(
    description='Parser photos from wikipedia')

argparser.add_argument('persons', type=str,
    help='path to json file with persons from declarator')

argparser.add_argument('out', type=str,
    help='path to save results')

argparser.add_argument('--start-from', type=str,
    help="File with last results. \
    Needed for start since the collapse of the program")

args = argparser.parse_args()