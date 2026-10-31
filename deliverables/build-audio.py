import json
import wave
from pathlib import Path

root = Path(__file__).parent
scenes = json.loads((root / 'narration.json').read_text(encoding='utf-8'))['scenes']
clips = []
output = root / 'chalukou-voice.wav'
subtitles = root / 'chalukou-demo.srt'
entries = []
clip_index = 0
params = None
frames_per_second = 16000


def timestamp(seconds):
    milliseconds = round(seconds * 1000)
    hours, milliseconds = divmod(milliseconds, 3600000)
    minutes, milliseconds = divmod(milliseconds, 60000)
    secs, milliseconds = divmod(milliseconds, 1000)
    return f'{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}'


def wrap(text, width=20):
    if len(text) <= width:
        return text
    lines = []
    while text:
        lines.append(text[:width])
        text = text[width:]
    return '\n'.join(lines)


with wave.open(str(output), 'wb') as combined:
    for scene in scenes:
        cursor = float(scene['start'])
        for sentence in scene['sentences']:
            clip_index += 1
            path = root / 'audio' / f'{clip_index:02d}.wav'
            with wave.open(str(path), 'rb') as clip:
                current_params = clip.getparams()
                if params is None:
                    params = current_params
                    combined.setparams(params)
                    frames_per_second = clip.getframerate()
                assert clip.getnchannels() == params.nchannels
                assert clip.getsampwidth() == params.sampwidth
                assert clip.getframerate() == params.framerate
                frames = clip.readframes(clip.getnframes())
                duration = clip.getnframes() / clip.getframerate()
            combined.writeframes(frames)
            entries.append((cursor, cursor + duration, sentence))
            cursor += duration
            silence = 0.45
            combined.writeframes(b'\x00' * int(frames_per_second * silence) * params.sampwidth * params.nchannels)
            cursor += silence
        remaining = float(scene['end']) - cursor
        assert remaining >= 0, f'配音超出场景：{scene["name"]} {-remaining:.2f}s'
        combined.writeframes(b'\x00' * int(frames_per_second * remaining) * params.sampwidth * params.nchannels)

subtitles.write_text('\n\n'.join(
    f'{index}\n{timestamp(start)} --> {timestamp(end)}\n{wrap(text)}'
    for index, (start, end, text) in enumerate(entries, 1)
) + '\n', encoding='utf-8')
print(f'clips={clip_index}; subtitles={len(entries)}; output={output}')
