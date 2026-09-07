class_name PhantomView
extends Node2D
## Painterly distance, crisp gameplay, then the car interior nearest the viewer.

const CREAM := Color("f4eee1")
const CYAN := Color("86fff0")
const INK := Color("101c2a")
const ORANGE := Color("ffb17b")

var state: PhantomRun
var runner := RunnerArt.new()
var sky: Texture2D = preload("res://assets/sunset_city.png")
var interior: Texture2D = preload("res://assets/child_in_car_reflection_v2.png")
var font: Font = preload("res://assets/fonts/Barlow-Regular.ttf")
var title_font: Font = preload("res://assets/fonts/BarlowCondensed-SemiBold.ttf")
var mono: Font = preload("res://assets/fonts/ShareTechMono-Regular.ttf")
var intro_time := 0.0
var intro_duration := 7.5
var menu_time := 0.0
var paused := false
var muted := false
var assist := false
var demo := false
var mouse := Vector2.ZERO

func _ready() -> void:
	var key_material := ShaderMaterial.new()
	key_material.shader = preload("res://assets/chroma.gdshader")
	material = key_material

func _draw() -> void:
	if state == null:
		return
	if state.mode == "title":
		_draw_title()
		return
	var shake := Vector2(sin(state.time * 87), cos(state.time * 113)) * state.shake * 0.5
	draw_set_transform(shake)
	_draw_outside()
	draw_set_transform(Vector2.ZERO)
	_draw_glass()
	_draw_frame()
	if state.mode == "intro":
		_draw_intro()
	else:
		_draw_hud()
	if state.flash > 0:
		draw_rect(Rect2(0, 0, 1280, 720), Color(1, 0.64, 0.46, state.flash * 0.30))
	if state.mode == "lose" or state.mode == "win":
		_draw_result()
	if paused:
		_draw_pause()

func _draw_outside() -> void:
	var d := state.distance
	var t := state.time
	# Overscan leaves enough painted scenery for the entire route without a seam.
	var sky_x := minf(d * 0.018, 560)
	draw_texture_rect(sky, Rect2(-sky_x, -162, 1856, 730), false)
	# Haze between the painted horizon and the elevated road.
	gradient(Rect2(0, 380, 1280, 130), Color(0.87, 0.49, 0.38, 0), Color(0.36, 0.37, 0.45, 0.45))
	_draw_buildings(d)
	_draw_far_traffic(d, t)
	# Parallel roads, never a vanishing-point camera.
	draw_rect(Rect2(0, 508, 1280, 77), Color("3b4453"))
	draw_line(Vector2(0, 512), Vector2(1280, 512), Color("c0a18e"), 3)
	for i in range(-1, 9):
		var x := i * 210 - fposmod(d * 0.83, 210)
		draw_line(Vector2(x, 541), Vector2(x + 100, 541), Color("b9a691"), 2)
	_draw_roadside(d)
	gradient(Rect2(0, 577, 1280, 100), Color("343e4b"), Color("182731"))
	draw_rect(Rect2(0, 580, 1280, 5), Color("c2b0a2"))
	draw_rect(Rect2(0, 585, 1280, 5), Color("4a5660"))
	for i in range(-1, 17):
		var x := i * 102 - fposmod(d, 102)
		draw_line(Vector2(x, 582), Vector2(x + 18, 590), Color("232f3b"), 2)
	for i in range(-1, 7):
		var x := i * 285 - fposmod(d * 1.22, 285)
		poly([Vector2(x, 624), Vector2(x + 135, 624), Vector2(x + 126, 628), Vector2(x - 9, 628)], Color("c0ad83"))
	# Fine asphalt aggregate and long reflected sunset glints.
	for i in range(100):
		var x := fposmod(i * 137.61 - d * 1.18, 1320) - 20
		var y := 596 + fposmod(i * 43.18, 71)
		draw_line(Vector2(x, y), Vector2(x + 3 + (i % 9), y), Color(0.71, 0.64, 0.60, 0.08), 1)
	for gap in state.gaps:
		var x: float = gap.x
		var w: float = gap.w
		poly([Vector2(x, 580), Vector2(x + 12, 587), Vector2(x + 4, 601), Vector2(x + 21, 613), Vector2(x + w - 15, 613), Vector2(x + w - 3, 597), Vector2(x + w - 12, 589), Vector2(x + w, 580)], Color("0c1c2c"))
		draw_line(Vector2(x + 10, 596), Vector2(x + w - 10, 596), Color("182b3b"), 3)
		for edge in [x - 12, x + w + 7]:
			draw_line(Vector2(edge, 581), Vector2(edge, 550), Color("6a6f71"), 4)
			glow(Vector2(edge, 548), 15, ORANGE, 0.12)
			draw_circle(Vector2(edge, 548), 4, ORANGE)
	for p in state.platforms:
		_draw_platform(p)
	for p in state.pickups:
		var pos: Vector2 = p.pos + Vector2(0, sin(t * 4 + p.seed) * 5)
		glow(pos, 24, CYAN, 0.11)
		var spin := 8 * absf(cos(t * 2 + p.seed)) + 3
		poly([pos + Vector2(0, -12), pos + Vector2(spin, 0), pos + Vector2(0, 12), pos + Vector2(-spin, 0)], CYAN)
		draw_line(pos + Vector2(0, -7), pos + Vector2(0, 6), Color("ffffff"), 2)
	for e in state.enemies:
		_draw_enemy(e)
	if state.phase == "boss":
		_draw_boss()
	for g in state.ghosts:
		runner.render_afterimage(self, g.pos, g.pose, g.life)
	# Contact shadow stays on the surface below the runner.
	var shadow_y := PhantomRun.FLOOR + 3
	for p in state.platforms:
		if state.player.x > p.x and state.player.x < p.x + p.w and state.player.y <= p.y + 2:
			shadow_y = minf(shadow_y, p.y + 3)
	var altitude := maxf(0, shadow_y - state.player.y)
	draw_set_transform(Vector2(state.player.x, shadow_y), 0, Vector2(1.0, 0.18))
	draw_circle(Vector2.ZERO, maxf(15, 41 - altitude * 0.08), Color(0.025, 0.07, 0.12, maxf(0.08, 0.4 - altitude * 0.001)))
	draw_set_transform(Vector2.ZERO)
	var runner_pos := state.player
	if state.mode == "intro":
		runner_pos.x = lerpf(-100, 390, smoothstep(3.5, intro_duration, intro_time))
	var character_pose := state.runner_motion.pose
	if state.mode == "intro":
		character_pose = RunnerMotion.sample(fposmod(state.distance / RunnerMotion.STRIDE, 1), state.time, 1, 0, 0, 0, 0, 0, 0, false, 0)
	# Keep the silhouette readable through movement; impacts already flash the scene.
	runner.render(self, runner_pos, character_pose)
	for b in state.shots:
		var color := Color("ff846c") if b.enemy else CYAN
		var direction: Vector2 = b.vel.normalized()
		var radius := 13.0 if b.charged else 5.0
		glow(b.pos, radius * 3, color, 0.16)
		draw_line(b.pos - direction * (52 if b.charged else 28), b.pos, Color(color, 0.4), radius * 1.5, true)
		draw_line(b.pos - direction * 13, b.pos, color, radius, true)
		draw_circle(b.pos, radius * 0.55, CREAM)
	for p in state.particles:
		var color: Color = p.color
		color.a = clampf(p.life / p.max, 0, 1)
		draw_line(p.pos, p.pos - p.vel * 0.021, color, maxf(1, p.size * color.a), true)
	_draw_foreground(d)
	if state.phase == "brake" or state.phase == "boss" or state.phase == "depart":
		_draw_signal()

