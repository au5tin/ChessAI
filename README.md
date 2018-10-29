#################################
#           !My Code!           #
#################################
Code for the AI is located in ...
/Jouer.py/games/chess/ai.py
and
/Jouer.py/games/chess/ai_utilities.py

#################################
#          !IMPORTANT!          #
#################################

Read the README in the sub-directory corresponding to your chosen language.  

Read the chess framework's documentation for your chosen language here : http://docs.siggame.io/chess/ 

#################################
#       Compiling & Running	#
#################################

You have been provided a bash script called "play.sh", which compiles and runs your code; it also starts a game session between your AI and itself. DO NOT MODIFY THIS SCRIPT.
You can run "play.sh" using the following command format :

	./play.sh Joueur.<lang> Session_ID testRunArg1 ... testRunArgN

Where Joueur.<lang> is the directory for the language you are coding in and where testRunArg# is an optional argument that is accepted by the provided testRun script. An example of the above command for c++ would be :

	./play.sh Joueur.cpp AIisAwesome

	./play.sh Joueur.cpp AIisAwesome --gameSettings fen=b6k%2F8%2F8%2F8%2F5p2%2F6q1%2F4P3%2F7K%20w%20K%20-%200%201

You can find some helpful FEN strings in the file FEN.txt. There are FENs for testing castling, en passant and check.

You can find a more advanced play.sh script in the adv_tools sub-directory. It can play multiple games, redirect game output to files, check output files for win/draw/stalemate/error in bulk, run a local server, run against a different client on the same computer, run on the forge, run on a specified server address, and supports all arguments you could provide to testRun. Run ./play.sh --help to see usage.
