#programmatically animate little cook and whisk "a la paper pocky "


#presentation video export works
#next steps
# - extract video generation and define api
# - make simple video cut / concat tool

#recipe appears
#bowl appears
#floor appears
#floor goes to below bowl
#wisk appears
import pygame
import random, sys, time, math
import shutil,os
from pygame.locals import *
#params
render_pics=True
gen_scripts=True
#render_folder="d:/tmp/tuto/"
render_folder="c:/tmp/tuto/"


## all generated sounds shall match these characteristics of the imported sound clips
# (could be determined/checks run by ffprobe -json in the future )
global_sample_rate="44100"
global_channels="mono"
global_channels_nb="1"

#test param, to test on just a fragment of render
#if params > 0 , frames are rendered and added to list.txt only in this interval
#first_render_frame=0
first_render_frame=None
last_render_frame=None
#last_render_frame=1000

avi_input_name_for_sound="to_mix.avi"
current_nb=0 #cycles / frames
current_sound_to_merge=1
sounds_to_merge=[] # we intercept file name and cycles number as event is triggered
concatlist=None
list_tr_sh="tr '\r' ' ' < list.txt > trlist.txt "
##-vf \"transpose=2,transpose=2\"
concat_sh = "ffmpeg.exe -r 30 -f concat -i trlist.txt  -an -c:v rawvideo -pix_fmt rgba -r 30 nullsound.avi "

#TODO use this to generate blank sound
#ffmpeg -i $TMP/$myfolder/nosoundraw.avi -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=48000 -c:v copy -c:a pcm_s16le -map 1:a -map 0:v -shortest -r 30 $TMP/$myfolder/blanksound.avi
blanksound_sh="ffmpeg -i "+render_folder+"nullsound.avi -f lavfi -i anullsrc=channel_layout="+global_channels+":sample_rate="+global_sample_rate+" -c:v copy -c:a pcm_s16le -map 1:a -map 0:v -shortest -r 30 "+render_folder+avi_input_name_for_sound


#TODO use this to mix sounds at correct time
#ffmpeg -i $TMP/$myfolder/blanksound.avi -i sound.ogg   -filter_complex amix=inputs=2:duration=first -c:v copy -c:a pcm_s16le -ac 2 -b:a 1536k -ar 48000 -r 30 $TMP/1.avi
##mixsound_sh="ffmpeg -i $TMP/$myfolder/blanksound.avi -i sound.ogg   -filter_complex amix=inputs=2:duration=first -c:v copy -c:a pcm_s16le -ac 2 -b:a 1536k -ar 48000 -r 30 mix1.avi"

#ref "ffmpeg -loop 1 -i %s%d.bmp -an -c:v rawvideo -pix_fmt rgba -t %f -r 30 %s%d.avi \n"
if render_pics:
      #let's clean the folder
      try:
            shutil.rmtree(render_folder)
      except FileNotFoundError:
            print("dir not preexisting")
      os.mkdir(render_folder)
if render_pics:
      concatlist=open(render_folder+"list.txt","w")


#constants
FRAME_RATE=30
FRAME_TIME=33
#eventtypes

NEW_OBJECT="new_object"
NEW_RELATIVE="new_relative"
SOUND="sound"
MOVE="move"
DELAY="delay"
DISAPPEAR="disappear"
END="end" #placeholder event

#attributes, for quick readability of event script in idle
#also mystypig will give an error on run
TO="to"
HINT="hint"
TYPE="type"
KEY="key"
FILE="file"
WAIT_INACTIVE="wait_inactive"
WAIT_END="wait_end"
CYCLES="cycles"
RELATIVE="relative"

#end of constant

folder="interpreter/"
PIC="pic"

