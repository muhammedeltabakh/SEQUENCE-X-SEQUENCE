from gi.repository import Gtk as gtk

from Bio import AlignIO

from algorithm import Algorithm

import urllib.request


class GUI(gtk.Window):

	def __init__(self, title):
		
		gtk.Window.__init__(self, title=title)
		self.set_size_request(0, 600)
		self.set_resizable(False)
		self.set_border_width(5)
		self.connect('delete-event', gtk.main_quit)

		self.algorithm = Algorithm()

		self.file_type = 'fasta'
		self.first_seq = ""
		self.second_seq = ""

		self.main_box = gtk.Box(spacing=5, orientation=gtk.Orientation.VERTICAL)
		self.add(self.main_box)

		self.add_logo()
		self.add_file_type_radio_buttons()

		self.add_first_squence_widgets()
		self.main_box.pack_start(gtk.Label(), False, False, 0)
		self.add_second_squence_widgets()

		self.add_controls_buttons()


	def add_logo(self):
		
		logo_img = gtk.Image.new_from_file("logo.png")
		self.main_box.pack_start(logo_img, False, False, 0)


	def add_file_type_radio_buttons(self):
		
		hbox = gtk.Box(spacing = 5)
		self.main_box.pack_start(hbox, False, False, 0)

		fasta_radio_button = gtk.RadioButton.new_with_label_from_widget(None, "FASTA")
		fasta_radio_button.connect("toggled", self.file_type_toggled, "fasta")
		hbox.pack_start(fasta_radio_button, True, True, 0)

		genbank_radio_button = gtk.RadioButton.new_with_label_from_widget(fasta_radio_button, "GenBank")
		genbank_radio_button.connect("toggled", self.file_type_toggled, "genbank")
		hbox.pack_start(genbank_radio_button, True, True, 0)


	def add_first_squence_widgets(self):
		
		# label
		
		seq_label = gtk.Label("First Sequence")
		self.main_box.pack_start(seq_label, False, False, 0)

		# direct input
		
		scrolled_window = gtk.ScrolledWindow()
		scrolled_window.set_hexpand(True)
		scrolled_window.set_vexpand(True)
		self.main_box.pack_start(scrolled_window, True, True, 0)
		text_view = gtk.TextView()
		self.first_seq_text_buffer = text_view.get_buffer()
		scrolled_window.add(text_view)

		# file input
		
		hbox = gtk.Box(spacing=5)
		self.main_box.pack_start(hbox, False, False, 0)
		choose_file_button = gtk.Button(label="Choose File")
		hbox.pack_start(choose_file_button, False, False, 0)

		self.first_seq_file_entry = gtk.Entry()
		self.first_seq_file_entry.set_placeholder_text("File Path")
		self.first_seq_file_entry.set_editable(False)
		hbox.pack_start(self.first_seq_file_entry, True, True, 0)
		choose_file_button.connect('clicked', self.choose_file_callback, self.first_seq_file_entry)

		# online input with accession number
		
		self.first_seq_online_entry = gtk.Entry()
		self.first_seq_online_entry.set_placeholder_text("ID Number")
		self.main_box.pack_start(self.first_seq_online_entry, False, False, 0)


	def add_second_squence_widgets(self):
		
		# label
		
		seq_label = gtk.Label("Second Sequence")
		self.main_box.pack_start(seq_label, False, False, 0)

		# direct input
		
		scrolled_window = gtk.ScrolledWindow()
		scrolled_window.set_hexpand(True)
		scrolled_window.set_vexpand(True)
		self.main_box.pack_start(scrolled_window, True, True, 0)
		text_view = gtk.TextView()
		self.second_seq_text_buffer = text_view.get_buffer()
		scrolled_window.add(text_view)

		# file input
		
		hbox = gtk.Box(spacing=5)
		self.main_box.pack_start(hbox, False, False, 0)
		choose_file_button = gtk.Button(label="Choose File")
		hbox.pack_start(choose_file_button, False, False, 0)

		self.second_seq_file_entry = gtk.Entry()
		self.second_seq_file_entry.set_placeholder_text("File Path")
		self.second_seq_file_entry.set_editable(False)
		hbox.pack_start(self.second_seq_file_entry, True, True, 0)
		choose_file_button.connect('clicked', self.choose_file_callback, self.second_seq_file_entry)

		# online input with accession number
		
		self.second_seq_online_entry = gtk.Entry()
		self.second_seq_online_entry.set_placeholder_text("ID Number")
		self.main_box.pack_start(self.second_seq_online_entry, False, False, 0)


	def add_controls_buttons(self):
		
		hbox = gtk.Box(spacing=5)
		self.main_box.pack_start(hbox, False, False, 0)

		exit_button = gtk.Button("Exit")
		exit_button.connect('clicked', gtk.main_quit)
		hbox.pack_start(exit_button, True, True, 0)

		calculate_button = gtk.Button('Calculate')
		calculate_button.connect('clicked', self.calculate)
		hbox.pack_start(calculate_button, True, True, 0)


	def choose_file_callback(self, button, seq_file_entry):
		
		dialog = gtk.FileChooserDialog("Please choose a file", self,
        	gtk.FileChooserAction.OPEN,
        	(("_Cancel"), gtk.ResponseType.CANCEL,
        		("_Open"), gtk.ResponseType.OK))

		self.add_filters(dialog)

		response = dialog.run()
		if response == gtk.ResponseType.OK:
			seq_file_entry.set_text(dialog.get_filename())
		elif response == gtk.ResponseType.CANCEL:
			pass

		dialog.destroy()


	def add_filters(self, dialog):
		
		filter_text = gtk.FileFilter()
		filter_text.set_name("Text files")
		filter_text.add_mime_type("text/plain")
		dialog.add_filter(filter_text)

		filter_any = gtk.FileFilter()
		filter_any.set_name("Any files")
		filter_any.add_pattern("*")
		dialog.add_filter(filter_any)


	def file_type_toggled(self, button, name):
		
		if button.get_active():
			self.file_type = name


	def calculate(self, button):
	
		self.get_first_seq()
		self.get_second_seq()

		if (len(self.first_seq) == 0):
			self.show_message("Error", "The first sequence is missed")
			return

		if (len(self.second_seq) == 0):
			self.show_message("Error", "The second sequence is missed")
			return

		self.algorithm.run(self.first_seq, self.second_seq, self)


	def get_first_seq(self):
		
		start_buf, end_buf = self.first_seq_text_buffer.get_bounds()
		seq_direct = self.first_seq_text_buffer.get_text(start_buf, end_buf, False).upper()

		seq_file = self.first_seq_file_entry.get_text()
		seq_online = self.first_seq_online_entry.get_text()

		if (seq_direct):
			self.first_seq = seq_direct

		if (seq_file):
			align = AlignIO.read(seq_file, self.file_type)
			self.first_seq = str(align[0].seq)


		if (seq_online):
			if self.file_type == 'fasta':
				f_type = 'fasta'
			elif self.file_type == 'genbank':
				f_type = 'gb'

			url = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nucleotide&amp;id='+seq_online+'&amp;rettype='+f_type+''
			f = urllib.request.urlopen(url)
			result = f.read().decode('utf-8')
			if len(result) < 10:
				self.show_message("Error", "Failed to retrieve the first sequence (please check your ID Number)")
				return
			else:
				file_name = "cache/"+seq_online+"."+self.file_type+""
				file = open(file_name, "w")
				file.write(result)
				file.close()
				align = AlignIO.read(file_name, self.file_type)
				self.first_seq = str(align[0].seq)


	def get_second_seq(self):
		
		start_buf, end_buf = self.second_seq_text_buffer.get_bounds()
		seq_direct = self.second_seq_text_buffer.get_text(start_buf, end_buf, False).upper()

		seq_file = self.second_seq_file_entry.get_text()
		seq_online = self.second_seq_online_entry.get_text()

		if (seq_direct):
			self.second_seq = seq_direct

		if (seq_file):
			align = AlignIO.read(seq_file, self.file_type)
			self.second_seq = str(align[0].seq)


		if (seq_online):
			if self.file_type == 'fasta':
				f_type = 'fasta'
			elif self.file_type == 'genbank':
				f_type = 'gb'

			url = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nucleotide&amp;id='+seq_online+'&amp;rettype='+f_type+''
			f = urllib.request.urlopen(url)
			result = f.read().decode('utf-8')
			if len(result) < 10:
				self.show_message("Error", "Failed to retrieve the second sequence (please check your ID Number)")
				return
			else:
				file_name = "cache/"+seq_online+"."+self.file_type+""
				file = open(file_name, "w")
				file.write(result)
				file.close()
				align = AlignIO.read(file_name, self.file_type)
				self.second_seq = str(align[0].seq)


	def show_message(self, message1, message2):
		
		dialog = gtk.MessageDialog(self, 0, buttons=gtk.ButtonsType.OK, message_format=message1)

		dialog.format_secondary_text(message2)
		dialog.run()

		dialog.destroy()