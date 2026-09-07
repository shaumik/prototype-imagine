class_name AirMotion
extends RefCounted
## Contact compression follows impact speed without delaying the next jump.

const LAND_DURATION := 0.18

var landing := 0.0
var landing_strength := 0.0

func reset() -> void:
	landing = 0
	landing_strength = 0

func launch() -> void:
	landing = 0

func touchdown(impact_speed: float) -> void:
	landing = LAND_DURATION
	landing_strength = clampf(impact_speed / 740.0, 0.25, 1.0)

func advance(dt: float, _grounded: bool, _vertical_speed: float) -> void:
	landing = maxf(0, landing - dt)

func landing_squash() -> float:
	if landing <= 0:
		return 0.0
	return sin((1.0 - landing / LAND_DURATION) * PI) * 0.07 * landing_strength
