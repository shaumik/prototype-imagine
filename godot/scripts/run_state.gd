class_name PhantomRun
extends RefCounted
## Deterministic simulation. All scenery shares distance; the camera belongs to the car.

const FLOOR := 584.0
const CRUISE := 480.0
const ROUTE_LENGTH := 23500.0
const CYAN := Color("75fff1")
const CORAL := Color("ff825f")

var rng := RandomNumberGenerator.new()
var mode := "title"
var phase := "run"
var time := 0.0
var route_time := 0.0
var distance := 0.0
var speed := CRUISE
var player := Vector2(390, FLOOR)
var velocity := Vector2.ZERO
var grounded := true
var air_motion := AirMotion.new()
var dash_motion := DashMotion.new()
var runner_motion := RunnerMotion.new()
var sword := SwordCombo.new()
var jumps := 0
var jump_buffer := 0.0
var coyote := 0.1
var dash := 0.0
var dash_cooldown := 0.0
var slash: float:
	get: return sword.remaining()
var shoot_cooldown := 0.0
var recoil := 0.0
var recoil_charged := false
var slash_targets: Array[Dictionary] = []
var slash_boss_hit := false
var slash_sound_played := false
var charge := 0.0
var invulnerable := 0.0
var health := 6
var score := 0
var combo := 0
var combo_timer := 0.0
var kills := 0
var shake := 0.0
var hitstop := 0.0
var flash := 0.0
var travel_spawn := 900.0
var spawn_index := 0
var platforms: Array[Dictionary] = []
var gaps: Array[Dictionary] = []
var enemies: Array[Dictionary] = []
var shots: Array[Dictionary] = []
var particles: Array[Dictionary] = []
var ghosts: Array[Dictionary] = []
var pickups: Array[Dictionary] = []
var sounds: Array[String] = []
var boss_hp := 80
var boss_max_hp := 80
var boss_pos := Vector2(980, 385)
var boss_time := 0.0
var boss_fire := 1.8
var boss_flash := 0.0
var warning := 0.0
var phase_time := 0.0
var hint := "SPACE  ·  jump twice to reach the upper route"
var hint_time := 7.0
var easy := false

func _init() -> void:
	rng.seed = 74017
	runner_motion.reset()

func start(assist: bool = false) -> void:
	mode = "play"
	phase = "run"
	time = 0
	route_time = 0
	distance = 0
	speed = CRUISE
	player = Vector2(390, FLOOR)
	velocity = Vector2.ZERO
	grounded = true
	air_motion.reset()
	dash_motion.reset()
	runner_motion.reset()
	jumps = 0
	jump_buffer = 0
	coyote = 0.1
	dash = 0
	dash_cooldown = 0
	sword.reset()
	shoot_cooldown = 0
	recoil = 0
	recoil_charged = false
	slash_targets.clear()
	slash_boss_hit = false
	slash_sound_played = false
	charge = 0
	invulnerable = 1
	health = 6
	score = 0
	combo = 0
	combo_timer = 0
	kills = 0
	shake = 0
	hitstop = 0
	flash = 0
	travel_spawn = 800
	spawn_index = 0
	platforms.clear()
	gaps.clear()
	enemies.clear()
	shots.clear()
	particles.clear()
	ghosts.clear()
	pickups.clear()
	sounds.clear()
	boss_hp = boss_max_hp
	boss_time = 0
	boss_fire = 1.8
	boss_flash = 0
	warning = 0
	phase_time = 0
	hint = "SPACE  ·  jump twice to reach the upper route"
	hint_time = 7
	easy = assist
	rng.seed = 74017
	platforms.append({"x": 1000.0, "y": 486.0, "w": 300.0, "kind": 0})
	add_pickup(Vector2(1130, 446))

