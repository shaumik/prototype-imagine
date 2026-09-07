extends SceneTree
## Behavior checks for the runner simulation. Run with Godot --headless --script.

var failures: Array[String] = []
var checks := 0

func _initialize() -> void:
	_test_jumps()
	_test_jump_animation()
	_test_platforms()
	_test_gaps()
	_test_combat()
	_test_sword_combo()
	_test_combo_poses()
	_test_dash()
	_test_dash_animation()
	_test_continuous_runner()
	_test_intersection()
	_test_restart()
	for failure in failures:
		printerr("FAIL: " + failure)
	print("SIMULATION TESTS: %d checks, %d failures" % [checks, failures.size()])
	quit(0 if failures.is_empty() else 1)

func fresh() -> PhantomRun:
	var s := PhantomRun.new()
	s.start()
	s.platforms.clear()
	s.pickups.clear()
	s.travel_spawn = 1e9
	s.invulnerable = 0
	return s

func check(condition: bool, label: String) -> void:
	checks += 1
	if not condition:
		failures.append(label)

func advance(s: PhantomRun, seconds: float, input: Dictionary = {}) -> void:
	for i in range(roundi(seconds * 120)):
		s.tick(1.0 / 120, input)

func _test_jumps() -> void:
	var s := fresh()
	s.tick(1.0 / 120, {"jump": true})
	check(s.velocity.y < -600 and s.jumps == 1 and not s.grounded, "jump leaves road")
	advance(s, 0.2)
	s.tick(1.0 / 120, {"jump": true})
	check(s.jumps == 2 and s.velocity.y < -600, "air jump restores ascent")
	advance(s, 0.14)
	var before := s.velocity.y
	s.tick(1.0 / 120, {"jump": true})
	check(s.jumps == 2 and s.velocity.y > before, "third jump is rejected")
	advance(s, 1.2)
	check(s.grounded and s.jumps == 0 and is_equal_approx(s.player.y, PhantomRun.FLOOR), "road landing resets jump count")
	s.tick(1.0 / 120, {"jump": true})
	s.tick(1.0 / 120, {"jump_release": true})
	check(s.velocity.y > -480, "early release makes a short hop")

func _test_platforms() -> void:
	var s := fresh()
	s.platforms.append({"x": 100.0, "y": 480.0, "w": 900.0, "kind": 0})
	s.player = Vector2(390, 440)
	s.velocity.y = 180
	s.grounded = false
	s.jumps = 1
	advance(s, 0.2)
	check(s.grounded and is_equal_approx(s.player.y, 480), "descending feet land on moving platform top")
	s.platforms[0].x = -1000
	advance(s, 0.1)
	check(not s.grounded and s.player.y > 480, "walking off a platform resumes gravity")
	check(s.runner_motion.air_weight > 0.9 and s.runner_motion.visual_vy > 0, "walking off a ledge blends into falling")

func _test_jump_animation() -> void:
	var s := fresh()
	s.tick(1.0 / 120, {"jump": true})
	check(s.runner_motion.air_weight > 0 and s.runner_motion.air_weight < 1 and s.velocity.y < 0, "takeoff starts an immediate transition from the running pose")
	var reached_air_pose := false
	for i in range(120):
		reached_air_pose = reached_air_pose or s.runner_motion.air_weight == 1
		s.tick(1.0 / 120, {})
		if s.grounded:
			break
	check(reached_air_pose, "a full jump reaches its folded airborne pose")
	check(s.grounded and s.air_motion.landing > 0, "touchdown starts the landing recovery")
	check(s.runner_motion.phase < 0.02 and s.runner_motion.air_weight > 0, "landing rejoins a contact stride while blending out of the air pose")
	advance(s, 0.25)
	check(s.air_motion.landing == 0, "standing on the road does not repeatedly restart landing recovery")
	s = fresh()
	s.tick(1.0 / 120, {"jump": true, "jump_release": true})
	advance(s, 0.25)
	check(s.velocity.y > 0 and s.runner_motion.visual_vy > 0, "a short hop reaches its falling pose sooner than a held jump")
	s = fresh()
	s.tick(1.0 / 120, {"jump": true})
	advance(s, 0.60)
	var falling_ankle: Vector2 = s.runner_motion.pose.ankle_a
	s.tick(1.0 / 120, {"jump": true})
	check(s.velocity.y < -600 and s.runner_motion.pose.ankle_a.distance_to(falling_ankle) < 10, "air jump responds immediately without snapping the leg pose")
	advance(s, 0.18)
	check(s.runner_motion.visual_vy < 0 and s.runner_motion.pose.ankle_a.y < -30, "air jump folds the legs smoothly back into ascent")
	advance(s, 0.7)
	check(s.air_motion.landing > 0, "air jump settles into landing on contact")
	s.tick(1.0 / 120, {"jump": true})
	check(not s.grounded and s.air_motion.landing == 0, "jumping again can interrupt landing recovery")
	s.start()
	check(s.runner_motion.air_weight == 0 and s.air_motion.landing == 0 and s.runner_motion.phase == 0, "restart clears airborne and landing animation state")

