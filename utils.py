from pydub import AudioSegment
from pydub.playback import play
import os

def play_sample_sound(filename):
    play(AudioSegment.from_file(filename, sample_width=10)[5000:10000].fade_in(1000).fade_out(1000))


def filter_item_by_attribute(items, attribute):
    return filter(lambda x: x[attribute] >= max(map(lambda x: x[attribute], items)), items)[0]


def assert_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)