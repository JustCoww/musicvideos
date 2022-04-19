class AudioModifier:
    def __init__(self, audio, name):
        from soundfile import read
        self.name = name
        self.file, self.sample_rate = read(audio)
        self.audio = audio
        self.modified = self.file

    def speed(self, speed):
        '''
        This function will change
        the class defined audio file
        speed, you can make it slower
        or faster (0..10 faster) (-10..0 slower)
        '''

        prefix = '[Speed Modifier]'
        
        print(prefix, 'Changing the speed...')
        self.sample_rate += int((speed / 25) * self.sample_rate)

        return print(prefix, 'Done')

    def reverb(self, dry, wet):
        '''
        This function will add reverb
        to the class defined audio file
        for now, you can only
        change the dry and wet options
        '''

        prefix = '[Reverb]'

        print(prefix, 'Adding reverb...')
        from pedalboard import VST3Plugin
        from pathlib import Path
        vst = VST3Plugin(str(Path(__file__).parent / "vst/TAL-Reverb-4.vst3"))
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

        return print(prefix, 'Done')

    def write(self):

        prefix = '[Audio Modifier]'

        print(prefix, 'Writing the changes to the file...')
        from soundfile import write
        output = f'modified {self.name}.wav'
        write(output, self.modified, self.sample_rate)
        return print(prefix, 'Done')