func _draw_buildings(d: float) -> void:
	for i in range(-1, 12):
		var index := i + int(d * 0.14 / 148)
		var x := i * 148 - fposmod(d * 0.14, 148)
		var height := 28 + fposmod(index * 73.1, 75)
		var y := 480 - height
		gradient(Rect2(x, y, 122, height), Color("454d5b"), Color("303d4f"))
		draw_rect(Rect2(x + 116, y, 9, height), Color("29384b"))
		draw_line(Vector2(x, y), Vector2(x + 122, y), Color("987f7c"), 2)
		for row in range(2, int(height / 16)):
			for col in range(1, 8):
				var lit := fposmod(index * 13 + col * 7 + row * 17, 11) < 3
				draw_rect(Rect2(x + col * 14, y + row * 13, 5, 6), Color("bd947e") if lit else Color("59606b"))
		if index % 3 == 0:
			draw_rect(Rect2(x + 22, y - 14, 31, 14), Color("424b59"))
			draw_line(Vector2(x + 35, y - 14), Vector2(x + 35, y - 37), Color("545464"), 2)
	# Utility cables tie the scene to actual roadside scale.
	for i in range(-1, 4):
		var x := i * 580 - fposmod(d * 0.38, 580)
		draw_line(Vector2(x, 260), Vector2(x, 510), Color("3d4655"), 7)
		draw_line(Vector2(x - 27, 286), Vector2(x + 27, 286), Color("454754"), 5)
		for wire in range(3):
			var ps := PackedVector2Array()
			for j in range(25):
				var f := j / 24.0
				ps.append(Vector2(x + f * 580, 275 + wire * 11 + sin(f * PI) * 24))
			draw_polyline(ps, Color("424453"), 1.4, true)

