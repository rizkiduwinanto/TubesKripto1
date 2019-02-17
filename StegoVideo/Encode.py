from VideoParser import getVideo, writeVideo
from VideoSteganography import encode

encodedFrames = encode(video.frames, 'test.txt')