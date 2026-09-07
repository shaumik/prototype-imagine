extends SceneTree
## Deterministic footage of the real game renderer, with isolated movement inputs.

var state := PhantomRun.new()
var view := PhantomView.new()

func _initialize() -> void:
	state.start(true)
	state.platforms.clear()
	state.pickups.clear()
	state.travel_spawn = 1e9
	state.invulnerable = 0
	view.state = state
	root.add_child.call_deferred(view)
	record.call_deferred()

func record() -> void:
	await process_frame
	for frame in range(540):
		var controls := {}
		if frame in [120, 360]:
			controls.jump = true
		if frame in [141, 291, 382]:
			controls.dash = true
		if frame in [225, 270, 470]:
			controls.slash = true
		if frame in [80, 92, 102, 161, 310]:
			controls.shoot = true
		state.tick(1.0 / 120, controls)
		state.tick(1.0 / 120, {})
		view.queue_redraw()
		await process_frame
		await RenderingServer.frame_post_draw
		if frame == 90:
			root.get_texture().get_image().save_png("res://captures/runner-game.png")
	print("MOTION_REVIEW: 540 simulation frames / 9 seconds")
	quit()
