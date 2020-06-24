import os
import sys

try:
	directory = "/"   # Starting directory
	root = False

	green = "\u001b[32m"
	red = "\u001b[31m"
	bold = "\u001b[1m"
	reset = "\u001b[0m"

	if os.geteuid() == 0: root = True	# Check if running as root
	else: root = False

	def pyfm():
		global directory
		
		os.system("clear")	# Clear the window
		
		files = []
		filesAmount = 0
			
		print(red + bold + "Root: " + str(root) + reset)		      # Display root status
		print(green + bold + "Directory: " + reset + directory)	      # Display current directory
		
		for file in os.listdir(directory):
			filesAmount += 1
			files.append(file)

		print(green + bold + "Files found: " + reset + str(filesAmount))    # Display the amount of files found
		print()
		
		lineLength = 20 # Display width is 40 but 20 is the length of the lines
		cursor = 0
		rows = 2	# Display found files 2 rows
		
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
						sys.stdout.write(green + bold + printFile + reset + "`"*emptySpace)
						cursor += 1
						
				print()	# Seperate lines from each other
				
		else: print(" "*int(lineLength/2*2 - len("~~ EMPTY ~~")/2) + "~~ EMPTY ~~")	# Center the text
		
		print(red + "="*lineLength*2 + reset)



		# Change directory -------------------------------
		while True:
			cd = input(bold + "\ncd: " + reset)
			if cd == ".." and directory != "/":
				directory = directory[:-1]

				while True:				
					if directory[-1] == "/":
						pyfm()
						break

					else: directory = directory[:-1]

			elif cd == "cmd" or cd == "commandline" or cd == "command":
				command = input(red + "commandline > " + reset)
				os.system(command)

			elif cd not in files:
				print(red + "Directory not found!" + reset)

			else:
				try:
					directory += cd + "/"
					pyfm()
					break

				except(PermissionError):
					print()
					print(red + "="*lineLength*2 + reset)
					print(bold + "Can't access to this directory\nwithout root privileges!" + reset)
					print(red + "="*lineLength*2 + reset)


	pyfm()
	
except(KeyboardInterrupt):
	os.system("clear")
