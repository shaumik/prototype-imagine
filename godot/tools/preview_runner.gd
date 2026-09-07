extends SceneTree
## Contact sheet from the exact renderer used by the game.

class Board extends Node2D:
	var runner := RunnerArt.new()
	var font := preload("res://assets/fonts/BarlowCondensed-SemiBold.ttf")
	func _draw() -> void:
		for i in range(16):
			var cycle := (i % 8) / 8.0
			var label := "STRIDE %d / 8" % (i + 1)
			var air := 0.0
			var boost := 0.0
			var slash := 0.0
			var recoil := 0.0
			var running := 1.0
			if i >= 8:
				label = ["AIR / RISE", "AIR / FALL", "DASH / GROUND", "DASH / AIR", "BLADE / WINDUP", "BLADE / CUT", "BUSTER / RECOIL", "AT THE RED LIGHT"][i - 8]
				air = 1.0 if i in [8, 9, 11] else 0.0
				boost = 1.0 if i in [10, 11] else 0.0
				slash = CombatMotion.SLASH_DURATION - (0.045 if i == 12 else 0.125) if i in [12, 13] else 0.0
				recoil = 0.13 if i == 14 else 0.0
				running = 0.0 if i == 15 else 1.0
			var pose := RunnerMotion.sample(cycle, 0.3, running, air, 640 if i == 9 else -300, boost, slash, 0, recoil, false, 0)
			var origin := Vector2((i % 4) * 480, (i / 4) * 360)
			draw_rect(Rect2(origin + Vector2(4, 4), Vector2(472, 352)), Color("172d3b"))
			draw_string(font, origin + Vector2(18, 30), label, HORIZONTAL_ALIGNMENT_LEFT, -1, 20, Color("bfece7"))
			draw_line(origin + Vector2(20, 326), origin + Vector2(460, 326), Color("37616b"), 1)
			draw_set_transform(origin + Vector2(235, 325), 0, Vector2(1.6, 1.6))
			runner.render(self, Vector2.ZERO, pose)
			draw_set_transform(Vector2.ZERO)

func _initialize() -> void:
	root.size = Vector2i(1920, 1440)
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
	root.get_texture().get_image().save_png("res://captures/runner-rig-poses.png")
	quit()