script=[
        {
            TYPE:SOUND,
#            FILE:"1Cuisinierrecette.wav",
            FILE:"1interpreterlikecook.wav",
            KEY:"s1"
        },
         {
         TYPE:NEW_OBJECT,
         KEY:"cook",
         PIC:"cook.png",
         "x":20,
         "y":200
         },
        {
            TYPE:NEW_OBJECT,
            KEY:"recipe",
            PIC:"recipe.png",
             "x":20,
             "y":32
        },
         {
         TYPE:NEW_OBJECT,
         KEY:"bowl",
         PIC:"bowl.png",
         "x":100,
         "y":100
         },
         {
         TYPE:NEW_RELATIVE,
         #TYPE:NEW_OBJECT,
         KEY:"milk",
         PIC:"milk.png",
         RELATIVE:"bowl",
         HINT:"right"
         #"x":160,
         #"y":100
         },
         {
         TYPE:NEW_RELATIVE,
         #TYPE:NEW_OBJECT,
         KEY:"flour",
         PIC:"flour.png",
         RELATIVE:"milk",
         HINT:"right"
#         "x":200,
#         "y":100
         },
         {
         TYPE:NEW_RELATIVE,
         KEY:"eggs",
         PIC:"eggs.png",
         RELATIVE:"bowl",
         HINT:"right"
         },
         {
         TYPE:NEW_RELATIVE,
         KEY:"whisk",
         PIC:"whisk.png",
         RELATIVE:"eggs",
         HINT:"right"
         },
        {
            WAIT_END:"s1", #we wait for completion of
            #prvious event to trigger this one ( sync )
            TYPE:SOUND,
#            FILE:"2Prendsunbol.wav",
            FILE:"2fetchabowl.wav",
            KEY:"s2"
        },
        {
            TYPE:MOVE,
            KEY:"cook",
            TO:"bowl",
            HINT:"below",
            CYCLES:60
        },
         {
         WAIT_INACTIVE:"cook",
         TYPE:DISAPPEAR,
         KEY:"bowl",
         },
        {
            TYPE:MOVE,
            KEY:"cook",
            TO:"recipe",
            HINT:"below",
            CYCLES:60
        },
         {
         WAIT_INACTIVE:"cook",
         TYPE:NEW_OBJECT,
         KEY:"bowl",
         PIC:"bowl.png",
         "x":20,
         "y":100
         },
        {
            TYPE:MOVE,
            KEY:"cook",
            TO:"bowl",
            HINT:"below",
            CYCLES:60
        },
        {
            WAIT_END:"s2", #we wait for completion of
            #prvious event to trigger this one ( sync )
            TYPE:SOUND,
#            FILE:"3Prendsfarinemetsbol.wav",
            FILE:"3flourinthebowl.wav",
            KEY:"s3"
        },
        {
            TYPE:MOVE,
            KEY:"cook",
            TO:"flour",
            HINT:"below",
            CYCLES:120
        },
         {
         WAIT_INACTIVE:"cook",
         TYPE:DISAPPEAR,
         KEY:"flour",
         },
        {
            TYPE:MOVE,
            KEY:"cook",
            TO:"bowl",
            HINT:"below",
            CYCLES:120
        },
         {
         WAIT_INACTIVE:"cook",
         TYPE:NEW_RELATIVE,
         KEY:"flour",
         PIC:"flour.png",
         RELATIVE:"bowl",
         HINT:"below"
         #"x":20,
         #"y":180
         },
        {
            TYPE:MOVE,
            KEY:"cook",
            TO:"flour",
            HINT:"below",
            CYCLES:120
        },

        {
            WAIT_END:"s3", #we wait for completion of
            #prvious event to trigger this one ( sync )
            TYPE:SOUND,
            FILE:"4Prendsdesoeufsetmetslesdanslebol.wav",
            KEY:"s4"
        },
        {
            TYPE:MOVE,
            KEY:"cook",
            TO:"eggs",
            HINT:"below",
            CYCLES:120
        },
         {
         WAIT_INACTIVE:"cook",
         TYPE:DISAPPEAR,
         KEY:"eggs",
         },
        {
            TYPE:MOVE,
            KEY:"cook",
            TO:"flour",
            HINT:"below",
            CYCLES:120
        },
         {
         WAIT_INACTIVE:"cook",
         TYPE:NEW_RELATIVE,
         KEY:"eggs",
         PIC:"eggs.png",
         RELATIVE:"flour",
         HINT:"below"
         },
        {
            TYPE:MOVE,
            KEY:"cook",
            TO:"eggs",
            HINT:"below",
            CYCLES:120
        },
        {
            WAIT_END:"s4", #we wait for completion of
            #prvious event to trigger this one ( sync )
            TYPE:SOUND,
            FILE:"5Prendslaitmetsdansbol.wav",
            KEY:"s5"
        },
        {
            TYPE:MOVE,
            KEY:"cook",
            TO:"milk",
            HINT:"below",
            CYCLES:120
        },
         {
         WAIT_INACTIVE:"cook",
         TYPE:DISAPPEAR,
         KEY:"milk",
         },
        {
            TYPE:MOVE,
            KEY:"cook",
            TO:"eggs",
            HINT:"below",
            CYCLES:120
        },
         {
         WAIT_INACTIVE:"cook",
         TYPE:NEW_RELATIVE,
         KEY:"milk",
         PIC:"milk.png",
         RELATIVE:"eggs",
         HINT:"below"
         },
        {
            TYPE:MOVE,
            KEY:"cook",
            TO:"milk",
            HINT:"below",
            CYCLES:120
        },
        {
            WAIT_END:"s5", #we wait for completion of
            #prvious event to trigger this one ( sync )
            TYPE:SOUND,
            FILE:"6Prendslefouetetremues.wav",
            KEY:"s6"
        },
        {
            TYPE:MOVE,
            KEY:"cook",
            TO:"whisk",
            HINT:"below",
            CYCLES:120
        },
         {
         WAIT_INACTIVE:"cook",
         TYPE:DISAPPEAR,
         KEY:"whisk",
         },
        {
            TYPE:MOVE,
            KEY:"cook",
            TO:"milk",
            HINT:"below",
            CYCLES:120
        },
         {
         WAIT_INACTIVE:"cook",
         TYPE:NEW_RELATIVE,
         KEY:"whisk",
         PIC:"whisk.png",
         RELATIVE:"milk",
         HINT:"below"
         },
        {
            TYPE:MOVE,
            KEY:"cook",
            TO:"whisk",
            HINT:"below",
            CYCLES:120
        },


#5Prendslaitmetsdansbol.wav
#6Prendslefouetetremues.wav##        {
##            TYPE:DELAY,
##            "duration":3000
##        },
##        {
##            TYPE:DELAY,
##            "duration":12000
##        },
        {
            WAIT_INACTIVE:"cook",
            TYPE:DELAY,
            "duration":3000
        },
        #extraobject just to prevent quick exit
        {
            TYPE:END
        },
    ]

