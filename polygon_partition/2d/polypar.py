from PyQt4 import QtCore, QtGui, QtOpenGL
from PyQt4.QtGui import QVector2D
from OpenGL import GL
from OpenGL import GLUT
import math
from collections import deque

class PolyPar:
	def __init__(self):
		self.verts = []
		self.indecies=[]
	def AddPoint(self,p):
		self.verts.append(p)
		self.rebuild_mesh()
	def Render(self):
		GL.glPointSize(5.0)
		GL.glBegin(GL.GL_POINTS)
		for p in self.verts:
			GL.glVertex2f(p.x(),p.y())
		GL.glEnd()
		if len(self.indecies)==0:return
		# GL.glBegin(GL.GL_TRIANGLES)
		GL.glPolygonMode(GL.GL_FRONT_AND_BACK,GL.GL_LINE)
		GL.glBegin(GL.GL_TRIANGLES)
		for cur_index in self.indecies:
			p = self.verts[cur_index]
			GL.glVertex2f(p.x(),p.y())
			# print cur_index
		GL.glEnd()

	def rebuild_mesh(self):
		self.indecies = []
		n=len(self.verts)
		max_val = 9999
		if n<3:	return
		# dp
		c=[[(max_val,-1) for j in range(n)] for i in range(n)]
		for i in range(n-1,-1,-1):
			for j in range(i+1,n):
				cur_len = (self.verts[i]-self.verts[j]).length()
				if abs(i-j)==1:
					c[i][j]=(cur_len,-2)
				else:
					if self.check_inner_diag(i,j):
						for k in range(i+1,j):
							cur_val = cur_len+c[i][k][0]+c[k][j][0]
							if cur_val<c[i][j][0]:
								c[i][j]=(cur_val,k)
		# bfs
		que = deque()
		que.append((0,n-1))
		while(len(que)>0):
			front_node = que.pop()
			p=front_node[0]
			q=front_node[1]
			if q==p+1: continue
			r = c[p][q][1]
			if r<0: continue
			self.indecies.extend([q,r,p])
			que.extend([(p,r),(r,q)])
		# self.rec_search_tris(c,0,n-1)
	# maybe can optimize
	def check_inner_diag(self,p,q):
		n = len(self.verts)
		if abs(p-q)==n-1: return True
		sign = None
		for r in range(n):
			if r==p or r==q: continue
			p0 = self.verts[r]
			p1 = self.verts[p]
			p2 = self.verts[q]
			y_on_line = (p0.x()-p1.x())*(p2.y()-p1.y())/(p2.x()-p1.x()) + p1.y()
			cur_sign = (y_on_line>p0.y())
			# print [p,r,q]
			# print cur_sign
			if sign !=None:
				if (sign>0) != cur_sign: 
					# print [p,r,q]
					# print "---------------------------"
					return True
			else:
				sign = cur_sign
		# print "---------------------------"
		return False
	def rec_search_tris(self,c,p,q):
		if q==p+1:return
		r = c[p][q][1]
		if r<0: return
		self.indecies.extend([q,r,p])
		self.rec_search_tris(c,p,r)
		self.rec_search_tris(c,r,q)

			




