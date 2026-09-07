extends Node2D

var state := PhantomRun.new()
var view := PhantomView.new()
var audio := PhantomAudio.new()
var pending := {"jump": false, "jump_release": false, "dash": false, "slash": false}
var intro := 0.0
var demo := false
var demo_clock := 0.0
var showcase := false
var capture_frames := false
var captured: Dictionary = {}
var end_after := 0.0
var app_clock := 0.0
var auto_dash_timer := 0.0
var recording := false
var finishing := false

func _ready() -> void:
	add_child(view)
	view.state = state
	add_child(audio)
	DisplayServer.window_set_title("Highway Phantom — A Backseat Daydream")
	get_tree().auto_accept_quit = false
	for arg in OS.get_cmdline_user_args():
		if arg == "--demo":
			begin_ride(true)
		if arg == "--showcase":
			showcase = true
			begin_ride(true)
		if arg == "--capture":
			capture_frames = true
		if arg == "--recording":
			recording = true
			set_physics_process(false)
		if arg.begins_with("--end-after="):
			end_after = arg.trim_prefix("--end-after=").to_float()
	audio.start()

func _process(_dt: float) -> void:
	# Movie capture advances once per encoded frame, independent of disk/render speed.
	if recording and not finishing:
		_physics_process(1.0 / 30.0)

func _notification(what: int) -> void:
	if what == NOTIFICATION_WM_CLOSE_REQUEST:
		finish()

func finish() -> void:
	if finishing:
		return
	finishing = true
	audio.shutdown()
	await get_tree().process_frame
	await get_tree().process_frame
	get_tree().quit()

func begin_ride(autoplay: bool = false, skip_intro: bool = false) -> void:
	demo = autoplay
	view.demo = autoplay
	view.paused = false
	state.start(view.assist or autoplay)
	intro = 0
	demo_clock = 0
	auto_dash_timer = 0
	if not skip_intro:
		state.mode = "intro"
	else:
		state.mode = "play"

func _physics_process(dt: float) -> void:
	if finishing:
		return
	app_clock += dt
	view.menu_time += dt
	view.mouse = get_global_mouse_position()
	if view.paused:
		audio.update(state, true, view.muted)
		view.queue_redraw()
		return
	if state.mode == "intro":
		intro += dt
		state.time += dt
		state.distance += state.speed * dt
		view.intro_time = intro
		if intro >= view.intro_duration:
			state.start(view.assist or demo)
	elif state.mode == "play":
		var controls := read_controls()
		if demo:
			controls = demo_controls(dt)
		state.tick(dt, controls)
		for key in pending:
			pending[key] = false
	else:
		state.time += dt
	audio.update(state, view.paused, view.muted)
	view.queue_redraw()
	if capture_frames:
		for mark in [1, 5, 10, 14, 19, 24, 30]:
			if app_clock >= mark and not captured.has(mark):
				captured[mark] = true
				capture.call_deferred("res://captures/frame-%02d.png" % mark)
	if end_after > 0 and app_clock >= end_after:
		print("RUN_COMPLETE mode=%s phase=%s distance=%.1f health=%d score=%d kills=%d" % [state.mode, state.phase, state.distance, state.health, state.score, state.kills])
		finish()

func read_controls() -> Dictionary:
	var result := pending.duplicate()
	result.axis = float(Input.is_physical_key_pressed(KEY_D) or Input.is_physical_key_pressed(KEY_RIGHT)) - float(Input.is_physical_key_pressed(KEY_A) or Input.is_physical_key_pressed(KEY_LEFT))
	result.shoot = Input.is_physical_key_pressed(KEY_J) or Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT)
	result.charge = Input.is_physical_key_pressed(KEY_K)
	return result

