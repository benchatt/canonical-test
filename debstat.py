#first pass, hard-coded filename, pretty ugly output, slow
#to do: speed up?
#  improve output aesthetics
#  get file from ftp location`
topten = []
with open('/home/ben/Downloads/Contents-armhf') as fh:
    for line in fh.readlines():
        preparsed_line = line.strip().split()
        if len(preparsed_line) != 2:
            continue
        (file,location) = preparsed_line
        if file.lower() == 'file' or location.lower() == 'location':
            continue
        location_list = location.split(',')
        if len(topten) < 10:
            topten.append([len(location_list),file])
            continue
        for i in range(len(topten)):
            if len(location_list) > topten[i][0]:
                topten.insert(i,[len(location_list),file])
                break
        if len(topten) > 10:
            topten = topten[:10]

for i,entry in enumerate(topten):
    print(f"\t{i+1}. {entry[1]}\t{entry[0]}")

