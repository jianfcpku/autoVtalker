from src import utils
import sys
import soundfile as sf
import pyworld as pw
WAVpath = sys.argv[1]
inGrid = open(sys.argv[2], 'r')
outVSQX = open(sys.argv[3], 'w')

x, fs = sf.read(WAVpath)
f0, t = pw.dio(x, fs, frame_period = utils.ms_per_dot)
utils.write_head(outVSQX, tot_time = t[-1]*1500)

utils.write_pit(outVSQX, f0, t)
utils.write_note(outVSQX, inGrid)
utils.write_tail(outVSQX)
inGrid.close()
outVSQX.close()