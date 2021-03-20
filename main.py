#!/usr/bin/env python3
# main.py
# Return to Bali
# spring 2021
# tested on ubuntu 18 LTS, kernel 5.3.0
#-------------------------------------------------------------------------------
#1. start virtual env
#2. launch the program
# python3 main.py ubuntu firefox debug, or
# python3 main.py mac chromium no-debug\' for example.

# OS: ubuntu or mac. Browsers: chromium or firefox.
#(works on Mac OS as well)

# issue: can not get flask-caching to work properly
# solution: Classic Cache Killer for Chrome; after install check options (right click, enable at start)

# update
# aroid is in fact suweg. Update across the complete project later.
# adjust not (see lines 190 ff
# adjust testclassifiers.html (see line 30)
#------------------------------------------------------------------------------
import sys, os, time, shutil, glob
import eventlet, json
import random, threading, webbrowser
from flask import Flask, flash, current_app, send_file, render_template, request, redirect, url_for, session, send_from_directory
from flask_socketio import SocketIO, emit
from werkzeug.utils import secure_filename

from stt import *
from av_helper import *
from inputs import *
from utilities import *
from similarities import *
from pyt_utilities import *
from maps_sats import *
from collect_weatherdata_Bali import *
#-------------------------------------------------------------------------------

satref_url = 'https://filedn.com/lqzjnYhpY3yQ7BdfTulG1yY/AIE_maps/'
weatherref_url = 'https://filedn.com/lqzjnYhpY3yQ7BdfTulG1yY/AIE_weather/BaliBotanicalGardenWeather_Ref.csv'
weathercurrent_url = 'https://filedn.com/lqzjnYhpY3yQ7BdfTulG1yY/AIE_weather/AIE_weather.csv'
seasons_url = 'https://filedn.com/lqzjnYhpY3yQ7BdfTulG1yY/AIE_context/seasons.csv'
events_url = 'https://filedn.com/lqzjnYhpY3yQ7BdfTulG1yY/AIE_context/events.csv'
interview_url = 'https://filedn.com/lqzjnYhpY3yQ7BdfTulG1yY/AIE_context/darmaja_interview_1min.webm'
weatherref_file = 'refweatherdata.csv'
weathercurrent_file = 'weather.csv'

#-------------------------------------------------------------------------------
app = Flask(__name__, template_folder="templates")
cwd = app.root_path

t_dir = cwd + '/tmp/';
s_dir = cwd + '/static/';       i_dir = cwd + '/images/'
m_dir = cwd + '/models/';       c_dir = cwd + '/collection/'
r_dir = cwd + '/results/';      ar_dir = cwd + '/archive/'
f_dir = cwd + '/find/';         cl_dir = cwd + '/classify/'
te_dir = cwd + '/tests/';       co_dir = cwd + '/context/'

dirs = [t_dir, s_dir, i_dir, m_dir, c_dir, r_dir, ar_dir, f_dir, cl_dir, te_dir, co_dir]
for dir in dirs:
    if not os.path.exists(dir):
        os.makedirs(dir)

app.config['SECRET_KEY'] = 'you-will-not-guess'
app.config['TMP'] = t_dir;      app.config['STATIC'] = s_dir
app.config['IMAGES'] = i_dir
app.config['MODELS'] = m_dir;   app.config['COLLECTION'] = c_dir
app.config['RESULTS'] = r_dir;  app.config['FIND'] = f_dir
app.config['ARCHIVE'] = ar_dir; app.config['CLASSIFY'] = cl_dir
app.config['TESTS'] = te_dir;   app.config['CONTEXT'] = co_dir

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

socketio = SocketIO(app, async_mode="eventlet")
#------------------------------------------------------------------------------
@app.route('/')
@app.route('/index')
def index():
    session.clear()
    formats = ('*.json', '*.webm', '*.wav', '*.mp4', '*.MP4', '*.txt', '*.zip', '*.prof', '*.mkv', '*.jpg', '*.csv', '*.pth')
    locations = ('STATIC', 'TMP', 'IMAGES', 'RESULTS')
    exception = 'voiceover'

    try:
        removefiles(app, formats, locations, exception)
    except:
        pass

    if not os.path.exists(i_dir):
        os.makedirs(i_dir)

    template = 'index.html'
    return render_template(template)