func _draw_far_traffic(d: float, t: float) -> void:
	draw_rect(Rect2(0, 470, 1280, 32), Color("565968"))
	draw_line(Vector2(0, 472), Vector2(1280, 472), Color("a28b82"), 3)
	for i in range(-1, 5):
		var x := i * 405 - fposmod(d * 0.45 + t * 32, 405)
		var y := 469.0
		var truck := i % 3 == 0
		var paint := Color("ac755e") if truck else (Color("657483") if i % 2 == 0 else Color("b4a99b"))
		if truck:
			draw_rect(Rect2(x, y - 54, 115, 46), paint)
			draw_rect(Rect2(x + 117, y - 40, 38, 32), Color("936753"))
			draw_rect(Rect2(x + 136, y - 35, 17, 13), Color("354554"))
			for z in range(5):
				draw_line(Vector2(x + 10, y - 46 + z * 7), Vector2(x + 108, y - 46 + z * 7), Color(0.3, 0.28, 0.31, 0.2), 1)
		else:
			poly([Vector2(x, y - 17), Vector2(x + 16, y - 22), Vector2(x + 29, y - 36), Vector2(x + 66, y - 36), Vector2(x + 84, y - 22), Vector2(x + 101, y - 18), Vector2(x + 103, y - 6), Vector2(x, y - 6)], paint)
			poly([Vector2(x + 23, y - 23), Vector2(x + 33, y - 32), Vector2(x + 65, y - 32), Vector2(x + 77, y - 23)], Color("344856"))
		for wheel in [20, 135 if truck else 78]:
			draw_circle(Vector2(x + wheel, y - 7), 10, Color("25323e"))
			draw_circle(Vector2(x + wheel, y - 7), 5, Color("7f8386"))
		draw_line(Vector2(x + (155 if truck else 99), y - 17), Vector2(x + (155 if truck else 99), y - 12), ORANGE, 3)
	# Fence in front of the opposite carriageway.
	for i in range(-1, 18):
		var x := i * 83 - fposmod(d * 0.63, 83)
		draw_line(Vector2(x, 487), Vector2(x, 518), Color("333e4b"), 4)
	for y in [490, 500, 506]:
		draw_line(Vector2(0, y), Vector2(1280, y), Color("77808a") if y == 490 else Color("434e5c"), 3)

func _draw_roadside(d: float) -> void:
	for i in range(-1, 4):
		var x := i * 730 - fposmod(d * 0.83, 730)
		# Arcing gooseneck lamps, warmed by the setting sun.
		draw_line(Vector2(x, 520), Vector2(x, 267), Color("34404c"), 6)
		draw_line(Vector2(x + 2, 505), Vector2(x + 2, 270), Color("8e827a"), 1)
		var points := PackedVector2Array([Vector2(x, 270), Vector2(x + 4, 254), Vector2(x + 15, 245), Vector2(x + 40, 245)])
		draw_polyline(points, Color("36414c"), 5, true)
		draw_line(Vector2(x + 27, 248), Vector2(x + 47, 248), ORANGE, 4)
		glow(Vector2(x + 38, 249), 22, ORANGE, 0.07)
		poly([Vector2(x + 27, 251), Vector2(x - 5, 480), Vector2(x + 105, 480), Vector2(x + 46, 251)], Color(1, 0.74, 0.44, 0.026))
	# Small road markers act as a strong, fast reference for movement.
	for i in range(-1, 5):
		var x := i * 360 - fposmod(d, 360)
		draw_rect(Rect2(x, 545, 7, 35), Color("303e4b"))
		draw_rect(Rect2(x - 2, 537, 11, 13), Color("d8b688"))
		draw_rect(Rect2(x, 539, 7, 4), ORANGE)

func _draw_platform(p: Dictionary) -> void:
	var x: float = p.x
	var y: float = p.y
	var w: float = p.w
	# Collision surface exactly follows the luminous top edge.
	draw_rect(Rect2(x + 16, y + 13, w - 32, PhantomRun.FLOOR - y - 13), Color("263842"))
	for i in range(int(w / 44)):
		var a := Vector2(x + 19 + i * 44, y + 23)
		draw_line(a, a + Vector2(35, PhantomRun.FLOOR - y - 26), Color("3a5058"), 3)
		draw_line(a + Vector2(35, 0), a + Vector2(0, PhantomRun.FLOOR - y - 26), Color("3a5058"), 3)
	for px in [x + 12, x + w - 24]:
		draw_rect(Rect2(px, y + 5, 12, PhantomRun.FLOOR - y - 5), Color("4c646a"))
		draw_line(Vector2(px, y + 6), Vector2(px, PhantomRun.FLOOR), Color("718084"), 2)
		draw_rect(Rect2(px - 5, PhantomRun.FLOOR - 5, 22, 5), Color("1b303b"))
	draw_rect(Rect2(x, y, w, 18), Color("293944"))
	draw_rect(Rect2(x, y, w, 4), Color("9bd5cd"))
	draw_rect(Rect2(x + 4, y + 5, w - 8, 2), Color("c4b59b"))
	for i in range(int(w / 30)):
		var sx := x + i * 30
		poly([Vector2(sx + 2, y + 9), Vector2(sx + 13, y + 9), Vector2(sx + 7, y + 17), Vector2(sx - 4, y + 17)], Color("b28b5d"))
	for px in [x + 5, x + w - 9]:
		glow(Vector2(px, y + 3), 12, CYAN, 0.06)
		draw_rect(Rect2(px, y + 1, 4, 4), CYAN)
	text_at("MAINTENANCE  /  07" if p.kind == 0 else "TRANSIT WORKS", Vector2(x + 35, y + 38), 10, Color("8b9999"), mono)

