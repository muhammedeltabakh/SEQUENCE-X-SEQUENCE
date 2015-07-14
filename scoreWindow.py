from gi.repository import Gtk as gtk

from gi.repository import Pango as pango


class ScoreWindow(gtk.Dialog):
	
	def __init__(self, parent, first_seq, second_seq, score):
		
		gtk.Dialog.__init__(self, "Score", parent, 0, (gtk.STOCK_OK, gtk.ResponseType.OK))

		self.set_size_request(600, 400)
		self.set_resizable(False)
		self.set_border_width(5)
		fontdesc = pango.FontDescription("monospace 16")

		ruller = self.generate_ruller(len(first_seq))

		box = self.get_content_area()

		# First Seq
		
		box.add(gtk.Label("First Sequence"))
		scrolled_window1 = gtk.ScrolledWindow()
		scrolled_window1.set_hexpand(True)
		scrolled_window1.set_vexpand(True)
		box.add(scrolled_window1)
		
		text_view1 = gtk.TextView()
		text_view1.set_editable(False)
		text_view1.modify_font(fontdesc)
		scrolled_window1.add(text_view1)

		buffer1 = text_view1.get_buffer()
		buffer1.set_text(first_seq + '\n' + ruller)

		# Separator
		
		box.add(gtk.Label(""))

		# Second Seq
		
		box.add(gtk.Label("Second Sequence"))
		scrolled_window2 = gtk.ScrolledWindow()
		scrolled_window2.set_hexpand(True)
		scrolled_window2.set_vexpand(True)
		box.add(scrolled_window2)
		
		text_view2 = gtk.TextView()
		text_view2.set_editable(False)
		text_view2.modify_font(fontdesc)
		scrolled_window2.add(text_view2)

		buffer2 = text_view2.get_buffer()
		buffer2.set_text(second_seq + '\n' + ruller)

		percent = score / (len(second_seq) * 10)
		percent = percent * 100
		percent = str(percent) + '%'
		box.add(gtk.Label("Score percent: " + percent))

		# Separator
		
		box.add(gtk.Label(""))
		box.add(gtk.Label(""))

		box.add(gtk.Label("Score = " + str(score)))

		self.show_all()


	def generate_ruller(self, length):
		
		ruller = [' '] * length
		ruller[0] = '0'

		for i in range(0, length):
			if i % 10 == 0:
				ruller[i:i+1] = str(i)

		ruller = str.join('', ruller)
		ruller = ruller.strip()
		return ruller