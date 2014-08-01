import audiolab
import numpy as np
from math import pi
import Image, colorsys

def frequency(k):
    return samplerate * k / window

def saveImage(spectrogram):
    spectrogram = spectrogram.transpose()
    imArray = np.array((spectrogram,spectrogram,spectrogram))
    #has shape (3,rows,columns)
    imArray = np.swapaxes(imArray,0,1)
    #has shape (rows,3,columns)
    imArray = np.swapaxes(imArray,1,2)
    #has shape(rows,columns,3)
    imArray *= 1 / imArray.max()      #normalize
    
    
    for i in range(imArray.shape[0]):
        for j in range(imArray.shape[1]):
            x = imArray[i,j,0]
            if x < 0.005:
                colorpixel = (0,0,0)
            else:
                colorpixel = colorsys.hsv_to_rgb(0.7*(1-x),
                                        0.4+0.5*x,
                                        0.1+0.8*x)
            imArray[i,j,:] = np.array(colorpixel)
    
    imArray *= 255
    imArray = np.array(imArray,np.uint8)
    
    imArray = np.array(imArray[::-1,:,:])   #reverse the columns

    #put reference dots along the bottom
    i = 0
    pps = samplerate / window  #pixels per second
    while i*pps < imArray.shape[1]:
        imArray[-1,i*pps,0] = 255
        i += 1
    print imArray.shape
    imout = Image.fromarray(imArray,mode="RGB")
    imout.save("out.bmp")
    

def main():
    global window, samplerate
    
    fin = audiolab.Sndfile("C:\\Users\\Philip\\Videos\\stranger.wav",'r')
    data = fin.read_frames(fin.nframes - fin.nframes % 64)
    samplerate = fin.samplerate
    window = int(window * samplerate / 1000.0)  #now window = samples per block
    fin.close()
    print "window = %d\nsamplerate = %d\ndt = %f\ndf = %f\n" % \
    (window, samplerate, float(window)/samplerate, float(samplerate)/window)
    
    data = data[:,0]    #discard 2nd channel
    #now decide how many window sample blocks to do:
    nblocks = len(data) // window
    data = data[:nblocks*window]   #truncate the excess that won't fit in a block

    cols = (window // 2) + 1    #rfft only produces half the coefficients
    spectrogram = np.zeros( (nblocks,cols), np.float32 )

    #compute the spectrogram:
    for i in range(1,nblocks-1):
        block = data[i*window:(i+1)*window]
        spectrogram[i] = np.absolute(np.fft.rfft(block))

    #throw away frequencies over 4kHz
    spectrogram = spectrogram[:,:int(4000.0*window/samplerate)]
    
    #display spectrogram:
    saveImage(spectrogram)
    
#REMEMBER:
#f = samplerate*x/window   (where window is samples per block)
#then df = samplerate/window
#and dt = window / samplerate


window = 125     #window size, milliseconds
samplerate = None

if __name__ == "__main__":
    main()
