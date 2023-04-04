from __future__ import print_function
from argparse import ArgumentParser, FileType

import datetime
from PyPDF2 import PdfFileReader
import sys

parser = argparse.ArgumentParser('Metadata from PDF')
parser.add_argument('PDF_FILE', help='Path to PDF file',type=FileType('rb'))
args = parser.parse_args()

pdf_file = PdfFileReader(args.PDF_FILE)
xmpm = pdf_file.getXmpMetadata()

if xmpm is None:
   print("No XMP metadata found in document.")
   sys.exit()

custom_print("Title: {}", xmpm.dc_title)
custom_print("Creator(s): {}", xmpm.dc_creator)
custom_print("Contributors: {}", xmpm.dc_contributor)
custom_print("Subject: {}", xmpm.dc_subject)
custom_print("Description: {}", xmpm.dc_description)
custom_print("Created: {}", xmpm.xmp_createDate)
custom_print("Modified: {}", xmpm.xmp_modifyDate)
custom_print("Event Dates: {}", xmpm.dc_date)

def custom_print(fmt_str, value):
   if isinstance(value, list):
      print(fmt_str.format(", ".join(value)))
   elif isinstance(value, dict):
      fmt_value = [":".join((k, v)) for k, v in value.items()]
      print(fmt_str.format(", ".join(value)))
   elif isinstance(value, str) or isinstance(value, bool):
      print(fmt_str.format(value))
   elif isinstance(value, bytes):
      print(fmt_str.format(value.decode()))
   elif isinstance(value, datetime.datetime):
      print(fmt_str.format(value.isoformat()))
   elif value is None:
      print(fmt_str.format("N/A"))
   else:
      print("warn: unhandled type {} found".format(type(value)))

if xmpm.custom_properties:
   print("Custom Properties:")
   
   for k, v in xmpm.custom_properties.items():
      print("\t{}: {}".format(k, v))
