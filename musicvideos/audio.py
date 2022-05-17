
from pedalboard import VST3Plugin
from soundfile import write
from soundfile import read
from pathlib import Path
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='\033[92;1m| INFO | \033[0m%(message)s')

class Audio:
    def __init__(self, audio):
        if audio is None:
            logger.error(f'Audio file not defined in the AudioMod class...')
            return
        self.audio = audio
        self.file, self.sample_rate = read(audio)
        self.modified = self.file

    def speed(self, speed):
        '''
        This function will change
        the class defined audio file
        speed, you can make it slower
        or faster (0..10 faster) (-10..0 slower)
        '''

        logger.info(f'Changing the speed to "{speed}"...')
        self.sample_rate += int((speed / 25) * self.sample_rate)

    def reverb(self, dry=60, wet=25):
        '''
        This function will add reverb
        to the class defined audio file
        for now, you can only
        change the dry and wet options
        '''

        logger.info(f'Adding reverb with "{dry} dry" "{wet} wet" levels...')
        vst_plugin = str(Path(__file__).parent / "vst/TAL-Reverb-4.vst3")
        vst = VST3Plugin(vst_plugin)
        vst.delay = '0.0000 s'
        vst.diffuse = 100
        vst.modulation_rate = 0
        vst.size = 60
        vst.modulation_depth = 0
        vst.low_cut = 75
        vst.high_cut = 4000
        vst.dry = dry
        vst.wet = wet
        self.modified = vst(self.file, self.sample_rate)

    def export(self, output):
        '''
        This function will write the
        changes to the function defined
        file (output)
        '''

        logger.info(f'Writing the changes to "{output}"...')
        write(output, self.modified, self.sample_rate)

'''

Examples:

(Slowed):
aud = AudioMod('xXXi_wud_nvrstop_UUXXx.wav')
aud.speed(-4)
aud.write('slowed xXXi_wud_nvrstop_UUXXx.wav')

(Nightcore):
aud = AudioMod('xXXi_wud_nvrstop_UUXXx.wav')
aud.speed(5)
aud.write('nightcore xXXi_wud_nvrstop_UUXXx.wav')

(Reverb):
aud = AudioMod('xXXi_wud_nvrstop_UUXXx.wav')
aud.reverb(80, 25)
aud.write('reverbed xXXi_wud_nvrstop_UUXXx.wav')

(Slowed + Reverb):
aud = AudioMod('xXXi_wud_nvrstop_UUXXx.wav')
aud.speed(-4)
aud.reverb(80, 25)
aud.write('slowed_reverb xXXi_wud_nvrstop_UUXXx.wav')

'''