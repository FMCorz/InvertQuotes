# -*- coding: utf-8 -*-

"""
Invert Quotes

Plugin for Sublime Text 2 to convert single quotes to double quotes and vice versa

Copyright (c) 2012 Frédéric Massart - FMCorz.net

Licensed under The MIT License
Redistributions of files must retain the above copyright notice.

http://github.com/FMCorz/InvertQuotes
"""

import sublime, sublime_plugin

class InvertQuotesCommand(sublime_plugin.TextCommand):

	def __init__(self, view):
		sublime_plugin.TextCommand.__init__(self, view)

	def run(self, edit, invert_all = False):
		view = self.view
		regions = view.sel()

		for region in regions:

			if region.empty():
				whole_region = self.get_string_region(region)
				if not whole_region: continue
			else:
				whole_region = region
				
			if not invert_all:
				begin = sublime.Region(whole_region.begin(), whole_region.begin() + 1)
				end = sublime.Region(whole_region.end(), whole_region.end() - 1)

				if view.substr(begin) in ('"', "'") and view.substr(end) in ('"', "'"):
					view.replace(edit, begin, "'" if view.substr(begin) == '"' else '"')
					view.replace(edit, end, "'" if view.substr(end) == '"' else '"')

			else:
				from_position = whole_region.begin() -1
				while True:
					subregion = view.find('"|\'', from_position)

					if not subregion or not whole_region.contains(subregion):
						break

					view.replace(edit, subregion, "'" if view.substr(subregion) == '"' else '"')
					from_position = subregion.end()

	def get_string_region(self, region):
		region_begin = region.begin()
		region_end = region.end()

		if self.view.score_selector(region_begin, 'string'):
			while self.view.score_selector(region_begin - 1, 'string'):
				region_begin -= 1
				if region_begin <= 0:
					break
			while self.view.score_selector(region_end, 'string'):
				region_end += 1
				if region_end >= self.view.size():
					break
			region = sublime.Region(region_begin, region_end)

		else:
			region = None

		return region