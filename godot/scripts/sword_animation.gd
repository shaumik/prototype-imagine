class_name SwordAnimation
extends RefCounted
## Authored downstroke, rising return and overhead finisher. Angles are unwrapped.
## Keys: seconds, hand x/y, blade angle, body lean, hip x/y offset.

const CLIPS := [
	[
		[0.000, -28, 25, 2.83, 0.00, 0, 0],
		[0.050, -25, -13, 4.10, -0.12, -3, 2],
		[0.070, -6, -24, 4.75, -0.03, 0, 3],
		[0.125, 46, 6, 6.55, 0.23, 9, 4],
		[0.180, 28, 32, 7.63, 0.14, 7, 3],
		[0.205, 28, 32, 7.63, 0.14, 7, 3],
		[0.285, -7, 37, 8.55, 0.03, 1, 1],
		[0.360, -28, 25, 9.113185, 0.00, 0, 0],
	],
	[
		[0.000, 28, 32, 1.346815, 0.14, 7, 3],
		[0.045, 35, 25, 1.05, 0.18, 6, 5],
		[0.090, 45, -1, 0.05, 0.04, 10, 1],
		[0.150, 14, -39, -1.75, -0.16, 4, -2],
		[0.195, -13, -32, -2.38, -0.12, 1, 0],
		[0.215, -13, -32, -2.38, -0.12, 1, 0],
		[0.300, -33, 7, -3.20, -0.04, 0, 1],
		[0.370, -28, 25, -3.453185, 0.00, 0, 0],
	],
	[
		[0.000, -13, -32, -2.38, -0.12, 1, 0],
		[0.075, -4, -44, -1.82, -0.18, -3, 3],
		[0.105, 13, -40, -1.25, 0.05, 3, 5],
		[0.170, 47, 15, 0.65, 0.38, 15, 7],
		[0.230, 20, 40, 1.70, 0.28, 11, 8],
		[0.290, 5, 39, 2.05, 0.20, 5, 6],
		[0.380, -24, 29, 2.62, 0.04, 0, 2],
		[0.480, -28, 25, 2.83, 0.00, 0, 0],
	],
]

static func sample(step: int, age: float) -> Dictionary:
	var keys: Array = CLIPS[clampi(step - 1, 0, 2)]
	var values: Array = keys.back()
	for i in range(1, keys.size()):
		if age <= keys[i][0]:
			var amount := smoothstep(keys[i - 1][0], keys[i][0], age)
			values = []
			for j in range(7):
				values.append(lerpf(keys[i - 1][j], keys[i][j], amount))
			break
	return {"hand": Vector2(values[1], values[2]), "angle": values[3], "lean": values[4], "hip": Vector2(values[5], values[6])}

static func blended_sample(step: int, age: float, entry: Dictionary) -> Dictionary:
	var pose := sample(step, age)
	if not entry.is_empty() and age < 0.045:
		var weight := smoothstep(0, 0.045, age)
		pose.hand = entry.hand.lerp(pose.hand, weight)
		pose.angle = lerp_angle(entry.angle, pose.angle, weight)
		pose.lean = lerpf(entry.lean, pose.lean, weight)
		pose.hip = entry.hip.lerp(pose.hip, weight)
	return pose

static func trail(step: int, age: float, shoulder: Vector2) -> Array[Dictionary]:
	var samples: Array[Dictionary] = []
	var hit_start: float = SwordCombo.HIT_START[step - 1]
	var hit_end: float = SwordCombo.HIT_END[step - 1]
	if age < hit_start or age > hit_end + 0.065:
		return samples
	var last := minf(age, hit_end)
	for i in range(9):
		var t := maxf(hit_start, last - (8 - i) * 0.009)
		var clip := sample(step, t)
		var hand: Vector2 = shoulder + clip.hand
		var direction := Vector2.from_angle(clip.angle)
		samples.append({"inner": hand + direction * 14, "outer": hand + direction * (84 if step == 3 else 75)})
	return samples
