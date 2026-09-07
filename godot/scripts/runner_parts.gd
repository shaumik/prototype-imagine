class_name RunnerParts
extends RefCounted
## Source rectangles and joint anchors for one consistent generated character.

const ATLAS := preload("res://assets/runner_rig.png")
const PARTS := {
	"head": Rect2(8, 8, 316, 315),
	"torso": Rect2(400, 10, 241, 325),
	"pelvis": Rect2(757, 62, 300, 247),
	"cannon": Rect2(1106, 75, 410, 180),
	"thigh": Rect2(88, 330, 145, 332),
	"shin": Rect2(455, 337, 116, 331),
	"boot": Rect2(774, 469, 305, 169),
	"shoulder": Rect2(1223, 384, 255, 238),
	"upper_arm": Rect2(92, 673, 120, 318),
	"forearm": Rect2(448, 671, 120, 332),
	"blade": Rect2(661, 777, 467, 98),
	"scarf": Rect2(1134, 724, 389, 235),
}
const ANCHORS := {
	"head": Vector2(180, 286), "torso": Vector2(126, 309),
	"pelvis": Vector2(137, 183), "cannon": Vector2(49, 87),
	"boot": Vector2(91, 64), "shoulder": Vector2(61, 127),
	"blade": Vector2(51, 46), "scarf": Vector2(364, 35),
}
const BONES := {
	"torso": [Vector2(126, 309), Vector2(112, 25)],
	"thigh": [Vector2(43, 49), Vector2(56, 293)],
	"shin": [Vector2(51, 47), Vector2(42, 300)],
	"upper_arm": [Vector2(42, 39), Vector2(55, 275)],
	"forearm": [Vector2(52, 39), Vector2(68, 286)],
}

var texture := CanvasTexture.new()

func _init() -> void:
	texture.diffuse_texture = ATLAS
	texture.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR

func draw(target: Node2D, name: String, transform: Transform2D, color: Color) -> void:
	var rect: Rect2 = PARTS[name]
	var corners := PackedVector2Array([Vector2.ZERO, Vector2(rect.size.x, 0), rect.size, Vector2(0, rect.size.y)])
	var points := PackedVector2Array()
	var uvs := PackedVector2Array()
	for corner in corners:
		points.append(transform * corner)
		uvs.append((rect.position + corner) / ATLAS.get_size())
	target.draw_polygon(points, PackedColorArray([color]), uvs, texture)

func attached(target: Node2D, name: String, position: Vector2, angle: float, scale: Vector2, color: Color) -> void:
	var transform := Transform2D(angle, scale, 0, position) * Transform2D(0, -ANCHORS[name])
	draw(target, name, transform, color)

func bone(target: Node2D, name: String, start: Vector2, end: Vector2, color: Color, width: float = 1.0) -> void:
	var anchors: Array = BONES[name]
	var source: Vector2 = anchors[1] - anchors[0]
	var destination := end - start
	var scale := destination.length() / source.length()
	var transform := Transform2D(destination.angle() - PI / 2, Vector2(scale * width, scale), 0, start)
	draw(target, name, transform * Transform2D(PI / 2 - source.angle(), Vector2.ZERO) * Transform2D(0, -anchors[0]), color)

func scarf(target: Node2D, position: Vector2, wave: float, boost: float, color: Color) -> void:
	var rect: Rect2 = PARTS.scarf
	var anchor: Vector2 = ANCHORS.scarf
	for i in range(10):
		var points := PackedVector2Array()
		var uvs := PackedVector2Array()
		for uv in [Vector2(i / 10.0, 0), Vector2((i + 1) / 10.0, 0), Vector2((i + 1) / 10.0, 1), Vector2(i / 10.0, 1)]:
			var source: Vector2 = uv * rect.size
			var point := (source - anchor) * Vector2(0.16, 0.085)
			point.y += sin(wave - uv.x * 5) * (1 - uv.x) * lerpf(4.0, 1.4, boost)
			points.append(position + point)
			uvs.append((rect.position + source) / ATLAS.get_size())
		target.draw_polygon(points, PackedColorArray([color]), uvs, texture)
