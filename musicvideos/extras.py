from musicvideos.tools import yt_variables, download_audio, download_cover, check_if_url, export, compress
from musicvideos.video import VideoIMG
from musicvideos.audio import AudioMod
from musicvideos.youtube import upload

from os import mkdir, chdir, getcwd

class PublishVideo:
    def __init__(self):
        self.effects = []

    def files(self, audio=None, cover=None):
        
        if check_if_url(audio):
            self.audio_download = True
        else:
            self.audio_download = False
        self.audio = audio
        if check_if_url(cover):
            self.cover_download = True
        else:
            self.cover_download = False
        self.cover = cover

    def speed(self, speed):
        self.speed = speed
        if speed > 0:
            self.effects.append('Nightcore')
        elif speed < 0:
            self.effects.append('Slowed')

    def reverb(self, dry, wet):
        self.reverb = dry, wet
        if wet > 0:
            self.effects.append('Reverb')

    def info(self, artist='artist', song='song', toptext=None):
        self.artist = artist
        self.song = song
        self.videofile = f'videofile {self.song}.mp4'
        self.videoimgfile = f'video {self.song}.png'
        self.thumbfile = f'thumb {self.song}.png'
        if toptext is not None:
            self.toptext = f'({toptext})'
            self.effects = [toptext]
            self.folder = f'{toptext.lower()} {self.song}'
            self.audiofile = f'{toptext.lower()} {self.song}.wav'
        elif len(self.effects) != 0:
            self.folder = f'{self.effects[0].lower()} {self.song}'
            self.audiofile = f'{self.effects[0].lower()} {self.song}.wav'
            if len(self.effects) > 1:
                self.toptext = f'({self.effects[0]} + {self.effects[1]})'
            else:
                self.toptext = f'({self.effects[0]})'
        else:
            self.toptext = ''
            self.audiofile = f'pagman? {self.song}.wav'
            self.folder = f'pagman? {self.song}'

    def make(self, compress_files=False, upload_yt=None, secrets_folder=None, client_secrets=None):

        new_folder = False
        self.starting_directory = getcwd()
        while not new_folder:
            try:
                mkdir(self.folder)
                chdir(self.folder)
                new_folder = True
            except Exception as e:
                print(e)
                chdir(self.folder)

        self.files_directory = getcwd()
        
        if self.audio_download:
            self.audio = download_audio(self.audio, outFile='original.wav')
            print(self.audio)

        if self.cover_download:
            self.cover = download_cover(self.cover, outFile='cover.png')

        self.youtube_variables = yt_variables(effects=self.effects, artist=self.artist, song=self.song)


        vid = VideoIMG(coverFile=self.cover)
        vid.video(toptext=self.toptext, song=self.song, artist=self.artist, outFile=self.videoimgfile)
        vid.thumbnail(outFile=self.thumbfile)

        aud = AudioMod(audioFile=self.audio)
        aud.speed(self.speed)
        aud.reverb(dry=self.reverb[0], wet=self.reverb[1])
        aud.write(self.audiofile)

        export(image=self.videoimgfile, audio=self.audiofile, outFile=self.videofile)

        if compress_files:
            compress(self.audio)
            compress(self.audiofile)

        chdir(self.starting_directory)


    def upload(self, client_secrets='client_secrets.json'):
        if '/' in client_secrets:
            slash_location = client_secrets.rfind('/')
            chdir(client_secrets[:slash_location])
        upload(client_secrets=client_secrets, video_file=f'{self.files_directory}/{self.videofile}', thumbnail=f'{self.files_directory}/{self.thumbfile}', category='10', 
                title=self.youtube_variables[0], description=self.youtube_variables[1], tags=self.youtube_variables[2])
        chdir(self.starting_directory)
        
'''

Exemple:

new_video = PublishVideo()
new_video.files(audio='https://soundcloud.com/vodgka/laura-les-what-do-i-know-20190208', cover='http://avyss-magazine.com/wp-content/uploads/2019/10/100-gecs_remix.jpg')
new_video.speed(-4)
new_video.reverb(dry=80, wet=25)
new_video.info(artist='Laura Les', song='what do i know')
new_video.make(compress_files=True)
new_video.upload(client_secrets='/home/justcow/code/musicvideos/musicvideos/secrets/client_secrets.json')

'''