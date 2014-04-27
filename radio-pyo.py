#!/usr/bin/python2

import os, random, datetime, glob, sys, shutil

def select_song(path=None):
    songs_list = [ i for i in glob.glob(path+'*.ogg') ]
    song = random.choice(songs_list)
    # do not pick file if it's marked for deletion
    stamp_files = [i for i in glob.glob(os.path.splitext(song)[0]+'*.stamp')]
    if len(stamp_files) > 0:
        return select_song(path)
    # do not pick a locked file
    if os.path.isfile(song+'.lock'):
        return select_song(path)
    # ices2 needs this
    print song
    from pyo import sndinfo
    song_duration = sndinfo(song)[1]
    now = datetime.datetime.now()
    # tag for update at now + song duration
    removal_date = now + datetime.timedelta(seconds = song_duration)
    song_stamp = song+'('+str(removal_date)+').stamp'
    open(song_stamp, 'a').close()

def update_song(script_file):
    path = os.path.dirname(script_file)
    basename = os.path.basename(os.path.splitext(script_file)[0])
    ogg_file = path+'/'+basename+'.ogg'
    ogg_file_tmp = 'radiopyo.ogg'
    stamp_files = [i for i in glob.glob(os.path.splitext(script_file)[0]+'*.stamp')]
    # remove other eventual stamps for the same file
    for f in stamp_files:
        os.remove(f)
    # lock it to not be played during rendering
    open(ogg_file+'.lock', 'a').close()
    os.system(script_file)
    #TODO: use python import for that
    for l in open(script_file, 'r').readlines():
        if l.split('=')[0].strip() == 'TITLE':
            TITLE = clean_string(nocomment(l.split('=')[1]))
        if l.split('=')[0].strip() == 'ARTIST':
            ARTIST = clean_string(nocomment(l.split('=')[1]))
        if l.split('=')[0].strip() == 'DURATION':
            DURATION = clean_string(nocomment(l.split('=')[1]))
    # TODO: use a proper python library for this    
    cmd_tags = 'oggz comment -c vorbis -o '+ogg_file+' '+ogg_file_tmp+' TITLE="'+TITLE+'" ARTIST="'+ARTIST+'" DURATION="'+DURATION+'"'
    os.system(cmd_tags)
    os.remove(ogg_file_tmp)
    # unlock it
    os.remove(ogg_file+'.lock')

import tokenize
import io

def nocomment(string):
    result = []
    g = tokenize.generate_tokens(io.BytesIO(string).readline)  
    for toknum, tokval, _, _, _  in g:
        # print(toknum,tokval)
        if toknum != tokenize.COMMENT:
            result.append((toknum, tokval))
    return tokenize.untokenize(result)

def clean_string(string):
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    no_punct = ""
    for char in string:
       if char not in punctuations:
           no_punct = no_punct + char
    return no_punct.strip()
    
def update_songs(path=None):
    for name in glob.glob(path+'*.stamp'):
        now = datetime.datetime.now()
        scheduled_time = datetime.datetime.strptime(name.split('(')[1].split(')')[0].split('.')[0], '%Y-%m-%d %H:%M:%S')
        if now > scheduled_time:
	    script_file = os.path.splitext(name.split('(')[0])[0]+'.py'
            update_song(script_file)
            break # avoid generating same file twice, go to a new loop

def update_all_songs(path=None):
    for name in glob.glob(path+'*.py'):
        update_song(name)

### Main program ###

RADIOPYO_PATH = "/home/tiago/audio/"
cmdargs = sys.argv

if len(cmdargs) == 1:
    select_song(RADIOPYO_PATH)
else:
    if cmdargs[1] == 'update':
        update_songs(RADIOPYO_PATH)
    elif cmdargs[1] == 'update_all':
        update_all_songs(RADIOPYO_PATH)
    elif cmdargs[1] == 'update_song':
        update_song(cmdargs[2])
