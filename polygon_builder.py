import pygame
from pygame.locals import KEYDOWN, MOUSEBUTTONDOWN, K_BACKSPACE
from math import dist
from config import RED, GREEN, BLACK
from polygon_utils import segment_segment_intersect, is_ccw

class PolygonBuilder:
	
	EDGE_SIZE = 2
	VERTEX_SIZE = 3
	MAX_SNAP_DIST = 15

	def __init__(self, screen):
		self._polygon = []
		self._polygon_closed = False
		self._screen = screen

	def update(self, event):
		'Update the polygon based on the event'
		needs_draw = False
		if event.type == MOUSEBUTTONDOWN:
			pos = pygame.mouse.get_pos()
			self._add_vertex(pos)
			needs_draw = True
		elif event.type == KEYDOWN and event.key == K_BACKSPACE:
			self._delete_vertex()
			needs_draw = True

		if needs_draw:
			self._screen.fill(BLACK) # Clear screen
			self._draw_polygon()
			pygame.display.flip() # Update the display

	def get_polygon(self):
		'Return a list of tuples representing a ccw, closed polygon'
		if self._polygon_closed and not self._intersections():
			ret = self._polygon[:-1] # ignore duplicated last element
			return ret if is_ccw(ret) else ret[::-1]

	def _draw_polygon(self):
		'Draw polygon edges then vertices'
		inter = self._intersections()
		for i in range(len(self._polygon) - 1):
			edge_color = RED if i in inter else GREEN
			pygame.draw.line(self._screen, edge_color, self._polygon[i], self._polygon[i+1], PolygonBuilder.EDGE_SIZE)
		
		for p in self._polygon:
			pygame.draw.circle(self._screen, RED, p, PolygonBuilder.VERTEX_SIZE)

	def _add_vertex(self, pos):
		'Add a vertex to the polygon or close the polygon'
		if not self._polygon_closed and pos not in self._polygon:
			if len(self._polygon) >= 3 and dist(self._polygon[0], pos) <= PolygonBuilder.MAX_SNAP_DIST: 
				pos = self._polygon[0]
				self._polygon_closed = True
			self._polygon.append(pos)

	def _delete_vertex(self):
		'Delete the last added vertex'
		if self._polygon:
			del self._polygon[-1]
			self._polygon_closed = False

	def _intersections(self):
		'Return a set of edge indices that have intersections'
		n_edges = len(self._polygon) - 1

		idx = set()
		for i in range(n_edges):
			for j in range(i+2, n_edges):
				if not (self._polygon_closed and (j+1)%n_edges == i):
					seg1 = (self._polygon[i],self._polygon[i+1])
					seg2 = (self._polygon[j],self._polygon[j+1])
					if segment_segment_intersect(seg1, seg2):
						idx.add(i)
						idx.add(j)
		return idx
