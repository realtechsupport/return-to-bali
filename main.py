#!/usr/bin/env python3
# main.py
# AI for Ethnobotany
# spring 2020
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
#-------------------------------------------------------------------------------
print('hello checkout github')

satref_url = 'https://filedn.com/lqzjnYhpY3yQ7BdfTulG1yY/AIE_maps/'
weatherref_url = 'https://filedn.com/lqzjnYhpY3yQ7BdfTulG1yY/AIE_weather/BaliBotanicalGardenWeather_Ref.csv'
weathercurrent_url = 'https://filedn.com/lqzjnYhpY3yQ7BdfTulG1yY/AIE_weather/AIE_weather.csv'
seasons_url = 'https://filedn.com/lqzjnYhpY3yQ7BdfTulG1yY/AIE_context/seasons.csv'
events_url = 'https://filedn.com/lqzjnYhpY3yQ7BdfTulG1yY/AIE_context/events.csv'
weatherref_file = 'refweatherdata.csv'
weathercurrent_file = 'AIE_weather.csv'

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

#------------------------------------------------------------------------------
@app.route('/inputview', methods=['GET', 'POST'])
def inputview():
    form = GetTextinputs()
    template = 'inputview.html'
    results = []
    searchresults = []
    revsource = ''
    filename = ''
    upl = False

    if (request.method == 'POST'):
        if("view" in request.form):
            temp = session.get('s_filename', None)
            if(temp == ''):
                s_filename = ''
            else:
                s_filename = temp

            file = request.files['vid']
            filename = secure_filename(file.filename).lower()
            revsource = os.path.join(app.config['STATIC'], filename)

            if(s_filename == None):
                print('no file yet..')
                pass
            elif((s_filename.split('.')[0]) == filename.split('.')[0]):
                m = os.path.join(app.config['STATIC'], s_filename)
                if(os.path.isfile(m)):
                    upl = True;
                    print('file already uploaded')

            if(upl == False):
                print('.... uploading .....')
                file.save(revsource)

                videoformat = (filename.split('.')[1]).lower()
                print('this is the videoformat: ', videoformat)

            session['s_filename'] = filename
        #------------------------------------------
        elif("capture" in request.form):
            temp = session.get('s_filename', None)
            if(temp == ''):
                s_filename = ''
            else:
                s_filename = temp

            file = request.files['vid']
            filename = secure_filename(file.filename).lower()
            revsource = os.path.join(app.config['STATIC'], filename)

            if(s_filename == None):
                print('no file yet..')
                pass
            elif((s_filename.split('.')[0]) == filename.split('.')[0]):
                m = os.path.join(app.config['STATIC'], s_filename)
                if(os.path.isfile(m)):
                    upl = True;
                    print('file already uploaded')

            if(upl == False):
                print('.... uploading .....')
                file.save(revsource)

                videoformat = (filename.split('.')[1]).lower()
                print('this is the videoformat: ', videoformat)

            destination = os.path.join(app.config['TMP'], filename)
            shutil.copyfile(revsource, destination)

            session['s_filename'] = filename
            s_h = 0
            s_m = form.s_m.data; s_s = form.s_s.data
            e_h = 0
            e_m = form.e_m.data; e_s = form.e_s.data

            start_time = s_s + 60*s_m + 3600*s_h
            end_time = e_s + 60*e_m + 3600*e_h
            duration = end_time - start_time
            start = seconds_to_hms(start_time); end = seconds_to_hms(end_time)

            if('searchterm' in form.search.data):
                searchterm = ''
            else:
                searchterm = form.search.data

            try:
                auth_file = request.files['auth']
                auth_filename = secure_filename(auth_file.filename).lower()
                authsource = os.path.join(app.config['STATIC'], auth_filename)
                auth_file.save(authsource)
            except:
                print('no credential file selected - cannot capture text without a valid [.json] credential ')
                return redirect(url_for('inputview'))

            #now get the text from the set segment
            os.chdir(app.config['TMP'])
            maxattempts = 5
            results, searchresults = extract_text(app, destination, form.lang.data, start_time, duration, form.chunk.data, form.conf.data, maxattempts, searchterm, authsource)
            print('\n finished extracting text from video..\n')
            #session variables limited to 4kb !!
            session['s_results'] = results; session['s_searchresults'] = searchresults

            for line in results:
                print (line)

            template = 'outputview.html'
            return redirect(url_for('outputview'))

    else:
        results = None
        searchresults = None

    return(render_template(template, form=form, result=results, sresult=searchresults, showvideo=filename))