#-------------------------------------------------------------------------------
@app.route('/testclassifiers', methods=['GET', 'POST'])
def testclassifiers():
    form = TestClassifiers()
    comment = ''; morecomments = []
    choice = ''; input = ''; images = ''; files = ''; c_classifier = ''
    result = ''; moreresults = ''; tp_vals = []
    template = 'testclassifiers.html'

    if (request.method == 'POST'):
        testcollection = form.testcollection.data
        print('test collection is: ', testcollection)
        location = os.path.join(app.config['FIND'], testcollection)
        zfile = os.path.join(app.config['FIND'], testcollection) + '.zip'

        # -------------------------------------
        # move section to utilities
        try:
            path, dirs, files = next(os.walk(location))
        except:
            pass

        if(len(files) == 0):
            if(testcollection == 'bali26samples'):
                archive = bali26_samples_zip
            elif(testcollection == 'balimixedplants'):
                archive = bali_mixedplants_zip
            else:
                archive = bali26_samples_zip

            '''
            print('this is the archive: ', archive)
            print('this is the testcollection', testcollection)
            '''
            print('downloading the samples...')
            wget.download(archive, zfile)
            shutil.unpack_archive(zfile, app.config['FIND'], 'zip')
            os.remove(zfile)
        #----------------------------------

        images = os.listdir(location)

        if("display" in request.form):
            session['s_testcollection'] = testcollection

        elif(("classify" in request.form) and (session.get('s_choices', None) != '' )):
            classifier = form.classifier.data
            session['s_testcollection'] = testcollection

            if(testcollection == 'balimixedplants'):
                class_names = bali26_class_names

                if('Resnet152'.lower() in classifier):
                    archive = bali26_resnet152
                elif('Resnext50'.lower() in classifier):
                    archive = bali26_rexnext50
                elif('Alexnet'.lower() in classifier):
                    archive = bali26_alexnet
                else:
                    archive = bali26_alexnet


            if(testcollection == 'bali26samples'):
                class_names = bali26_class_names

                if('Resnet152'.lower() in classifier):
                    archive = bali26_resnet152
                elif('Resnext50'.lower() in classifier):
                    archive = bali26_rexnext50
                elif('Alexnet'.lower() in classifier):
                    archive = bali26_alexnet
                else:
                    archive = bali26_alexnet


            path, dirs, files = next(os.walk(app.config['MODELS']))
            if(classifier in files):
                pass
            else:
                print('getting the matching trained classifier...')
                modelname = archive.split('/')[-1]
                wget.download(archive, (os.path.join(app.config['MODELS'], modelname)))


            try:
                tchoices = session.get('s_choices', None)
                choice = json.loads(tchoices)
                #print('\nHERE is the image choice: ', choice)
                image_path = os.path.join(app.config['FIND'],  testcollection, choice)
                pclassifier = os.path.join(app.config['MODELS'], classifier)
                processor='cpu'; tk=3; threshold=90;
                model = load_checkpoint(pclassifier, processor)
                predictions, percentage, outcategory = predict_image(image_path, model, predict_transform, class_names, tk, processor)
                tp_indeces = predictions[1].tolist()[0]
                for k in tp_indeces:
                    tp_vals.append(class_names[k])

                #---------------------------------------------------------------
                #check groundtruth
                c=0
                groundtruth_found = False
                for item in tp_vals:
                    if(item in choice):
                        #print('\nITEM info: ', item, choice, c)
                        groundtruth_position = c
                        groundtruth_found = True
                    if ('aroid' in item):
                        tp_vals[c] = 'suweg'
                        break
                    c=c+1

                #Fix aroid -> suweg ... address this formally in the next release...
                if('aroid' in choice):
                    choice = 'suweg.jpg'
                    outcategory = 'suweg'

                #HERE qualify the result  --------------------------------------
                f_percentage = float(percentage)
                if(f_percentage > 95):
                    comment = 'this classifier seems very confident of the validity of the result'
                elif((f_percentage <= 95) and (f_percentage > 90)):
                    comment = 'this classifier seems confident of the validity of the result'
                elif((f_percentage <= 90) and (f_percentage > 80)):
                    comment = 'this classifier seems somewhat unsure of the validity of the result'
                elif((f_percentage <= 80) and (f_percentage > 70)):
                    comment = 'this classifier is not at all confident of the validity of the result'
                elif(f_percentage <= 70):
                    comment = 'this classifier has insufficient confidence in the validity of the result'
                else:
                    comment = ''
                #---------------------------------------------------------------

                input = 'test image: ' + choice
                c_classifier = 'classifier: ' + classifier
                result = 'top prediction: ' + outcategory + ' (with confidence level ' + percentage + '%)'
                moreresults = 'ranked prediction list: ' + str(tp_vals)

                if(groundtruth_found == True):
                    morecomments = 'plant in selected image (' + choice.split('.jpg')[0] + ') detected in position ' + str(groundtruth_position) + ' of prediction list.'
                else:
                    morecomments = 'plant in selected image (' + choice.split('.jpg')[0] + ') -NOT- detected'


            except:
                print('... display images before you classify and pick an image with left mouse click... ')
                return redirect(url_for('testclassifiers'))

        elif("context" in request.form):
            images = ''

        #left click on mouse collects the images
        else:
            try:
                imagenames = request.form['data']
                session['s_choices'] = imagenames

            except:
                print('no image selected to classify')
                pass

    return render_template(template, form=form, images=images, result=result, comment=comment, morecomments = morecomments, moreresults=moreresults, classifier=c_classifier, input=input)

