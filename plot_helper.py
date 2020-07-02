# plot_helper.py (python3)
# utilities for graphic display of training and evaluation of CNNs
# experiments in knowledge documentation; with an application to AI for ethnobotany
# March 2020
#-------------------------------------------------------------------------------
import os, sys, glob
from pyt_utilities import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.dates as mdt
from matplotlib.pyplot import cm
import numpy
import pandas
pandas.set_option('display.max_columns', 50)
pandas.set_option('display.width', 1000)
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import csv
from datetime import datetime
from datetime import date

#-------------------------------------------------------------------------------
def plot_training(e_val_loss, e_train_loss, e_val_acc, e_train_acc, training_image):

    ind = [i for i in range(len(e_val_loss))]
    best = 'best eval accuracy: ' + str(numpy.max(e_val_acc)) + '; best train accuracy: ' + str(numpy.max(e_train_acc))
    print(best)

    fig, axs = plt.subplots(2, figsize=(16, 8))
    axs[0].plot(ind, e_val_loss,  marker='x', markersize=14, c='r', linestyle = '--', linewidth=1)
    axs[1].plot(ind, e_val_acc,  marker='x', markersize=14, c='r', linestyle = '--', linewidth=1)
    #axs[2].plot(ind, e_train_loss,  marker='s', markersize=6, c='r', linestyle = '--', linewidth=1)
    #axs[3].plot(ind, e_train_acc,  marker='s', markersize=3, c='r', linestyle = '--', linewidth=1)

    for i in range (0,2):
        axs[i].yaxis.set_major_locator(plt.MaxNLocator(8))
        axs[i].set_ylabel('score')
        axs[i].grid()
        axs[i].set_xlabel('training epochs')

    for ax in axs.flat:
        ax.label_outer()

    text = 'Evaluation loss (top) and accuracy (bottom); \n' + best + '\n'
    fig.suptitle(text, fontsize=18)
    fig.subplots_adjust(top=0.9)
    plt.savefig(training_image)

#------------------------------------------------------------------------------
def plot_toperrors(datapath, testcollection, network, toperrors_filename, toperrors_image, pretrained, nepochs, max_images, ttp):

    columnnames = ['dataset', 'network', 'pretrained', 'training_percentage', 'epochs', 'maximages', 'normalization', 'plant', 'top1e', 'top1val']
    dataset = pandas.read_csv(toperrors_filename, sep=',' , names=columnnames)
    dataset['top1val'] = pandas.to_numeric(dataset['top1val'], errors='coerce')
    #dataset['top3val'] = pandas.to_numeric(dataset['top3val'], errors='coerce')

    pagewidth = 14; pageheight = 6
    plt.rc('axes', labelsize=18)
    plt.rc('axes', titlesize=20)
    plt.rc('xtick', labelsize=16)
    fig = plt.figure(figsize=(pagewidth, pageheight))
    ax = fig.add_axes([0,0,1,1])
    bars_e1 = ax.bar(dataset['plant'], dataset['top1val'], color='lightgray')
    autolabel(bars_e1, ax, 16)

    #bars_e3 = ax.bar(data['plant'], data['top3val'], color='g')
    #autolabel(bars_e3, ax, 14)
    plt.xticks(rotation=0, ha='right')
    plt.grid(b=True, which='major', color='darkgray', linestyle='-')
    plt.ylim(top=100)
    plt.ylabel('percentage')

    titletext = 'TOP-1 error:' + network + ' on '+ testcollection + ': ' + str(nepochs) + ' epochs, ' + str(ttp) + '% training, ' + str(max_images) + ' images per category'
    ax.set_title(titletext,fontsize= 18)
    fig.subplots_adjust(top=0.9)
    plt.savefig(toperrors_image, transparent=True, bbox_inches='tight')

#------------------------------------------------------------------------------
def autolabel(bars, ax, fs):
    for rect in bars:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 0.9*height,'%d' % int(height),ha='center', va='bottom', fontsize=fs)

