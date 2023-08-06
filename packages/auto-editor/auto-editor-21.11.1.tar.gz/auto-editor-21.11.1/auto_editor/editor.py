'''editor.py'''

# Included libraries
from usefulFunctions import sep

# Internal libraries
import os
import platform
from shutil import move, rmtree
from urllib.parse import quote

def formatXML(base: int, *args: str) -> str:
    r = ''
    for line in args:
        r += ('\t' * base) + line + '\n'
    return r

def speedup(speed) -> str:
    return formatXML(6, '<filter>', '\t<effect>', '\t\t<name>Time Remap</name>',
        '\t\t<effectid>timeremap</effectid>',
        '\t\t<effectcategory>motion</effectcategory>',
        '\t\t<effecttype>motion</effecttype>',
        '\t\t<mediatype>video</mediatype>',
        '\t\t<parameter authoringApp="PremierePro">',
        '\t\t\t<parameterid>variablespeed</parameterid>',
        '\t\t\t<name>variablespeed</name>', '\t\t\t<valuemin>0</valuemin>',
        '\t\t\t<valuemax>1</valuemax>',
        '\t\t\t<value>0</value>',
        '\t\t</parameter>',
        '\t\t<parameter authoringApp="PremierePro">',
        '\t\t\t<parameterid>speed</parameterid>',  '\t\t\t<name>speed</name>',
        '\t\t\t<valuemin>-100000</valuemin>', '\t\t\t<valuemax>100000</valuemax>',
        f'\t\t\t<value>{speed}</value>',
        '\t\t</parameter>',
        '\t\t<parameter authoringApp="PremierePro">',
        '\t\t\t<parameterid>reverse</parameterid>',
        '\t\t\t<name>reverse</name>', '\t\t\t<value>FALSE</value>',
        '\t\t</parameter>',
        '\t\t<parameter authoringApp="PremierePro">',
        '\t\t\t<parameterid>frameblending</parameterid>',
        '\t\t\t<name>frameblending</name>', '\t\t\t<value>FALSE</value>',
        '\t\t</parameter>', '\t</effect>', '</filter>')

def fixUrl(path: str, resolve: bool) -> str:
    if(platform.system() == 'Windows'):
        if(resolve):
            pathurl = 'file:///' + quote(os.path.abspath(path)).replace('%5C', '/')
        else:
            pathurl = 'file://localhost/' + quote(os.path.abspath(path)).replace('%5C', '/')
    else:
        # Resolve is suprisingly resilient on MacOS.
        pathurl = 'file://localhost' + os.path.abspath(path)
    return pathurl


