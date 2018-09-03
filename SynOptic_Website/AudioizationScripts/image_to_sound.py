from .hilbert_curve import *
from midiutil.MidiFile import MIDIFile
from PIL import Image
from .median_color_quantifier import *
from django.core.files.temp import NamedTemporaryFile
from wsgiref.util import FileWrapper
from tempfile import TemporaryFile
from django.http import FileResponse


# Testing stuff with specific colors to specific notes
test_palette = [(174,0,0),(255,0,0),(255,0,0),(255,102,0),(255,239,0),
                (153,255,0),(40,255,0),(0,255,242),(0,122,255),(5,0,255),
                (71,0,237),(99,0,178) ]
respective_notes = [66,67,68,69,70,71,72,73,74,75,76,77]

def lengthen_scale_octave(scale):
    returnScale = scale
    for i in range(len(scale)):
        returnScale.append(scale[i] + 8)
    return returnScale

def image_to_audio(imageBinary, input_scale,palette_size):
    """
    Outputs a MIDI file that is a piano interpretation of an image

    :param imageBinary: Binary image data\n
    :param input_scale: Desired musical scale (in the form of list of MIDI note values)\n
    :param palette_size: Number of unique colors the image will be compressed to (must be power of 2)\n
    :return: MIDI binary file
    """
    #double_amount = int(math.log(palette_size,2)-3)
    scale = input_scale
    #for i in range(double_amount):
        #scale = lengthen_scale_octave(scale);
    # Open the image data
    im = Image.open(imageBinary)
    pix = im.load()
    color_palette = color_quantify(palette_size,im)                 # Simplify the image's number of colors to the palette size
    color_palette.sort(key=lambda tup: (tup[0]+tup[1]+tup[2]))      # Sort the colors from darkest to brightest (will map the darker colors to lower scale notes)
    m = im.size[0]
    mf = MIDIFile(1)
    
    track = 0
    time = 0
    channel = 0
    volume = 100
    time = 0
    duration = 1
    
    mf.addTrackName(track,time,'ImageSong')
    mf.addTempo(track,time,120)
    
    
    numOfSkipPixels = 1
    i = 0
    while i < m**2:
        numOfSkipPixels = 1
        duration = 0.5
        timeIncrement = 0.5
        coordinate = d2xy(m,i)
        rgbVal = pix[coordinate[0],coordinate[1]]
        note = color_palette.index(closest_color(color_palette,rgbVal))    
        
        #note = test_palette.index(closest_color(test_palette,rgbVal)) #This is testing with specific colors to notes
        for j in range(i+1,m**2):
            coordinate2 = d2xy(m,j)
            rgbVal2 = pix[coordinate2[0],coordinate2[1]]
            
            note2 = color_palette.index(closest_color(color_palette,rgbVal2))  
            
            #note2 = test_palette.index(closest_color(test_palette,rgbVal2)) #This is testing with specific colors to notes
            
            if (note2 == note):
                duration += 0.5
                timeIncrement += 0.5
                numOfSkipPixels += 1
            else:
                break
            
        mf.addNote(track, channel, scale[note], time, duration, volume)
        time += timeIncrement

        i += numOfSkipPixels

    return mf

    # write it to disk
    #mf.writeFile(temp)
    #with open("C:\\Users\\Kenny\\Desktop\\aye.mid", 'wb') as outf:
        #mf.writeFile(outf)