print(script)

#let's build a graphics cache for the script
pic_cache={}
sound_cache={}

def load_assets():
    #for all events and sub events we laod surf corresponding to pic
    for evt in script:
        #TODO add recursion depending on type
        print(evt[TYPE])
        try:
            to_cache=evt[PIC]
            path=folder+to_cache
            print("TO CACHE "+str(path))
            pic_cache[to_cache]=pygame.transform.smoothscale(pygame.image.load(path),(64,64))
        except KeyError:
            print("no key")
        if evt[TYPE]==SOUND:
            try:
                to_cache=evt[FILE]
                path=folder+to_cache
                #path=to_cache
                print("TO CACHE "+str(path))
                #TODO feed in sound cache
                #tmp=pygame.mixer.Sound(path)
                sound_cache[to_cache]=pygame.mixer.Sound(path)
                shutil.copyfile(path,render_folder+to_cache)
            except KeyError:
                print("no key")

#dict use so that we can reference them by key when new event update them
#COMMENT harder to remove a key while iterating on dict content :(
active_objects_pool={}

#TODO refactor with cycles
#def function pointer behavior test
def elapse_time(self,key,to_remove):
#    start=self["start"]
#    duration=self["duration"]*1000
#    current=pygame.time.get_ticks()
#<    print("dbg current "+str(current)+" start "+str(start)+" duration 1000 "+str(duration) )
    left=self["left_duration"]
    self["left_duration"]=left-1
    if self["left_duration"]<=0:
        print("sound finished")
        to_remove.append(key)
        #active_objects_pool.pop(key,None)

#behavior function with steps x steps y n cycle left
def move_obj(self,key,to_remove):
    todo=self["todo"]
    todo-=1
    self["x"]=self["x"]+self["offx"]
    self["y"]=self["y"]+self["offy"]
    if todo<=0:
        #TODO we need to remove behavior function as move is finished
        del self["behavior"]
        print("removing behavior, cycles finished")
        return
    self["todo"]=todo