#-------------------------------------------------------------------------------
def create_weatherplot(referenceweatherdatafile, currentweatherdatafile, destination_folder, add_current_data):

    dataset = pandas.read_csv(referenceweatherdatafile, low_memory=False)
    #get rid of the row below the header
    dataset.drop(dataset.index[[0,1]], inplace = True)
    dataset['Date+Time'] = dataset['Dates_only'].astype(str) + ' ' + dataset['Time'].astype(str)
    dataset['Date+Time'] = pandas.to_datetime(dataset['Date+Time'])
    dataset = dataset.sort_values(by='Date+Time',ascending=True)
    dataset.drop_duplicates(subset='Date+Time', keep=False, inplace=True)
    #print(dataset.head(10))
    print(dataset['Dates_only'].tail(10))
    print(dataset['Date+Time'].tail(10))

    fig, ax1 = plt.subplots(figsize=(24,8))
    ax1.set_facecolor('whitesmoke')
    ax1.scatter(dataset['Dates_only'], dataset['maxtemp'],  marker='o', s=5.0, alpha = 0.3, linewidths=None, edgecolors = 'none', c='r')
    ax1.scatter(dataset['Dates_only'], dataset['mintemp'],  marker='o', s=5.0, alpha = 0.2, linewidths=None, edgecolors = 'none', c='b')

    ax2 = ax1.twinx()
    ax2.scatter(dataset['Dates_only'], dataset['rain'],  marker='o', s=5.0, alpha=1.0, linewidths=None, c='g')
    ax2.set_ylabel('Rain [mm]', fontsize = 16)
    ax2.xaxis.set_major_locator(plt.MaxNLocator(20))

    if(add_current_data == True):
        results = []
        with open(currentweatherdatafile, newline='\r\n') as csvfile:
            data = csv.reader(csvfile, delimiter=',')
            for row in data:
                results.append(row)

        for item in results:
            if('localtime' in item[0]):
                newdate = item[1]
            elif('rainfall' in item[0]):
                nrain = float(item[1])
            elif('current_temperature' in item[0]):
                ntemp = float(item[1])

        #map month and day onto the reference data (2018-2019)
        newdate = newdate.split('_')[0].strip()
        month = newdate.split('-')[1].strip()
        day =  newdate.split('-')[2].strip()

        if((int(month) >= 12) and (int(month) < 12)):
            year = '2018'
        else:
            year = '2019'

        ndate = year + '-' + month + '-' + day
        #print('\nchecking localtime, mapped time: ', newdate, ndate)

        titletext = 'Temperature and rain fail typical of Central Bali (data from the Bali Botanical Garden, year 2018-2019) \n  ' + \
        ' current data from local weather station in Ubud added with red and green circles'

        weatherplot = referenceweatherdatafile.split('.csv')[0] + '_currentdata.jpg'

        plt.sca(ax1)
        ax1.scatter(ndate, ntemp, marker='o', s=150, alpha = 1.0, color='darkred', edgecolors='darkred', linewidth=2.0)
        plt.annotate(str(ntemp), (ndate, ntemp), textcoords='offset points', color = 'k', xytext=(0,10), ha='center', size=14)

        plt.sca(ax2)
        ax2.scatter(ndate, nrain, marker='o', s=150, alpha = 1.0, color='darkgreen', edgecolors='darkgreen', linewidth=2.0)
        plt.annotate(str(nrain), (ndate, nrain), textcoords='offset points', color = 'k', xytext=(0,10), ha='center', size=14)

    else:
        titletext = 'Temperature and rain fail typical of Central Bali (data from the Bali Botanical Garden, year 2018-2019)'
        weatherplot = referenceweatherdatafile.split('.csv')[0] + '.jpg'


    ax1.set_title(titletext, fontdict={'fontsize': 18, 'fontweight': 'medium'})
    ax1.set_ylabel('Temp [C]', fontsize = 16)
    ax1.tick_params(axis='x', labelrotation=60)
    ttl = ax1.title
    ttl.set_position([.5, 1.05])

    plt.xticks(ha='right')
    fig.subplots_adjust(top=0.85)
    fig.subplots_adjust(bottom=0.2)

    weatherplotname = weatherplot.split('/')[-1]
    destination = os.path.join(destination_folder, weatherplotname)
    plt.savefig(destination)

    return(weatherplotname)

