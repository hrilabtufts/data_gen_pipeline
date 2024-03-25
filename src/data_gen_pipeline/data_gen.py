#!/usr/bin/env python3

import openai
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config_file_path", "-c", type=str, required=True)