def calculate_traj(obj,target,hint,cycles):
    tx=target["x"]
    ty=target["y"]
    ox=obj["x"]
    oy=obj["y"]
    if hint=="below":
        obj["y"]+=64
    offx=(tx-ox)/cycles

    offy=(ty-oy)/cycles
    obj["offx"]=offx
    obj["offy"]=offy
    obj["todo"]=cycles
    obj["behavior"]=move_obj

def consume_event(ctx):

    #in fact "wait disappearance" , presence in object pool
    if WAIT_END in ctx.next_event :
        wait_key=ctx.next_event[WAIT_END]
        #print("dbg checking evt end "+wait_key )
        if wait_key in active_objects_pool:
            #print("event in object ppool")
            return False

    #"wait inactive" , obj with key in object pool, no behavior
    if WAIT_INACTIVE in ctx.next_event :
        wait_key=ctx.next_event[WAIT_INACTIVE]
        #print("dbg checking evt end "+wait_key )
        if wait_key in active_objects_pool and "behavior" in active_objects_pool[wait_key]:
         #   print("parent event active")
            return False



    print("consuming: "+str(ctx.next_event))
    #TODO
    #check event type
    #if new object we add a graphical object
    if ctx.next_event[TYPE]==NEW_OBJECT :
        #we add a new displayable object to the gaphic objects pool
        obj={}
## default mode , we add
        obj["x"]=ctx.next_event["x"]
        obj["y"]=ctx.next_event["y"]
        obj[PIC]=ctx.next_event[PIC]
        active_objects_pool[ctx.next_event[KEY]]=obj
    elif ctx.next_event[TYPE]==NEW_RELATIVE :
        #we need to get the relative object to position
        obj={}
        relative=active_objects_pool[ctx.next_event[RELATIVE]]
        obj["x"]=relative["x"]
        obj["y"]=relative["y"]
        if ctx.next_event[HINT]=="below":
            obj["y"]=obj["y"]+64 # TODO hardcoded
        if ctx.next_event[HINT]=="right":
            obj["x"]=obj["x"]+64 # TODO hardcoded
        obj[PIC]=ctx.next_event[PIC]
        active_objects_pool[ctx.next_event[KEY]]=obj

    elif ctx.next_event[TYPE]==DELAY:
        ctx.wait_state=ctx.next_event["duration"]
        print("wait state set to : "+str(ctx.wait_state))
    elif ctx.next_event[TYPE]==SOUND:
        print("playing sound " )
        sound_cache[ctx.next_event[FILE]].play()
        obj={}
        soundInMillisecs=sound_cache[ctx.next_event[FILE]].get_length()*1000
        print(" sound ms "+ str(soundInMillisecs))
        obj["left_duration"]=soundInMillisecs/(FRAME_TIME)
        print("number of cycles for sound "+str(obj["left_duration"]))
#        obj["start"]=pygame.time.get_ticks() #TODO refac with cycles, don't keep start
        obj["behavior"]=elapse_time
        active_objects_pool[ctx.next_event[KEY]]=obj
        if gen_scripts:
              global current_sound_to_merge
              sounds_to_merge.append({"index":current_sound_to_merge,FILE:ctx.next_event[FILE],"begin_cycle":current_nb})
              current_sound_to_merge+=1
    elif ctx.next_event[TYPE]==DISAPPEAR:
        active_objects_pool.pop(ctx.next_event[KEY],None)
    elif ctx.next_event[TYPE]==MOVE:
        #we take an already active object
        obj=active_objects_pool[ctx.next_event[KEY]]
        #we take a target object
        target=active_objects_pool[ctx.next_event[TO]]
        print("to : "+str(target) )
        #we calculate target coordinates,
        hint=ctx.next_event[HINT]
        cycles=ctx.next_event[CYCLES]
        #incremental moves in x and y each cycles
        #we assign him the corresponding behavior
        calculate_traj(obj,target,hint,cycles)
        pass
##        {
##            TYPE:MOVE,
##            KEY:"cook",
##            "to":"floor",
##            "hint":"below",
##            "time":2000 #ms
##        },

    return True

