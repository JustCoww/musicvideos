from moviepy.editor import AudioFileClip, ImageClip
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='\033[92;1m| INFO | \033[0m%(message)s')

def exportvideo(image=None, audio=None, output='video.mp4'):
    '''
    This function will create a video
    with the defined image and the defined audio.

    Example:

    export(audio='nightcore xXXi_wud_nvrstop_UUXXx.wav', image='video.png', outFile='videofile pagmann.mp4')

    '''

    logger.debug('Checking arguments...')
    variables = [('image', image), ('audio', audio)]
    for i in variables:
        if i[1] is None:
            print(f'{i[0]} is not defined')
            return

    # Import files
    logger.info(f'Opening files "{audio}" "{image}"...')
    audio = AudioFileClip(audio)
    video = ImageClip(image)

    # Mix into video
    logger.debug(f'Setting up audio and video to export...')
    video = video.set_audio(audio)
    video.duration = audio.duration
    video.fps = 1
    logger.info(f'Exporting video to "{output}"...')
    video.write_videofile(output)
    return output