func _draw_enemy(e: Dictionary) -> void:
	var p: Vector2 = e.pos
	var body := Color("eee7d8") if e.flash > 0 else Color("4c4f65")
	var rim := Color("a88c91")
	if e.kind == "drone":
		for side in [-1, 1]:
			var rotor := p + Vector2(side * 36, -14)
			draw_line(p + Vector2(side * 12, -2), rotor, INK, 8)
			draw_set_transform(rotor, 0, Vector2(1, 0.28))
			draw_arc(Vector2.ZERO, 25, 0, TAU, 28, Color("2b3548"), 6, true)
			draw_arc(Vector2.ZERO, 26, PI, TAU, 18, rim, 2, true)
			draw_line(Vector2(-22, 0), Vector2(22, 0), Color(0.85, 0.72, 0.72, 0.5), 2)
			draw_set_transform(Vector2.ZERO)
			glow(rotor + Vector2(0, 14), 12, Color("ff7c72"), 0.11)
		poly([p + Vector2(-24, -13), p + Vector2(15, -17), p + Vector2(28, 1), p + Vector2(13, 24), p + Vector2(-16, 19), p + Vector2(-29, 2)], body, INK, 3)
		poly([p + Vector2(-18, -12), p + Vector2(12, -15), p + Vector2(17, -6), p + Vector2(-22, -3)], rim)
		draw_circle(p, 13, INK)
		glow(p, 18, Color("ff705e"), 0.13)
		draw_circle(p, 7, Color("ff7563"))
		draw_circle(p + Vector2(-2, -2), 3, Color("ffe7b3"))
		draw_line(p + Vector2(-5, 21), p + Vector2(-10, 31), INK, 5)
		draw_line(p + Vector2(13, 21), p + Vector2(18, 30), INK, 5)
	else:
		draw_rect(Rect2(p.x - 31, p.y + 14, 63, 17), INK)
		for x in [-23, -8, 8, 23]:
			draw_circle(p + Vector2(x, 23), 7, Color("69717b"))
		poly([p + Vector2(-24, 15), p + Vector2(-21, -15), p + Vector2(7, -28), p + Vector2(28, -16), p + Vector2(33, 15)], body, INK, 3)
		draw_line(p + Vector2(-4, -9), p + Vector2(-39, -9), INK, 15)
		draw_line(p + Vector2(-8, -13), p + Vector2(-36, -13), rim, 3)
		draw_circle(p + Vector2(9, -12), 7, Color("ff8068"))
		glow(p + Vector2(9, -12), 16, Color("ff705e"), 0.10)
		draw_line(p + Vector2(-18, 7), p + Vector2(25, 7), rim, 2)

func _draw_boss() -> void:
	var p := state.boss_pos
	var t := state.time
	var body := CREAM if state.boss_flash > 0 else Color("464d65")
	# Articulated four-arm signal warden.
	for side in [-1, 1]:
		for row in [-1, 1]:
			var root := p + Vector2(side * 42, row * 26)
			var elbow := p + Vector2(side * (96 + sin(t * 2 + row) * 12), row * 67)
			var hand := p + Vector2(side * 132, row * 27 + sin(t * 2.5 + side) * 15)
			draw_line(root, elbow, INK, 21, true)
			draw_line(root, elbow, body, 14, true)
			draw_line(elbow, hand, INK, 18, true)
			draw_line(elbow, hand, Color("7e7382"), 10, true)
			draw_circle(elbow, 14, INK)
			draw_circle(elbow, 8, Color("aa847e"))
			draw_circle(hand, 18, body)
			glow(hand, 25, Color("ff7d68"), 0.15)
			draw_circle(hand, 8, Color("ff9e79"))
	poly([p + Vector2(-39, -78), p + Vector2(34, -78), p + Vector2(69, -36), p + Vector2(61, 39), p + Vector2(27, 79), p + Vector2(-34, 72), p + Vector2(-66, 25), p + Vector2(-66, -37)], body, INK, 5)
	poly([p + Vector2(-36, -72), p + Vector2(30, -72), p + Vector2(45, -47), p + Vector2(-48, -47)], Color("9e8689"))
	for side in [-1, 1]:
		poly([p + Vector2(side * 43, -35), p + Vector2(side * 63, -24), p + Vector2(side * 58, 36), p + Vector2(side * 36, 47)], Color("303e53"))
		draw_line(p + Vector2(side * 48, -20), p + Vector2(side * 46, 20), Color("e59982"), 3)
	for y in [-40, 0, 40]:
		draw_circle(p + Vector2(0, y), 20, INK)
		draw_circle(p + Vector2(0, y), 13, Color("7c4249") if y != -40 else Color("ff826c"))
		if y == -40:
			glow(p + Vector2(0, y), 32, Color("ff6f5f"), 0.2)
			draw_circle(p + Vector2(-3, y - 3), 6, Color("ffe0ae"))
	var core := p + Vector2(0, 0)
	if state.warning > 0:
		glow(core, 50 * state.warning, Color("ff9874"), 0.2)
		draw_arc(core, 33 + sin(t * 13) * 3, 0, TAU, 48, Color(1, 0.54, 0.42, state.warning), 2, true)
	for i in range(5):
		var x := p.x - 33 + i * 16
		var length := 15 + sin(t * 25 + i) * 11
		draw_line(Vector2(x, p.y + 76), Vector2(x, p.y + 90 + length), Color(0.5, 0.9, 1, 0.25), 8, true)

