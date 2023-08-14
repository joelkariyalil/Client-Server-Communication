import datetime

#clear the file before the iteration begins
f = open('Server Messages.txt','w')
f.write('')
f.close()

def intotxt(message):
    file = open('Server Messages.txt','a')
    str = f"\n{datetime.datetime.now()}\n{message}\n"
    file.write(str)
    file.close()