# Slowed Videos Scripts

Various scritps from justcow.


# Install
```sh
pip install musicvideos
```


# Dependencies

You will need to have ffmpeg in your **PATH**.


**Arch Based**
```sh
sudo pacman -S ffmpeg
```
  
  
**Debian Based**
```sh
sudo apt install ffmpeg
```
  
  
**Other**

Just install ffmpeg and make it availabe in your **PATH**.


# Examples


**Downloading audio from soundcloud**
```python
from slowedvideos.audio import downloadurl

# Variables
url = 'https://soundcloud.com/100gecs/gecgecgec'
output = 'downloaded' # It will download as .wav 

downloadurl(url, output)
```
https://soundcloud.com/100gecs/gecgecgec


**Slowing and adding reverb to the downloaded audio**
```python
from slowedvideos.audio import makeslowed

# Variables
audio = 'downloaded.wav'
speed = 10 # This changes how slow the audio will be
output = 'slowed gecgecgec.wav'

makeslowed(audio, speed, output)
```
https://soundcloud.com/justcoww/slowed-gecgecgec


**Creating the video image**
```python
from slowedvideos.video import makevideo

# Variables
cover = 'cover.jpg'
song = 'gecgecgec'
artist = '100 gecs'
toptext = '(Slowed + Reverb)'
video_output = 'video gecgecgec.png'

makevideo(cover, song, artist, toptext, video_output)
```
![video gecgecgec](https://user-images.githubusercontent.com/68345611/158889345-75f4ec35-63e9-4c61-a307-f4332401f743.png)


**Creating the thumbnail image**
```python
from slowedvideos.video import makethumb

# Variables
cover = 'cover.jpg'
thumb_output = 'thumb gecgecgec.png'

makethumb(cover, thumb_output)
```
![thumb gecgecgec](https://user-images.githubusercontent.com/68345611/158889421-41a81372-a2af-453e-9075-99991964b8dd.png)


**Exporting the video**
```python
from slowedvideos.video import exportvideo

# Variables
audio = 'slowed gecgecgec.wav'
image = 'video gecgecgec.png'
output = 'videofile gecgecgec.mp4'
mode = 'moviepy'

exportvideo(audio, image, mode, output)
```
https://user-images.githubusercontent.com/68345611/158889533-050e7a14-7a11-4cee-8437-c6c9e9c77334.mp4
