from pathlib import Path

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise

self_path = Path(__file__)

viola_sf = SimpleFormat(
    midis=[60, 66, 64, 71],
    quarter_durations=[1, 2, 1.5, 3.5]
)



sf.chords[0].add_dynamics('ff')
sf.chords[0].add_articulation('staccato')
sf.chords[1].add_dynamics('pp')
sf.chords[1].add_slur('start')
sf.chords[-1].add_slur('stop')

score = TreeScoreTimewise()
sf.to_stream_voice().add_to_score(score)
xml_path = self_path.with_suffix('.xml')
score.write(path=xml_path)
