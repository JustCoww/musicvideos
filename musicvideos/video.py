class Video:
    def __init__(self):
        prefix =  '[Video]'
        print(prefix, 'Initialized...')

    def info(self, **info):
        prefix =  '[Video Info]'
        print(prefix, 'Getting info...')
        if 'cover' in info:
            self.cover = info['cover']
        if 'toptext' in info:
            self.toptext = info['toptext']
        if 'song' in info:
            self.song = info['song']
        if 'artist' in info:
            self.artist = info['artist']
        if 'audio' in info:
            self.audio = info['audio']

    def thumbnail(self):
        '''
        This function will use PILLOW
        to create a thumbnail image with the defined image
        the thumbnail will be a blurred and stretched version of the original
        image but covering the whole screen and the original image with rounded corners
        in the middle of the screen
        '''

        try: self.cover, self.song
        except Exception as e:
            print(f'[ERROR] {e} (Check if you defined both the "song and cover" variables in Video.info() )')
            return

        output = f'thumbnail {self.song}.png'
        self.thumbnail = output

        prefix = '[Thumbnail PNG]'

        from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

        # Sizes
        x, y = (626, 626) # Cover size
        X, Y = (1920, 1080) # Background size
        
        # Get the middle coordinates of the image
        middleX = int((X-x) / 2)
        middleY = int((Y-y) / 2)
        middle = (middleX, middleY)
        
        # Import cover
        print(prefix, f'Importing {self.cover} ...')
        tb = Image.open(self.cover)
        cv = Image.open(self.cover)

        # Resizing
        print(prefix, 'Resizing cover and background...')
        cv = cv.resize((x, y))
        tb = tb.resize((X, Y))
        
        # Create a rounded cornered square mask for the rounded cover
        rad = 45
        circle = Image.new('L', (rad * 2, rad * 2), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
        rounded_mask = Image.new('L', (x, y), "white")
        rounded_mask.paste(circle.crop((0, 0, rad, rad)), (0, 0))
        rounded_mask.paste(circle.crop((0, rad, rad, rad * 2)), (0, y - rad))
        rounded_mask.paste(circle.crop((rad, 0, rad * 2, rad)), (x - rad, 0))
        rounded_mask.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (x - rad, y - rad))
        
        # Add a shadow (Black square with blur)
        print(prefix, 'Creating the shadow...')
        square = Image.new(mode = "RGBA", size = (x, y), color = 'black')
        tb.paste(square, middle, rounded_mask)

        # Blur and turn brightness down
        print(prefix, 'Adding blur to background...')
        tb = ImageEnhance.Brightness(tb).enhance(0.4)
        tb = tb.filter(ImageFilter.GaussianBlur(25))

        # Paste cover into the background
        print(prefix, 'Merging cover with background...')
        tb.paste(cv, middle, rounded_mask)
        
        # Export final thing to a file
        print(prefix, f'Exporting thumbnail as {output} ...')
        tb.save(output)
        
        return print(prefix, 'Done')
        
    def video(self):
        '''
        This function will use PILLOW
        to create a video image with the defined image
        it will be a blurred and stretched version of the original
        image but covering the whole screen with the original image with rounded corners
        in the middle of the screen and some text saying the name of the song, a top text, and the artist
        '''

        try: self.cover, self.toptext, self.song, self.artist
        except Exception as e:
            print(f'[ERROR] {e} (Check if you defined all the "cover, toptext, song, artist" variables in Video.info() )')
            return

        output = f'video {self.song}.png'
        self.video = output

        prefix = '[Video PNG]'

        from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
        from importlib import resources
        import io

        x, y = (2500, 2500) # Cover size
        X, Y = (7680, 4320) # Background size

        # Import cover
        print(prefix, f'Importing {self.cover} ...')
        bg = Image.open(self.cover)
        cv = Image.open(self.cover)

        # Middles
        middleX = int((X-x) / 2)
        middleY = int((Y-y) / 2)
        middle = (middleX, middleY)

        # Resizing
        print(prefix, 'Resizing cover and background...')
        cv = cv.resize((x, y))
        bg = bg.resize((X, Y))

        # Create a rounded cornered square mask for the rounded cover
        rad = 100
        circle = Image.new('L', (rad * 2, rad * 2), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
        rounded_mask = Image.new('L', (x, y), "white")
        rounded_mask.paste(circle.crop((0, 0, rad, rad)), (0, 0))
        rounded_mask.paste(circle.crop((0, rad, rad, rad * 2)), (0, y - rad))
        rounded_mask.paste(circle.crop((rad, 0, rad * 2, rad)), (x - rad, 0))
        rounded_mask.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (x - rad, y - rad))

        # Add a shadow (Black square with blur)
        print(prefix, 'Creating the shadow...')
        square = Image.new(mode = "RGBA", size = (2500, 2500), color = 'black')
        bg.paste(square, (middleX, 659), rounded_mask)

        # Blur and turn brightness down
        print(prefix, 'Adding blur to background...')
        bg = ImageEnhance.Brightness(bg).enhance(0.4)
        bg = bg.filter(ImageFilter.GaussianBlur(120))

        # Paste cover into the background
        print(prefix, 'Merging cover with background')
        bg.paste(cv, (middleX, 659), rounded_mask)


        ### Text
        text = ImageDraw.Draw(bg)

        # Layout is [text, y-coordinates (from top), font, font-size]
        toptext = [self.toptext, 300, 'toptext_font.ttf', 250]
        song = [self.song, 3250, 'down1_font.ttf', 279]
        artist = [self.artist, 3640, 'down2_font.ttf', 186]

        # Generate the text
        for i in [toptext, song, artist]:

            # Get font from module subfolder "makeimages"
            with resources.open_binary('musicvideos.fonts', i[2]) as font:
                font = io.BytesIO(font.read())
            
            print(prefix, f'Writing "{i[0]}" with "{i[2]}" font')
            font = ImageFont.truetype(font, i[3])
            x, y = text.textsize(i[0], font=font)
            text.text(((X-x)/2, i[1]), i[0], fill='white', font=font, align='center')

        # Export final thing to a file
        print(prefix, f'Exporting file as {output} ...')
        bg.save(output)

        return print(prefix, 'Done')

    def export(self):
        
        try: self.video, self.audio, self.song
        except Exception as e:
            print(f'[ERROR] {e} (Check if you ran Video.video() and defined the "audio" variable in Video.info() before running the export)')
            return

        output = f'videofile {self.song}.mp4'
        self.video = f'video {self.song}.png'
        
        prefix = '[Export MP4]'

        from moviepy.editor import AudioFileClip, ImageClip
        print(prefix, 'Starting to export video with "MOVIEPY"')

        # Import files
        print(prefix, f'Importing {self.audio}, {self.video} ...')
        audio = AudioFileClip(self.audio)
        video = ImageClip(self.video)
        
        # Mix into video
        print(prefix, 'Setting audio...')
        video = video.set_audio(audio)
        print(prefix, 'Setting video duration...')
        video.duration = audio.duration
        print(prefix, 'Setting video at 1 fps...')
        video.fps = 1
        print(prefix, f'Exporting {output}...')
        video.write_videofile(output)

        return print(prefix, 'Done')