func _draw_foreground(d: float) -> void:
	# A close rail rushes below the action, doubling the perceived travel speed.
	for i in range(-1, 9):
		var x := i * 190 - fposmod(d * 1.55, 190)
		draw_rect(Rect2(x, 647, 8, 26), Color("0e1e2a"))
		draw_rect(Rect2(x, 647, 2, 26), Color("6a7577"))
	draw_rect(Rect2(0, 642, 1280, 9), Color("273b47"))
	draw_line(Vector2(0, 642), Vector2(1280, 642), Color("879290"), 2)
	if state.speed > 70:
		for i in range(13):
			var x := fposmod(i * 123.7 - d * (1.4 + (i % 3) * 0.3), 1420) - 100
			var y := 151 + fposmod(i * 73.7, 453)
			draw_line(Vector2(x, y), Vector2(x + 35 + (i % 4) * 28, y - 0.3), Color(1, 0.90, 0.76, 0.04 + state.dash * 0.2), 1, true)

func _draw_signal() -> void:
	var x := 1105.0
	if state.phase == "brake":
		x += maxf(0, 370 - state.phase_time * 100)
	elif state.phase == "depart":
		x -= state.phase_time * state.phase_time * 45
	draw_line(Vector2(x + 80, 610), Vector2(x + 80, 176), Color("1f2f3c"), 10)
	draw_line(Vector2(x + 80, 178), Vector2(x - 92, 178), Color("30424c"), 8)
	draw_rect(Rect2(x - 48, 176, 41, 121), Color("142535"))
	draw_style_box(panel_style(Color("1b2838"), Color("8b786e"), 7), Rect2(x - 49, 176, 42, 121))
	for i in range(3):
		var pos := Vector2(x - 28, 199 + i * 37)
		var lit := (i == 2 and state.phase == "depart") or (i == 0 and state.phase != "depart")
		var color := CYAN if i == 2 else Color("ff725f")
		draw_circle(pos, 13, Color("0b1927"))
		draw_circle(pos, 10, color if lit else Color("3b404b"))
		if lit:
			glow(pos, 28, color, 0.17)
	text_at("EAST  /  07", Vector2(x - 40, 158), 13, CREAM, mono)

func _draw_glass() -> void:
	# Glass catches the sun but stays transparent over the play space.
	poly([Vector2(310, 39), Vector2(480, 32), Vector2(225, 649), Vector2(172, 650)], Color(1, 0.88, 0.73, 0.018))
	poly([Vector2(1037, 28), Vector2(1094, 33), Vector2(825, 657), Vector2(798, 655)], Color(1, 0.9, 0.77, 0.028))
	for i in range(18):
		var pos := Vector2(110 + fposmod(i * 173.7, 1100), 100 + fposmod(i * 131.1, 515))
		draw_line(pos, pos + Vector2(-3, 5), Color(1, 0.94, 0.84, 0.07), 1, true)
	# Faint reflection of the child remains near the rear edge of the window.
	draw_set_transform(Vector2(127, 342), -0.06, Vector2(0.82, 1))
	draw_circle(Vector2.ZERO, 35, Color(0.9, 0.72, 0.6, 0.033))
	poly([Vector2(-42, -8), Vector2(-33, -33), Vector2(-8, -43), Vector2(21, -33), Vector2(38, -10), Vector2(18, -20), Vector2(10, -9), Vector2(-5, -19)], Color(0.12, 0.20, 0.24, 0.07))
	poly([Vector2(-20, 28), Vector2(17, 33), Vector2(54, 102), Vector2(-57, 102)], Color(0.5, 0.73, 0.72, 0.035))
	draw_set_transform(Vector2.ZERO)

