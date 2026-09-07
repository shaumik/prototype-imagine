extends SceneTree
## Render the actual ground/air dash poses and their weapon attachments.

class Board extends Node2D:
	var runner := RunnerArt.new()
	var font := preload("res://assets/fonts/BarlowCondensed-SemiBold.ttf")
	func _draw() -> void:
		var labels := ["ENTER", "PUSH", "ACCELERATE", "BOOST", "BOOST / HOLD", "RELEASE", "RECOVER", "RUN / RECOVER", "AIR / ENTER", "AIR / BOOST", "AIR / RELEASE", "AIR / RECOVER", "RUN / BEFORE", "RUN / AFTER", "BOOST / FIRE", "AIR / FIRE"]
		var ages := [0.0, 0.035, 0.075, 0.12, 0.17, 0.22, 0.28, 0.33, 0.02, 0.13, 0.24, 0.31, 0.35, 0.35, 0.12, 0.13]
		for i in range(labels.size()):
			var boost := DashMotion.new()
			boost.age = ages[i]
			var air := AirMotion.new()
			var grounded := i < 8 or i in [12, 13, 14]
			var origin := Vector2((i % 4) * 480, (i / 4) * 320)
			draw_rect(Rect2(origin + Vector2(4, 4), Vector2(472, 312)), Color("172d3b"))
			draw_string(font, origin + Vector2(18, 30), labels[i], HORIZONTAL_ALIGNMENT_LEFT, -1, 20, Color("bfece7"))
			draw_line(origin + Vector2(20, 296), origin + Vector2(460, 296), Color("37616b"), 1)
			draw_set_transform(origin + Vector2(235, 295), 0, Vector2(1.5, 1.5))
			var pose := RunnerMotion.sample(0, 0.3, 1, 0.0 if grounded else 1.0, -50, boost.intensity(), 0, 0, 0.13 if i >= 14 else 0, false, 0)
			runner.render(self, Vector2.ZERO, pose)
			draw_set_transform(Vector2.ZERO)

func _initialize() -> void:
	root.size = Vector2i(1920, 1280)
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
	root.get_texture().get_image().save_png("res://captures/dash-poses.png")
	quit()
