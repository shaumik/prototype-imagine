extends SceneTree
## Enlarged poses from the exact in-game rig and authored attack clips.

class Board extends Node2D:
	var runner := RunnerArt.new()
	var font := preload("res://assets/fonts/BarlowCondensed-SemiBold.ttf")
	func _draw() -> void:
		for row in range(3):
			for col in range(4):
				var ages: Array = [[0.05, 0.125, 0.18, 0.30], [0.045, 0.09, 0.15, 0.30], [0.075, 0.17, 0.23, 0.38]][row]
				var age: float = ages[col]
				var pose := RunnerMotion.sample(0.12 + age * 1.5, age, 1, 0, 0, 0, SwordCombo.DURATIONS[row] - age, 0, 0, false, 0, -1, row + 1)
				var origin := Vector2(col * 400, row * 370)
				draw_rect(Rect2(origin + Vector2(4, 4), Vector2(392, 362)), Color("172d3b"))
				draw_string(font, origin + Vector2(18, 30), "%s / %.3fs" % [["DOWNSTROKE", "RISING CUT", "FINISHER"][row], age], HORIZONTAL_ALIGNMENT_LEFT, -1, 20, Color("bfece7"))
				draw_line(origin + Vector2(20, 337), origin + Vector2(380, 337), Color("37616b"), 1)
				draw_set_transform(origin + Vector2(167, 336), 0, Vector2(1.65, 1.65))
				runner.render(self, Vector2.ZERO, pose)
				draw_set_transform(Vector2.ZERO)

func _initialize() -> void:
	root.size = Vector2i(1600, 1110)
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
	root.get_texture().get_image().save_png("res://captures/three-slash-poses.png")
	quit()
