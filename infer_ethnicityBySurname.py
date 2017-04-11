import os, sys
import csv
import time
import re
import glob, operator


## Set a dictionary for ethnicity distribution comparison as well as mode ethnicity extraction of each name ##
def Census_surnameDist():
    Surname_dist = {}
    with open('/home/local/QCRI/mp867/ethnicity_censusNameMatching/names_census.csv', 'rb') as f:
        reader = csv.reader(f)
        next(reader, None) #Skip the header

        for row in reader:
            surname = row[0].lower()
            try:
                pctwhite = float(row[5]) #Percent Non-Hispanic White Only
            except ValueError:
                pctwhite = 0.0
            try:
                pctblack = float(row[6]) #Percent Non-Hispanic Black Only
            except ValueError:
                pctblack = 0.0
            try:
                pctapi = float(row[7]) #Percent Non-Hispanic Asian and Pacific Islander Only
            except ValueError:
                pctapi = 0.0
            try:
                pctaian = float(row[8]) #Percent Non-Hispanic American Indian and Alaskan Native Only
            except ValueError:
                pctaian = 0.0
            try:
                pct2prace = float(row[9]) #Percent Non-Hispanic of Two or More Races
            except ValueError:
                pct2prace = 0.0
            try:
                pcthispanic = float(row[10]) #Percent Hispanic Origin
            except ValueError:
                pcthispanic = 0.0

            if surname not in Surname_dist:
                Surname_dist[surname] = {}
                Surname_dist[surname]['pctwhite'] = pctwhite
                Surname_dist[surname]['pctblack'] = pctblack
                Surname_dist[surname]['pctapi'] = pctapi
                Surname_dist[surname]['pctaian'] = pctaian
                Surname_dist[surname]['pct2prace'] = pct2prace
                Surname_dist[surname]['pcthispanic'] = pcthispanic

    return Surname_dist


if __name__ == '__main__':
    
    Census_surnameDist = Census_surnameDist()

    for filename in glob.iglob('/export/sc/demographics_twitter/screenname_agegroup_race_gender_bios_*.txt'):
        state = filename.split('_bios_')[1].split('.txt')[0]

    #   outfile = open('/export/sc/demographics_twitter/screenname_fpagegroup_fprace_fpgender_bios_cnrace_' + state + '.txt', 'w')
        outfile = open('/home/local/QCRI/mp867/ethnicity_censusNameMatching/result/screenname_fpagegroup_fprace_fpgender_bios_cnrace_' + state + '.txt', 'w')

        pattern = re.compile('([A-Z]{1}[a-z]+) ([A-Z]{1}[a-z]+)') #Find out right names, capitalized two words including a whitespace between them
        for line in open(filename, 'r'):
            field = line.strip().split('\t')
            name = field[5]
            m = pattern.findall(name)

            items = ''
            for item in field:
                items += item + '\t'
            items = items[:-1]

            if len(m) != 1:
                print >> outfile, '{0}\t{1}\t{2}'.format(items, 'NA', 'NA')
            else:
                lastname = m[0][1].lower()

                if lastname in Census_surnameDist:
                    maxval = max(Census_surnameDist[lastname].iteritems(), key=operator.itemgetter(1))[1]
                    key = [k for k,v in Census_surnameDist[lastname].items() if v==maxval]
                
                    if len(key) > 1:
                        print >> outfile, '{0}\t{1}\t{2}'.format(items, 'NA', 'NA')
                    else:
                        race = key[0]
                        if Census_surnameDist[lastname][race] >= 70:
                            print >> outfile, '{0}\t{1}\t{2}'.format(items, race, race)
                        else:
                            print >> outfile, '{0}\t{1}\t{2}'.format(items, race, 'NA')
        
        outfile.close()
