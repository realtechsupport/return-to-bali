#!/usr/bin/env python3
# stt.py
# utilities for STT
# Catch+Release
# Flask interface for linux computers
# experiments in knowledge documentation; with an application to AI for ethnobotany
#spring 2020
# tested on ubuntu 18 LTS, kernel 5.3.0
#-------------------------------------------------------------------------------
import sys, os
from av_helper import *
from utilities import *
from stt_helper import *

#-------------------------------------------------------------------------------
def extract_text(app, videofile, language, startsecs, duration, chunk, tconfidence, maxattempts, searchterm, authsource):
    print2screen = True
    #cpath = os.getcwd()
    cpath = app.config['TMP']
    now = strftime("%Y-%m-%d_%H:%M", gmtime())
    videoname = videofile.split('/')[-1] + '_'
    textlog = app.config['TMP'] +'s2tlog_' + videoname + now +'.txt'
    encoding = 'wav'
    path_audioinput = extract_audio_from_video(videofile, encoding)
    audioinput = path_audioinput.split('/')[-1]
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = authsource

    #create the slices
    destination = app.config['TMP']
    starts=[]
    starts = make_slices_from_audio(cpath, videofile, audioinput, startsecs, duration, chunk, destination, onechan=True)

    #transcribe each slice
    afiles=[]
    p, d, files = next(os.walk(destination))
    token = '1ch_16k'
    for file in files:
        if (token in file):
            afiles.append(file)
        else:
            pass

    afiles.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
    f_count = len(files)
    j=0
    results=[]
    searchresults=[]
    print('afiles: ', len(afiles)); print('starts: ', len(starts))

    for file in afiles:
        transcript, confidence = transcribe_longrunning_audio(destination+file, language, maxattempts)
        print('transcript length: ', len(transcript))
        #print(transcript, confidence)
        time.sleep(3)
        if (print2screen):
            for i in range (len(transcript)):
                if(confidence[i] >= tconfidence):
                    tr_confidence = '%.4f'%(confidence[i])
                    transcript[i] = transcript[i].lower()   #search is case sensitive
                    message = '... start: ' + str(starts[j]) + ' ... ' + 'text: ' + transcript[i] + ' ... ' + 'confidence: ' + str(tr_confidence)
                    print(i, j, message)

                    write2file(textlog, file + '\n')
                    write2file(textlog, starts[j] + '\n')
                    write2file(textlog, str(confidence[i]) + '\n')
                    write2file(textlog, transcript[i] + '\n\n')
                    results.append(message)

                    if(searchterm != ''):
                        if(searchterm in transcript[i]):
                            searchresults.append(message)

        j=j+1
    #turn this empty until you use it again
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = ''
    return(results, searchresults)

#-------------------------------------------------------------------------------