func _test_combat() -> void:
	var s := fresh()
	s.add_enemy(Vector2(670, PhantomRun.FLOOR - 62), "drone")
	advance(s, 0.8, {"shoot": true})
	check(s.kills == 1 and s.score >= 100, "buster collision destroys enemy and awards score")
	s = fresh()
	s.add_enemy(s.player + Vector2(75, -45), "sentry")
	s.tick(1.0 / 120, {"slash": true})
	check(s.kills == 0 and s.enemies[0].hp == 3, "blade windup does not damage before the visible swing")
	advance(s, 0.16)
	check(s.enemies.is_empty() and s.kills == 1, "blade destroys a nearby armored sentry")
	s = fresh()
	s.shots.append({"pos": s.player + Vector2(105, -55), "vel": Vector2(-300, 0), "life": 2.0, "enemy": true, "charged": false})
	s.tick(1.0 / 120, {"slash": true})
	advance(s, 0.15)
	check(not s.shots[0].enemy and s.shots[0].vel.x > 0, "blade reflects hostile projectiles")
	s = fresh()
	advance(s, 0.8, {"charge": true})
	s.tick(1.0 / 120, {})
	check(s.shots.size() == 1 and s.shots[0].charged, "holding and releasing charge emits charged shot")
	check(s.recoil > 0.25 and s.recoil_charged, "charged shot triggers the stronger recoil animation")
	advance(s, 0.4)
	check(s.recoil == 0, "cannon returns to its aiming pose after recoil")
	s.damage()
	s.damage()
	check(s.health == 5, "damage grace period prevents duplicate damage")
	s = fresh()
	s.add_pickup(s.player - Vector2(0, 48))
	s.tick(1.0 / 120, {})
	check(s.score == 50 and s.pickups.is_empty(), "collecting an imagination shard awards points")
	s = fresh()
	s.add_enemy(s.player + Vector2(130, -45), "sentry")
	s.enemies[0].hp = 20
	s.tick(1.0 / 120, {"slash": true})
	advance(s, 0.3)
	check(s.enemies[0].hp == 16, "one sword swing cannot damage the same target on every animation frame")
	s = fresh()
	s.tick(1.0 / 120, {"shoot": true})
	check(s.recoil > 0 and not s.recoil_charged, "normal shot triggers cannon recoil")
	s.start()
	check(s.recoil == 0 and s.slash_targets.is_empty(), "restart clears weapon animation state")

func _test_gaps() -> void:
	var s := fresh()
	s.gaps.append({"x": 250.0, "w": 850.0})
	advance(s, 0.2)
	check(s.player.y > PhantomRun.FLOOR and not s.grounded, "broken road has no collision floor")
	advance(s, 0.35)
	check(s.health == 5 and s.player.y < PhantomRun.FLOOR, "falling costs one hit and safely returns the runner")

