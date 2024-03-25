# Scene data set generation using Chat-GPT and DALL-E

Generating data sets of scenes is time-consuming to produce: many scenes need
to be photographed and painstakingly labeled. This repository contains code to
accelerate this process by generating a bulk of scene descriptions via Chat-GPT
and then rendering them using DALL-E.

## Example Scenes

- 'Alice and Bob are drinking coffee in a cafe.'
- 'Bob is drinking coffee. Alice is cleaning up.'

# Installation and Setup

## Installation Dependencies

This wrapper uses Python 3+. Tested on Python 3.8.10, but should work on any
other version of Python. Python package dependencies are `openai`, `argparse`,
and `pyyaml`, which can all be installed using the provided `requirements.txt`
file:

```
python3 -m pip install -r requirements.txt
```

## Configuration Setup

To configure a set of potential scenes, we consider a handful of viable parameters:

- Number of potential people in a scene (either a fixed integer or range of
  integers)
- Names of potential people in a scene (or blank, to randomly generate names)
- Potential settings ('in a cafe', 'at the park', etc.). Samples must be
  provided, and can be either used verbatim or can be used to generate
  additional examples.
- Potential actions ('drinking coffee', 'cleaning up', etc.). Samples must be
  provided, and can be either used verbatim or can be used to generate
  additional examples.

## Running

With a configuration file ready, they can be provided to `data_gen.py`. Use the
`-c` flag to specify a single configuration file, or `-d` to specify a directory containing
multiple configuration files.
