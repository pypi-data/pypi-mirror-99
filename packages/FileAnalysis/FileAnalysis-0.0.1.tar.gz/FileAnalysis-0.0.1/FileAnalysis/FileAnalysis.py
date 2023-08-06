#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" This file analyze emergence of characters in file (to decrypt with statistics). """

###################
#    This file analyze emergence of characters in file (to decrypt with statistics).
#    Copyright (C) 2021  Maurice Lambert

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
###################

import matplotlib.pyplot as plt
from string import ascii_letters
from argparse import ArgumentParser
from typing import Dict

FRENCH_FREQUENCE = {
	"E" : 12.10,
	"A" : 7.11,
	"I" : 6.59,
	"S" : 6.51,
	"N" : 6.39,
	"R" : 6.07,
	"T" : 5.92,
	"O" : 5.02,
	"L" : 4.96,
	"U" : 4.49,
	"D" : 3.67,
	"C" : 3.18,
	"M" : 2.62,
	"P" : 2.49,
	"G" : 1.23,
	"B" : 1.14,
	"V" : 1.11,
	"H" : 1.11,
	"F" : 1.11,
	"Q" : 0.65,
	"Y" : 0.46,
	"X" : 0.38,
	"J" : 0.34,
	"K" : 0.29,
	"W" : 0.17,
	"Z" : 0.15,
}

class FileAnalysis:

	""" This class analyze emergence of characters. """

	def __init__(self, filename: str, alphabet_only: bool = False):
		self.filename = filename
		self.alphabet_only = alphabet_only
		self.encoded_letters = ascii_letters.encode()
		self.compteur = 0
		self.chars = {}

	def analysis_filecontent(self) -> Dict[str, int]:

		""" This function analyze file content. """

		with open(self.filename, "rb") as file:
			char = " "
			while char:
				char = file.read(1)
				if char:
					self.analysis_char(char)

		return self.chars

	def analysis_char(self, char: bytes) -> None:

		""" This function analyse a character. """

		if self.alphabet_only and char in self.encoded_letters:
			self.compteur += 1
			char = char.decode().upper()
			self.chars.setdefault(char, 0)
			self.chars[char] += 1
		elif not self.alphabet_only:
			self.compteur += 1
			char = chr(char[0])
			self.chars.setdefault(char, 0)
			self.chars[char] += 1

	def get_pourcent(self) -> Dict[str, float]:

		""" This function return pourcent from chars. """

		for char, emergence in self.chars.items():
			self.chars[char] = emergence / self.compteur * 100

		return self.chars

	def build_chart(self) -> None:

		""" This function use pyplot to build the chart from chars. """

		positions = range(len(self.chars))
		plt.bar(positions, self.chars.values())
		plt.xticks(positions, self.chars.keys())
		plt.title(f"File analysis: {self.filename}")
		plt.show()


def parse() -> ArgumentParser:

	""" This function parse arguments. """

	args = ArgumentParser(description="This programme analyze emergence of characters.")
	args.add_argument("--filename", "-f", help="Filename to analyze")
	args.add_argument("--french-emergence", "-F", help="Show french emergence.", default=False, action="store_true")
	args.add_argument("--alphabet-only", "-a", help="Show chart with alphabet only.", default=False, action="store_true")
	args.add_argument("--number", "-n", help="Show chart with emergence character number (default is pourcent).", default=False, action="store_true")

	return args


def main() -> None:
	args = parse().parse_args()
	if args.french_emergence:
		analysis = FileAnalysis("French emergence.")
		analysis.chars = FRENCH_FREQUENCE
		analysis.build_chart()
	elif args.filename:
		analysis = FileAnalysis(args.filename, alphabet_only=args.alphabet_only)
		analysis.analysis_filecontent()
		if not args.number:
			analysis.get_pourcent()
		analysis.build_chart()
	else:
		print(
			"ERROR use --filename/-f option or --french-emergence/-F option"
			"\nTo get help message use --help/-h"
		)
		exit(1)


if __name__ == "__main__":
	main()