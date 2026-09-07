"""Original synthesized score and game sounds. No samples or dependencies."""
from array import array
import math
from pathlib import Path
import random
import wave

RATE = 22050
OUT = Path(__file__).resolve().parents[1] / "assets" / "audio"
OUT.mkdir(parents=True, exist_ok=True)
random.seed(71)
TAU = math.tau

def save(name, values):
    samples = array("h", (int(max(-1, min(1, x)) * 29000) for x in values))
    with wave.open(str(OUT / (name + ".wav")), "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(RATE)
        f.writeframes(samples.tobytes())

def freq(midi):
    return 440 * 2 ** ((midi - 69) / 12)

beat = 60 / 104
duration = beat * 32
track = [0.0] * int(RATE * duration)

def note(start, length, midi, volume, kind="pluck"):
    hz = freq(midi)
    base = int(start * RATE)
    for j in range(int(length * RATE)):
        k = base + j
        if k >= len(track):
            break
        t = j / RATE
        if kind == "pad":
            env = min(1, t / 0.4) * min(1, (length - t) / 0.5)
            value = (math.sin(TAU * hz * t) + 0.3 * math.sin(TAU * hz * 1.003 * t) + 0.16 * math.sin(TAU * hz * 2 * t)) * env
        else:
            env = min(1, t / 0.009) * math.exp(-t * (5 if kind == "pluck" else 3.5))
            value = (math.sin(TAU * hz * t) + 0.25 * math.sin(TAU * hz * 2 * t) + 0.11 * math.sin(TAU * hz * 3 * t)) * env
        track[k] += volume * value

chords = [(38, [62,65,69,72]), (34, [62,65,70,74]), (41, [60,65,69,72]), (36, [60,64,67,74])]
for bar in range(8):
    bass, chord = chords[(bar // 2) % 4]
    start = bar * 4 * beat
    for pitch in chord:
        note(start, beat * 4, pitch - 12, 0.027, "pad")
    for step in range(8):
        note(start + step * beat / 2, beat * 0.85, chord[[0,2,1,3,2,1,3,2][step]] + 12, 0.07 if step % 2 == 0 else 0.045)
        note(start + step * beat / 2, beat * 0.8, bass, 0.11, "bass")
        if step in [0,4]:
            at = int((start + step * beat / 2) * RATE)
            for j in range(int(RATE * 0.20)):
                if at + j < len(track):
                    t = j / RATE
                    track[at+j] += math.sin(TAU * (48 * t + 4 * (1 - math.exp(-t * 33)))) * math.exp(-t * 22) * 0.31
        if step in [2,6]:
            at = int((start + step * beat / 2) * RATE)
            for j in range(int(RATE * 0.13)):
                if at+j < len(track):
                    t = j/RATE
                    track[at+j] += (random.uniform(-1,1) * 0.13 + math.sin(TAU * 175*t) * 0.06) * math.exp(-t*29)
        at = int((start + step * beat / 2) * RATE)
        for j in range(int(RATE * 0.045)):
            if at+j < len(track):
                track[at+j] += random.uniform(-1,1) * math.exp(-j/RATE*95) * 0.038
save("music", track)

road = []
smooth = 0
for i in range(RATE * 4):
    t = i / RATE
    smooth = smooth * 0.91 + random.uniform(-1,1) * 0.09
    road.append(smooth * 0.65 + math.sin(TAU*42*t)*0.07 + math.sin(TAU*63*t)*0.025)
save("road", road)

def effect(name, length, start_hz, end_hz, noise=0, volume=0.6):
    values = []
    phase = 0
    smooth = 0
    for i in range(int(length * RATE)):
        t = i / RATE
        u = t / length
        hz = start_hz * (end_hz / start_hz) ** u
        phase += hz * TAU / RATE
        smooth = smooth * 0.5 + random.uniform(-1,1) * 0.5
        env = min(1, t/0.004) * (1-u) ** 1.7
        values.append((math.sin(phase) * (1-noise) + smooth * noise) * env * volume)
    save(name, values)

effect("shoot", .12, 1450, 420, .14, .38)
effect("charge", .35, 2400, 180, .22, .7)
effect("jump", .20, 260, 1000, .04, .45)
effect("dash", .24, 800, 180, .85, .9)
effect("slash", .23, 1700, 270, .78, .8)
effect("hit", .10, 190, 65, .50, .65)
effect("pickup", .24, 1100, 2000, 0, .36)
effect("explode", .55, 110, 32, .72, .95)
effect("hurt", .31, 220, 60, .35, .8)
effect("warning", .75, 740, 580, 0, .42)
effect("enemy", .18, 550, 180, .1, .4)
effect("victory", 1.8, 440, 1760, .04, .6)
print("Wrote original score, road ambience and 12 sound effects.")
