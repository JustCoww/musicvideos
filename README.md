# Music Videos Scripts

Old slowedvideos now musicvideos, Various scripts from justcow.


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
from musicvideos.tools import download_audio

download_audio('https://soundcloud.com/100gecs/gecgecgec', output='gecgecgec.wav')
```
https://soundcloud.com/100gecs/gecgecgec


**Making the audio faster and adding reverb**
```python
from musicvideos.audio import AudioMod

aud = Audio('gecgecgec.wav')
aud.speed(7)
aud.reverb(dry=0, wet=100)
aud.write(output='gecgecgec but faster and with reverb.wav')
```
https://youtu.be/xjBq9D4kLDE


**Creating the video image**
```python
from musicvideos.video import VideoImages

vid = VideoImages(cover='gec.jpg')
vid.main(toptext='(Sloowed + Reeeverb)', song='gecgecgec', artist='100 gecs')
```
![video](https://user-images.githubusercontent.com/68345611/164984378-fb88442a-4115-4119-9873-958923d93942.png)


**Creating the thumbnail image**
```python
from musicvideos.video import VideoImages

vid = VideoImages(covere='gec.jpg')
vid.thumbnail()
```
![thumbnail](https://user-images.githubusercontent.com/68345611/164984372-e5c687b0-fab3-41c7-ae52-fc0e9d1959e4.png)


**Exporting the video**
```python
from musicvideos.video import exportvideo

exportvideo(image='video.png', audio='gecgecgec but faster and with reverb.wav')
```
https://user-images.githubusercontent.com/68345611/164984364-eb57af53-148f-4949-9747-81561cf8f7c2.mp4