func tick(dt: float, input: Dictionary) -> void:
	time += dt
	if mode != "play":
		return
	# Consume attack edges even while impacts freeze simulation time.
	if input.get("slash", false) and sword.press():
		_begin_swing()
	if input.get("jump", false):
		jump_buffer = 0.12
	if hitstop > 0:
		hitstop -= dt
		return
	route_time += dt
	dash_motion.advance(dt)
	if sword.advance(dt):
		_begin_swing()
	for key in ["dash", "dash_cooldown", "shoot_cooldown", "recoil", "invulnerable", "combo_timer", "flash", "hint_time", "boss_flash", "jump_buffer"]:
		set(key, maxf(0, float(get(key)) - dt))
	shake = move_toward(shake, 0, dt * 24)
	if combo_timer <= 0:
		combo = 0
	_update_phase(dt)
	distance += speed * dt
	if grounded:
		coyote = 0.10
	else:
		coyote = maxf(0, coyote - dt)
	if jump_buffer > 0 and (coyote > 0 or jumps < 2):
		dash = 0
		dash_motion.reset()
		velocity.y = -745 if jumps == 0 else -670
		air_motion.launch()
		grounded = false
		jumps += 1
		jump_buffer = 0
		coyote = 0
		burst(player - Vector2(0, 7), 12, CYAN, 150)
		sounds.append("jump")
	if input.get("jump_release", false) and velocity.y < -280:
		velocity.y *= 0.60
	if input.get("dash", false) and dash_cooldown <= 0:
		dash = DashMotion.DURATION
		dash_motion.start(velocity.x)
		dash_cooldown = 0.85
		invulnerable = maxf(invulnerable, 0.27)
		velocity.y *= 0.18
		shake = 3
		sounds.append("dash")
	if input.get("charge", false):
		charge = minf(charge + dt, 1.2)
	elif charge > 0:
		fire(charge >= 0.7)
		charge = 0
	if input.get("shoot", false) and shoot_cooldown <= 0:
		fire(false)
	var axis: float = input.get("axis", 0.0)
	var target_vx := axis * 280.0
	if absf(axis) < 0.1:
		target_vx = (390.0 - player.x) * 1.8 if phase != "boss" else 0.0
	var last_y := player.y
	if dash > 0:
		velocity.x = dash_motion.speed_at(target_vx, dt * 0.5)
		player.x += velocity.x * dt
	else:
		velocity.x = move_toward(velocity.x, target_vx, dt * 1700)
		velocity.y += 1900 * dt
		player += velocity * dt
	player.x = clampf(player.x, 135, 1045)
	grounded = false
	for p in platforms:
		p.x -= speed * dt
		if velocity.y >= 0 and player.x > p.x - 13 and player.x < p.x + p.w + 13 and last_y <= p.y + 4 and player.y >= p.y:
			player.y = p.y
			_land()
	var over_gap := false
	for gap in gaps:
		gap.x -= speed * dt
		if player.x > gap.x + 8 and player.x < gap.x + gap.w - 8:
			over_gap = true
	gaps = gaps.filter(func(g): return g.x + g.w > -100)
	if player.y >= FLOOR and not over_gap:
		player.y = FLOOR
		_land()
	if player.y > 740:
		damage()
		player.y = 325
		velocity.y = 0
		air_motion.reset()
		dash_motion.reset()
		dash = 0
		ghosts.clear()
		sword.reset()
		runner_motion.reset()
		jumps = 1
		invulnerable = 1.6
		burst(player, 25, CYAN, 250)
	air_motion.advance(dt, grounded, velocity.y)
	runner_motion.advance(dt, self)
	platforms = platforms.filter(func(p): return p.x + p.w > -100)
	if grounded and speed > 10 and int(time * 32) != int((time - dt) * 32):
		particles.append({"pos": player - Vector2(8, 4), "vel": Vector2(-rng.randf_range(80, 210), -rng.randf_range(5, 50)), "life": 0.32, "max": 0.32, "size": rng.randf_range(2, 5), "color": Color("d6bfac")})
	if phase == "run" and distance > travel_spawn:
		_spawn_pattern()
	if sword.striking():
		if not slash_sound_played:
			sounds.append("slash_%d" % sword.step)
			slash_sound_played = true
		_attack_blade()
	_update_enemies(dt)
	_update_shots(dt)
	_update_pickups(dt)
	for p in particles:
		p.life -= dt
		p.pos += p.vel * dt
		p.vel.y += 160 * dt
	particles = particles.filter(func(p): return p.life > 0)
	for g in ghosts:
		g.life -= dt
		g.pos.x -= speed * dt
	ghosts = ghosts.filter(func(g): return g.life > 0)
	if dash > 0 and dash_motion.emit_ghost():
		ghosts.append({"pose": runner_motion.pose.duplicate(), "pos": player, "life": DashMotion.GHOST_LIFE})