#-------------------------------------------------------------------------------
@app.route('/outputview', methods=['GET', 'POST'])
def outputview():
    form = DownloadInputs()
    template = 'outputview.html'

    s_results = session.get('s_results', None)
    s_searchresults = session.get('s_searchresults', None)
    s_filename = session.get('s_filename', None)

    if (request.method == 'POST'):
        print('inside the download option..')
        template = 'index.html'
        if("download" in request.form):
            resultspath = os.path.join(current_app.root_path, app.config['TMP'])
            for name in glob.glob(resultspath + '*s2tlog*'):
                log = name

            return send_file(log, as_attachment=True)

    return render_template(template, form=form, result=s_results, sresult=s_searchresults, showvideo=s_filename)

#-------------------------------------------------------------------------------
@app.route('/checkimagesview',  methods=['GET', 'POST'])
def checkimagesview():
    form = Checkimagesinputs()
    current_video = ''
    category = ''
    dfiles = ''
    template = 'checkimagesview.html'

    videoname = session.get('s_videoname', None)
    current_video = videoname.split('/')[-1]
    category = session.get('s_category', None)
    images = os.listdir(app.config['IMAGES'] + category)

    lastentry_d = 0; firstentry_s = 0

    if (request.method == 'POST'):
        ssim_min = form.ssim_min.data;
        lum_max = form.lum_max.data;
        lum_min = form.lum_min.data;

        if("add" in request.form):
            destination = os.path.join(app.config['COLLECTION'], category)

            if not os.path.exists(destination):
                os.makedirs(destination)

            #find the highest number in the destination and the lowest in the source
            dfiles = glob.glob(destination + '/*.jpg')
            source = os.path.join(app.config['IMAGES'], category)
            sfiles = glob.glob(source + '/*.jpg')

            try:
                dfiles = [i.split('/')[-1] for i in dfiles]
                dfiles = [i.split('.')[0] for i in dfiles]
                dfiles = sorted([int(i) for i in dfiles])
                lastentry_d = dfiles[-1]
            except:
                lastentry_d = 0

            try:
                ssfiles = [i.split('/')[-1] for i in sfiles]
                ssfiles = [i.split('.')[0] for i in ssfiles]
                ssfiles = sorted([int(i) for i in ssfiles])
                firstentry_s = ssfiles[0]
            except:
                firstentry_s = 0

            if(firstentry_s < lastentry_d):
                print('first entry source smaller than in last in destination...renaming source images')
                rename_all(source, lastentry_d)

            #copy the files
            rfiles = glob.glob(source + '/*.jpg')
            rfiles = sorted(rfiles)
            for file in rfiles:
                shutil.copy(file, destination)
            print('COPIED images to collection')

        elif("divergent" in request.form):
            print('removing fuzzy, over and underexposed images...')
            try:
                images2remove = session.get('s_images2remove', None)
                imlist = json.loads(images2remove)
                im_loc = os.path.join(app.config['IMAGES'], key) + '/'
                im_ref =  imlist[-1]
                nbad = remove_fuzzy_over_under_exposed(im_ref, im_loc, images, ssim_min, lum_max, lum_min)
                print('removed ' +  str(nbad) + ' images...')
            except:
                print('no images selected to create reference...')

        elif("delete" in request.form):
            print('removing highlighted images...')
            try:
                images2remove = session.get('s_images2remove', None)
                imlist = json.loads(images2remove)
                for im in imlist:
                    im_s = os.path.join(app.config['IMAGES'], key, im)
                    print(im_s)
                    try:
                        os.remove(im_s)
                    except:
                        print('image already removed')
            except:
                print('no images selected for removal...')

        elif("remove" in request.form):
            try:
                print('delelting the entire collection !')
                shutil.rmtree(app.config['COLLECTION'])
            except:
                pass
            if not os.path.exists(app.config['COLLECTION']):
                os.makedirs(app.config['COLLECTION'])

        elif("archive" in request.form):
            #shutil.make_archive(app.config['COLLECTION'], 'zip', app.config['COLLECTION'])... works from commandline...
            zfile = 'collection.zip'; timezone = 'America/New_York'
            stamped_zfile = create_timestamp(zfile, timezone)
            zipit(app.config['COLLECTION'], stamped_zfile)
            source = os.path.join(app.config['COLLECTION'], stamped_zfile)
            destination = os.path.join(app.config['ARCHIVE'], stamped_zfile)
            shutil.move(source, destination)

        elif("context" in request.form):
            pass

        elif("share" in request.form):
            pass

        #left click on mouse collects the images
        else:
            try:
                imagenames = request.form['data']
                session['s_images2remove'] = imagenames
            except ValueError:
                pass

    return render_template(template, form=form, category = category, videoname = current_video, images = images)

