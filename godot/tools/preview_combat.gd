extends SceneTree
## Render pose references using the same runtime rig as the browser game.

class Board extends Node2D:
	var runner := RunnerArt.new()
	var font := preload("res://assets/fonts/BarlowCondensed-SemiBold.ttf")
	func _draw() -> void:
		var poses := [
			["RUN / REST", 0.0, 0.0, 0.0, false],
			["BLADE / WINDUP", 0.085, 0.0, 0.0, false],
			["BLADE / OVERHEAD", 0.145, 0.0, 0.0, false],
			["BLADE / STRIKE", 0.195, 0.0, 0.0, false],
			["BLADE / FOLLOW THROUGH", 0.255, 0.0, 0.0, false],
			["BLADE / RECOVERY", 0.38, 0.0, 0.0, false],
			["BUSTER / FIRE", 0.0, 0.0, 0.18, false],
			["BUSTER / RECOIL", 0.0, 0.0, 0.13, false],
			["BUSTER / RETURN", 0.0, 0.0, 0.04, false],
			["BUSTER / CHARGE", 0.0, 1.0, 0.0, false],
			["CHARGED / FIRE", 0.0, 0.0, 0.30, true],
			["CHARGED / RECOIL", 0.0, 0.0, 0.25, true],
		]
		var gait_study := OS.get_cmdline_user_args().has("--gait")
		if gait_study:
			poses.clear()
			for i in range(16):
				poses.append(["RUN %d%s" % [i % 8 + 1, " / RECOIL" if i >= 8 else ""], 0.0, 0.0, 0.13 if i >= 8 else 0.0, false])
		for i in range(poses.size()):
			var p: Array = poses[i]
			var origin := Vector2((i % 4) * 480, (i / 4) * 360)
			draw_rect(Rect2(origin + Vector2(4, 4), Vector2(472, 352)), Color("172d3b"))
			draw_string(font, origin + Vector2(18, 30), p[0], HORIZONTAL_ALIGNMENT_LEFT, -1, 20, Color("bfece7"))
			draw_line(origin + Vector2(20, 326), origin + Vector2(460, 326), Color("37616b"), 1)
			draw_set_transform(origin + Vector2(235, 325), 0, Vector2(1.5, 1.5))
			var pose := RunnerMotion.sample((i % 8) / 8.0 if gait_study else 0, 0.3, 1, 0, 0, 0, CombatMotion.SLASH_DURATION - p[1] if p[1] > 0 else 0.0, p[2], p[3], p[4], 0)
			runner.render(self, Vector2.ZERO, pose)
			draw_set_transform(Vector2.ZERO)

func _initialize() -> void:
	root.size = Vector2i(1920, 1440 if OS.get_cmdline_user_args().has("--gait") else 1080)
	root.content_scale_size = root.size
	var board := Board.new()
	var shader := ShaderMaterial.new()
	shader.shader = preload("res://assets/chroma.gdshader")
	board.material = shader
	root.add_child.call_deferred(board)
	capture.call_deferred()

func capture() -> void:
	await process_frame
	await process_frame
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png("res://captures/pixel-gaits.png" if OS.get_cmdline_user_args().has("--gait") else "res://captures/combat-poses.png")
	quit()