func _land() -> void:
	if velocity.y > 140:
		air_motion.touchdown(velocity.y)
	if velocity.y > 300:
		burst(player, 8, Color("d1bcb0"), 105)
	velocity.y = 0
	grounded = true
	jumps = 0

func _update_phase(dt: float) -> void:
	if phase == "run":
		speed = move_toward(speed, CRUISE, 160 * dt)
		if distance >= ROUTE_LENGTH:
			phase = "brake"
			phase_time = 0
			hint = "RED LIGHT  /  Something is waiting at the intersection."
			hint_time = 4
			sounds.append("warning")
	elif phase == "brake":
		phase_time += dt
		speed = move_toward(speed, 0, 125 * dt)
		if speed <= 0:
			phase = "boss"
			phase_time = 0
			enemies.clear()
			platforms.clear()
			gaps.clear()
			shots.clear()
			pickups.clear()
			health = mini(6, health + 2)
			hint = "BREAK THE SIGNAL  ·  Hold K to charge / Shift through attacks"
			hint_time = 6
	elif phase == "boss":
		boss_time += dt
		boss_pos = Vector2(930 + sin(boss_time * 0.55) * 110, 372 + sin(boss_time * 1.7) * 78)
		boss_fire -= dt
		warning = clampf(1.0 - boss_fire / 0.7, 0, 1)
		if boss_fire <= 0:
			var enraged := boss_hp < boss_max_hp / 2
			boss_fire = 1.4 if enraged else 2.0
			var target := (player - Vector2(0, 55) - boss_pos).normalized()
			for i in range(-1, 2):
				shots.append({"pos": boss_pos + Vector2(-55, 16), "vel": target.rotated(i * 0.20) * (340 if enraged else 285), "life": 5.0, "enemy": true, "charged": false})
			sounds.append("enemy")
			if enraged:
				shots.append({"pos": Vector2(1160, FLOOR - 24), "vel": Vector2(-350, 0), "life": 4.0, "enemy": true, "charged": true})
	elif phase == "depart":
		phase_time += dt
		speed = move_toward(speed, CRUISE, dt * 110)
		if phase_time > 6:
			mode = "win"

func _spawn_pattern() -> void:
	spawn_index += 1
	travel_spawn += rng.randf_range(1000, 1420)
	var kind := spawn_index % 5
	if kind == 0 or kind == 3:
		platforms.append({"x": 1370.0, "y": 480.0, "w": 320.0, "kind": 0})
		platforms.append({"x": 1790.0, "y": 377.0, "w": 260.0, "kind": 1})
		add_pickup(Vector2(1510, 441))
		add_pickup(Vector2(1910, 338))
		add_enemy(Vector2(1620, 436), "drone")
		gaps.append({"x": 1560.0, "w": 195.0})
	elif kind == 1:
		add_enemy(Vector2(1450, FLOOR - 31), "sentry")
		add_enemy(Vector2(1770, 417), "drone")
		platforms.append({"x": 1610.0, "y": 464.0, "w": 280.0, "kind": 0})
		add_pickup(Vector2(1750, 421))
	elif kind == 2:
		platforms.append({"x": 1420.0, "y": 493.0, "w": 370.0, "kind": 1})
		add_enemy(Vector2(1560, 445), "drone")
		add_enemy(Vector2(2010, FLOOR - 31), "sentry")
	else:
		add_enemy(Vector2(1500, 418), "drone")
		add_enemy(Vector2(1800, 505), "drone")
		add_enemy(Vector2(2100, FLOOR - 31), "sentry")
		for i in range(4):
			add_pickup(Vector2(1550 + i * 80, 330 - sin(i * PI / 3) * 40))
	if spawn_index == 2:
		hint = "J  ·  buster     L  ·  cyber blade     SHIFT  ·  invincible dash"
		hint_time = 6
	if spawn_index == 5:
		hint = "Hold K, then release  ·  charged buster pierces armor"
		hint_time = 5
	if spawn_index == 3:
		hint = "ROADWORK AHEAD  ·  leap the break or take the upper platforms"
		hint_time = 5