def fcpXML(myInput: str, temp: str, output, ffprobe, clips, chunks, tracks: int,
    sampleRate, audioFile, fps, log):

    pathurl = 'file://' + os.path.abspath(myInput)
    name = os.path.splitext(os.path.basename(myInput))[0]

    def fraction(inp, fps) -> str:
        from fractions import Fraction

        if(inp == 0):
            return '0s'

        if(isinstance(inp, float)):
            inp = Fraction(inp)
        if(isinstance(fps, float)):
            fps = Fraction(fps)

        frac = Fraction(inp, fps).limit_denominator()
        num = frac.numerator
        dem = frac.denominator

        if(dem < 3000):
            factor = int(3000 / dem)

            if(factor == 3000 / dem):
                num *= factor
                dem *= factor
            else:
                # Good enough but has some error that are impacted at speeds such as 150%.
                total = 0
                while(total < frac):
                    total += Fraction(1, 30)
                num = total.numerator
                dem = total.denominator

        return f'{num}/{dem}s'

    if(not audioFile):
        width, height = ffprobe.getResolution(myInput).split('x')
        total_dur = ffprobe.getDuration(myInput)
        if(total_dur == 'N/A'):
            total_dur = ffprobe.pipe(['-show_entries', 'format=duration', '-of',
                'default=noprint_wrappers=1:nokey=1', myInput]).strip()
    else:
        width, height = '1920', '1080'
        total_dur = ffprobe.getAudioDuration(myInput)
    total_dur = float(total_dur) * fps

    with open(output, 'w', encoding='utf-8') as outfile:

        frame_duration = fraction(1, fps)

        outfile.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        outfile.write('<!DOCTYPE fcpxml>\n\n')
        outfile.write('<fcpxml version="1.9">\n')
        outfile.write('\t<resources>\n')
        outfile.write(f'\t\t<format id="r1" name="FFVideoFormat{height}p{fps}" '\
            f'frameDuration="{frame_duration}" width="{width}" height="{height}"'\
            ' colorSpace="1-1-1 (Rec. 709)"/>\n')

        outfile.write(f'\t\t<asset id="r2" name="{name}" start="0s" '\
            'hasVideo="1" format="r1" hasAudio="1" '\
            f'audioSources="1" audioChannels="2" audioRate="{sampleRate}">\n')

        outfile.write(f'\t\t\t<media-rep kind="original-media" '\
            f'src="{pathurl}"></media-rep>\n')
        outfile.write('\t\t</asset>\n')
        outfile.write('\t</resources>\n')
        outfile.write('\t<library>\n')
        outfile.write('\t\t<event name="auto-editor output">\n')
        outfile.write(f'\t\t\t<project name="{name}">\n')
        outfile.write(formatXML(4,
            f'<sequence format="r1" tcStart="0s" tcFormat="NDF" '\
            'audioLayout="stereo" audioRate="48k">',
            '\t<spine>')
        )

        last_dur = 0

        for j, clip in enumerate(clips):
            clip_dur = (clip[1] - clip[0]) / (clip[2] / 100)
            dur = fraction(clip_dur, fps)

            close = '/' if clip[2] == 100 else ''

            if(last_dur == 0):
                outfile.write(formatXML(6, f'<asset-clip name="{name}" offset="0s" ref="r2"'\
                f' duration="{dur}" audioRole="dialogue" tcFormat="NDF"{close}>'))
            else:
                start = fraction(clip[0] / (clip[2] / 100), fps)
                off = fraction(last_dur, fps)
                outfile.write(formatXML(6,
                    f'<asset-clip name="{name}" offset="{off}" ref="r2"'\
                    f' duration="{dur}" start="{start}" audioRole="dialogue" tcFormat="NDF"{close}>',
                ))

            if(clip[2] != 100):
                # See "Time Maps" in developer.apple.com/library/archive/documentation/FinalCutProX/Reference/FinalCutProXXMLFormat/StoryElements/StoryElements.html

                frac_total = fraction(total_dur, fps)
                total_dur_divided_by_speed = fraction((total_dur) / (clip[2] / 100), fps)

                outfile.write(formatXML(6,
                    '\t<timeMap>',
                    '\t\t<timept time="0s" value="0s" interp="smooth2"/>',
                    f'\t\t<timept time="{total_dur_divided_by_speed}" value="{frac_total}" interp="smooth2"/>',
                    '\t</timeMap>',
                    '</asset-clip>'
                ))

            last_dur += clip_dur

        outfile.write('\t\t\t\t\t</spine>\n')
        outfile.write('\t\t\t\t</sequence>\n')
        outfile.write('\t\t\t</project>\n')
        outfile.write('\t\t</event>\n')
        outfile.write('\t</library>\n')
        outfile.write('</fcpxml>')


