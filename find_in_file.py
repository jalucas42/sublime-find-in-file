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


    
    
#### JAL: This is a good example of a quick panel
####    
###class InsertDatePanelCommand(sublime_plugin.TextCommand):
###
###    def on_done(self, index):
###
###        #  if user cancels with Esc key, do nothing
###        #  if canceled, index is returned as  -1
###        if index == -1:
###            return
###
###        # if user picks from list, return the correct entry
###        self.view.run_command(
###            "insert_my_text", 
###            {
###            	"args": {
###            		'text': self.list[index]
###            	}
###            }
###        );
###
###    def run(self, edit):
###
###    	# this will populate the quick_panel with 4 date formats
###        d1 = str(datetime.datetime.now())
###        d2 = str(datetime.date.today())
###
###        d3 = datetime.date.today().strftime("%d %B %Y (%A)") + \
###            ' @ ' + datetime.datetime.now().strftime("%H:%M")
###
###        d4 = datetime.date.today().strftime("%A, %d-%B-%Y") + \
###            datetime.datetime.now().strftime(" %I:%M %p")
###
###        self.list = [d1, d2, d3, d4]
###
###        # show_quick_panel(items, on_done, <flags>, <default_index>)
###        # ref: http://www.sublimetext.com/forum/viewtopic.php?f=4&t=7139
###        # take the list, and place it in a quick_panel, make 3rd item
###        # default pick
###
###        self.view.window().show_quick_panel(self.list, self.on_done, 1, 2)
###
###
###class InsertMyText(sublime_plugin.TextCommand):
###
###    def run(self, edit, args):
###
###        # add this to insert at current cursor position
###        # http://www.sublimetext.com/forum/viewtopic.php?f=6&t=11509
###
###        self.view.insert(edit, self.view.sel()[0].begin(), args['text'])    
###        