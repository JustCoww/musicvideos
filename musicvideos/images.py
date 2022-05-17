
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from importlib import resources
import logging
import io

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='\033[92;1m| INFO | \033[0m%(message)s')

class VideoImages:
    def __init__(self, cover=None):
        if cover is None:
            logger.error(f'Cover file not defined in the VideoIMG class...')
            return
        self.cover = cover

    def thumbnail(self, output='thumbnail.png'):
        '''
        This function will use PILLOW
        to create a thumbnail image with the defined image
        the thumbnail will be a blurred and stretched version of the original
        image but covering the whole screen and the original image with rounded corners
        in the middle of the screen
        '''

        # Sizes
        logger.debug('Creating size variables')
        x, y = (626, 626) # Cover size
        X, Y = (1920, 1080) # Background size

        # Get the middle coordinates of the image
        logger.debug('Creating middleX, middleY and middle variables...')
        middleX = int((X-x) / 2)
        middleY = int((Y-y) / 2)
        middle = (middleX, middleY)

        # Import cover
        logger.info('Opening cover image...')
        tb = Image.open(self.cover)
        tb = tb.convert('RGBA')
        cv = Image.open(self.cover)

        # Resizing
        logger.debug('Resizing cover and background...')
        cv = cv.resize((x, y))
        tb = tb.resize((X, Y))

        # Create a rounded cornered square mask for the rounded cover
        logger.debug('Creating rounded square mask')
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
        logger.info('Creating the shadow')
        square = Image.new(mode = "RGBA", size = (x, y), color = 'black')
        tb.paste(square, middle, rounded_mask)

        # Blur and turn brightness down
        logger.info('Adding blur to the background')
        tb = ImageEnhance.Brightness(tb).enhance(0.4)
        tb = tb.filter(ImageFilter.GaussianBlur(25))

        # Paste cover into the background
        logger.debug('Pasting cover in background with the rounded square mask')
        tb.paste(cv, middle, rounded_mask)

        # Export final thing to a file
        logger.info(f'Exporting file as "{output}"...')
        tb.save(output)

    def main(self, toptext=None, song=None, artist=None, output='video.png'):
        '''
        This function will use PILLOW
        to create a video image with the defined image
        it will be a blurred and stretched version of the original
        image but covering the whole screen with the original image with rounded corners
        in the middle of the screen and some text saying the name of the song, a top text, and the artist
        '''

        logger.debug('Checking arguments...')
        variables = [('toptext', toptext),('song', song), ('artist', artist)]
        for i in variables:
            if i[1] is None:
                print(f'{i[0]} is not defined')
                return

        # Sizes
        logger.debug('Creating size variables')
        x, y = (2500, 2500) # Cover size
        X, Y = (7680, 4320) # Background size



        # Get the middle coordinates of the image
        logger.debug('Creating middleX, middleY and middle variables...')
        middleX = int((X-x) / 2)
        middleY = int((Y-y) / 2)
        middle = (middleX, middleY)

        # Import cover
        logger.info('Opening cover image...')
        bg = Image.open(self.cover)
        bg = bg.convert('RGBA')
        cv = Image.open(self.cover)

        # Resizing
        logger.debug('Resizing cover and background...')
        cv = cv.resize((x, y))
        bg = bg.resize((X, Y))

        # Create a rounded cornered square mask for the rounded cover
        logger.debug('Creating rounded square mask')
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
        logger.info('Creating the shadow')
        square = Image.new(mode = "RGBA", size = (2500, 2500), color = 'black')
        bg.paste(square, (middleX, 659), rounded_mask)

        # Blur and turn brightness down
        logger.info('Adding blur to the background')
        bg = ImageEnhance.Brightness(bg).enhance(0.4)
        bg = bg.filter(ImageFilter.GaussianBlur(120))

        # Paste cover into the background
        logger.debug('Pasting cover in background with the rounded square mask')
        bg.paste(cv, (middleX, 659), rounded_mask)

        # Layout is [text, y-coordinates (from top), font, font-size]
        logger.debug('Setting up text things (text, y-coordinates, font, font-size)...')
        toptext_t = [toptext, 300, 'toptext.ttf', 250]
        song_t = [song, 3250, 'down1.ttf', 279]
        artist_t = [artist, 3640, 'down2.ttf', 186]

        # Generate the text
        text = ImageDraw.Draw(bg)
        for i in [toptext_t, song_t, artist_t]:
            # Get font from module subfolder "makeimages"
            with resources.open_binary('musicvideos.fonts', i[2]) as font:
                font = io.BytesIO(font.read())

            logger.info(f'Writing "{i[0]}" with "{i[2]}"...')
            font = ImageFont.truetype(font, i[3])
            x, y = text.textsize(i[0], font=font)
            text.text(((X-x)/2, i[1]), i[0], fill='white', font=font, align='center')


        # Export final thing to a file
        logger.info(f'Exporting file as "{output}"...')
        bg.save(output)

'''

Example:

vid = VideoIMG(coverFile='pagman.png')
vid.video(toptext='(Reverb + Slowed)', song='fadeeed', artist='alanwalker', outFile='video faaaded.png')
vid.thumbnail(outFile='thumb faddeeed.png')

'''