#-------------------------------------------------------------------------------
@app.route('/checkimagesview/<filename>')
def send_image(filename):
    category = session.get('s_category', None)
    location = 'images/' + category
    return send_from_directory(location, filename)

#-------------------------------------------------------------------------------
@app.route('/labelimagesview', methods=['GET', 'POST'])
def labelimagesview():
    form = VideoLabelInputs()
    revsource = ''
    videoname = ''
    file = ''
    category = ''
    template = 'labelimagesview.html'

    if (request.method == 'POST'):
        if("load" in request.form):
            file = request.files['vid']
            videoname = secure_filename(file.filename).lower()
            revsource = os.path.join(app.config['STATIC'], videoname)
            file.save(revsource)

        elif("bulk" in request.form):
            print('...labelling bulk category')
            framerate = form.framerate.data
            file = request.files['vid']
            videoname= secure_filename(file.filename)
            videonamepath = os.path.join(app.config['TMP'], videoname)
            file.save(videonamepath)
            category = form.folder.data
            savepath = os.path.join(app.config['IMAGES'],  category) + '/'
            create_images_from_video(savepath, category, videonamepath, framerate)
            print('FINISHED bulk saving')

    session['s_videoname'] = videoname
    session['s_category'] = category


    return render_template(template, form=form, showvideo=videoname)

