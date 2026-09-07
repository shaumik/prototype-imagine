extends SceneTree
## Packs the runnable source and exactly the imported resources it consumes.

var files: Dictionary = {}

func _initialize() -> void:
	collect("res://assets")
	collect("res://scripts")
	collect("res://scenes")
	files["res://project.godot"] = true
	files["res://.godot/global_script_class_cache.cfg"] = true
	for path in files.keys():
		if path.ends_with(".import"):
			var config := ConfigFile.new()
			config.load(path)
			for imported in config.get_value("deps", "dest_files", []):
				files[imported] = true
	var pack := PCKPacker.new()
	var result := pack.pck_start("res://build/HighwayPhantom.pck")
	if result != OK:
		printerr("Cannot start resource pack: ", result)
		quit(1)
		return
	for path in files:
		result = pack.add_file(path, path)
		if result != OK:
			printerr("Cannot pack ", path, ": ", result)
			quit(1)
			return
	pack.flush()
	print("Packed %d project resources." % files.size())
	quit()

func collect(path: String) -> void:
	var dir := DirAccess.open(path)
	for file in dir.get_files():
		files[path.path_join(file)] = true
	for folder in dir.get_directories():
		if not folder.begins_with("."):
			collect(path.path_join(folder))
