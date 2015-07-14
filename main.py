#!/bin/python

from gui import GUI

from gi.repository import Gtk as gtk


def main():
	
	win = GUI("Sequence X Sequence")
	win.show_all()
	gtk.main()


if __name__ == "__main__":
	main()