#-------------------------------------------------------------------------------
@app.route('/testclassifiers', methods=['GET', 'POST'])
def testclassifiers():
    form = TestClassifiers()
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
                print('downloading the samples...')
                wget.download(archive, zfile)
                shutil.unpack_archive(zfile, app.config['FIND'], 'zip')
                os.remove(zfile)
            else:
                #here other archives
                archive = bali26_samples_zip

        #----------------------------------
        images = os.listdir(location)

        if("display" in request.form):
            session['s_testcollection'] = testcollection

        elif(("classify" in request.form) and (session.get('s_choices', None) != '' )):
            classifier = form.classifier.data
            session['s_testcollection'] = testcollection

            if(testcollection != 'bali26samples'):
                print('here actions for other testcollections')

            if(testcollection == 'bali26samples'):
                class_names = bali26_class_names

                if('Resnet152'.lower() in classifier):
                    archive = bali26_resnet152
                elif('Resnext50'.lower() in classifier):
                    archive = bali26_rexnext50
                elif('Alexnet'.lower() in classifier):
                    archive = bali16_alexnet
                else:
                    archive = bali16_alexnet

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
                image_path = os.path.join(app.config['FIND'],  testcollection, choice)
                pclassifier = os.path.join(app.config['MODELS'], classifier)
                processor='cpu'; tk=3; threshold=90;
                model = load_checkpoint(pclassifier, processor)
                predictions, percentage, outcategory = predict_image(image_path, model, predict_transform, class_names, tk, processor)
                tp_indeces = predictions[1].tolist()[0]
                for k in tp_indeces:
                    tp_vals.append(class_names[k])

                input = 'selected image: ' + choice
                c_classifier = 'selected classifier: ' + classifier
                result = 'best prediction: ' + outcategory + ' (with confidence level ' + percentage + '%)'
                moreresults = 'top three predictions: ' + str(tp_vals)

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

    return render_template(template, form=form, images=images, result=result, moreresults=moreresults, classifier=c_classifier, input=input)

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

            #-----------
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
            #------------

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
@app.route('/weathersatview', methods=['GET', 'POST'])
def weathersatview():
    sat_map = ''; weatherplot = ''; weathertable = ''
    template = 'weathersatview.html'

    location = app.config['CONTEXT']
    dest_folder = app.config['STATIC']
    wreftarget = os.path.join(location, weatherref_file)
    wcurtarget = os.path.join(location, weathercurrent_file)

    downloadweather_check(weathercurrent_url, weatherref_url, weatherref_file, wcurtarget, location, wreftarget)

    #now produce the reference image and current data, copy to static folder
    weatherplotname = create_weatherplot(wreftarget, wcurtarget, dest_folder, add_current_data = True)
    weathertablename = create_weathertable(wcurtarget, dest_folder)

    #get the sat-map asset and move to static folder; add title
    task = loop.create_task(get_map_sat(app, satref_url))
    satmap = loop.run_until_complete(task)

    title = 'Satellite image of field study site in Central Bali'
    titlesize = 22; color = (255,255,255); titlelocation = (10,10)
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

    downloadweather_check(weathercurrent_url, weatherref_url, weatherref_file, wcurtarget, location, wreftarget)
    downloadassets_check(seasons_url, location, seasons)
    downloadassets_check(events_url, location, festivals)

    festivalsdatafilepath = os.path.join(location, festivals)
    seasonsdatafilepath = os.path.join(location, seasons)
    weathereventsfloraname = create_weather_flora_events_plot(wreftarget, seasonsdatafilepath, festivalsdatafilepath, dest_folder)

    return render_template(template, multiplot=weathereventsfloraname)

#-------------------------------------------------------------------------------
@app.route('/prepareview', methods=['GET', 'POST'])
def prepareview():
    form = PrepareInputs()
    template = 'prepareview.html'
    chunkresult = '...'
    filename = ''

    if (request.method == 'POST'):
        if("samples" in request.form):
            zfile = os.path.join(app.config['TESTS'], 'tests.zip')
            lzfile = 'tests.zip'
            path, dirs, files = next(os.walk(app.config['TESTS']))
            if(lzfile in files):
                print('already downloaded the sample data..')
                pass
            else:
                try:
                    wget.download(tests_zip, zfile)
                    shutil.unpack_archive(zfile, app.config['TESTS'], 'zip')
                except:
                    print('can not get the samples...')
                    return redirect(url_for('prepareview'))

        elif("chunk" in request.form):
            chunksize = form.chunk.data
            try:
                file = request.files['vid']
                filename = secure_filename(file.filename).lower()
                #print(filename, chunksize)
                destination = os.path.join(app.config['TMP'], filename)
                file.save(destination)
                location = app.config['TMP']
                nfiles = chunk_large_videofile(destination, chunksize, location)
                chunkresult = 'result: ' + str(nfiles) + ' files of max ' + str(chunksize) + ' min...'
            except:
                print('Something went wrong...file less than 1 min long? No file chosen? Supported fromats are .webm and .mp4 only. Try again...')
                return redirect(url_for('prepareview'))

        else:
            print('SOMETHING ELSE')

    return render_template(template, form=form, result=chunkresult)

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
            print('\n > operating system: ', osy)
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
