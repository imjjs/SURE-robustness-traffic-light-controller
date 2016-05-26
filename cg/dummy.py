from optparse import OptionParser



if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-c", "--cores", dest="cores")
    parser.add_option("-i", "--intersectionID", dest="iid")
    parser.add_option("-p", "--parameter", dest="pm")
    (options, args) = parser.parse_args()
    pstring = options.pm
    pl = pstring.split(',')
    parameterList = []
    for idx in range(0,len(pl),2):
        t = (pl[idx], pl[idx + 1])
        parameterList.append(t)

    print '2,2'