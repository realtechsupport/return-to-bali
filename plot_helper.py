# plot_helper.py (python3)
# utilities for graphic display of training and evaluation of CNNs
# experiments in knowledge documentation; with an application to AI for ethnobotany
# March 2020
#-------------------------------------------------------------------------------
import os, sys, glob
from pyt_utilities import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy
import pandas
pandas.set_option('display.max_columns', 50)
pandas.set_option('display.width', 1000)
import csv

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
def create_weatherplot(referenceweatherdatafile, currentweatherdatafile):
    #open the file and read in the current weatherdata..
    results = []
    with open(currentweatherdatafile, newline='\r\n') as csvfile:
        data = csv.reader(csvfile, delimiter=',')
        for row in data:
            results.append(row)

    for item in results:
        if('timestamp' in item[0]):
            newdate = item[1]

        elif('rainfall' in item[0]):
            nrain = float(item[1])

        elif('cur_temp' in item[0]):
            ntemp = float(item[1])

    #map month and day onto the reference data (2018-2019)
    newdate = newdate.split('_')[0]
    month = newdate.split('-')[1]
    day =  newdate.split('-')[2]
    if((int(month) >= 12) and (int(month) <= 12)):
        year = '2018'
    else:
        year = '2019'
    ndate = year + '-' + month + '-' + day


    dataset = pandas.read_csv(referenceweatherdatafile, low_memory=False)
    #get rid of the row below the header
    dataset.drop(dataset.index[[0,1]], inplace = True)
    dataset['Date+Time'] = dataset['Dates_only'].astype(str) + ' ' + dataset['Time'].astype(str)
    dataset['Date+Time'] = pandas.to_datetime(dataset['Date+Time'])
    dataset = dataset.sort_values(by='Date+Time',ascending=True)
    dataset.drop_duplicates(subset='Date+Time', keep=False, inplace=True)
    #print(dataset.head(10))#print(dataset.tail(10))
    #---------------------------------------------------------------------------

    fig, ax1 = plt.subplots(figsize=(24,8))

    ax1.set_facecolor('whitesmoke')
    ax1.scatter(dataset['Dates_only'], dataset['maxtemp'],  marker='o', s=5.0, alpha = 0.3, linewidths=None, edgecolors = 'none', c='r')
    ax1.scatter(dataset['Dates_only'], dataset['mintemp'],  marker='o', s=5.0, alpha = 0.2, linewidths=None, edgecolors = 'none', c='b')
    '''
    titletext = 'Bali Botanical Garden Research Station Climate Reference Year [Dec 2018 to Dec 2019]\n min, max temperature (blue and red) ' + \
    ' and rainfall (green) \n red and green circles are current [' + month + '-' + day + ']' \
    ' temperature and rain data from a local weather station in Ubud, Bali mapped onto the reference chart below'
    '''
    titletext = 'Bali Botanical Garden Research Station Climate Reference Year [Dec 2018 to Dec 2019]'
    ax1.set_title(titletext, fontdict={'fontsize': 18, 'fontweight': 'medium'})
    #ax1.set(xlabel = 'Date', ylabel = 'Temp [C]', title = titletext)
    ax1.set_ylabel('Temp [C]', fontsize = 16)
    ax1.tick_params(axis='x', labelrotation=60)
    ttl = ax1.title
    ttl.set_position([.5, 1.05])

    ax2 = ax1.twinx()
    ax2.scatter(dataset['Dates_only'], dataset['rain'],  marker='o', s=5.0, alpha=1.0, linewidths=None, c='g')
    ax2.set_ylabel('Rain [mm]', fontsize = 16)
    ax2.xaxis.set_major_locator(plt.MaxNLocator(20))

    plt.xticks(ha='right')
    fig.subplots_adjust(top=0.85)
    fig.subplots_adjust(bottom=0.2)

    plt.sca(ax1)
    ax1.scatter(ndate, ntemp, marker='o', s=150, alpha = 1.0, color='w', edgecolors='darkred', linewidth=2.0)
    plt.annotate(str(ntemp), (ndate, ntemp), textcoords='offset points', color = 'k', xytext=(0,10), ha='center', size=14)

    plt.sca(ax2)
    ax2.scatter(ndate, nrain, marker='o', s=150, alpha = 1.0, color='w', edgecolors='darkgreen', linewidth=2.0)
    plt.annotate(str(nrain), (ndate, nrain), textcoords='offset points', color = 'k', xytext=(0,10), ha='center', size=14)

    weatherplot = referenceweatherdatafile.split('.csv')[0] + '.jpg'
    plt.savefig(weatherplot)

    return(weatherplot)

#-------------------------------------------------------------------------------