#-------------------------------------------------------------------------------
@app.route('/testclassifiers/<filename>')
def classify_image(filename):
    testcollection = session.get('s_testcollection', None)
    location = os.path.join(app.config['FIND'], testcollection)
    return send_from_directory(location, filename)

#-------------------------------------------------------------------------------
@app.route('/trainclassifiers', methods=['GET', 'POST'])
def trainclassifiers():
    form = MakeClassifiers()
    ti = ''; ei = ''
    template = 'trainclassifiers.html'

    if (request.method == 'POST'):
        if("train" in request.form):
            network = form.classifier.data; testcollection = form.testcollection.data
            epochs = form.epochs.data; gamma = form.gamma.data; lr = form.learning_rate.data
            momentum = form.momentum.data; max_images = form.max_images.data
            training_percentage = form.training_percentage.data;
            pretrained = form.pretrained.data; normalization = form.normalization.data;

            #location = app.config['FIND']
            #prepare_collection(testcollection, location)

            try:
                print('deleting the existing collection...')
                shutil.rmtree(os.path.join(app.config['FIND'], testcollection))
            except:
                pass

            if(testcollection == 'bali-3'):
                archive = bali3_zip
            elif(testcollection == 'bali-3B'):
                archive = bali3B_zip
            elif(testcollection == 'bali-3C'):
                archive = bali3C_zip
            elif(testcollection == 'bali-3D'):
                archive = bali3D_zip
            else:
                archive = bali3_zip

            lzfile = testcollection + '.zip'
            path, dirs, files = next(os.walk(app.config['FIND']))
            zfile = os.path.join(app.config['FIND'], testcollection) + '.zip'

            if(lzfile in files):
                print('already downloaded the archive..')
                pass
            else:
                try:
                    print('getting the test collection...')
                    wget.download(archive, zfile)
                except:
                    print('can not get the test collection...exiting')
                    exit()

            shutil.unpack_archive(zfile, app.config['FIND'], 'zip')


            path, categories, files = next(os.walk(os.path.join(app.config['FIND'], testcollection)))

            if(network == 'vanillanet'):
                model = vanillanet(len(categories))
                pretrained = False
            else:
                model = models.alexnet(pretrained=pretrained)
                model.classifier[6] = torch.nn.Linear(4096,len(categories))

            cn = network + '_' + testcollection + '_checkpoint.pth'
            checkpointname = os.path.join(app.config['RESULTS'], cn)
            ti = network + '_' + testcollection + '_training.jpg'
            ei = network + '_' + testcollection + '_errors.jpg'
            training_image = os.path.join(app.config['RESULTS'], ti)
            datapath = os.path.join(app.config['FIND'], testcollection) + '/'

            print('\nstarting the training with: ', network, testcollection)
            plots = train_model(app, checkpointname, network, testcollection, model, categories, datapath, epochs, gamma, lr, momentum, max_images,\
             training_percentage, pretrained, training_image, normalization)

            tplot = os.path.join(app.config['STATIC'], ti)
            eplot = os.path.join(app.config['STATIC'], ei)
            copyfile(plots[0], tplot)
            copyfile(plots[1], eplot)

    return render_template(template, form=form, image1=ti, image2=ei)

#-------------------------------------------------------------------------------
@app.route('/showinfoview')
def showinfoview():
    template = 'showinfoview.html'
    return render_template(template)

#-------------------------------------------------------------------------------
@app.route('/contextview', methods=['GET', 'POST'])
def contextview():
    template = 'contextview.html'

    return render_template(template)

#-------------------------------------------------------------------------------
@app.route('/contextview_bahasa', methods=['GET', 'POST'])
def contextview_bahasa():
    template = 'contextview_bahasa.html'

    return render_template(template)