#-------------------------------------------------------------------------------

def create_weather_flora_events_plot(referenceweatherdatafile, seasonsdatafilepath, festivalsdatafilepath, destination_folder):

    #weather
    dataset = pandas.read_csv(referenceweatherdatafile, low_memory=False)
    #get rid of the row below the header
    dataset.drop(dataset.index[[0,1]], inplace = True)
    dataset['Date+Time'] = dataset['Dates_only'].astype(str) + ' ' + dataset['Time'].astype(str)
    dataset['Date+Time'] = pandas.to_datetime(dataset['Date+Time'])
    dataset = dataset.sort_values(by='Date+Time',ascending=True)
    dataset.drop_duplicates(subset='Date+Time', keep=False, inplace=True)

    #events
    fdataset = pandas.read_csv(festivalsdatafilepath, low_memory=False)
    fdataset['start'] = pandas.to_datetime(fdataset['start'])
    fdataset['end'] = pandas.to_datetime(fdataset['end'])

    #seasons
    sdataset = pandas.read_csv(seasonsdatafilepath, low_memory=False)
    sdataset = (sdataset.filter( ['plant', 'fruiting_start', 'fruiting_end'])).dropna()
    sdataset['fruiting_start'] = pandas.to_datetime(sdataset['fruiting_start'])
    sdataset['fruiting_end'] = pandas.to_datetime(sdataset['fruiting_end'])

    #PLOTS --------------------------------------------------------------------

    fig, (ax1, ax2, ax3) = plt.subplots(3, figsize=(24,24))

    #ax1 - weather
    ax1.set_facecolor('whitesmoke')
    ax1.scatter(dataset['Dates_only'], dataset['maxtemp'],  marker='o', s=5.0, alpha = 0.3, linewidths=None, edgecolors = 'none', c='r')
    ax1.scatter(dataset['Dates_only'], dataset['mintemp'],  marker='o', s=5.0, alpha = 0.2, linewidths=None, edgecolors = 'none', c='b')
    ax1.tick_params(axis='both', which='major', labelsize=16)

    #ax1.xaxis.set_major_locator(mdt.DayLocator())
    #ax1.xaxis.set_major_formatter(mdt.DateFormatter('%M-%d'))
    #ax1.set_xlim(dataset['Dates_only'].values[0], dataset['Dates_only'].values[-1])

    ax4 = ax1.twinx()
    ax4.scatter(dataset['Dates_only'], dataset['rain'],  marker='o', s=5.0, alpha=1.0, linewidths=None, c='g')
    ax4.set_ylabel('Rain [mm]', fontsize = 18)
    ax4.tick_params(axis='both', which='major', labelsize=16)
    ax4.xaxis.set_major_locator(plt.MaxNLocator(20))

    titletext = 'Temperature and rain fail Central Bali 2018-2019 (Bali Botanical Gardens)'
    ax1.set_title(titletext, fontdict={'fontsize': 18, 'fontweight': 'medium'})
    ax1.set_ylabel('Temp [C]', fontsize = 18)
    ax1.tick_params(axis='x', labelrotation=60)
    ttl = ax1.title
    ttl.set_position([.5, 1.05])

    #ax2 - events -------------------------------------------------------------
    ax2.set_facecolor('whitesmoke')
    index = fdataset.index
    n = len(index)
    for i in range(0, n-1):
        diff =  fdataset['end'][i] - fdataset['start'][i]
        diff = diff / numpy.timedelta64(1,'M')

        if(diff < 1):
            lw = 25
            c = 'black'
        else:
            lw = 8
            c = 'gray'

        ax2.hlines(fdataset['event'][i],fdataset['start'][i], fdataset['end'][i], linewidth=lw, color = c)

    ax2.tick_params(axis='x', labelrotation=60)
    ax2.grid()
    ax2.tick_params(axis='both', which='major', labelsize=16)
    ax2.set_xlim([date(2018, 11, 15), date(2019, 12, 31)])
    titletext = 'Religious events in Bali 2018-2019'
    ax2.set_title(titletext, fontdict={'fontsize': 18, 'fontweight': 'medium'})
    ttl = ax2.title
    ttl.set_position([.5, 1.05])


    #ax3 - seasons -------------------------------------------------------------
    ax3.set_facecolor('whitesmoke')
    ax3.hlines(sdataset['plant'],sdataset['fruiting_start'], sdataset['fruiting_end'], linewidth=5, color='gray')
    ax3.tick_params(axis='x', labelrotation=60)
    ax3.grid()
    ax3.tick_params(axis='both', which='major', labelsize=16)
    ax3.set_xlim([date(2018, 11, 15), date(2019, 12, 31)])
    titletext = 'Flowering seasons of the plants in the bali-26 dataset'
    ax3.set_title(titletext, fontdict={'fontsize': 18, 'fontweight': 'medium'})
    ttl = ax3.title
    ttl.set_position([.5, 1.05])

    months = mdt.MonthLocator()
    ax2.xaxis.set_major_locator(months)
    ax3.xaxis.set_major_locator(months)

    #fig.autofmt_xdate()
    plt.xticks(ha='right')
    fig.subplots_adjust(top=0.85)
    fig.subplots_adjust(bottom=0.2)
    fig.tight_layout(pad=5.0)

    weathereventseasonsplot = referenceweatherdatafile.split('.csv')[0] + '.jpg'
    weathereventseasonsplotname = weathereventseasonsplot.split('/')[-1]
    destination = os.path.join(destination_folder, weathereventseasonsplotname)

    plt.savefig(destination)

    return(weathereventseasonsplotname)

