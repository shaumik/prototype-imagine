class_name PhantomAudio
extends Node

var music := AudioStreamPlayer.new()
var road := AudioStreamPlayer.new()
var voices: Array[AudioStreamPlayer] = []
var sounds: Dictionary = {}
var next_voice := 0

func _ready() -> void:
	add_child(music)
	add_child(road)
	for i in range(12):
		var voice := AudioStreamPlayer.new()
		add_child(voice)
		voices.append(voice)
	for sound in ["music", "road", "jump", "dash", "slash", "shoot", "charge", "hit", "pickup", "explode", "hurt", "warning", "enemy", "victory"]:
		var file: String = "res://assets/audio/" + sound + ".wav"
		if ResourceLoader.exists(file):
			sounds[sound] = load(file)
	for key in ["music", "road"]:
		if sounds.has(key):
			var stream: AudioStreamWAV = sounds[key]
			stream.loop_mode = AudioStreamWAV.LOOP_FORWARD
			stream.loop_begin = 0
			stream.loop_end = stream.data.size() / 2

func start() -> void:
	if sounds.has("music"):
		music.stream = sounds.music
		music.volume_db = -11
		music.play()
	if sounds.has("road"):
		road.stream = sounds.road
		road.volume_db = -21
		road.play()

func update(state: PhantomRun, paused: bool, muted: bool) -> void:
	AudioServer.set_bus_mute(0, muted)
	road.volume_db = lerpf(-43, -19, state.speed / PhantomRun.CRUISE) if state.mode != "title" else -31
	road.pitch_scale = 0.75 + state.speed / PhantomRun.CRUISE * 0.35
	music.volume_db = -17 if state.mode in ["title", "intro"] or paused else -11
	for sound in state.sounds:
		play_sfx(sound)
	state.sounds.clear()

func play_sfx(sound: String) -> void:
	var source := "slash" if sound.begins_with("slash_") else sound
	if not sounds.has(source):
		return
	var voice := voices[next_voice]
	next_voice = (next_voice + 1) % voices.size()
	voice.stream = sounds[source]
	voice.volume_db = -11 if sound == "shoot" else -5
	voice.pitch_scale = randf_range(0.96, 1.04)
	if source == "slash":
		voice.pitch_scale = {"slash_1": 1.12, "slash_2": 0.94, "slash_3": 0.73}.get(sound, 1.0)
		voice.volume_db = -3 if sound == "slash_3" else -6
	voice.play()

func shutdown() -> void:
	music.stop()
	road.stop()
	music.stream = null
	road.stream = null
	for voice in voices:
		voice.stop()
		voice.stream = null
	sounds.clear()

func _exit_tree() -> void:
	shutdown()