func _draw_frame() -> void:
	# Persistent asymmetric passenger-window aperture with layered rubber/chrome trim.
	var top := [Vector2(0, 0), Vector2(1280, 0), Vector2(1280, 93), Vector2(1209, 61), Vector2(1112, 42), Vector2(414, 40), Vector2(239, 51), Vector2(129, 77), Vector2(77, 133), Vector2(0, 174)]
	poly(top, Color("111c27"))
	poly([Vector2(0, 0), Vector2(1280, 0), Vector2(1280, 19), Vector2(580, 15), Vector2(260, 27), Vector2(92, 77), Vector2(0, 134)], Color("202a32"))
	var curve := PackedVector2Array([Vector2(50, 154), Vector2(78, 116), Vector2(129, 75), Vector2(240, 48), Vector2(415, 36), Vector2(1112, 38), Vector2(1210, 57), Vector2(1280, 88)])
	draw_polyline(curve, Color("050e19"), 15, true)
	draw_polyline(curve, Color("756b61"), 3, true)
	draw_polyline(PackedVector2Array([Vector2(93, 112), Vector2(135, 79), Vector2(245, 53), Vector2(419, 41), Vector2(1108, 43), Vector2(1209, 62)]), Color("c59970"), 1.5, true)
	poly([Vector2(0, 101), Vector2(91, 91), Vector2(68, 170), Vector2(67, 539), Vector2(107, 660), Vector2(0, 720)], Color("18242e"))
	poly([Vector2(0, 129), Vector2(48, 148), Vector2(44, 510), Vector2(63, 645), Vector2(0, 682)], Color("25313a"))
	draw_polyline(PackedVector2Array([Vector2(91, 102), Vector2(70, 174), Vector2(71, 538), Vector2(111, 657)]), Color("050f1d"), 9, true)
	draw_polyline(PackedVector2Array([Vector2(80, 144), Vector2(73, 190), Vector2(74, 534), Vector2(111, 650)]), Color("a28b72"), 1.5, true)
	poly([Vector2(1280, 68), Vector2(1234, 77), Vector2(1239, 519), Vector2(1208, 658), Vector2(1280, 720)], Color("17232e"))
	draw_polyline(PackedVector2Array([Vector2(1237, 92), Vector2(1240, 518), Vector2(1207, 659)]), Color("080f1b"), 8, true)
	draw_polyline(PackedVector2Array([Vector2(1233, 96), Vector2(1236, 517), Vector2(1202, 654)]), Color("8c7e6e"), 1.5, true)
	poly([Vector2(0, 655), Vector2(148, 652), Vector2(561, 667), Vector2(1018, 665), Vector2(1226, 649), Vector2(1280, 648), Vector2(1280, 720), Vector2(0, 720)], Color("18242e"))
	poly([Vector2(0, 681), Vector2(304, 680), Vector2(602, 694), Vector2(1020, 692), Vector2(1280, 673), Vector2(1280, 720), Vector2(0, 720)], Color("202d35"))
	var sill := PackedVector2Array([Vector2(78, 650), Vector2(170, 653), Vector2(564, 669), Vector2(1019, 667), Vector2(1210, 652)])
	draw_polyline(sill, Color("080f1a"), 12, true)
	draw_polyline(sill, Color("7c7971"), 3, true)
	draw_polyline(PackedVector2Array([Vector2(80, 647), Vector2(169, 650), Vector2(564, 666), Vector2(1018, 664), Vector2(1207, 649)]), Color("c8a176"), 1.4, true)
	# Leather seam and recessed door handle, both fixed to the camera.
	for i in range(79):
		var x := 55 + i * 15
		draw_line(Vector2(x, 704), Vector2(x + 5, 704), Color(0.56, 0.56, 0.51, 0.24), 1, true)
	poly([Vector2(964, 683), Vector2(1125, 677), Vector2(1109, 710), Vector2(978, 713)], Color("0e1b27"), Color("35434c"), 2)
	poly([Vector2(986, 687), Vector2(1110, 683), Vector2(1102, 694), Vector2(991, 699)], Color("738080"))
	draw_line(Vector2(991, 688), Vector2(1109, 685), Color("babcb0"), 2)
	# Small seat/child silhouette at the extreme left foreground.
	poly([Vector2(0, 454), Vector2(16, 464), Vector2(25, 498), Vector2(37, 522), Vector2(35, 555), Vector2(55, 578), Vector2(65, 628), Vector2(90, 679), Vector2(76, 720), Vector2(0, 720)], Color("0c1924"))
	draw_line(Vector2(25, 568), Vector2(63, 686), Color("314346"), 4, true)

