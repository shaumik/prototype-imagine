extends SceneTree
## Inspect matching air poses, grounded transitions, and firing attachments at game scale.

class Board extends Node2D:
	var runner := RunnerArt.new()
	var font := preload("res://assets/fonts/BarlowCondensed-SemiBold.ttf")
	func _draw() -> void:
		var labels := ["RUN", "PUSH OFF", "RISING", "KNEES TUCK", "APEX", "FALLING", "REACH / CONTACT", "LAND / ABSORB", "RISING / FIRE", "APEX / FIRE", "FALL / FIRE", "AIR / BLADE"]
		for i in range(12):
			var air := AirMotion.new()
			var grounded := i in [0, 7]
			var air_frame: int = i - 1 if i < 7 else [0, 1, 3, 5, 3][i - 7]
			if i == 7:
				air.touchdown(650)
				air.landing = 0.10
			var origin := Vector2((i % 4) * 480, (i / 4) * 360)
			draw_rect(Rect2(origin + Vector2(4, 4), Vector2(472, 352)), Color("172d3b"))
			draw_string(font, origin + Vector2(18, 30), labels[i], HORIZONTAL_ALIGNMENT_LEFT, -1, 20, Color("bfece7"))
			draw_line(origin + Vector2(20, 326), origin + Vector2(460, 326), Color("37616b"), 1)
			draw_line(origin + Vector2(20, 110), origin + Vector2(460, 110), Color("294653"), 1)
			draw_set_transform(origin + Vector2(235, 325), 0, Vector2(1.5, 1.5))
			var pose := RunnerMotion.sample(0.375, 0.3, 1, 0.0 if grounded else 1.0, -600 + air_frame * 240, 0, 0.27 if i == 11 else 0, 0, 0.13 if i in [8, 9, 10] else 0, false, air.landing_squash())
			runner.render(self, Vector2.ZERO, pose)
			draw_set_transform(Vector2.ZERO)

func _initialize() -> void:
	root.size = Vector2i(1920, 1080)
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
	root.get_texture().get_image().save_png("res://captures/jump-poses.png")
	quit()
