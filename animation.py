import images2gif 
from PIL import Image
import os
import os.path
import numpy
import commands


DURATION = 2.0

def get_command(filenames,output,delay=10):
    command = "convert -delay %d %s %s"
    return command % (delay, " ".join(filenames), output)

def write_animatedgif(quake_snapshots, filename):
    images = [ snapshot.image for snapshot in quake_snapshots ]

    quake_filenames = [snapshot.savepath for snapshot in quake_snapshots]

    #execute
    write_animated_gif = get_command(quake_filenames, filename)
    print write_animated_gif
    #commands.getoutput("rm %s" % filename)
    print commands.getoutput(write_animated_gif)