func _test_sword_combo() -> void:
	var s := fresh()
	s.tick(1.0 / 120, {"slash": true})
	advance(s, 0.6)
	check(s.sword.serial == 1 and s.sword.step == 0, "a single press plays only the opening slash and recovers")
	s.tick(1.0 / 120, {"slash": true})
	check(s.sword.step == 1, "an expired combo starts again with the opening slash")
	s = fresh()
	s.tick(1.0 / 120, {"slash": true})
	advance(s, 0.08)
	s.hitstop = 0.1
	var frozen_age := s.sword.age
	s.tick(1.0 / 120, {"slash": true})
	s.tick(1.0 / 120, {"slash": true})
	check(s.sword.age == frozen_age and s.sword.queued == 2, "two follow-up presses are retained while an impact freezes the animation")
	advance(s, 1.3)
	check(s.sword.serial == 3 and s.sword.step == 0, "three buffered presses play exactly three slashes")
	check(s.sounds.count("slash_1") == 1 and s.sounds.count("slash_2") == 1 and s.sounds.count("slash_3") == 1, "each slash has one distinct audible strike")
	s = fresh()
	s.tick(1.0 / 120, {"slash": true})
	advance(s, 0.3)
	var last_hand: Vector2 = s.runner_motion.pose.hand
	var last_angle: float = s.runner_motion.pose.blade_angle
	s.tick(1.0 / 120, {"slash": true})
	check(s.sword.step == 2 and s.runner_motion.pose.hand.distance_to(last_hand) < 6 and absf(angle_difference(last_angle, s.runner_motion.pose.blade_angle)) < 0.15, "a late follow-up tap blends from the current sword pose instead of snapping to a new windup")
	s = fresh()
	s.phase = "boss"
	s.speed = 0
	s.add_enemy(s.player + Vector2(68, -85), "sentry")
	s.enemies[0].hp = 30
	for i in range(150):
		s.tick(1.0 / 120, {"slash": true} if i in [0, 14, 35] else {})
	check(s.enemies[0].hp == 15, "all three visible cuts can hit the same target once, with a stronger finisher")
	s = fresh()
	s.tick(1.0 / 120, {"jump": true, "slash": true})
	s.tick(1.0 / 120, {"slash": true})
	s.tick(1.0 / 120, {"slash": true})
	advance(s, 0.44)
	check(not s.grounded and s.sword.step == 3, "the complete combo remains available during a jump")
	s.start()
	check(s.sword.step == 0 and s.sword.queued == 0 and s.sword.serial == 0, "restart clears the active combo and buffered attacks")

func _test_combo_poses() -> void:
	var limb_error := 0.0
	var min_knee_drop := INF
	var max_foot_lift := 0.0
	var max_foot_reach := 0.0
	for i in range(240):
		var cycle := i / 240.0
		var gait := RunnerMotion.sample(cycle, 0, 1, 0, 0, 0, 0, 0, 0, false, 0)
		for side in ["a", "b"]:
			min_knee_drop = minf(min_knee_drop, gait["knee_" + side].y - gait.hip.y)
			max_foot_lift = maxf(max_foot_lift, -gait["ankle_" + side].y)
			max_foot_reach = maxf(max_foot_reach, absf(gait["ankle_" + side].x))
		for step in range(1, 4):
			var remaining: float = SwordCombo.DURATIONS[step - 1] * (1 - cycle)
			for boost in [0.0, 1.0]:
				var pose := RunnerMotion.sample(cycle, 0, 1, 0, 0, boost, remaining, 0, 0, false, 0, -1, step)
				limb_error = maxf(limb_error, absf(pose.blade_shoulder.distance_to(pose.blade_elbow) - 25))
				limb_error = maxf(limb_error, absf(pose.blade_elbow.distance_to(pose.hand) - 28))
				for side in ["a", "b"]:
					var hip: Vector2 = pose.hip + (Vector2(3, 0) if side == "a" else Vector2(-4, -1))
					limb_error = maxf(limb_error, absf(hip.distance_to(pose["knee_" + side]) - RunnerMotion.UPPER_LEG))
					limb_error = maxf(limb_error, absf(pose["knee_" + side].distance_to(pose["ankle_" + side]) - RunnerMotion.LOWER_LEG))
	check(min_knee_drop > 10 and max_foot_lift < 25 and max_foot_reach < 55, "the gait stays low and compact instead of lifting the knees to the hips")
	check(limb_error < 0.01, "all three attacks preserve arm and leg lengths while running and dashing (maximum error %.3f)" % limb_error)
	for step in range(1, 3):
		var ending := SwordAnimation.sample(step, SwordCombo.CHAIN_AT[step - 1])
		var beginning := SwordAnimation.sample(step + 1, 0)
		check(ending.hand.distance_to(beginning.hand) < 0.01 and absf(angle_difference(ending.angle, beginning.angle)) < 0.01 and ending.hip.distance_to(beginning.hip) < 0.01, "slash %d connects to the next attack without a pose snap" % step)

func _test_dash() -> void:
	var s := fresh()
	s.tick(1.0 / 120, {"dash": true})
	var x := s.player.x
	advance(s, 0.1)
	check(s.player.x > x + 50 and s.dash > 0, "dash advances alongside the car")
	s.damage()
	check(s.health == 6, "dash protects against contact damage")
	advance(s, 0.2)
	s.tick(1.0 / 120, {"dash": true})
	check(s.dash <= 0 and s.dash_cooldown > 0, "dash cannot repeat during cooldown")
	advance(s, 0.65)
	s.tick(1.0 / 120, {"dash": true})
	check(s.dash > 0, "dash is available after cooldown")

