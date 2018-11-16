import sublime
import sublime_plugin
import re
import datetime

class FindInFileCommand(sublime_plugin.TextCommand):
	
	def run(self, edit):

		# Create a 'find_in_files' output panel, or fetch the existing one.
		win   = sublime.active_window()
		panel = win.create_output_panel("find_in_files_panel")
		win.run_command('show_panel',{"panel":"output.find_in_files_panel"})
		
		# Set the file and line regexes.  This allows us to double-click lines in the output panel
		# and jump to the original code.  Note that if the line regex matches, sublime will search backward
		# to find a file regex to use.  That's how we get the file/line pair.
		panel.settings().set("result_file_regex", r"^In file: '(.+?)'");
		panel.settings().set("result_line_regex", r"^(\d+):");
		
		# Make the panel writeable.  If it already existed from a previous search, it would be read-only.
		panel.set_read_only(False);

		# Get the selection text as the search term.  Only take the first selection region if there are multiple.
		# TODO: Pretty sure there is a more efficient way to do this without a one-iteration loop.
		selection = self.view.sel()
		search_term = "";
		for region in selection:
			search_term = self.view.substr(region);
			break;

		# Print the search information.
		panel.run_command("append", {"characters": "Searching for '" + search_term + "'\n"})
		panel.run_command("append", {"characters": "In file: '" + self.view.file_name() + "'\n\n"});
		
		# Halt if search term is empty.
		if (len(search_term) == 0):
			panel.run_command("append", {"characters": "Search term is blank!\n"});
		
		else:		
			# Add the matching lines to the output panel.
			matching_regions = self.view.find_all(search_term, sublime.IGNORECASE);
			for region in matching_regions:
				region = self.view.line(region);
				region_text = self.view.substr(region)
				(row,col) = self.view.rowcol(region.begin())
				panel.run_command("append", {"characters": "%04d: %s%s\n" % (row+1, region_text, " " * 200)})		

		# Make the panel read-only.
		panel.set_read_only(True);