func _draw_hud() -> void:
	# Quiet editorial HUD floats on the glass.
	text_at("PHANTOM", Vector2(111, 102), 26, CREAM, title_font)
	text_at("IMAGINATION", Vector2(112, 121), 9, Color("d5c8b7"), mono)
	for i in range(6):
		var x := 113 + i * 24
		poly([Vector2(x, 132), Vector2(x + 18, 132), Vector2(x + 13, 139), Vector2(x - 5, 139)], CYAN if i < state.health else Color(0.1, 0.18, 0.23, 0.5))
	text_at("%06d" % state.score, Vector2(110, 166), 16, CREAM, mono)
	if state.combo > 1:
		text_at("%d× FLOW" % state.combo, Vector2(111, 189), 13, CYAN, mono)
	var mph := roundi(state.speed / PhantomRun.CRUISE * 68)
	text_at("%02d" % mph, Vector2(1090, 104), 47, CREAM, title_font)
	text_at("MPH", Vector2(1144, 101), 11, Color("d7cec0"), mono)
	text_at("CAR SPEED", Vector2(1079, 123), 9, Color("d5c8b7"), mono)
	var progress := clampf(state.distance / PhantomRun.ROUTE_LENGTH, 0, 1)
	draw_line(Vector2(936, 143), Vector2(1157, 143), Color(0.13, 0.2, 0.25, 0.4), 3)
	draw_line(Vector2(936, 143), Vector2(936 + 221 * progress, 143), CYAN, 2)
	draw_circle(Vector2(936 + 221 * progress, 143), 4, CREAM)
	draw_circle(Vector2(1157, 143), 5, Color("ff8b70") if state.phase != "depart" else CYAN)
	text_at("EASTBOUND", Vector2(935, 167), 10, Color("e7d9c6"), mono)
	text_at("07", Vector2(1142, 167), 10, Color("e7d9c6"), mono)
	if state.phase == "boss":
		text_center("THE SIGNAL WARDEN", 108, 21, CREAM, title_font)
		draw_rect(Rect2(465, 123, 350, 4), Color(0.08, 0.12, 0.18, 0.5))
		draw_rect(Rect2(465, 123, 350 * state.boss_hp / float(state.boss_max_hp), 4), Color("ff9376"))
		text_center("INTERSECTION  /  BREAK THE SIGNAL", 148, 9, Color("eed1b9"), mono)
	elif state.phase == "brake":
		text_center("RED LIGHT AHEAD", 110, 28, ORANGE, title_font)
	elif state.route_time < 4:
		var a := clampf(4 - state.route_time, 0, 1)
		text_center("01  /  THE LONG WAY HOME", 197, 27, Color(CREAM, a), title_font)
		text_center("EASTBOUND EXPRESSWAY     •     7:42 PM", 220, 10, Color(CREAM, a * 0.75), mono)
	if state.hint_time > 0:
		var a := minf(1, state.hint_time)
		draw_style_box(panel_style(Color(0.06, 0.11, 0.16, a * 0.74), Color(0.7, 0.85, 0.83, a * 0.15), 5), Rect2(252, 599, 776, 30))
		text_center(state.hint, 619, 12, Color(CREAM, a))
	# Inputs live on the door rather than competing with the action.
	text_at("SPACE  JUMP     J  BUSTER     K  CHARGE     L ×3  SWORD COMBO     SHIFT  DASH", Vector2(113, 693), 10, Color("a5b4b2"), mono)
	var ready := state.dash_cooldown <= 0
	text_at("DASH READY" if ready else "RECHARGING", Vector2(796, 693), 10, CYAN if ready else Color("788f93"), mono)
	text_at("ESC  PAUSE", Vector2(1084, 630), 9, Color(0.9, 0.90, 0.85, 0.55), mono)
	if demo:
		text_center("DEMO DRIVE  /  ENTER TO TAKE OVER", 570, 10, CYAN, mono)

func _draw_title() -> void:
	var z := 1.015 + sin(menu_time * 0.1) * 0.008
	draw_texture_rect(interior, Rect2(-12, -8, 1280 * z, 720 * z), false)
	gradient(Rect2(0, 0, 1280, 720), Color(0.015, 0.045, 0.08, 0.12), Color(0.015, 0.035, 0.06, 0.58))
	# Right-hand shade puts the typography over the open window, away from the child.
	var points := PackedVector2Array([Vector2(540, 0), Vector2(1280, 0), Vector2(1280, 720), Vector2(540, 720)])
	draw_polygon(points, PackedColorArray([Color(0.02, 0.05, 0.09, 0), Color(0.02, 0.05, 0.09, 0.47), Color(0.02, 0.05, 0.09, 0.55), Color(0.02, 0.05, 0.09, 0)]))
	text_at("A BACKSEAT DAYDREAM", Vector2(782, 169), 11, Color("ead6bc"), mono)
	draw_line(Vector2(784, 184), Vector2(838, 184), CYAN, 2)
	text_at("HIGHWAY", Vector2(776, 288), 104, CREAM, title_font)
	text_at("PHANTOM", Vector2(776, 378), 104, CREAM, title_font)
	text_at("The world rushes past.", Vector2(785, 416), 17, Color("e6d4bd"))
	text_at("Your imagination keeps up.", Vector2(785, 441), 17, Color("e6d4bd"))
	var rect := Rect2(784, 484, 342, 53)
	var hover := rect.has_point(mouse)
	draw_style_box(panel_style(Color("bbfff0") if hover else CYAN, CYAN, 3), rect)
	text_at("START THE RIDE", Vector2(807, 518), 24, INK, title_font)
	text_at("ENTER  >", Vector2(1029, 516), 12, INK, mono)
	text_at("D  WATCH DEMO", Vector2(785, 571), 11, CREAM, mono)
	text_at("G  ASSIST: " + ("ON" if assist else "OFF"), Vector2(975, 571), 11, CYAN if assist else CREAM, mono)
	text_at("B  INTERSECTION PRACTICE", Vector2(785, 603), 10, Color("b1c9c3"), mono)
	text_at("HEADPHONES RECOMMENDED", Vector2(55, 671), 9, Color("acb8b6"), mono)
	text_at("01 / THE LONG WAY HOME", Vector2(784, 656), 11, Color("d7c6af"), mono)
	text_at("A PLAYABLE DAYDREAM     •     GODOT 4", Vector2(784, 679), 9, Color("a3b4b4"), mono)
	text_at("F11  FULLSCREEN", Vector2(55, 692), 9, Color("acb8b6"), mono)

