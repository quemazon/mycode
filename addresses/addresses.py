import easygui as eg

filename = eg.fileopenbox(msg=None, title=None, default='*', filetypes=None)

first = []
last = []
street = []
city = []
zcode = []
state = []
city = []

myfile = open(filename, 'r')

addresses = myfile.read()
addresses = addresses.split("\n")
numaddr = len(addresses)/4
for i in range(numaddr):
    temp = addresses[i*4].strip("\r\n")
    last.append(temp.rsplit(" ")[-1])
    first.append(temp.rsplit(" ", 1)[-2])
    street.append(addresses[i*4+1].strip("\r\n"))
##    city.append(addresses[i*4+2].strip("\r\n"))
    temp = addresses[i*4+2].strip("\r\n")
    zcode.append(temp.split(" ")[-1])
    state.append(temp.split(" ")[-2])
    city.append(temp.split(",")[0])

myfile.close()

