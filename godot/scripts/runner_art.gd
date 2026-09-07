class_name RunnerArt
extends RefCounted
## One connected character, drawn from continuous joints instead of unrelated frames.

var parts := RunnerParts.new()

func render(target: Node2D, position: Vector2, pose: Dictionary, alpha: float = 1.0, echo: bool = false) -> void:
	if pose.is_empty():
		return
	var front := Color(1, 1, 1, alpha)
	var rear := Color(0.73, 0.81, 0.94, alpha)
	var hip: Vector2 = position + pose.hip
	var neck: Vector2 = position + pose.neck
	if not echo:
		_draw_boost(target, position, pose, alpha)
		_draw_sword_trail(target, position, pose, alpha)
	parts.scarf(target, neck + Vector2(-3, 1), pose.scarf_wave, pose.boost, front)
	_draw_leg(target, position, pose, "b", rear)
	if pose.sword_step == 0:
		_draw_blade_arm(target, position, pose, rear, echo)
	_draw_leg(target, position, pose, "a", front)
	parts.attached(target, "pelvis", hip, pose.lean * 0.25, Vector2(0.085, 0.085), front)
	parts.bone(target, "torso", hip, neck, front, 1.08)
	parts.attached(target, "head", neck, pose.lean * 0.16, Vector2(0.145, 0.145), front)
	var shoulder: Vector2 = position + pose.shoulder
	var elbow: Vector2 = position + pose.elbow
	parts.bone(target, "upper_arm", shoulder, elbow, front)
	parts.attached(target, "shoulder", shoulder, pose.lean * 0.35, Vector2(0.081, 0.081), front)
	parts.attached(target, "cannon", position + pose.gun, pose.gun_angle, Vector2(43.0 / 339.0, 43.0 / 339.0), front)
	if pose.sword_step > 0:
		_draw_blade_arm(target, position, pose, front, echo)
	if not echo:
		_draw_buster_light(target, position + pose.muzzle, Vector2.from_angle(pose.gun_angle), pose, alpha)

func render_afterimage(target: Node2D, position: Vector2, pose: Dictionary, life: float) -> void:
	var alpha := 0.20 * pow(clampf(life / DashMotion.GHOST_LIFE, 0, 1), 1.5)
	render(target, position, pose, alpha, true)

func _draw_leg(target: Node2D, position: Vector2, pose: Dictionary, side: String, color: Color) -> void:
	var hip: Vector2 = position + pose.hip + (Vector2(3, 0) if side == "a" else Vector2(-4, -1))
	var knee: Vector2 = position + pose["knee_" + side]
	var ankle: Vector2 = position + pose["ankle_" + side]
	parts.bone(target, "thigh", hip, knee, color, 1.1)
	parts.bone(target, "shin", knee, ankle, color, 1.1)
	parts.attached(target, "boot", ankle, pose["foot_angle_" + side], Vector2(0.075, 0.075), color)

func _draw_blade_arm(target: Node2D, position: Vector2, pose: Dictionary, color: Color, echo: bool) -> void:
	var shoulder: Vector2 = position + pose.blade_shoulder
	var elbow: Vector2 = position + pose.blade_elbow
	var hand: Vector2 = position + pose.hand
	parts.bone(target, "upper_arm", shoulder, elbow, color)
	parts.bone(target, "forearm", elbow, hand, color, 0.85)
	var blade_scale := 0.19 if pose.sword_step == 3 else 0.17
	parts.attached(target, "blade", hand, pose.blade_angle, Vector2(blade_scale, blade_scale), color)

func _draw_sword_trail(target: Node2D, position: Vector2, pose: Dictionary, alpha: float) -> void:
	var trail: Array = pose.trail
	if trail.size() < 2:
		return
	var fade := 1.0 - clampf((pose.sword_age - SwordCombo.HIT_END[pose.sword_step - 1]) / 0.065, 0, 1)
	var heavy: bool = pose.sword_step == 3
	for i in range(1, trail.size()):
		var strength := float(i) / (trail.size() - 1) * alpha * fade
		var a: Dictionary = trail[i - 1]
		var b: Dictionary = trail[i]
		if a.outer.distance_squared_to(b.outer) < 0.01:
			continue
		var points := PackedVector2Array([position + a.inner, position + a.outer, position + b.outer, position + b.inner])
		# A ribbon follows the actual hand and saber sweep, including the rising cut.
		target.draw_colored_polygon(points, Color(0.3, 1, 0.9, strength * (0.48 if heavy else 0.30)))
		target.draw_line(position + a.outer, position + b.outer, Color(0.85, 1, 1, strength), 4 if heavy else 2, true)

func _draw_boost(target: Node2D, position: Vector2, pose: Dictionary, alpha: float) -> void:
	var strength: float = pose.boost
	if strength < 0.01:
		return
	var tail: Vector2 = position + pose.hip + Vector2(-10, 1)
	target.draw_line(tail, tail - Vector2(104 * strength, 0), Color(0.3, 1, 0.9, alpha * strength * 0.14), 12)
	target.draw_line(tail, tail - Vector2(71 * strength, 0), Color(0.7, 1, 0.94, alpha * strength * 0.65), 2)

func _draw_buster_light(target: Node2D, muzzle: Vector2, direction: Vector2, pose: Dictionary, alpha: float) -> void:
	var charge: float = pose.charge
	if charge > 0:
		var radius := 7 + charge * 13
		var pulse := 0.7 + 0.3 * sin(charge * 30)
		var ring := PackedVector2Array()
		for i in range(25):
			ring.append(muzzle + Vector2.from_angle(i * TAU / 24) * radius)
		target.draw_polyline(ring, Color(0.1, 0.9, 1, alpha * pulse), 2, true)
		target.draw_circle(muzzle, 3, Color(0.85, 1, 1, alpha))
	var duration := CombatMotion.CHARGED_SHOT_DURATION if pose.charged else CombatMotion.SHOT_DURATION
	var flash := 1.0 - (duration - float(pose.recoil)) / (0.09 if pose.charged else 0.055)
	if pose.recoil > 0 and flash > 0:
		var size := (37.0 if pose.charged else 23.0) * flash
		var normal := direction.orthogonal()
		var points := PackedVector2Array([muzzle - direction * 4, muzzle + direction * 7 + normal * size * 0.5, muzzle + direction * size * 1.8, muzzle + direction * 7 - normal * size * 0.5])
		target.draw_colored_polygon(points, Color(0.1, 0.9, 1, alpha))
		target.draw_line(muzzle, muzzle + direction * size, Color(0.95, 1, 1, alpha), 4)
