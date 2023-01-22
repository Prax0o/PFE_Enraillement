import math

def get_2center(x0, y0, x1, y1):
  width = x1 - x0
  height = y1 - y0
  x = x0 + width / 2
  y = y0 + height / 2
  return x, y

def get_4points(x_center, y_center, width, height):
  x0 = x_center - width / 2
  y0 = y_center - height / 2
  x1 = x_center + width / 2
  y1 = y_center - height / 2
  x2 = x_center + width / 2
  y2 = y_center + height / 2
  x3 = x_center - width / 2
  y3 = y_center + height / 2
  return x0, y0, x1, y1, x2, y2, x3, y3

# Dessin des rails
def init_rails(height, thickness, canvas):
  canvas.create_line(0, height-thickness, 500, height-thickness, width=5)
  canvas.create_line(0, height+thickness, 500, height+thickness, width=5)

# Dessin de la route
def init_roads(width, thickness, canvas):
  canvas.create_line(width-thickness, 0, width-thickness, 500, width=2)
  canvas.create_line(width+thickness, 0, width+thickness, 500, width=2)

def rotate_point(x, y, center_x, center_y, angle_degre):
  radians = angle_degre * math.pi / 180
  x_rotated = (x - center_x) * math.cos(radians) - (y - center_y) * math.sin(radians) + center_x
  y_rotated = (x - center_x) * math.sin(radians) + (y - center_y) * math.cos(radians) + center_y
  return (x_rotated, y_rotated)

def rotate(polygon_id, angle, canvas):
  x0, y0, x1, y1, x2, y2, x3, y3 = canvas.coords(polygon_id)
  pt0, pt1, pt2, pt3 = [x0, y0], [x1, y1], [x2, y2], [x3, y3]
  x_center, y_center = get_2center(*pt0, *pt2)
  new_pt0 = rotate_point(*pt0, x_center, y_center, angle)
  new_pt1 = rotate_point(*pt1, x_center, y_center, angle)
  new_pt2 = rotate_point(*pt2, x_center, y_center, angle)
  new_pt3 = rotate_point(*pt3, x_center, y_center, angle)
  canvas.coords(polygon_id, *new_pt0, *new_pt1, *new_pt2, *new_pt3)

def move_forward(polygon, distance, angle):
  # Convert the angle to radians. 
  angle -= 90
  angle_rad = angle * math.pi / 180

  # Calculate the movement in the x and y directions.
  dx = distance * math.cos(angle_rad)
  dy = distance * math.sin(angle_rad)

  return (dx, dy)