#-------------------------------------------------------------------------------
@app.route('/weathersatview', methods=['GET', 'POST'])
def weathersatview():
    sat_map = ''; weatherplot = ''; weathertable = ''
    template = 'weathersatview.html'

    location = app.config['CONTEXT']
    dest_folder = app.config['STATIC']
    wreftarget = os.path.join(location, weatherref_file)
    wcurtarget = os.path.join(location, weathercurrent_file)

    #downloadweather_check(weatherref_url, weatherref_file, wcurtarget, location, wreftarget)
    downloadweather_check(weathercurrent_url, weatherref_url, weatherref_file, wcurtarget, location, wreftarget)

    #New
    station_loc = 'Ubud'
    get_local_weather(station_loc)

    #now produce the reference image and current data, copy to static folder
    weatherplotname = create_weatherplot(wreftarget, wcurtarget, dest_folder, add_current_data = False)
    weathertablename = create_weathertable(wcurtarget, dest_folder)
    #weathertablename = create_weathertable(weathercurrent_file, dest_folder)

    #get the sat-map asset and move to static folder; add title
    task = loop.create_task(get_map_sat(app, satref_url))
    satmap = loop.run_until_complete(task)

    title = 'Satellite image of field study site in Central Bali'
    titlesize = 18; color = (255,255,255); titlelocation = (10,10)
    satmapname = 'current_satmap.jpg'
    add_title(satmap, satmapname, title, titlesize, dest_folder)

    return render_template(template, weatherplot=weatherplotname, satmap=satmapname, weathertable=weathertablename)

#-------------------------------------------------------------------------------
@app.route('/floraclimateview', methods=['GET', 'POST'])
def floraclimateview():
    template = 'floraclimateview.html'
    weathereventsfloraname = '';

    location = app.config['CONTEXT']
    dest_folder = app.config['STATIC']
    seasons = seasons_url.split('/')[-1]
    festivals = events_url.split('/')[-1]

    wreftarget = os.path.join(location, weatherref_file)
    wcurtarget = os.path.join(location, weathercurrent_file)

    #downloadweather_check(weatherref_url, weatherref_file, wcurtarget, location, wreftarget)
    downloadweather_check(weathercurrent_url, weatherref_url, weatherref_file, wcurtarget, location, wreftarget)

    asset_saved = downloadassets_check(seasons_url, location, seasons)
    print('\ngot the asset: ', asset_saved)
    asset_saved = downloadassets_check(events_url, location, festivals)
    print('\ngot the asset: ', asset_saved)

    festivalsdatafilepath = os.path.join(location, festivals)
    seasonsdatafilepath = os.path.join(location, seasons)
    weathereventsfloraname = create_weather_flora_events_plot(wreftarget, seasonsdatafilepath, festivalsdatafilepath, dest_folder)

    return render_template(template, multiplot=weathereventsfloraname)

#-------------------------------------------------------------------------------
@app.route('/integratedagricultureview', methods=['GET', 'POST'])
def integratedagricultureview():
    template = 'integratedagricultureview.html'
    avideo = interview_url.split('/')[-1]
    location = app.config['CONTEXT']
    destination = app.config['STATIC']
    asset_saved = downloadassets_check(interview_url, location, avideo)
    print('\ngot the asset: ', asset_saved)
    if(asset_saved == True):
        #issue - moving the file generates an error (in eventlet wsgi.py) but not a failure... only in debug mode
        #Path(start).rename(end)
        #os.replace(start, end)
        start = os.path.join(location, avideo)
        end = os.path.join(destination, avideo)
        shutil.copyfile(os.path.join(location, avideo), os.path.join(destination, avideo))

    return render_template(template, showvideo=avideo)

#-------------------------------------------------------------------------------
if __name__ == '__main__':
    if(len(sys.argv) < 3):
        print('\nplease provide OS, browser and dubug choice when you start the program.')
        print('\'python3 main.py ubuntu firefox debug\', or \'python3 main.py mac chromium no-debug\' for example.\n')
        print('OS: Ubuntu or MAC. Ubuntu browsers: chromium or firefox; MAC only chrome: \'python3 main.py mac chrome no-debug\' \n')
        sys.exit(2)
    else:
        try:
            osy = sys.argv[1]
            browser = sys.argv[2]
            debug_mode = sys.argv[3]
            print('\n> operating system: ', osy)
            print('> browser: ', browser)
            print('> mode: ', debug_mode)
        except:
            print('... using default ubuntu and chromium in non-debug mode ...')
            osy = 'ubuntu'
            browser = 'chromium-browser'
            debug_mode = 'debug'

    port = 5000
    url = "http://127.0.0.1:{0}".format(port)

    #Two browsers supported in ubuntu; only one (Chrome) in MAC OS
    if('firefox' in browser):
        browser = 'firefox'
    else:
        browser = 'chromium-browser'


    if('ubuntu' in osy):
        threading.Timer(1.25, lambda: webbrowser.get(browser).open(url) ).start()
    else:
        #launch Chrome on MAC OS
        threading.Timer(1.25, lambda: webbrowser.get('open -a /Applications/Google\ Chrome.app %s').open(url)).start()

    if(debug_mode == 'debug'):
        socketio.run(app, port=port, debug=True)
    else:
        socketio.run(app, port=port, debug=False)
#-------------------------------------------------------------------------------