func add_enemy(pos: Vector2, kind: String) -> void:
	enemies.append({"pos": pos, "base_y": pos.y, "kind": kind, "hp": 3 if kind == "sentry" else 2, "fire": rng.randf_range(1.1, 2.8), "seed": rng.randf() * TAU, "flash": 0.0})

func add_pickup(pos: Vector2) -> void:
	pickups.append({"pos": pos, "seed": rng.randf() * TAU})

func fire(charged: bool) -> void:
	if not charged and shoot_cooldown > 0:
		return
	shoot_cooldown = 0.18 if not charged else 0.34
	var muzzle: Vector2 = player + runner_motion.pose.muzzle
	recoil = CombatMotion.CHARGED_SHOT_DURATION if charged else CombatMotion.SHOT_DURATION
	recoil_charged = charged
	var aim := Vector2.RIGHT
	var nearest := 950.0
	for enemy in enemies:
		var offset: Vector2 = enemy.pos - muzzle
		if offset.x > 0 and offset.length() < nearest and absf(offset.y) < 155:
			nearest = offset.length()
			aim = Vector2.from_angle(clampf(offset.angle(), -0.26, 0.26))
	if phase == "boss":
		var offset := boss_pos - muzzle
		if offset.x > 0:
			aim = Vector2.from_angle(clampf(offset.angle(), -0.32, 0.32))
	shots.append({"pos": muzzle, "vel": aim * 1260, "life": 1.4, "enemy": false, "charged": charged})
	sounds.append("charge" if charged else "shoot")
	if charged:
		shake = 4
	burst(muzzle, 5, CYAN, 90)

func _begin_swing() -> void:
	slash_targets.clear()
	slash_boss_hit = false
	slash_sound_played = false

func _blade_reaches(point: Vector2, radius: float) -> bool:
	var pose := runner_motion.pose
	var local := point - player
	if local.distance_to(Geometry2D.get_closest_point_to_segment(local, pose.hand, pose.blade_tip)) <= radius:
		return true
	# Swept segments cover the fast cut between simulation frames.
	for segment in pose.trail:
		if local.distance_to(Geometry2D.get_closest_point_to_segment(local, segment.inner, segment.outer)) <= radius:
			return true
	return false

func _attack_blade() -> void:
	var index := sword.step - 1
	for e in enemies:
		if e not in slash_targets and _blade_reaches(e.pos, 48):
			slash_targets.append(e)
			e.hp -= SwordCombo.DAMAGE[index]
			e.flash = 0.14
			burst(e.pos, 26 if sword.step == 3 else 12, CYAN, 310 if sword.step == 3 else 220)
			hitstop = maxf(hitstop, SwordCombo.IMPACT_PAUSE[index])
			shake = 8 if sword.step == 3 else 3
	for b in shots:
		if b.enemy and _blade_reaches(b.pos, 22):
			b.enemy = false
			b.vel = Vector2(1100, 0)
			b.charged = true
			score += 25
	if phase == "boss" and not slash_boss_hit and _blade_reaches(boss_pos, 80):
		slash_boss_hit = true
		_hit_boss(SwordCombo.BOSS_DAMAGE[index])
		hitstop = maxf(hitstop, SwordCombo.IMPACT_PAUSE[index])
		shake = maxf(shake, 8 if sword.step == 3 else 3)

