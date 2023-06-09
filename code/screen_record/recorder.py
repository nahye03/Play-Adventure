from .audio import Audio
from .video import Video
from uuid import uuid1
from os import mkdir,listdir,getcwd
from threading import Thread
import ffmpeg
from .exceptions import ffmpegerror
class Recorder(Video,Audio):
    def __init__(self,x,y,w,h):
        unique_id = uuid1()
        self.unique_id = unique_id
        directory = listdir("./screen_record/")
        if "tmp" not in directory:
            mkdir("./screen_record/tmp")
        Video.__init__(self,self.unique_id,x,y,w,h)
        Audio.__init__(self,self.unique_id)
        
    
    def record_screen(self):
        video_thread = Thread(target=self._record_video)
        audio_thread = Thread(target=self._record_audio)
        video_thread.start()
        audio_thread.start()

    def _combine_audio_and_video(self,path):
        try:
            video = ffmpeg.input(getcwd() + '/screen_record/tmp/{}.avi'.format(self.unique_id))
            audio = ffmpeg.input(getcwd() + '/screen_record/tmp/{}.wav'.format(self.unique_id))
            out = ffmpeg.output(video, audio, path, vcodec='copy', acodec='aac', strict='experimental')
            # out = ffmpeg.output(video, path, vcodec='copy', acodec='aac', strict='experimental')
            out.run()
        except:
            raise ffmpegerror(path)
        

    def stop(self):
        self.record=False
        
        
    def save(self,path):
        print("Saving....")
        self._combine_audio_and_video(path)
        print("FILE SAVED")

        

