class_name SwordCombo
extends RefCounted
## Three explicit attacks, with queued button presses carried through impact pauses.

const DURATIONS := [0.36, 0.37, 0.48]
const HIT_START := [0.065, 0.055, 0.095]
const HIT_END := [0.175, 0.175, 0.255]
const CHAIN_AT := [0.205, 0.215]
const DAMAGE := [4, 4, 7]
const BOSS_DAMAGE := [6, 6, 10]
const IMPACT_PAUSE := [0.025, 0.030, 0.065]

var step := 0
var age := 0.0
var queued := 0
var cooldown := 0.0
var serial := 0
var entry_pose: Dictionary = {}

func reset() -> void:
	step = 0
	age = 0
	queued = 0
	cooldown = 0
	serial = 0
	entry_pose = {}

func press() -> bool:
	if step > 0:
		queued = mini(3 - step, queued + 1)
		return false
	if cooldown > 0:
		return false
	begin(1)
	return true

func begin(next_step: int) -> void:
	entry_pose = SwordAnimation.sample(step, age) if step > 0 else {}
	step = next_step
	age = 0
	serial += 1

func advance(dt: float) -> bool:
	cooldown = maxf(0, cooldown - dt)
	if step == 0:
		return false
	age += dt
	if step < 3 and queued > 0 and age >= CHAIN_AT[step - 1]:
		queued -= 1
		begin(step + 1)
		return true
	if age >= DURATIONS[step - 1]:
		cooldown = 0.09 if step == 3 else 0.0
		step = 0
		queued = 0
	return false

func remaining() -> float:
	return maxf(0, DURATIONS[step - 1] - age) if step > 0 else 0.0

func striking() -> bool:
	return step > 0 and age >= HIT_START[step - 1] and age <= HIT_END[step - 1]
