class_name DashMotion
extends RefCounted
## A short boost followed by an interruptible visual recovery.

const DURATION := 0.23
const RECOVERY := 0.12
const TOTAL := DURATION + RECOVERY
const GHOST_INTERVAL := 1.0 / 30.0
const GHOST_LIFE := 0.16
const PEAK_SPEED := 935.0

var age := TOTAL
var entry_velocity := 0.0
var ghost_timer := 0.0

func reset() -> void:
	age = TOTAL
	entry_velocity = 0
	ghost_timer = 0

func start(horizontal_velocity: float) -> void:
	age = 0
	entry_velocity = horizontal_velocity
	ghost_timer = 0.045

func advance(dt: float) -> void:
	age = minf(TOTAL, age + dt)
	ghost_timer = maxf(0, ghost_timer - dt)

func active() -> bool:
	return age < TOTAL

func speed_at(target_velocity: float, sample_offset: float = 0.0) -> float:
	var t := age + sample_offset
	var launch := smoothstep(0, 0.035, t)
	var release := smoothstep(DURATION - 0.075, DURATION, t)
	return lerpf(lerpf(entry_velocity, PEAK_SPEED, launch), target_velocity, release)

func intensity() -> float:
	return smoothstep(0, 0.045, age) * (1.0 - smoothstep(0.18, 0.29, age))

func emit_ghost() -> bool:
	if age >= DURATION or ghost_timer > 0:
		return false
	ghost_timer = GHOST_INTERVAL
	return true
