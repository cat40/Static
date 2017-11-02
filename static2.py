#it = []
import time
startMain = time.clock()
import os
#import PIL
from PIL import Image
#start = time.clock()
import pygame # about 2 seconds, but only with a print statement after it
#it.append(time.clock()-start)
import itertools
import random
import sys
import tempfile
#start = time.clock()
import numpy
#it.append(time.clock() - start); start = time.clock()
import scipy.io.wavfile
#it.append(time.clock() - start)
#import wave
##import pyaudio
print time.clock() - startMain
def isFalse(x):
    if x.lower() == 'false':
        return False
    try: x = int(x)
    except:
        pass
    return bool(x)
            
playSong = len(sys.argv) > 1 and isFalse(sys.argv[1]) #if the argument is false, the song will not play
#generate a bunch of random images 25x25px
size = 25 #ideal seems to be about 25
imagedir = '.\\images\\'
songname = '.\\music.mp3'
if not os.path.isdir(imagedir):
    os.mkdir(imagedir)
def makeImages(imageNum):
    #grays (more likley)
    grays = tuple((x, x, x) for x in xrange(0, 256, 5))
    #colors
    colors = tuple(itertools.permutations(xrange(0, 256, 5), 3))
    pixels = list((grays*10 + colors))
    for i in xrange(imageNum):
        image = Image.new('RGB', (size, size))
        image.putdata([random.choice(pixels) for _ in xrange(size**2)])
        image.save(os.path.join(imagedir, '%04d.png' % i))
        
def playStatic():
    static = tempfile.TemporaryFile()
    data = numpy.random.uniform(-1, 1, 44100*50) #generate some random samples
    scaled = numpy.int16(data/numpy.max(numpy.abs(data)) * 32767) #converts float to integers
    scipy.io.wavfile.write(static, 44100, scaled) #writes to file
    pygame.mixer.music.load(static)
    pygame.mixer.music.play(-1)
    
start = time.clock()   
#get screen size and number of images to produce
pygame.init()
info = pygame.display.Info()
w = info.current_w
h = info.current_h
#pygame.quit()
print time.clock() - start; start = time.clock() #.4 seconds
imageNum = (w*h)//(size**2)//1000 #may result in being one short, we'll see
#check if images exist, if not, make them
#could use a while loop and generate an image until full
#print len(filter(lambda x: not os.path.isfile(x), os.listdir(imagedir))), imageNum
if len(filter(lambda x: not os.path.isfile(x), os.listdir(imagedir))) < imageNum:
##    #deletes and remakes the image directory in case something else in in there
##    os.remove(imagedir)
##    os.mkdir(imagedir)
    print 'generating images'
    makeImages(imageNum)

#starting pygame stuff now
#pygame.init()
#loads all the random images into pygame
print time.clock() - start; start = time.clock()
images = [pygame.image.load(os.path.join(imagedir, img)) for img in filter(lambda x: not os.path.isfile(x), os.listdir(imagedir))]
print time.clock() - start; start = time.clock() #.64 seconds
#gets all possible image corner locations
locations = tuple((x, y) for x in xrange(0, w, size) for y in xrange(0, h, size))
print time.clock() - start; start = time.clock()
#print locations
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
print time.clock() - start; start = time.clock()
pygame.mixer.init()
SONG_END = pygame.USEREVENT + 1 #custom event
pygame.mixer.music.set_endevent(SONG_END)
playStatic()
done = False
start = time.clock()
while True:
    if time.clock() - start >= random.randint(5, 15)+random.random() and not done and os.path.isfile(songname) and playSong:
        done = True
        pygame.mixer.music.load(open(songname, 'rb'))
        pygame.mixer.music.play()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        elif event.type == SONG_END and done:
            playStatic()
    for location in locations:
        screen.blit(random.choice(images), location)
    pygame.display.update()
    #print time.clock() - start
                                                                                                                   
