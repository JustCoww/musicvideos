class BuildVideo:
    def __init__(self):
        prefix =  '[BuildVideo]'
        print(prefix, 'Initialized...')

    def files(self, **info):
        prefix =  '[BuildVideo Files]'
        print(prefix, 'Getting files...')
        if 'audio' in info:
            self.audio = info['audio']
        if 'cover' in info:
            self.cover = info['cover']

    def audio(self, **modifiers):
        prefix =  '[BuildVideo Audio]'
        print(prefix, 'Doing things with the audio modifiers...')
        self.modify_speed = (False, 0)
        self.modify_reverb = (False, (0, 0))
        if 'speed' in modifiers:
            self.modify_speed = (True, modifiers['speed'])
        if 'reverb' in modifiers:
            self.modify_reverb = (True, modifiers['reverb'])

    def info(self, **info):
        prefix =  '[BuildVideo Info]'
        print(prefix, 'Getting info...')
        if 'toptext' in info:
            self.toptext = info['toptext']
        if 'song' in info:
            self.song = info['song']
        if 'artist' in info:
            self.artist = info['artist']

    def make(self):
        prefix =  '[BuildVideo Make]'
        print(prefix, 'Initialized...')
        from musicvideos.video import Video
        from musicvideos.audio import AudioModifier
        from multiprocessing import Process
        try: self.toptext
        except: 
            self.toptext = []
            if self.modify_speed[0]:
                if self.modify_speed[1] > 0:
                    self.toptext.append('Nightcore')
                elif self.modify_speed[1] < 0:
                    self.toptext.append('Slowed')
            if self.modify_reverb[0]:
                self.toptext.append('Reverb')
            if len(self.toptext) > 1:
                self.toptext = f'({self.toptext[0]} + {self.toptext[1]})'
            else:
                self.toptext = f'({self.toptext[0]})'

        # Downloads
        if Tools.check_if_url(self, self.audio):
            print(prefix, 'Downloading audio...')
            Tools.download_audio(self, self.audio)
        if Tools.check_if_url(self, self.cover):
            print(prefix, 'Downloading cover...')
            Tools.download_cover(self, self.cover)

        # Video

        vid = Video()
        vid.info(toptext=self.toptext, song=self.song, artist=self.artist, cover=self.cover, audio=f'modified {self.song}.wav')
        audio = AudioModifier(self.audio, self.song)

        if self.modify_speed[0]:
            audio.speed(self.modify_speed[1])
        if self.modify_reverb[0]:
            audio.reverb(self.modify_reverb[1][0], self.modify_reverb[1][1])


        print(prefix, 'Starting multiprocessing jobs...')
        video_img_cmd = Process(target=vid.video)
        thumb_img_cmd = Process(target=vid.thumbnail)
        export_video_cmd = Process(target=vid.export)
        audio_write_cmd = Process(target=audio.write)

        video_img_cmd.start()
        thumb_img_cmd.start()
        audio_write_cmd.start()
        video_img_cmd.join()
        audio_write_cmd.join()
        export_video_cmd.start()
        export_video_cmd.join()
        thumb_img_cmd.join()

class Tools:
    def check_if_url(self, url):
        if 'https://' in url or 'http://' in url:
            return True
        return False

    def download_audio(self, url):
        prefix = '[Audio Downloader]'
        from yt_dlp import YoutubeDL
        self.audio = self.song + '.wav'
        ytdl_opts = { 'format': 'bestaudio/best', 'outtmpl':self.audio, 'postprocessors':[{'key': 'FFmpegExtractAudio','preferredcodec': 'wav'}] }
        print(prefix, 'Downloading audio...')
        YoutubeDL(ytdl_opts).download([url])

    def download_cover(self, url):
        import requests, shutil
        prefix = '[Download Cover]'
        file_name = 'cover.png'
        res = requests.get(url, stream = True)

        if res.status_code == 200:
            with open(file_name,'wb') as f:
                shutil.copyfileobj(res.raw, f)
            print(prefix, f'Cover sucessfully downloaded: {file_name}')
            self.cover = file_name
        else:
            print(prefix, 'Cover could not be downloaded.')