func demo_controls(dt: float) -> Dictionary:
	demo_clock += dt
	auto_dash_timer += dt
	var command := {"axis": 0.0, "shoot": true, "charge": false, "jump": false, "jump_release": false, "dash": false, "slash": false}
	var obstacle_near := false
	for p in state.platforms:
		if p.x > state.player.x - 70 and p.x < state.player.x + 285 and state.player.y > p.y + 20:
			obstacle_near = true
	for gap in state.gaps:
		if gap.x > state.player.x - 70 and gap.x < state.player.x + 195:
			obstacle_near = true
	for e in state.enemies:
		var delta: Vector2 = e.pos - state.player
		if delta.x > 0 and delta.x < 210:
			if delta.y < -65:
				obstacle_near = true
			if delta.length() < 175:
				command.slash = true
	if obstacle_near and (state.grounded or (state.jumps == 1 and state.velocity.y > -80)):
		command.jump = true
	if auto_dash_timer > 4.8 and state.player.x < 740:
		command.dash = true
		auto_dash_timer = 0
	if showcase and demo_clock > 14 and state.phase == "run":
		state.distance = PhantomRun.ROUTE_LENGTH
	if state.phase == "boss":
		command.axis = 1.0 if state.player.x < 540 else (-1.0 if state.player.x > 650 else 0.0)
		if state.grounded and fposmod(demo_clock, 1.6) < 0.06:
			command.jump = true
		command.charge = fposmod(demo_clock, 1.3) < 1.05
		command.slash = state.player.distance_to(state.boss_pos) < 200
	# Autoplay issues individual presses just like a player tapping the button.
	command.slash = command.slash and int(demo_clock * 8) != int((demo_clock - dt) * 8)
	return command

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		var key: int = event.physical_keycode
		if key == KEY_F11:
			var fullscreen := DisplayServer.window_get_mode() == DisplayServer.WINDOW_MODE_FULLSCREEN
			DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_WINDOWED if fullscreen else DisplayServer.WINDOW_MODE_FULLSCREEN)
		if key == KEY_M:
			view.muted = not view.muted
			AudioServer.set_bus_mute(0, view.muted)
		if state.mode == "title":
			if key == KEY_ENTER or key == KEY_SPACE:
				begin_ride()
			elif key == KEY_D:
				begin_ride(true)
			elif key == KEY_G:
				view.assist = not view.assist
			elif key == KEY_B:
				begin_ride(false, true)
				state.distance = PhantomRun.ROUTE_LENGTH
			return
		if state.mode == "intro":
			if key == KEY_ENTER or key == KEY_SPACE:
				state.start(view.assist or demo)
			return
		if key == KEY_T and (view.paused or state.mode in ["win", "lose"]):
			state.mode = "title"
			view.paused = false
		if key == KEY_G and state.mode == "lose":
			view.assist = true
			begin_ride(false, true)
		if key == KEY_R or (key == KEY_ENTER and state.mode in ["win", "lose"]):
			begin_ride(false, true)
		elif key == KEY_ESCAPE or (key == KEY_ENTER and view.paused):
			view.paused = not view.paused
		elif key == KEY_ENTER and demo:
			demo = false
			view.demo = false
			state.easy = view.assist
		if not view.paused:
			if key == KEY_SPACE or key == KEY_W or key == KEY_UP:
				pending.jump = true
			if key == KEY_SHIFT:
				pending.dash = true
			if key == KEY_L:
				pending.slash = true
	elif event is InputEventKey and not event.pressed:
		if event.physical_keycode in [KEY_SPACE, KEY_W, KEY_UP]:
			pending.jump_release = true
	elif event is InputEventMouseButton and event.pressed:
		if state.mode == "title" and event.button_index == MOUSE_BUTTON_LEFT and Rect2(784, 484, 342, 53).has_point(get_global_mouse_position()):
			begin_ride()
		elif event.button_index == MOUSE_BUTTON_RIGHT:
			pending.slash = true

func capture(path: String) -> void:
	await RenderingServer.frame_post_draw
	var img := get_viewport().get_texture().get_image()
	img.save_png(path)
	print("CAPTURE " + path)
