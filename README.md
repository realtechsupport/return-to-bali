# Return to Bali

![alt text](https://github.com/realtechsupport/return-to-bali/blob/master/snakefruit_bamboo_dragonfruit.png?raw=true)

<b>Introduction</b>

Return to Bali’s goal is to facilitate the creation of under-represented knowledge in machine learning in general, and experimental datasets for neural network image classification in particular. Return to Bali applies these procedures to the study of Ethnobotany on the island of Bali where Mead and Bateson, of second order cybernetics fame, collected field data for the book <i>Balinese Character: A Photographic Analysis </i> (1942). 

While Bali has been subject to numerous exploitative practices, this project aims to bend machine learning to collect data responsibly and to assess if machine learning might help maintain the body of local ecological knowledge that has been documented as declining specifically amongst Balinese youth. 

Return to Bali includes a dataset, bali-26, produced from field videos documenting 26 ethnobotanically significant plants of South East Asia, several of which are
indigenous to the island of Bali. The videos show the plants in multiple stages of growth and include fruits, leaves, branches and bark where applicable, from
multiple locations within the field study site of Central Bali and under varying lighting conditions. It also includes several instances of some of the plants (such as snakefruit).
at local markets.

The high definition mobile phone video files shot by data collectors in the field were converted to labeled images with the <a href="https://github.com/realtechsupport/c-plus-r"> Catch & Release </a> software package.

The bali-26 data set is the first (minor) collection of ethnobotanically significant plants of South East Asia made amendable to neural network based image classification. As such, it
expands the domain of machine learning to include forms of knowledge that have not yet been represented. And on a purely technical level, the project demonstrates
that even the best machine learning algorithms struggle to understand the visual complexity contained in the rich flora of Bali captured in the wild.

<a href="http://www.realtechsupport.org/new_works/return2bali.html">Additional Documentation</a>

<b>License</b>

Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)
Cite this software project as follows: ‘Return to Bali version1’


<b>Context</b>

Return to Bali runs on Linux and Mac OS under Python3 and Flask with Chromium or Firefox. 
Recommended browser: Chromium.


<br>Project members</b>

Raunaq Jain, Wawan Sujarwo, Varun Chandola, Marc Böhlen


<b>Software Installation</b>

Clone the Return to Bali repository from GitHub.
Open a terminal window and type:

	git clone https://github.com/realtechsupport/return-to-bali.git
 

Cd to the project directory and run the following commands to update the python environment:

	chmod +x basics.sh
	sudo sh basics.sh

(This script just updates your Ubuntu installation and requires sudo to do so.)


Create a virtual environment:

	python3 -m venv env

Activate the environment:

	source ./env/bin/activate

Cd to to the ai-ethnobotany directory again. Install Requirements and Dependencies.
(This may take about 30 minutes.)

	pip3 install -r requirements.txt


<b>Launch Return to Bali</b>

Activate the virtual environment:

	source ./env/bin/activate
	
Run the program in the project directory:

	python3 main.py ubuntu firefox debug 			or 
	python3 main.py mac chromium no-debug

Specify all three items: OS, browser and debug mode. Supported OS: Ubuntu and Mac OS. 
Supported browsers: Chromium and Firefox (less stable). To run in debug mode replace’ no-debug’ with ‘debug’. 

The terminal window will display comments. You should see the launch screen in a browser window.


<i>Check the README_details.pdf file in the repository for a detailed description on how to use the modules.</i>
