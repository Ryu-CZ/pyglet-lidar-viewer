'''
Created on Feb 23, 2014

@author: ryu_cz
'''
from vec3 import Vec3
from pyglet.gl import GLfloat, glViewport, gluPerspective, glMatrixMode, GL_MODELVIEW, GL_PROJECTION, glPushMatrix, glLoadIdentity, glRotatef, glTranslatef, glGetFloatv, GL_MODELVIEW_MATRIX, glPopMatrix

class Camera(object):
	
	def __init__(self, x=0, y=0, z=0, fi=0., psi=90.0, fovy = 60.0, radius = 10):
		"""Constructor of camera class
		@param x,y,z: position of eye
		@param psi: left/right orientation of camera (twist)
		@param fi: up-down orientation of camera
		@param fovy: field of view in y size of canvas
		@param radius: distance between camera and hepfull target point. Importatnt for zooming"""
		self._init_fi = fi
		self._init_psi = psi
		self._init_fovy = fovy
		self._init_radius = radius
		self.sensitivity = 0.1
		self._init_position = Vec3(x,y,z)
		self.modelview = (GLfloat * 16)()  #Holds current projection and modelview matrices
		self.reset()
	
	def zoom (self, dx, dy): 
		"""Zooms in/out camera in direction of viewer. only parameter dy is used here
		@param dy: number of 'clicks' to zoom
		"""
		self.radius -= self.radius * dy * 0.5 * self.sensitivity;
		self.radius = max(self.radius, 1)
	
	
	def rotate(self, dx, dy):
		"""Add angles to actual state of rotation
		@param dx: add angle to fi angle (left/right)
		@param dy: add angle psi angle (up/down)"""
		self.fi += dx * self.sensitivity
		self.psi += dy * self.sensitivity

	def up(self, distance):
		"""Move camera up
        @param distance: distance to move"""
		self.position.z +=self.radius *distance* 5 * self.sensitivity

	def move(self, dx, dy):
		"""Moves with camer in left/right and forward/backward direction from point of viewer
		@param dx: moves in righ/left direction
		@param dy: moves in forward/backward direction"""
		cameraDX = self.radius * dx *5* self.sensitivity
		cameraDY = self.radius * dy *5* self.sensitivity
		glMatrixMode(GL_MODELVIEW)# GL_MODELVIEW_MATRIX
		glPushMatrix()
		glLoadIdentity()
		glRotatef(-self.fi, 0, 0, 1)
		glTranslatef(cameraDX, cameraDY, 0)
		glRotatef(self.fi, 0, 0, 1)
		self.modelview = (GLfloat * 16)()
		glGetFloatv(GL_MODELVIEW_MATRIX, self.modelview)
		self.position.x += self.modelview[12]
		self.position.y += self.modelview[13] 
		self.position.z += self.modelview[14]
		glPopMatrix()
	
	def zoomAndRotate(self):
		"""Performs zooming and rotation. Suggested to use with pan during displazing the scene:
		1.cam.zoomAndRotate()
		2.cam.pan()
		3.draw(some 3D objects)
		"""
		glTranslatef(0, 0, -self.radius)
		glRotatef(self.psi - 90, 1, 0, 0)
		glRotatef(self.fi, 0, 0, 1)
	
	def pan(self):
		"""Performs panning (translation). Suggested to use with pan during displazing the scene:
		1.cam.zoomAndRotate()
		2.cam.pan()
		3.draw(some 3D objects)
		"""
		glTranslatef(-self.position.x, -self.position.y, -self.position.z)
	
	def focus(self, width, height):
		"""Sets the projection matrix. Usefull for window.on_resize event
		@param width: width of resized window
		@param height: height of resized window"""
		self.width = width
		self.height = height
		glViewport(0, 0, width, height)
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		aspect = width/float(height)
		gluPerspective(self.fovy, aspect, 0.01, 1024.0 )
	
	def reset(self):
		"""Reset values of fi, psi, fovy, radius and position of camera to init values, passed in constructor."""
		self.fi = self._init_fi
		self.psi = self._init_psi
		self.fovy = self._init_fovy
		self.radius = self._init_radius
		self.sensitivity = 0.1
		self.position = self._init_position
		self.modelview = (GLfloat * 16)()
        
if __name__ == '__main__':
    print "\ncamera says: Hi I am module camera.\n"