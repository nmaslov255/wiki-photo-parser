#!/usr/bin/python3
import argparse

argparser = argparse.ArgumentParser(
    description='Parser photos from wikipedia')

argparser.add_argument('persons', type=str,
    help='path to json file with persons from declarator')

args = argparser.parse_args()