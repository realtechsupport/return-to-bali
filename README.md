# AI in Ethnobotany

<b>Introduction</b>

AI in Ethnobotany (AIE) is a collection of procedures that allow one to apply machine learning classification onto field videos. AIE’s goal is to facilitate the creation of under-represented knowledge in machine learning in general, and experimental datasets for neural network image classification in particular. AIE allows anyone with a mobile phone to create viable datasets for image classification and to train state of the art convolutional neural networks with these datasets.

Furthermore, AIE can extract text from video. 

This software and the bali-26 dataset are the basis for the ‘Return to Bali’ project that explores machine learning to support the representation of ethnobotanical knowledge and practices in Central Bali.
http://www.realtechsupport.org/new_works/return2bali.html 


<b>License</b>

Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)
Cite this software project as follows: ‘Catch&Release version1’


<b>Context</b>

AIE runs on Linux under Python3 and Flask with Chromium or Firefox. AIE uses the PyTorch framework to train and test image classifiers and connects to the Google Speech API (free) for speech processing. Library versions and dependencies are given in the requirements file. 
AIE has been tested on a desktop (i7-4770 CPU with 16GB of memory) and a laptop (i7-3667 CPU with 8GB of memory) with Ubuntu 18.04 TLS under kernels 5.2.8 and 5.3.0 with images sourced from .mp4 and .webm video (HD [1920 x 1080] at 30f/s; .mp4  H.264 encoded) from multiple (android OS) mobile phones and GoPro Hero 6 action cameras.

Recommended browser: Chromium. 
Install the free Classic Cache Killer:
https://chrome.google.com/webstore/detail/classic-cache-killer/kkmknnnjliniefekpicbaaobdnjjikfp?hl=en 



<b>Software Installation</b>

Clone the AIE repository on GitHub
Open a terminal window and type:

	git clone https://github.com/realtechsupport/ai-ethnobotany.git
	Username for 'https://github.com': realtechsupport
	Password for 'https://realtechsupport@github.com'
	<enter the access token> 


Cd to the ai-ethnobotany directory and  run the following commands to update your basic python environment:

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


Generate an STT key (optional)

While there are multiple providers of Speech to Text services, the most effective offering with the widest range of languages is at this moment provided by Google. If you want to make use of the text from video extraction you should obtain an access key to the Google Speech API. Creation of this key is free of charge and you can use it in this software at no cost as AIE operates within free limits of the API. However, you do require a google account in order to create the key. If that is not palatable, skip the section that makes use of the Speech API.

Instructions to generate a key:

    1. Navigate to the APIs & Services->Credentials panel in Cloud Platform Console.
    2. Select Create credentials, then select API key from the dropdown menu.
    3. Click the Create button. ... 
    4. Once you have the API key, download it and create a JSON file.
    5. Save to the AIE project


<b>Launch AIE</b>

Activate the virtual environment:		

	source ./env/bin/activate
	
Run the program:

	(in the ai-ethnobotany directory)    	
	python3 main.py chromium no-debug

To run in debug mode replace’ no-debug’ with ‘debug’. Firefox is also supported, but less stable.
The terminal window will display comments. You should see the launch screen in a browser window:  
AI in Ethnobotany

crtl +  /  ctrl – 	increase / decrease zoom factor.

Stop the app from the terminal:					
ctrl-c

Exit environment at the terminal:				
ctrl-d

If you see browser errors .. clear the browsing history: 	
ctrl-H
clear browsing data
clear data

<i>Check the README.pdf file in the repository for a detailed description on how to use the modules in AIE.</i>
