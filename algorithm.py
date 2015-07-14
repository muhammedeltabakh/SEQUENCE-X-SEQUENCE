from scoreWindow import ScoreWindow

from gi.repository import Gtk as gtk


class Algorithm:
	
	def __init__(self):
	
		pass


	def run(self, first_seq, second_seq, win):
		
		values = {'first_gap': -4, 'next_gap': -1, 'match_gap': 0, 'same_letter': 10, 'same_group': 0, 'different_group': -5}
		
		letters = ['A', 'G', 'T', 'C']

		seq1 = ["A", "G"]
		seq2 = ["T", "C"]


		max_length = max(len(first_seq), len(second_seq))

		if len(first_seq) < len(second_seq):
			gap_num = max_length - len(first_seq)
			g = '-' * gap_num
			first_seq = g + first_seq

		elif (len(second_seq) < len(first_seq)):
			gap_num = max_length - len(second_seq)
			g = '-' * gap_num
			second_seq = g + second_seq

		length = max_length
		score = 0
		first_gap = False


		for i in range(0, length):
			
			l1 = first_seq[i]
			l2 = second_seq[i]


			if l1 == '-' and l2 == '-':
				score = score + values['match_gap']
			elif l1 == '-' or l2 == '-':
				if not first_gap:
					first_gap = True
					score = score + values['first_gap']
				else:
					score = score + values['next_gap']
			else:
				if l1 not in letters or l2 not in letters:
					self.show_message("Error", "The sequence contain letters other than A,G,T,C", win)
					return


				first_gap = False
				
				if l1 == l2:
					score = score + values['same_letter']
				elif l1 in seq1 and l2 in seq1:
					score = score + values['same_group']
				elif l1 in seq2 and l2 in seq2:
					score = score + values['same_group']
				else:
					score = score + values['different_group']

		scoreWin = ScoreWindow(win, first_seq, second_seq, score)
		scoreWin.run()
		scoreWin.destroy()


	def show_message(self, message1, message2, win):
		
		dialog = gtk.MessageDialog(win, 0, buttons=gtk.ButtonsType.OK, message_format=message1)

		dialog.format_secondary_text(message2)
		dialog.run()

		dialog.destroy()