func _test_dash_animation() -> void:
	var s := fresh()
	s.tick(1.0 / 120, {"dash": true})
	check(s.velocity.x > 0 and s.velocity.x < 100, "dash begins moving immediately with a gentle launch")
	var boost_peak := 0.0
	var peak := 0.0
	var largest_step := 0.0
	var max_ghosts := 0
	var previous_vx := s.velocity.x
	var previous_ghost: Dictionary = {}
	var captured_hip := Vector2.INF
	for i in range(44):
		boost_peak = maxf(boost_peak, s.runner_motion.pose.boost)
		max_ghosts = maxi(max_ghosts, s.ghosts.size())
		if previous_ghost.is_empty() and not s.ghosts.is_empty():
			previous_ghost = s.ghosts[0]
			captured_hip = previous_ghost.pose.hip
		peak = maxf(peak, s.player.x)
		s.tick(1.0 / 120, {})
		largest_step = maxf(largest_step, absf(s.velocity.x - previous_vx))
		previous_vx = s.velocity.x
	check(boost_peak > 0.99 and s.runner_motion.pose.boost == 0, "ground dash leans fully into boost and smoothly recovers")
	check(peak - 390 > 135 and peak - 390 < 185, "eased dash preserves a useful crossing distance")
	check(largest_step < 360, "dash acceleration and release avoid an instant velocity jump")
	check(max_ghosts > 0 and max_ghosts <= 5, "dash trail remains limited to five fading afterimages")
	check(captured_hip.is_finite() and previous_ghost.pose.hip == captured_hip, "afterimage retains its original pose as the runner recovers")
	check(not s.dash_motion.active() and s.dash == 0, "dash exits both boost and visual recovery")
	check(s.runner_motion.pose.lean < 0.3, "dash recovery returns to the normal running posture")
	advance(s, 0.1)
	check(s.ghosts.is_empty(), "all afterimages fade after the boost")

	s = fresh()
	s.tick(1.0 / 120, {"dash": true})
	advance(s, 0.29)
	check(s.dash == 0 and s.dash_motion.active(), "visual recovery does not extend the dash combat window")
	s.damage()
	check(s.health == 5, "recovery does not extend dash invulnerability")
	s.tick(1.0 / 120, {"jump": true})
	check(s.velocity.y < -600 and not s.dash_motion.active(), "jump interrupts recovery immediately")

	s = fresh()
	s.tick(1.0 / 120, {"dash": true})
	advance(s, 0.09)
	s.tick(1.0 / 120, {"jump": true})
	check(s.dash == 0 and s.velocity.y < -600 and not s.grounded, "jump can cancel an active ground dash")

	s = fresh()
	s.tick(1.0 / 120, {"jump": true})
	advance(s, 0.15)
	var start_height := s.player.y
	s.tick(1.0 / 120, {"dash": true})
	boost_peak = 0
	var held_height := true
	for i in range(44):
		boost_peak = maxf(boost_peak, s.runner_motion.pose.boost)
		if s.dash > 0:
			held_height = held_height and is_equal_approx(s.player.y, start_height)
		s.tick(1.0 / 120, {})
	check(held_height, "air dash holds its height during boost")
	check(boost_peak > 0.99 and not s.grounded and s.runner_motion.air_weight == 1, "air dash keeps the legs tucked through launch and recovery")
	check(s.velocity.y > 0 and s.runner_motion.visual_vy > 0, "air dash recovery flows into falling")
	s.start()
	check(not s.dash_motion.active() and s.ghosts.is_empty(), "restart clears dash poses and afterimages")