#-------------------------------------------------------------------------------
def create_weathertable(currentweatherdatafile, destination_folder):

    data = pandas.read_csv(currentweatherdatafile, header=None)
    data.drop(data.tail(1).index,inplace=True)
    data.columns = ['', '']
    #print (data)

    fig, ax = plt.subplots(figsize=(8,6))
    fig.patch.set_visible(False)

    titletext = 'Latest weather in Ubud, Bali (30km from the Central Bali field site)'
    ax.set_title(titletext, fontdict={'fontsize': 12, 'fontweight': 'medium'})
    tt = ax.title
    tt.set_position([0.5, 1.35])
    fig.subplots_adjust(top=0.9)
    fig.subplots_adjust(bottom=0.1)

    table = ax.table(cellText=data.values, colLabels=data.columns, loc='center', cellLoc='center')
    table.scale(1, 5)
    fig.tight_layout()

    weathertable = currentweatherdatafile.split('.csv')[0] + '_table.jpg'

    ax.axis('off')
    ax.axis('tight')

    weathertablename = weathertable.split('/')[-1]
    destination = os.path.join(destination_folder, weathertablename)
    plt.savefig(destination)

    return(weathertablename)

#-------------------------------------------------------------------------------
def add_title(imagepath, satmapname, title, titlesize, destination_folder):
    img = mpimg.imread(imagepath)
    fig, ax = plt.subplots(figsize=(10,10))
    fig.patch.set_visible(False)
    imgplot = plt.imshow(img)
    ax.set_title(title, fontdict={'fontsize': titlesize, 'fontweight': 'medium'})
    tt = ax.title
    tt.set_position([0.5, 1.05])
    plt.axis('off')

    destination = os.path.join(destination_folder, satmapname)
    plt.savefig(destination)

#-------------------------------------------------------------------------------
