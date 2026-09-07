shader_type canvas_item;
// Production chroma key for the illustrated atlas; neutral to the rest of the canvas.
void fragment() {
	vec4 pixel = COLOR;
	float key = smoothstep(0.26, 0.62, min(pixel.r, pixel.b) - pixel.g);
	pixel.a *= 1.0 - key;
	if (key > 0.02) {
		pixel.rb = min(pixel.rb, vec2(pixel.g + 0.20));
	}
	float grain = fract(sin(dot(SCREEN_UV * vec2(1280.0, 720.0), vec2(12.9898, 78.233))) * 43758.5453);
	pixel.rgb += (grain - 0.5) * 0.018;
	COLOR = pixel;
}