def editorXML(myInput: str, temp: str, output, ffprobe, clips, chunks, tracks: int,
    sampleRate, audioFile, resolve: bool, fps, log):

    duration = chunks[len(chunks) - 1][1]
    pathurl = fixUrl(myInput, resolve)
    name = os.path.basename(myInput)

    log.debug('tracks: ' + str(tracks))
    log.debug(os.path.dirname(os.path.abspath(myInput)))

    if(tracks > 1):
        # XML's don't support multiple audio tracks so
        # we need to do some stupid things to get it working.

        inFolder = os.path.dirname(os.path.abspath(myInput))
        name_without_extension = name[:name.rfind(".")]
        newFolderName = f'{inFolder}{sep()}{name_without_extension}_tracks'
        try:
            os.mkdir(newFolderName)
        except OSError:
            rmtree(newFolderName)
            os.mkdir(newFolderName)

        trackurls = [pathurl]
        for i in range(1, tracks):
            newtrack = f'{newFolderName}{sep()}{i}.wav'
            move(f'{temp}{sep()}{i}.wav', newtrack)
            trackurls.append(fixUrl(newtrack, resolve))

    ntsc = 'FALSE'
    ana = 'FALSE' # anamorphic
    depth = '16'
    if(not audioFile):
        width, height = ffprobe.getResolution(myInput).split('x')
    else:
        width = '1920'
        height = '1080'

    pixelar = 'square' # pixel aspect ratio
    colordepth = '24'
    sr = sampleRate
    timebase = str(int(fps))

    if(audioFile):
        groupName = 'Auto-Editor Audio Group'
        with open(output, 'w', encoding='utf-8') as outfile:
            outfile.write('<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE xmeml>\n')
            outfile.write('<xmeml version="4">\n')
            outfile.write('\t<sequence>\n')
            outfile.write(f'\t\t<name>{groupName}</name>\n')
            outfile.write(f'\t\t<duration>{duration}</duration>\n')
            outfile.write('\t\t<rate>\n')
            outfile.write(f'\t\t\t<timebase>{timebase}</timebase>\n')
            outfile.write(f'\t\t\t<ntsc>{ntsc}</ntsc>\n')
            outfile.write('\t\t</rate>\n')
            outfile.write('\t\t<media>\n')

            outfile.write(formatXML(3, '<video>', '\t<format>',
                '\t\t<samplecharacteristics>',
                f'\t\t\t<width>{width}</width>',
                f'\t\t\t<height>{height}</height>',
                f'\t\t\t<pixelaspectratio>{pixelar}</pixelaspectratio>',
                '\t\t\t<rate>',
                f'\t\t\t\t<timebase>{timebase}</timebase>',
                f'\t\t\t\t<ntsc>{ntsc}</ntsc>',
                '\t\t\t</rate>',
                '\t\t</samplecharacteristics>',
                '\t</format>', '</video>'))

            outfile.write(formatXML(3, '<audio>',
                '\t<numOutputChannels>2</numOutputChannels>', '\t<format>',
                '\t\t<samplecharacteristics>',
                '\t\t\t<depth>{depth}</depth>',
                '\t\t\t<samplerate>{sr}</samplerate>',
                '\t\t</samplecharacteristics>',
                '\t</format>'))

            outfile.write('\t\t\t\t<track currentExplodedTrackIndex="0" premiereTrackType="Stereo">\n')

            total = 0
            for j, clip in enumerate(clips):
                myStart = int(total)
                total += (clip[1] - clip[0]) / (clip[2] / 100)
                myEnd = int(total)

                outfile.write(formatXML(5, f'<clipitem id="clipitem-{j+1}">',
                    '\t<masterclipid>masterclip-1</masterclipid>',
                    f'\t<name>{name}</name>',
                    f'\t<start>{myStart}</start>',
                    f'\t<end>{myEnd}</end>',
                    f'\t<in>{int(clip[0] / (clip[2] / 100))}</in>',
                    f'\t<out>{int(clip[1] / (clip[2] / 100))}</out>'))

                if(j == 0):
                    # Define file-1
                    outfile.write(formatXML(6, '<file id="file-1">',
                        f'\t<name>{name}</name>',
                        f'\t<pathurl>{pathurl}</pathurl>',
                        '\t<rate>',
                        f'\t\t<timebase>{timebase}</timebase>',
                        f'\t\t<ntsc>{ntsc}</ntsc>',
                        '\t</rate>',
                        '\t<media>',
                        '\t\t<audio>',
                        '\t\t\t<samplecharacteristics>',
                        f'\t\t\t\t<depth>{depth}</depth>',
                        f'\t\t\t\t<samplerate>{sr}</samplerate>',
                        '\t\t\t</samplecharacteristics>',
                        '\t\t\t<channelcount>2</channelcount>',
                        '\t\t</audio>', '\t</media>', '</file>'))
                else:
                    outfile.write('\t\t\t\t\t\t<file id="file-1"/>\n')
                outfile.write('\t\t\t\t\t\t<sourcetrack>\n')
                outfile.write('\t\t\t\t\t\t\t<mediatype>audio</mediatype>\n')
                outfile.write('\t\t\t\t\t\t\t<trackindex>1</trackindex>\n')
                outfile.write('\t\t\t\t\t\t</sourcetrack>\n')
                outfile.write('\t\t\t\t\t</clipitem>\n')

            outfile.write('\t\t\t\t</track>\n')
            outfile.write('\t\t\t</audio>\n')
            outfile.write('\t\t</media>\n')
            outfile.write('\t</sequence>\n')
            outfile.write('</xmeml>')

            # Exit out of this function prematurely.
            return None

    groupName = 'Auto-Editor Video Group'

    with open(output, 'w', encoding='utf-8') as outfile:
        outfile.write('<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE xmeml>\n')
        outfile.write('<xmeml version="4">\n')
        outfile.write('\t<sequence>\n')
        outfile.write(f'\t\t<name>{groupName}</name>\n')
        outfile.write('\t\t<rate>\n')
        outfile.write(f'\t\t\t<timebase>{timebase}</timebase>\n')
        outfile.write(f'\t\t\t<ntsc>{ntsc}</ntsc>\n')
        outfile.write('\t\t</rate>\n')
        outfile.write('\t\t<media>\n')

        outfile.write(formatXML(3, '<video>', '\t<format>',
            '\t\t<samplecharacteristics>',
            '\t\t\t<rate>',
            f'\t\t\t\t<timebase>{timebase}</timebase>',
            f'\t\t\t\t<ntsc>{ntsc}</ntsc>',
            '\t\t\t</rate>',
            f'\t\t\t<width>{width}</width>',
            f'\t\t\t<height>{height}</height>',
            f'\t\t\t<anamorphic>{ana}</anamorphic>',
            f'\t\t\t<pixelaspectratio>{pixelar}</pixelaspectratio>',
            '\t\t\t<fielddominance>none</fielddominance>',
            f'\t\t\t<colordepth>{colordepth}</colordepth>',
            '\t\t</samplecharacteristics>',
            '\t</format>',
            '\t<track>'))

        # Handle clips.
        total = 0
        for j, clip in enumerate(clips):
            myStart = int(total)
            total += (clip[1] - clip[0]) / (clip[2] / 100)
            myEnd = int(total)

            outfile.write(formatXML(5, f'<clipitem id="clipitem-{j+1}">',
                '\t<masterclipid>masterclip-2</masterclipid>',
                f'\t<name>{name}</name>',
                f'\t<start>{myStart}</start>',
                f'\t<end>{myEnd}</end>',
                f'\t<in>{int(clip[0] / (clip[2] / 100))}</in>',
                f'\t<out>{int(clip[1] / (clip[2] / 100))}</out>'))

            if(j == 0):
                outfile.write(formatXML(6, '<file id="file-1">',
                    f'\t<name>{name}</name>',
                    f'\t<pathurl>{pathurl}</pathurl>',
                    '\t<rate>',
                    f'\t\t<timebase>{timebase}</timebase>',
                    f'\t\t<ntsc>{ntsc}</ntsc>',
                    '\t</rate>',
                    f'\t<duration>{duration}</duration>',
                    '\t<media>', '\t\t<video>',
                    '\t\t\t<samplecharacteristics>',
                    '\t\t\t\t<rate>',
                    f'\t\t\t\t\t<timebase>{timebase}</timebase>',
                    f'\t\t\t\t\t<ntsc>{ntsc}</ntsc>',
                    '\t\t\t\t</rate>',
                    f'\t\t\t\t<width>{width}</width>',
                    f'\t\t\t\t<height>{height}</height>',
                    f'\t\t\t\t<anamorphic>{ana}</anamorphic>',
                    f'\t\t\t\t<pixelaspectratio>{pixelar}</pixelaspectratio>',
                    '\t\t\t\t<fielddominance>none</fielddominance>',
                    '\t\t\t</samplecharacteristics>',
                    '\t\t</video>', '\t\t<audio>',
                    '\t\t\t<samplecharacteristics>',
                    f'\t\t\t\t<depth>{depth}</depth>',
                    f'\t\t\t\t<samplerate>{sr}</samplerate>',
                    '\t\t\t</samplecharacteristics>',
                    '\t\t\t<channelcount>2</channelcount>',
                    '\t\t</audio>', '\t</media>', '</file>'))
            else:
                outfile.write('\t\t\t\t\t\t<file id="file-1"/>\n')

            if(clip[2] != 100):
                outfile.write(speedup(clip[2]))

            # Linking for video blocks
            for i in range(max(3, tracks + 1)):
                outfile.write('\t\t\t\t\t\t<link>\n')
                outfile.write(f'\t\t\t\t\t\t\t<linkclipref>clipitem-{(i*(len(clips)))+j+1}</linkclipref>\n')
                if(i == 0):
                    outfile.write('\t\t\t\t\t\t\t<mediatype>video</mediatype>\n')
                else:
                    outfile.write('\t\t\t\t\t\t\t<mediatype>audio</mediatype>\n')
                if(i == 2):
                    outfile.write('\t\t\t\t\t\t\t<trackindex>2</trackindex>\n')
                else:
                    outfile.write('\t\t\t\t\t\t\t<trackindex>1</trackindex>\n')
                outfile.write(f'\t\t\t\t\t\t\t<clipindex>{j+1}</clipindex>\n')
                if(i > 0):
                    outfile.write('\t\t\t\t\t\t\t<groupindex>1</groupindex>\n')
                outfile.write('\t\t\t\t\t\t</link>\n')

            outfile.write('\t\t\t\t\t</clipitem>\n')

        # End Video; Start Audio
        outfile.write(formatXML(3, '\t</track>', '</video>', '<audio>',
            '\t<numOutputChannels>2</numOutputChannels>',
            '\t<format>',
            '\t\t<samplecharacteristics>',
            f'\t\t\t<depth>{depth}</depth>',
            f'\t\t\t<samplerate>{sr}</samplerate>',
            '\t\t</samplecharacteristics>',
            '\t</format>'))

        # Audio Clips
        for t in range(tracks):
            if(t == 0):
                print('')
            log.debug('t variable: ' + str(t))
            total = 0
            outfile.write('\t\t\t\t<track currentExplodedTrackIndex="0" premiereTrackType="Stereo">\n')

            for j, clip in enumerate(clips):

                clipItemNum = len(clips) + 1 + j + (t * len(clips))

                outfile.write(f'\t\t\t\t\t<clipitem id="clipitem-{clipItemNum}" premiereChannelType="stereo">\n')
                outfile.write('\t\t\t\t\t\t<masterclipid>masterclip-2</masterclipid>\n')
                outfile.write(f'\t\t\t\t\t\t<name>{name}</name>\n')

                myStart = int(total)
                total += (clip[1] - clip[0]) / (clip[2] / 100)
                myEnd = int(total)

                outfile.write(f'\t\t\t\t\t\t<start>{myStart}</start>\n')
                outfile.write(f'\t\t\t\t\t\t<end>{myEnd}</end>\n')

                outfile.write(f'\t\t\t\t\t\t<in>{int(clip[0] / (clip[2] / 100))}</in>\n')
                outfile.write(f'\t\t\t\t\t\t<out>{int(clip[1] / (clip[2] / 100))}</out>\n')

                if(t > 0):
                    # Define arbitrary file
                    outfile.write(formatXML(6, f'<file id="file-{t+1}">',
                        f'\t<name>{name}{t}</name>',
                        f'\t<pathurl>{trackurls[t]}</pathurl>',
                        '\t<rate>',
                        f'\t\t<timebase>{timebase}</timebase>',
                        f'\t\t<ntsc>{ntsc}</ntsc>',
                        '\t</rate>',
                        '\t<media>',
                        '\t\t<audio>',
                        '\t\t\t<samplecharacteristics>',
                        f'\t\t\t\t<depth>{depth}</depth>',
                        f'\t\t\t\t<samplerate>{sr}</samplerate>',
                        '\t\t\t</samplecharacteristics>',
                        '\t\t\t<channelcount>2</channelcount>',
                        '\t\t</audio>', '\t</media>', '</file>'))
                else:
                    outfile.write(f'\t\t\t\t\t\t<file id="file-{t+1}"/>\n')
                outfile.write('\t\t\t\t\t\t<sourcetrack>\n')
                outfile.write('\t\t\t\t\t\t\t<mediatype>audio</mediatype>\n')
                outfile.write('\t\t\t\t\t\t\t<trackindex>1</trackindex>\n')
                outfile.write('\t\t\t\t\t\t</sourcetrack>\n')
                outfile.write('\t\t\t\t\t\t<labels>\n')
                outfile.write('\t\t\t\t\t\t\t<label2>Iris</label2>\n')
                outfile.write('\t\t\t\t\t\t</labels>\n')

                # Add speed effect for audio blocks
                if(clip[2] != 100):
                    outfile.write(speedup(clip[2]))

                outfile.write('\t\t\t\t\t</clipitem>\n')
            outfile.write('\t\t\t\t\t<outputchannelindex>1</outputchannelindex>\n')
            outfile.write('\t\t\t\t</track>\n')

        outfile.write('\t\t\t</audio>\n')
        outfile.write('\t\t</media>\n')
        outfile.write('\t</sequence>\n')
        outfile.write('</xmeml>')

    log.conwrite('')