func _draw_intro() -> void:
	var progress := smoothstep(1.0, 5.2, intro_time)
	var scale_factor := lerpf(1, 1.66, progress)
	var alpha := 1.0 - smoothstep(3.8, 6.3, intro_time)
	if alpha > 0:
		var origin := Vector2(940, 320)
		var offset := origin - origin * scale_factor
		draw_texture_rect(interior, Rect2(offset, Vector2(1280, 720) * scale_factor), false, Color(1, 1, 1, alpha))
	draw_rect(Rect2(0, 0, 1280, 32), Color("080f19"))
	draw_rect(Rect2(0, 671, 1280, 49), Color("080f19"))
	var caption := "The long way home."
	if intro_time > 2.5:
		caption = "You saw him too."
	if intro_time > 5.5:
		caption = "Keep up."
	text_center(caption, 702, 18, CREAM)
	text_at("ENTER  SKIP", Vector2(1133, 25), 9, Color("a3b6b8"), mono)

func _draw_pause() -> void:
	draw_rect(Rect2(0, 0, 1280, 720), Color(0.025, 0.05, 0.09, 0.8))
	text_center("HOLD THAT THOUGHT.", 256, 63, CREAM, title_font)
	text_center("ESC / ENTER   RESUME THE RIDE", 309, 13, CYAN, mono)
	text_center("A / D or arrow keys   Move alongside the car", 366, 15, CREAM)
	text_center("Space   Double jump       Shift   Dash through danger", 395, 15, CREAM)
	text_center("J / left click   Buster       Hold K   Charge       L / right click ×3   Sword combo", 424, 15, CREAM)
	text_center("R   Restart       T   Title       M   " + ("Unmute" if muted else "Mute") + "       F11   Fullscreen", 475, 13, Color("a8bcb9"), mono)
	text_center("ASSIST " + ("ON  /  Imagination cannot break" if assist else "OFF  /  Six hits before the daydream fades"), 520, 11, ORANGE, mono)

func _draw_result() -> void:
	draw_rect(Rect2(0, 0, 1280, 720), Color(0.025, 0.05, 0.09, 0.79))
	var won := state.mode == "win"
	text_center("THE RIDE GOES ON." if won else "DON’T LOSE THE DAYDREAM.", 280, 65 if won else 53, CREAM, title_font)
	text_center("Some heroes only need a window." if won else "He’s still out there. Close your eyes and try again.", 327, 17, Color("c5d0c8"))
	text_center("%06d    /    %d MACHINES BROKEN" % [state.score, state.kills], 391, 16, CYAN, mono)
	text_center("ENTER / R   RIDE AGAIN       T   TITLE", 458, 13, CREAM, mono)
	if not won:
		text_center("G   Retry with assist — keep the action, never lose the run", 504, 13, ORANGE)

func text_at(value: String, pos: Vector2, size: int, color: Color, face: Font = null) -> void:
	var f := face if face != null else font
	draw_string(f, pos + Vector2(0, 1), value, HORIZONTAL_ALIGNMENT_LEFT, -1, size, Color(0.02, 0.04, 0.08, color.a * 0.30))
	draw_string(f, pos, value, HORIZONTAL_ALIGNMENT_LEFT, -1, size, color)

func text_center(value: String, y: float, size: int, color: Color, face: Font = null) -> void:
	var f := face if face != null else font
	var width := f.get_string_size(value, HORIZONTAL_ALIGNMENT_LEFT, -1, size).x
	text_at(value, Vector2((1280 - width) / 2, y), size, color, f)

func poly(points: Array, color: Color, outline: Color = Color.TRANSPARENT, width: float = 1) -> void:
	var ps := PackedVector2Array(points)
	draw_colored_polygon(ps, color)
	if outline.a > 0:
		ps.append(ps[0])
		draw_polyline(ps, outline, width, true)

func glow(pos: Vector2, radius: float, color: Color, alpha: float) -> void:
	for i in range(4, 0, -1):
		draw_circle(pos, radius * i / 4.0, Color(color, alpha * (1 - i / 5.0)))

func gradient(rect: Rect2, top: Color, bottom: Color) -> void:
	draw_polygon(PackedVector2Array([rect.position, rect.position + Vector2(rect.size.x, 0), rect.end, rect.position + Vector2(0, rect.size.y)]), PackedColorArray([top, top, bottom, bottom]))

func panel_style(bg: Color, border: Color, radius: int) -> StyleBoxFlat:
	var style := StyleBoxFlat.new()
	style.bg_color = bg
	style.border_color = border
	style.set_border_width_all(1)
	style.set_corner_radius_all(radius)
	return style