def do_wait(ctx):
    #TODO obsolete event type, might suppress
    #TODO not suitable to render, just escaping cycle is better
    #( some other event can have moved and we still need to render )


    #we kill time by busy looping or (wait ) until next event can kick in
    #print("waitstate: "+str(ctx.wait_state))
    if ctx.wait_state>0:
        #print("waiting : "+str(ctx.wait_state))
        before=pygame.time.get_ticks()
        pygame.time.wait(20)
        after=pygame.time.get_ticks()
        ctx.wait_state-=after-before

# render the scene
WHITE = (255, 255, 255)
def render(ctx):
    DISPLAYSURF.fill(WHITE)
    for k in active_objects_pool.keys():
        try:
            to_blit = active_objects_pool[k]
            DISPLAYSURF.blit(pic_cache[to_blit[PIC]],(to_blit["x"],to_blit["y"]))
        except KeyError:
            pass
    #DISPLAYSURF.blit(
    pygame.display.update()

def update_dyn_objects(ctx):
    #print("TODO move dyn objects")
    to_remove=[]
    for key in active_objects_pool.keys():
        #act.
        act=active_objects_pool[key]
        if "behavior" in act.keys():
            act["behavior"](act,key,to_remove)
    for key in to_remove:
        active_objects_pool.pop(key,None)

def play_scenario(ctx):
    pygame.time.set_timer(USEREVENT,FRAME_TIME)

    #we do a while loop until we cursed all items and finished all wait events
    while ctx.index<ctx.max_event:
        for event in pygame.event.get():
            if event.type==USEREVENT or render_pics == True:
#                print("tick")
                if ctx.wait_state<=0:
                    #we need to check if next event is not waiting
                    # fro synchro ( key in active pool to disppear
                            #let's look at the next event
                            #can return false in case we wait
                            #for an event's completion
                            success =consume_event(ctx)
                            if success:
                                ctx.index+=1
                                if ctx.index<ctx.max_event:
                     #arming next event only if event left
                                    ctx.next_event=ctx.script[ctx.index]
                else:
                    do_wait(ctx)
                update_dyn_objects(ctx)
                #displaying picture
                #print("dbg rdr")
                render(ctx)
                global current_nb
                current_nb+=1
                if render_pics  :
                      if (first_render_frame is None or current_nb>=first_render_frame) and (last_render_frame is None or current_nb<=last_render_frame):
#                      if render_pics and first_render_frame>=0 and last_render_frame>=0 and current_nb>=first_render_frame and current_nb<=last_render_frame:
      #                    global current_nb

                          filename="frame"+str(current_nb)+".bmp"
                          print("saving "+filename+" render ")
                          pygame.image.save(DISPLAYSURF,render_folder+filename)
                          concatlist.write("file '" +filename+"'\n")

blank_sound_sh="ffmpeg -f lavfi -i anullsrc=channel_layout="+global_channels+":sample_rate="+global_sample_rate+" -c:a pcm_s16le -t %d %s.wav"

SOUND_LIST_SUFFIX="soundlist.txt"

sound_list_tr_sh="tr '\r' ' ' < %s > %s "
sound_list_tr_name="_do_tr_soundlist.sh"

def gen_sound_list(index,padding,sound):
      slfn=str(index)+SOUND_LIST_SUFFIX
      sound_list=open(render_folder+slfn,'w')
      sound_list.write("file '"+padding+".wav'\n")
      sound_list.write("file '"+sound+"'")
      sound_list.close()
      sound_list=open(render_folder+str(index)+sound_list_tr_name,'w')
      sound_list.write(sound_list_tr_sh%(slfn,"tred"+slfn))
      sound_list.close()



concat_sounds_sh="ffmpeg -f concat -i %s -codec copy %d.wav "

def gen_concat_sounds(index):
      my_sh=open(render_folder+str(sound["index"])+"_concatsounds.sh",'w')
      my_sh.write(concat_sounds_sh%((str(index)+SOUND_LIST_SUFFIX),index))
      my_sh.close()
      #pass


#      ffmpeg -i $TMP/$myfolder/blanksound.avi -i sound.ogg
 #     -filter_complex amix=inputs=2:duration=first
  #    -c:v copy
   #   -c:a pcm_s16le -ac 2
   #   -b:a 1536k -ar 48000
    #  -r 30 $TMP/1.avi