func _test_continuous_runner() -> void:
	var max_leg_error := 0.0
	var max_joint_step := 0.0
	var before := RunnerMotion.sample(0, 0, 1, 0, 0, 0, 0, 0, 0, false, 0)
	for i in range(1, 337):
		var pose := RunnerMotion.sample(i / 336.0, i / 480.0, 1, 0, 0, 0, 0, 0, 0, false, 0)
		for side in ["a", "b"]:
			var hip: Vector2 = pose.hip + (Vector2(3, 0) if side == "a" else Vector2(-4, -1))
			var knee: Vector2 = pose["knee_" + side]
			var ankle: Vector2 = pose["ankle_" + side]
			max_leg_error = maxf(max_leg_error, absf(hip.distance_to(knee) - RunnerMotion.UPPER_LEG))
			max_leg_error = maxf(max_leg_error, absf(knee.distance_to(ankle) - RunnerMotion.LOWER_LEG))
			max_joint_step = maxf(max_joint_step, ankle.distance_to(before["ankle_" + side]))
		before = pose
	check(max_leg_error < 0.01, "the entire running cycle preserves both leg lengths")
	check(max_joint_step < 3, "running joints move continuously through the loop seam")
	var contact_a := RunnerMotion.foot_path(0.10)
	var contact_b := RunnerMotion.foot_path(0.11)
	check(is_equal_approx(contact_a.y, -8) and is_equal_approx(contact_b.x - contact_a.x, -RunnerMotion.STRIDE * 0.01), "planted feet move exactly with the road instead of skating")
	var one := RunnerMotion.sample(0.1, 0, 1, 0, 0, 0, 0, 0, 0, false, 0)
	var other := RunnerMotion.sample(0.6, 0, 1, 0, 0, 0, 0, 0, 0, false, 0)
	check(one.ankle_a.distance_to(other.ankle_b) < 0.01 and one.ankle_b.distance_to(other.ankle_a) < 0.01, "the two legs exchange contact and swing every half stride")
	var firing := RunnerMotion.sample(0.1, 0, 1, 0, 0, 0, 0, 0, 0.13, false, 0)
	check(firing.ankle_a == one.ankle_a and firing.muzzle.x < one.muzzle.x - 8, "firing kicks the cannon back without freezing the legs")
	var attacking := RunnerMotion.sample(0.1, 0, 1, 0, 0, 0, CombatMotion.SLASH_DURATION - 0.20, 0, 0, false, 0)
	check(attacking.ankle_a == one.ankle_a and attacking.hand.distance_to(one.hand) > 40, "the blade swings independently over the running gait")
	var arm_error := 0.0
	for i in range(56):
		var pose := RunnerMotion.sample(0.1, 0, 1, 0, 0, 0, maxf(0, CombatMotion.SLASH_DURATION - i / 120.0), 0, 0, false, 0)
		arm_error = maxf(arm_error, absf(pose.blade_shoulder.distance_to(pose.blade_elbow) - 25))
		arm_error = maxf(arm_error, absf(pose.blade_elbow.distance_to(pose.hand) - 28))
	check(arm_error < 0.01, "the sword arm preserves its proportions throughout the swing")
	var s := fresh()
	var last: Vector2 = s.runner_motion.pose.ankle_a
	var largest_air_step := 0.0
	for i in range(170):
		s.tick(1.0 / 120, {"jump": true} if i in [12, 79] else {})
		var ankle: Vector2 = s.runner_motion.pose.ankle_a
		largest_air_step = maxf(largest_air_step, ankle.distance_to(last))
		last = ankle
	check(largest_air_step < 18, "jump, double jump and landing blend without snapping the feet")
	advance(s, 0.6)
	check(s.grounded and s.runner_motion.air_weight == 0, "landing fully returns to the connected running pose")
	s.phase = "boss"
	s.speed = 0
	advance(s, 0.5)
	var idle_phase := s.runner_motion.phase
	advance(s, 0.2)
	check(s.runner_motion.run_weight == 0 and s.runner_motion.phase == idle_phase, "the runner stops stepping when the car stops")

func _test_intersection() -> void:
	var s := fresh()
	s.distance = PhantomRun.ROUTE_LENGTH
	s.tick(1.0 / 120, {})
	check(s.phase == "brake", "route end triggers braking")
	advance(s, 4.2)
	check(s.phase == "boss" and is_zero_approx(s.speed), "car stops before boss fight")
	var d := s.distance
	advance(s, 0.5)
	check(is_equal_approx(s.distance, d), "road distance stays fixed at red light")
	var hp := s.boss_hp
	s.shots.append({"pos": s.boss_pos, "vel": Vector2.ZERO, "life": 1.0, "enemy": false, "charged": true})
	s.tick(1.0 / 120, {})
	check(s.boss_hp == hp - 5, "charged shot damages boss")
	s._hit_boss(1000)
	check(s.phase == "depart" and s.boss_hp == 0, "boss defeat changes the light")
	advance(s, 6.3)
	check(s.mode == "win" and s.speed > 400, "car accelerates into stage completion")

func _test_restart() -> void:
	var s := fresh()
	s.health = 1
	s.damage()
	check(s.mode == "lose", "zero imagination ends the run")
	s.start(true)
	s.invulnerable = 0
	s.health = 1
	s.damage()
	check(s.health == 1 and s.mode == "play", "assist protects the final health point")
	s.start()
	check(s.health == 6 and s.distance == 0 and s.score == 0 and s.phase == "run" and not s.easy, "restart resets all stage progress")