func _update_enemies(dt: float) -> void:
	for e in enemies:
		e.pos.x -= speed * dt * (1.02 if e.kind == "drone" else 1.0)
		e.flash = maxf(0, e.flash - dt)
		if e.kind == "drone":
			e.pos.y = e.base_y + sin(time * 3 + e.seed) * 22
		e.fire -= dt
		if e.fire <= 0 and e.pos.x < 1240 and e.pos.x > player.x + 60:
			e.fire = 2.8
			var direction: Vector2 = (player - Vector2(0, 55) - e.pos).normalized()
			shots.append({"pos": e.pos, "vel": direction * 300, "life": 4.0, "enemy": true, "charged": false})
		if e.pos.distance_to(player - Vector2(0, 45)) < 48:
			if dash > 0:
				e.hp = 0
			elif sword.step == 0 or sword.age > SwordCombo.HIT_END[sword.step - 1]:
				damage()
		if e.hp <= 0:
			_kill(e.pos)
	enemies = enemies.filter(func(e): return e.hp > 0 and e.pos.x > -140)

func _update_shots(dt: float) -> void:
	for b in shots:
		b.pos += b.vel * dt
		b.life -= dt
		if b.enemy:
			if b.pos.distance_to(player - Vector2(0, 50)) < (36 if b.charged else 26):
				damage()
				b.life = 0
		else:
			for e in enemies:
				if e.hp > 0 and b.life > 0 and b.pos.distance_to(e.pos) < (64 if b.charged else 43):
					e.hp -= 4 if b.charged else 1
					e.flash = 0.12
					burst(b.pos, 7, CORAL, 150)
					b.life = 0
					sounds.append("hit")
			if phase == "boss" and b.life > 0 and b.pos.distance_to(boss_pos) < (100 if b.charged else 80):
				_hit_boss(5 if b.charged else 1)
				b.life = 0
	shots = shots.filter(func(b): return b.life > 0 and b.pos.x > -100 and b.pos.x < 1450)

func _update_pickups(dt: float) -> void:
	for p in pickups:
		p.pos.x -= speed * dt
		if p.pos.distance_to(player - Vector2(0, 48)) < 90:
			p.pos = p.pos.move_toward(player - Vector2(0, 48), dt * 380)
		if p.pos.distance_to(player - Vector2(0, 48)) < 33:
			score += 50
			p.pos.x = -500
			burst(player - Vector2(0, 50), 10, CYAN, 120)
			sounds.append("pickup")
			if score % 500 == 0:
				health = mini(6, health + 1)
	pickups = pickups.filter(func(p): return p.pos.x > -100)

func _kill(pos: Vector2) -> void:
	kills += 1
	combo += 1
	combo_timer = 4
	score += 100 * mini(combo, 8)
	burst(pos, 25, CORAL, 320)
	burst(pos, 12, CYAN, 220)
	shake = maxf(shake, 5)
	hitstop = maxf(hitstop, 0.04)
	sounds.append("explode")

func _hit_boss(amount: int) -> void:
	boss_hp = maxi(0, boss_hp - amount)
	boss_flash = 0.12
	burst(boss_pos - Vector2(45, 0), 12, CORAL, 200)
	score += amount * 15
	shake = 3
	sounds.append("hit")
	if boss_hp <= 0:
		phase = "depart"
		phase_time = 0
		shots.clear()
		burst(boss_pos, 100, CYAN, 520)
		burst(boss_pos, 70, CORAL, 440)
		flash = 0.35
		shake = 15
		hint = "GREEN LIGHT  /  The ride goes on."
		hint_time = 5
		score += 2500
		sounds.append("victory")

func damage() -> void:
	if invulnerable > 0 or dash > 0:
		return
	health -= 1
	if easy:
		health = maxi(health, 1)
	invulnerable = 1.4
	combo = 0
	shake = 9
	flash = 0.15
	burst(player - Vector2(0, 50), 16, CORAL, 260)
	sounds.append("hurt")
	if health <= 0:
		mode = "lose"

func burst(pos: Vector2, count: int, color: Color, force: float) -> void:
	for i in range(count):
		var life := rng.randf_range(0.18, 0.65)
		particles.append({"pos": pos, "vel": Vector2.from_angle(rng.randf() * TAU) * rng.randf_range(force * 0.2, force), "life": life, "max": life, "color": color, "size": rng.randf_range(1.5, 4.5)})