#TODO not sure about target frame rate ( omitted )
cmd_mix_sound_with_final="ffmpeg -i %s -i %s -filter_complex amix=inputs=2:duration=first "
cmd_mix_sound_with_final+="-c:v copy -c:a pcm_s16le -ac "+global_channels_nb+" -ar "+global_sample_rate+" %s "
# -b:a 1536k


#each time after sound mix , the mixed file is renamed as input for next sound
def gen_mix_sound_with_final(index):
      my_sh=open(render_folder+str(index)+"_mix_with_final.sh",'w')

      my_sh.write(cmd_mix_sound_with_final%(avi_input_name_for_sound,str(index)+".wav","mixed.avi"))
      my_sh.close()

      pass

def gen_mix_script(sound):
      print( "gen mix scripts for " +str(sound[FILE]))
      #TODO generate blank sound with same codec
      #for "begin_cycle" duration
      my_sh=open(render_folder+str(sound["index"])+"_padding.sh",'w')
      pad_gen_file_name=str(sound["index"])+"_padding"
      my_sh.write(blank_sound_sh%((sound["begin_cycle"]/FRAME_RATE),pad_gen_file_name))
      my_sh.close()
      #TODO generate list file to use concat
      gen_sound_list(sound["index"],pad_gen_file_name,sound[FILE])
      #TODO add blank and real sound
      #TODO concat sh

      gen_concat_sounds( sound["index"] )

      #TODO mix in on final video
      gen_mix_sound_with_final(sound["index"])


def gen_full_master_script(max_sound_num):
## we write the scripts that calls all the scripts
      my_sh=open(render_folder+"to_tr_masterscript.sh",'w')

      #do tr on frames
      my_sh.write("./trlist.sh \n")
      my_sh.write("./nullsoundgen.sh \n")
## null sound
      #blank sound
      my_sh.write("./blanksoundgen.sh \n")

      # to_mix.avi generated
      #for each index
      index=1
      while index<=max_sound_num:
            if index>1:
                  my_sh.write("mv mixed.avi to_mix.avi\n")
            my_sh.write("./"+str(index)+"_do_tr_soundlist.sh\n")
            my_sh.write("./"+str(index)+"_padding.sh\n")
            my_sh.write("./"+str(index)+"_concatsounds.sh\n")
            my_sh.write("./"+str(index)+"_mix_with_final.sh\n")
            index+=1
      my_sh.write("mv mixed.avi finalraw.avi\n")

## padding
      #do tr
      #concat
      #mix xith to_mix
      #rename mixed to to_mix
      #continue for other sounds

      my_sh.close()
      my_trsh=open(render_folder+"trmaster.sh",'w')
      #WIP
      my_trsh.write("tr '\r' ' ' < to_tr_masterscript.sh > masterscript.sh ")
      my_trsh.close()

#beginning of "main"
#wrapper to pass global around without the dreaded "glob"
class Context(object):
    def __init__(self,script):
        self.script=script #we keep R/O ref
        self.index=0
        self.max_event=len(script)
        self.next_event=script[self.index]
        self.wait_state=0 #this is in ms

#        self.DISPLAYSURF=None
#        self.BASICFONT=None

#index=0
#max_event=len(script)
#next_event=script[index]

ctx=Context(script)

pygame.init()

load_assets()

WIDTH=640
HEIGHT=480

DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))

print( ctx.next_event )
#WIPtrigger event, arm next event, wait next event
play_scenario(ctx)

if render_pics:

    concatlist.close()

if gen_scripts:
    trsh=open(render_folder+"trlist.sh","w")
    trsh.write(list_tr_sh);
    trsh.close();


    nullsoundgen=open(render_folder+"nullsoundgen.sh","w")
    nullsoundgen.write(concat_sh);
    nullsoundgen.close();
    blanksoundgen=open(render_folder+"blanksoundgen.sh","w")
    blanksoundgen.write(blanksound_sh);
    blanksoundgen.close();
    for sound in sounds_to_merge:
          #file
          print("TODO generate scripts to mix in "+str(sound[FILE]))
          gen_mix_script(sound)
    gen_full_master_script(len(sounds_to_merge))
#TODO waiting for key press would be nice
pygame.quit()
sys.exit()
