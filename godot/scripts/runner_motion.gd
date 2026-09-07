class_name RunnerMotion
extends RefCounted
## Continuous body poses. Gameplay owns movement; this rig owns joint placement.

const STRIDE := 320.0
const STANCE := 0.20
const UPPER_LEG := 41.0
const LOWER_LEG := 43.0
const REST_BLADE := {"hand": Vector2(-28, 25), "angle": 2.83, "lean": 0.0, "hip": Vector2.ZERO}

var phase := 0.0
var clock := 0.0
var air_weight := 0.0
var run_weight := 1.0
var was_grounded := true
var visual_vy := 0.0
var reach_weight := 0.0
var pose: Dictionary = {}

func reset() -> void:
	phase = 0
	clock = 0
	air_weight = 0
	run_weight = 1
	was_grounded = true
	visual_vy = 0
	reach_weight = 0
	pose = sample(phase, clock, 1, 0, 0, 0, 0, 0, 0, false, 0)

func advance(dt: float, state) -> void:
	clock += dt
	var travel_speed := maxf(0, state.speed + state.velocity.x)
	run_weight = move_toward(run_weight, clampf(travel_speed / 160.0, 0, 1), dt * 8)
	if state.grounded and not was_grounded:
		# Rejoin on a planted contact instead of an arbitrary mid-swing frame.
		phase = 0
	if state.grounded and state.dash <= 0:
		phase = fposmod(phase + dt * travel_speed / STRIDE, 1)
	air_weight = move_toward(air_weight, 0.0 if state.grounded else 1.0, dt / 0.075)
	if not state.grounded:
		visual_vy = state.velocity.y
		# Limit leg unfolding directly, including the velocity reversal of a double jump.
		reach_weight = move_toward(reach_weight, smoothstep(100, 650, visual_vy), dt / 0.12)
	was_grounded = state.grounded
	pose = sample(phase, clock, run_weight, air_weight, visual_vy, state.dash_motion.intensity() if state.dash_motion.active() else 0.0, state.slash, state.charge, state.recoil, state.recoil_charged, state.air_motion.landing_squash(), reach_weight, state.sword.step, state.sword.entry_pose)

static func bezier(a: Vector2, b: Vector2, c: Vector2, d: Vector2, t: float) -> Vector2:
	var u := 1.0 - t
	return a * u * u * u + b * 3 * u * u * t + c * 3 * u * t * t + d * t * t * t

static func foot_path(cycle: float) -> Vector2:
	var t := fposmod(cycle, 1.0)
	var reach := STRIDE * STANCE * 0.5
	if t < STANCE:
		# Exact roadside velocity during contact: the supporting foot cannot skate.
		return Vector2(reach - STRIDE * t, -8)
	t = (t - STANCE) / (1.0 - STANCE)
	if t < 0.52:
		return bezier(Vector2(-reach, -8), Vector2(-76.3733, -8), Vector2(-42, -24), Vector2(-7, -22), t / 0.52)
	return bezier(Vector2(-7, -22), Vector2(25.3077, -20.1538), Vector2(72.96, -8), Vector2(reach, -8), (t - 0.52) / 0.48)

static func foot_angle(cycle: float) -> float:
	var t := fposmod(cycle, 1.0)
	return 0.0 if t < STANCE else sin((t - STANCE) / (1 - STANCE) * TAU) * 0.22

static func knee(hip: Vector2, ankle: Vector2) -> Vector2:
	return joint(hip, ankle, UPPER_LEG, LOWER_LEG, 1)

static func joint(start: Vector2, end: Vector2, upper: float, lower: float, bend: float) -> Vector2:
	var delta := end - start
	var distance := clampf(delta.length(), 1, upper + lower - 0.1)
	var direction := delta.normalized()
	var along := (upper * upper - lower * lower + distance * distance) / (2 * distance)
	var across := sqrt(maxf(0, upper * upper - along * along))
	return start + direction * along + Vector2(direction.y, -direction.x) * across * bend

