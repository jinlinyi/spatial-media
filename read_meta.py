"""
read mp4 metadata
"""

import argparse
import os
import re
import sys

path = os.path.dirname(sys.modules[__name__].__file__)
path = os.path.join(path, '..')
sys.path.insert(0, path)
from spatialmedia import metadata_utils, mpeg


def print_layer(layer, path=''):
  if path:
    path += ' -> '
  path += layer.name.decode('utf-8')

  if layer.contents:
    for content in layer.contents:
      print_layer(content, path)
  else:
      print(path)

def seek_layer(layer, hierarchy, depth=0):
  if depth + 1>= len(hierarchy):
    return layer
  # Check if current layer matches the current level in hierarchy
  if layer.name.decode('utf-8') == hierarchy[depth]:
    # # If this is the last element in the hierarchy, return this layer
    # if depth == len(hierarchy) - 1:
    #   return layer

      # Otherwise, continue searching in the contents
    if layer.contents:
      for content in layer.contents:
        found_layer = seek_layer(content, hierarchy, depth + 1)
        if found_layer:
          return found_layer
  return None



def main():
  """Main function for printing and injecting spatial media metadata."""

  parser = argparse.ArgumentParser(
      usage=
      "%(prog)s [options] [files...]\n\nBy default prints out spatial media "
      "metadata from specified files.")
  parser.add_argument("file", nargs="+", help="input/output files")

  args = parser.parse_args()
  infile = os.path.abspath(args.file[0])
  with open(infile, "rb") as in_fh:
    mpeg4_file = mpeg.load(in_fh)
  # reference https://docs.google.com/document/d/1M2c_2HHhuJtBZUhx3zSbvT1Lbxyp1FFQ8C_KltuZV7g/edit?tab=t.0
  # hierarchy = [
  #   'moov', 'trak', 'mdia', 'minf', 'stbl', 'stsd', 'avc1'
  # ]
  # hierarchy = [
  #   'moov', 'trak', 'mdia', 'minf', 'stbl', 'stsd', 'camm'
  # ]
  hierarchy = [
    'moov', 'trak', 'mdia', 'minf', 'stbl', 'stsd', 'avc1'
  ]
  content_idx = []
  print_layer(mpeg4_file.moov_box)
  layer = seek_layer(mpeg4_file.moov_box, hierarchy, depth=0)
  mpeg4_file.print_structure()
  breakpoint()



  return


if __name__ == "__main__":
  main()
