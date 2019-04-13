import csv as csv
import numpy as np
from random import randint
import random
import argparse

# read data
def ReadData(path):
    data_file = csv.reader(open(path, 'r'))
    datalist = []
    for row in data_file:
        datalist.append(''.join(row))
    datalist = np.array(datalist)
    return datalist

def GenerateDateTime(year, month):
    date = year + '/' + month.zfill(2) + '/' + str(randint(1, 31)).zfill(2) + ' '
    time = str(randint(0, 23)).zfill(2) + ':' + str(randint(0, 59)).zfill(2) + ':' + str(randint(0, 59)).zfill(2)
    return date + time

def Interpolate(path, instances):
    # read data in format of 'rank number of visits'
    data_file = csv.reader(open(path, 'r'))

    # keep ranks in datalist[0] and visits in datalist[1]
    datalist = [[], []]
    for row in data_file:
        itemlist = list(map(int, row[0].split()))
        datalist[0].append(itemlist[0])
        datalist[1].append(itemlist[1])

    # convert visits to probability
    visitsSum = sum(datalist[1])
    datalist[1] = [float(visit) / visitsSum for visit in datalist[1]]

    # interpolate
    allRanks = np.arange(1, instances + 1)
    ranksProbEst = np.interp(allRanks, datalist[0], datalist[1])

    # make interpolated probabilities sum to 1
    ranksProbEstSum = sum(ranksProbEst)
    ranksProb = [float(row) / ranksProbEstSum for row in ranksProbEst]

    # visits based on website indeces
    visits = np.random.choice(a=allRanks, size=instances, p=ranksProb)

    return visits

def GenerateVisits(output_file, instances, year, month, visitors_ip, websites_ip, interpolate):
    # read destination ip
    # websiteIP = ReadData(websites_ip)
    ranks = list(range(0, instances))
    wip = list(range(1, instances+1))
    websiteIP = dict(zip(ranks, wip))

    if instances > len(websiteIP):
        print('ERROR: Number of output rows cannot be greater than %s' % len(websiteIP))
        return

    # read visitors ip
    visitorIP = ReadData(visitors_ip)

    # generate samples based on interpolation
    visits = Interpolate(interpolate, instances)
    # np.savetxt('data/v', visits, delimiter="\t", fmt="%s") 

    # print generated logs
    ports = 10000;
    data = []
    for v in visits:
        myrow = []

        # visitor ip
        myrow.append(random.choice(visitorIP))

        # visitor port
        myrow.append(str(random.randint(0, ports)))

        # destination ip
        myrow.append(str(websiteIP[v-1]))
        # myrow.append('rank-' + str(websiteIP[v-1]))

        # destination port
        myrow.append(str(80))

        # visit time
        myrow.append(GenerateDateTime(year, month))

        data.append('\t'.join(myrow))

    outputFile = open(output_file, 'w')
    outputFile.write('\n'.join(data))
    print("See output in %s" % output_file)
    print("Done!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Daily log generator in the format of <source IP, source Port (random), destination IP, destination port (80), date/time>', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-v','--visitors-ip', help='filename for visitors ip', default='data/visitors-ip')
    parser.add_argument('-w','--websites-ip', help='filename for websites ip', default='data/websites-ip')
    parser.add_argument('-i','--interpolate', help='filename for interpolation in format of <website-rank visits-number>', default='data/interpolation')
    parser.add_argument('-r', '--rows', help='number of output rows', required=True)
    parser.add_argument('-o','--output', help='filename for generated logs', default='data/visits.log')
    parser.add_argument('-y','--year', help='year in YYYY format', default=1395, type=int)
    parser.add_argument('-m','--month', help='month in range of 1..12', default=5, type=int)

    args = parser.parse_args()

    if args.rows is not None:
        GenerateVisits(args.output, int(args.rows), str(args.year), str(args.month), args.visitors_ip, args.websites_ip, args.interpolate)
