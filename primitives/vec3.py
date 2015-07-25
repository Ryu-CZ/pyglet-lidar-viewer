'''
Created on Feb 22, 2014

@author: ryu_cz
'''

class Vec3(object):
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
 
    def __str__(self):
        return '(%0.4f, %0.4f, %0.4f)' % (self.x, self.y, self.z)
 
    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)
 
    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)
 
    def __mul__(self, f):
        return Vec3(self.x * f, self.y * f, self.z * f)
 
    def __repr__(self):
        return 'Point(%0.8f, %0.8f, %0.8f)' % (self.x, self.y, self.z)
 
    def dot_prod(self, other):
        return self.x*other.x + self.y*other.y + self.z*other.z
 
    def uv(self):
        return Vec3(self.x/self.magnitude(), self.y/self.magnitude(), self.z/self.magnitude())
 
    def cross_prod(self, other):
        return Vec3(self.y*other.z - self.z*other.y, self.z*other.x - self.x*other.z, self.x*other.y - self.y*other.x)
 
    def magnitude(self):
        return (self.x**2 + self.y**2 + self.z**2)**0.5
    
    def length(self):
        return (self.x**2 + self.y**2 + self.z**2)**0.5
    
    def normalize(self):
        reduct = 1.0/self.length()
        self.x *= reduct
        self.y *= reduct
        self.z *= reduct
        
if __name__ == '__main__':
    print "\nVec3 says: Hi I am module vec3.\n"