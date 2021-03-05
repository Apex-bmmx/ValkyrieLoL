from valkyrie import *			 


def valkyrie_menu(ctx) :		 
	ui = ctx.ui					 
	
def valkyrie_on_load(ctx) :	 
	cfg = ctx.cfg				 
	pass						 
	
def valkyrie_on_save(ctx) :	 
	cfg = ctx.cfg				 
	pass						 
	
	
def draw_rect(ctx, start_pos, end_pos, radius, color):
	
	dir = Vec3(end_pos.x - start_pos.x, 0, end_pos.z - start_pos.z).normalize()
				
	left_dir = Vec3(dir.x, dir.y, dir.z).rotate_y(90) * radius
	right_dir = Vec3(dir.x, dir.y, dir.z).rotate_y(-90) * radius
	
	p1 = Vec3(start_pos.x + left_dir.x,  start_pos.y + left_dir.y,  start_pos.z + left_dir.z)
	p2 = Vec3(end_pos.x + left_dir.x,    end_pos.y + left_dir.y,    end_pos.z + left_dir.z)
	p3 = Vec3(end_pos.x + right_dir.x,   end_pos.y + right_dir.y,   end_pos.z + right_dir.z)
	p4 = Vec3(start_pos.x + right_dir.x, start_pos.y + right_dir.y, start_pos.z + right_dir.z)
	
	ctx.rect(p1, p2, p3, p4, 3, color)
	
	
def missile_draw_line(ctx, missile, static):
	cast_info = missile.spell
	
	start  = missile.pos.clone()
	end    = cast_info.end_pos.clone()
	start.y = cast_info.start_pos.y
	end.y   = start.y
	if static.has_flag(Spell.CastDirection):
		end = start + (end - cast_info.start_pos).normalize() * (static.cast_range - start.distance(cast_info.start_pos))
		
	draw_rect(ctx, start, end, static.width, Col.Yellow)
	
def cast_draw_line(ctx, cast_info, static):
	
	start = cast_info.start_pos.clone()
	end = cast_info.end_pos.clone()
	end.y = start.y
	
	if static.has_flag(Spell.CastDirection):
		end = start + (end - start).normalize() * static.cast_range
	
	draw_rect(ctx, start, end, static.width, Col.Gray)
	
def cast_draw_area(ctx, cast_info, static):
	
	fill_percent = min(1.0, (ctx.time - cast_info.time_begin)/cast_info.cast_time)
	ctx.circle(cast_info.end_pos, static.cast_radius, 30, 3.0, Col.Gray)
	ctx.circle_fill(cast_info.end_pos, static.cast_radius*fill_percent, 30, Col(0.5, 0.5, 0.5, 0.5))
	
def cast_draw_cone(ctx, cast_info, static):
	
	start = cast_info.start_pos
	dir   = (cast_info.end_pos - start).normalize()
	angle = static.cast_cone_angle*2.0
	left  = start + dir.rotate_y(-angle) * static.cast_cone_distance
	right = start + dir.rotate_y(angle) * static.cast_cone_distance
	ctx.triangle(start, left, right, 5.0, Col.Gray)
	
	fill_percent = min(1.0, (ctx.time - cast_info.time_begin)/cast_info.cast_time)
	left  = start + dir.rotate_y(angle) * static.cast_cone_distance*fill_percent
	right = start + dir.rotate_y(-angle) * static.cast_cone_distance*fill_percent
	
	ctx.triangle_fill(start, left, right, Col(0.5, 0.5, 0.5, 0.5))
	

def draw_missile(ctx, missile):
	static = ctx.get_spell_static(missile.spell.static.parent)
	if static == None:
		return
		
	if static.has_flag(Spell.TypeLine):
		missile_draw_line(ctx, missile, static)

def draw_cast(ctx, champ):
	cast_info = champ.curr_casting
	if not cast_info or not cast_info.static:
		return
		
	static = cast_info.static
	if static.has_flag(Spell.TypeLine):
		cast_draw_line(ctx, cast_info, static)
	elif static.has_flag(Spell.TypeArea):
		cast_draw_area(ctx, cast_info, static)
	else:
		cast_draw_cone(ctx, cast_info, static)
	

def draw_spells(ctx):
	
	draw_cast(ctx, ctx.player)
	
	for missile in ctx.missiles:
		draw_missile(ctx, missile)
		
	
def valkyrie_exec(ctx) :	     
	
	draw_spells(ctx)

