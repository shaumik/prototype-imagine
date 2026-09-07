class_name CombatMotion
extends RefCounted
## Shared weapon timing keeps visible recoil and blade motion aligned with hits.

const SLASH_DURATION := 0.36
const SLASH_HIT_START := 0.065
const SLASH_HIT_END := 0.175
const SHOT_DURATION := 0.18
const CHARGED_SHOT_DURATION := 0.30

static func slash_elapsed(remaining: float) -> float:
	return SLASH_DURATION - remaining

static func slash_active(remaining: float) -> bool:
	var age := slash_elapsed(remaining)
	return remaining > 0 and age >= SLASH_HIT_START and age <= SLASH_HIT_END

static func recoil_amount(remaining: float, charged: bool) -> float:
	if remaining <= 0:
		return 0.0
	var duration := CHARGED_SHOT_DURATION if charged else SHOT_DURATION
	var age := duration - remaining
	return smoothstep(0.0, 0.025, age) * (1.0 - smoothstep(0.025, duration, age))