static func sample(cycle: float, time: float, running: float, airborne: float, vy: float, boost: float, slash: float, charge: float, recoil: float, charged: bool, landing: float, reach_override: float = -1.0, sword_step: int = 1, sword_entry: Dictionary = {}) -> Dictionary:
	var attacking := slash > 0 and sword_step > 0
	var sword_age: float = SwordCombo.DURATIONS[sword_step - 1] - slash if attacking else 0
	var clip: Dictionary = SwordAnimation.blended_sample(sword_step, sword_age, sword_entry) if attacking else REST_BLADE
	var bob := -1.8 * sin(cycle * TAU * 2) * running * (1 - airborne)
	var hip := Vector2(0, lerpf(-82, -70, running) + bob + landing * 45).lerp(Vector2(-5, -44), boost)
	hip += clip.hip * Vector2(0.35, 1.0) * (1 - boost * 0.6)
	var lean := lerpf(0.28 + 0.012 * sin(cycle * TAU), 1.02, boost) + float(clip.lean) * (1 - boost * 0.55)
	var step_a := Vector2(13, -8).lerp(foot_path(cycle), running)
	var step_b := Vector2(-14, -8).lerp(foot_path(cycle + 0.5), running)
	var reach := smoothstep(100, 650, vy) if reach_override < 0 else reach_override
	var air_a := Vector2(20, -34).lerp(Vector2(23, -9), reach)
	var air_b := Vector2(-27, -23).lerp(Vector2(-18, -15), reach)
	step_a = step_a.lerp(air_a, airborne)
	step_b = step_b.lerp(air_b, airborne)
	step_a = step_a.lerp(Vector2(-36, -13 - airborne * 12), boost)
	step_b = step_b.lerp(Vector2(-53, -8 - airborne * 18), boost)
	var angle_a := lerpf(foot_angle(cycle) * running, lerpf(-0.3, 0, reach), airborne)
	var angle_b := lerpf(foot_angle(cycle + 0.5) * running, 0.3, airborne)
	angle_a = lerpf(angle_a, 0.4, boost)
	angle_b = lerpf(angle_b, 0.3, boost)
	var chest := hip + Vector2(0, -36).rotated(lean)
	var neck := hip + Vector2(0, -45).rotated(lean)
	var shoulder := chest + Vector2(1, 2)
	var blade_shoulder := chest + Vector2(-8, 3)
	var kick := CombatMotion.recoil_amount(recoil, charged) * (1.45 if charged else 1.0)
	var brace := smoothstep(0, 0.7, charge)
	var elbow := shoulder + Vector2(18 - kick * 7 - brace * 3, 15).normalized() * 25
	var cannon_angle := -0.06 - kick * 0.12 - brace * 0.025 + float(clip.lean) * 0.6
	var gun_root := elbow + Vector2(-1 - kick * 6, -2)
	var hand: Vector2 = blade_shoulder + clip.hand
	var blade_angle: float = clip.angle
	var swing := 0.0
	var trail: Array[Dictionary] = []
	if attacking:
		swing = 1.0 if sword_age >= SwordCombo.HIT_START[sword_step - 1] and sword_age <= SwordCombo.HIT_END[sword_step - 1] else 0.0
		trail = SwordAnimation.trail(sword_step, sword_age, blade_shoulder)
	var blade_elbow := joint(blade_shoulder, hand, 25, 28, -1)
	return {
		"hip": hip, "chest": chest, "neck": neck, "lean": lean,
		"ankle_a": step_a, "ankle_b": step_b,
		"foot_angle_a": angle_a, "foot_angle_b": angle_b,
		"knee_a": knee(hip + Vector2(3, 0), step_a), "knee_b": knee(hip + Vector2(-4, -1), step_b),
		"shoulder": shoulder, "elbow": elbow, "gun": gun_root, "gun_angle": cannon_angle,
		"muzzle": gun_root + Vector2(43, 0).rotated(cannon_angle),
		"blade_shoulder": blade_shoulder, "blade_elbow": blade_elbow, "hand": hand, "blade_angle": blade_angle,
		"blade_tip": hand + Vector2.from_angle(blade_angle) * (84 if attacking and sword_step == 3 else 75),
		"sword_step": sword_step if attacking else 0, "sword_age": sword_age, "trail": trail,
		"scarf_wave": time * 11, "boost": boost, "swing": swing, "charge": charge,
		"recoil": recoil, "charged": charged, "air": airborne,
	}
