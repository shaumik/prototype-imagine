extends SceneTree

func _initialize() -> void:
	var svg := FileAccess.get_file_as_string("res://assets/icon.svg")
	DirAccess.make_dir_recursive_absolute("res://build/Phantom.iconset")
	for base in [16, 32, 128, 256, 512]:
		for mult in [1, 2]:
			var img := Image.new()
			img.load_svg_from_string(svg, base * mult / 512.0)
			var suffix := "@2x" if mult == 2 else ""
			img.save_png("res://build/Phantom.iconset/icon_%dx%d%s.png" % [base, base, suffix])
	quit()
