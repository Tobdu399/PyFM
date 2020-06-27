#!/usr/bin/python3
import os
import sys
lineLength = 20

try:
	directory = "/"   # Starting directory
	root = False

	green = "\u001b[32m"
	blue = "\u001b[36m"
	yellow = "\u001b[33m"
	red = "\u001b[31m"
	bold = "\u001b[1m"
	reset = "\u001b[0m"

	if os.geteuid() == 0: root = True	# Check if running as root
	else: root = False

	def pyfm():
		global lineLength
		global directory
		_, consoleWidth = os.popen('stty size', 'r').read().split()	# Get console width
		
		os.system("clear")	# Clear the window
		
		_, _, fileFound = next(os.walk(directory))
		
		files = []
		otherFiles = []
		otherFiles.append(fileFound)
		
		filesAmount = len(files)	# Total amount of the files
			
		if root == True: print(red + "Root: " + str(root) + reset)	# Display root status
		
		for file in os.listdir(directory):
			filesAmount += 1
			files.append(file)

		print(green + bold + "Current directory: " + reset + directory)      # Display current directory
		print(green + bold + "Files found: " + reset + str(filesAmount))
		print()
		
		emptySpace = ""
		cursor = 0
		rows = 2	# Display found files 2 rows
		
		emptySpace = lineLength*2 - len("dir")-len("file")
		print(blue + bold + "dir" + reset + " "*emptySpace + yellow + bold + "file" + reset)
		print(red + "="*lineLength*2 + reset)	# Print line using "=" depending on the given lineWidth

		if len(files) != 0:
			for _ in range(0, len(files), rows):
				for _ in range(0, rows):
					if cursor != len(files):
						printFile = files[cursor]
						
						# 3 for the three dots
						if len(printFile) > lineLength-3:
							# 5 for 2 empty spaces after the dots

							while len(printFile) > lineLength-5:
								printFile = printFile[:-1]

							printFile += "..."

						emptySpace = int(lineLength) - len(printFile)
						if printFile in otherFiles[0]: sys.stdout.write(yellow + printFile + reset + "`"*emptySpace)
						else: sys.stdout.write(blue + printFile + reset + "`"*emptySpace)
						
						cursor += 1
						
				print()	# Seperate lines from each other
				
		else: print(" "*int(lineLength/2*2 - len("EMPTY")/2) + "EMPTY")	# Center the text
		
		print(red + "="*lineLength*2 + reset)



		# Change directory -------------------------------
		while True:
			cd = input(bold + "\ncd/cmd: " + reset)
			
			try:
				# Check if user is trying to change the width
				cmd, arg = cd.split(" ")
				if cmd == "width":
					if arg == "max" or arg == "full":
						width = int(consoleWidth)/2
						lineLength = round(width)
					
					elif arg == "default" or arg == "normal": lineLength = 20	
					elif isinstance(int(arg), int): lineLength = int(arg)

					pyfm()
					break
				
				else: print(red + "Command not found!" + reset)
						

			# If this exception happens, user is propably trying to change the directory
			except(ValueError):
				if cd == ".." and directory != "/":
					directory = directory[:-1]

					while True:				
						if directory[-1] == "/":
							pyfm()
							break

						else: directory = directory[:-1]
						

				elif cd == "update" or cd == "clear":
					pyfm()
					break
					

				elif cd == "cmd" or cd == "commandline" or cd == "command" or cd == "shell":
					command = input(red + "shell > " + reset)
					os.system(command)
					
				elif cd == "exit":
					os.system("clear")
					exit()


				elif cd not in files:
					print(red + "Directory not found!" + reset)


				else:
					try:
						directory += cd + "/"
						pyfm()
						break

					except(PermissionError, StopIteration):
						print(green + bold + "Requested: " + reset + directory)
						print()
						print(red + "="*lineLength*2 + reset)
						print("Can't access to this directory\nwithout root privileges " + red + bold + "or" + reset +\
						" it is a file!")
															
						print(red + "="*lineLength*2 + reset)


	pyfm()	# Start program
	
except(KeyboardInterrupt):
	os.system("clear")
	exit()
