
from moviepy.editor import AudioFileClip, ImageClip
from yt_dlp import YoutubeDL
from os import system, remove, chdir
import logging

from musicvideos.youtube import upload

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

def check_if_url(arg):
    '''
    This function will return "True" if the argument is an URL
    or "False" if the argument is not an URL
    '''

    if 'https://' in arg or 'http://' in arg:
        return True
    return False

def download_audio(url, output='downloaded_audio.wav'):
    '''
    This function will use yt-dlp to download
    an audio file from the url defined in the arguments
    and convert it to .wav format
    '''

    ytdl_opts = { 'format': 'bestaudio/best', 'outtmpl':output, 'postprocessors':[{'key': 'FFmpegExtractAudio','preferredcodec': 'wav'}] }
    YoutubeDL(ytdl_opts).download([url])

def download_image(url, output='downloaded_cover.png'):
    '''
    This function will download an image
    from an URL using "request" and
    "shutil" to write the image to a file
    '''

    import requests, shutil
    res = requests.get(url, stream = True)

    if res.status_code == 200:
        with open(output,'wb') as f:
            shutil.copyfileobj(res.raw, f)
        print(f'Cover sucessfully downloaded: {output}')
    else:
        print(prefix, 'Cover could not be downloaded.')

def yt_variables(effects=[], artist='artist', song='song', channel='justcow', features=None, url=None):
    '''
    This function doesn't really serve much purpose other than
    creating the youtube video variables like "title, description, tags and features"
    based on my channel's template (justcow https://www.youtube.com/channel/UCvrcrqw10cPn9SqtgkQxPPQ)
    '''

    channel = 'justcow'
    tags = [artist, channel, song]
    if len(effects) > 1:
        effects_plus = f'({effects[0]} + {effects[1]})'
        effects_and = f'({effects[0]} and {effects[1]})'
        tags.append(f'{effects[0]} {song}')
        tags.append(f'{effects[0]} {effects[1]} {song}')
    else:
        effects_plus = f'({effects[0]})'
        effects_and = f'({effects[0]})'
        tags.append(f'{effects[0]} {song}')
    title = f'{artist} - {song} {effects_plus}'
    description = f'{song} {effects_and} \n\n{artist}'
    if url is not None:
        description = f'{song} {effects_and} \n{url} \n\n{artist} '
    if features is not None:
        for i in features:
            tags.append(i)
            description += f'\n{i}'
    return [title, description, tags]

def compress_file(audio):
    '''
    This function will get an .wav file
    and convert it to mp3, then it will delete
    the original .wav file
    '''

    system(f'ffmpeg -i "{audio}" -vn -ar 44100 -ac 2 -b:a 320k "{audio.replace(".wav", ".mp3")}"')
    remove(audio)
