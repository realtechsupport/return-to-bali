# Return to Bali

<b>Introduction</b>

Return to Bali’s goal is to facilitate the creation of under-represented knowledge in machine learning in general, and experimental datasets for neural network image classification in particular. Return to Bali applies these procedures to the study of Ethnobotany on the island of Bali where Mead and Bateson, of second order cybernetics fame, collected field data for the book <i>Balinese Character: A Photographic Analysis </i> (1942). 

While Bali has been subject to numerous exploitative practices, this project aims to bend machine learning to collect data responsibly and to assess if machine learning might help maintain the body of local ecological knowledge that has been documented as declining specifically amongst Balinese youth. 

Return to Bali includes a dataset, bali-26, produced from field videos documenting 26 ethnobotanically significant plants of South East Asia, several of which are indigenous to the island of Bali. The videos show the plants in multiple stages of growth and include fruits, leaves, branches and bark where applicable, from multiple locations within the field study site of Central Bali and under varying lighting conditions.

The high definition mobile phone video files shot by data collectors in the field were converted to labeled images with the <a href="https://github.com/realtechsupport/c-plus-r"> Catch & Release </a> software package.

The software modules included here allow one to parse text from video interviews and to experiment with image classification approaches on the bali-26 data set, the first small collection of ethnobotanically significant plants of South East Asia made amendable to neural network based image classification. The project demonstrates that even the best machine learning algorithms struggle to understand  the visual complexity contained in this image set.

<a href="http://www.realtechsupport.org/new_works/return2bali.html">Additional Documentation</a>

<b>License</b>

Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)
Cite this software project as follows: ‘Return to Bali version1’


<b>Context</b>

Return to Bali runs on Linux and Mac OS under Python3 and Flask with Chromium or Firefox. 

The software uses the PyTorch framework to train and test image classifiers and connects to the Google Speech API (free) for speech processing. Library versions and dependencies are given in the requirements file.
The software has been tested on a desktop (i7-4770 CPU with 16GB of memory) and a laptop (i7-3667 CPU with 8GB of memory) under Ubuntu (20. 04 LTS and 18.04 TLS under kernels 5.2.8 and 5.3.0 ) and under Mac OS (Catalina) with images sourced from .mp4 and .webm video (HD [1920 x 1080] at 30f/s; .mp4 H.264 encoded) from multiple (android OS) mobile phones and GoPro Hero 6 action cameras.


<b> Browser installation </b>

Recommended browser: Chromium.

Install Chromium on Ubuntu:
sudo apt install -y chromium-browser

Install Chromium on Mac OS:
https://apple.stackexchange.com/questions/78805/chromium-builds-for-mac-os-x/215426#215426

(Currently recommended method)

Install the free Classic Cache Killer:
https://chrome.google.com/webstore/detail/classic-cache-killer/kkmknnnjliniefekpicbaaobdnjjikfp?hl=en


<b>Software Installation</b>

Clone the Return to Bali repository on GitHub
Open a terminal window and type:

	git clone https://github.com/realtechsupport/ai-ethnobotany.git
 

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

While there are multiple providers of Speech to Text services, the most effective offering with the widest range of languages is at this moment provided by Google. If you want to make use of the text from video extraction you should obtain an access key to the Google Speech API. Creation of this key is free of charge and you can use it in this software at no cost as this project operates within free limits of the API. However, you do require a google account in order to create the key. If that is not palatable, skip the section that makes use of the Speech API.

Instructions to generate a key:

    1. Navigate to the APIs & Services->Credentials panel in Cloud Platform Console.
    2. Select Create credentials, then select API key from the dropdown menu.
    3. Click the Create button. ... 
    4. Once you have the API key, download it and create a JSON file.
    5. Save to the AIE project


<b>Launch Return to Bali</b>

Activate the virtual environment:		

	source ./env/bin/activate
	
Run the program:   

	python3 main.py browser debug_mode

browser = firefox or chromium; debug_mode = debug or no-debug. The terminal window will display comments. You should see the launch screen in a browser window.

	crtl +  /  ctrl – 	increase / decrease zoom factor.

Stop the app from the terminal:					
	ctrl-c

Exit environment at the terminal:				
	ctrl-d

If you see browser errors .. clear the browsing history: 	
	ctrl-H
	clear browsing data
	clear data

<i>Check the README.pdf file in the repository for a detailed description on how to use the modules.</i>
