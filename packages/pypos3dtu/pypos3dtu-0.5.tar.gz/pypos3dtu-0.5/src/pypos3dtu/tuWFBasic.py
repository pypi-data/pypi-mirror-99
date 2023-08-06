'''
Created on 8 déc. 2020

@author: olivier
'''
import unittest

from pypos3d.wftk.WFBasic import Point3d, Vector3d, TexCoord2f, existGeom, getOBJFile, LinePlaneInterSect,\
  FaceVisibility

class Test(unittest.TestCase):


  def setUp(self):
      pass


  def tearDown(self):
      pass

  def testPoint3dOps(self):
    # Vairous Init
    Orig = Point3d(0.0,0.0,0.0)
    Orig2 = Point3d(Orig)
    Orig3 = Point3d([0.1, 0.0, 0.0])
    
    Orig2.set( (50.0, 50.0, 50.0) )
    
    Orig2.scaleAdd(0.1, Orig3, Orig3)
    self.assertTrue( Orig2 == Point3d(0.11, 0.0, 0.0) )
    
    Orig2.set( 50.0, 50.0, 50.0 )
    
    self.assertEqual(Orig2[1], 50.0)
    
    Orig3 = Point3d.parseVector3d('')
    self.assertTrue( Orig3==None )
    Orig3 = Point3d.parseVector3d('0.1 0.0 0.0')
    
    self.assertTrue(Orig.isNull())
    self.assertFalse(Orig3.isNull())

    p0 = Orig + Point3d(1.0,1.0,1.0)
    self.assertEqual(p0.x, 1.0)
    p1 = Orig - Point3d(1.0,1.0,1.0)
    self.assertEqual(p1.x, -1.0)
    
    p0 = Orig + [1.0,1.0,1.0]
    self.assertEqual(p0.x, 1.0)
    p1 = Orig - [1.0,1.0,1.0]
    self.assertEqual(p1.x, -1.0)
    
    # Java like
    p0.add(Orig, Point3d(1.0,1.0,1.0))
    self.assertEqual(p0.x, 1.0)
    
    p1.sub(Orig, Point3d(1.0,1.0,1.0))
    self.assertEqual(p1.x, -1.0)

    p0.add((1.0,1.0,1.0), Orig)
    self.assertEqual(p0.x, 1.0)
    
    p1.sub((1.0,1.0,1.0), Orig)
    self.assertEqual(p1.x, 1.0)


    d = p0.distanceSquared(p1)
    self.assertEqual(d, 0.0)
    
    d = p0.distanceSquared([ 10.0, -5.0, 4.0 ])
    self.assertEqual(d, 126.0)
    
    s = p0.poserPrint()
    self.assertEqual(s, ' 1.00000000  1.00000000  1.00000000')

    Oz = Point3d.triangle_normal(Point3d(1.0,1.0,1.0), Point3d(2.0,1.0,1.0), Point3d(1.0,2.0,1.0) )
    self.assertEqual(Oz, Point3d(0.0,0.0,1.0))

    Oz = Point3d.triangle_raw_normal(Point3d(1.0,1.0,1.0), Point3d(2.0,1.0,1.0), Point3d(1.0,2.0,1.0) )
    self.assertEqual(Oz, Point3d(0.0,0.0,1.0))


  def testTexCoord2fOps(self):
    Orig = TexCoord2f(0.0,0.0)
    Orig2 = TexCoord2f(Orig)
    
    Orig2.set( (50.0, 50.0) )
    
    self.assertTrue(Orig==TexCoord2f(0.0,0.0))
    
    # Java like
    p0 = TexCoord2f()
    p0.add(Orig, TexCoord2f(1.0,1.0))
    self.assertEqual(p0.x, 1.0)
    
    p1 = TexCoord2f()
    p1.sub(Orig, TexCoord2f(1.0,1.0))
    self.assertEqual(p1.x, -1.0)

    p0.add((1.0,1.0,1.0), Orig)
    self.assertEqual(p0.x, 1.0)

    p0.add((1.0,1.0))
    self.assertEqual(p0.x, 2.0)
    
    p1.sub((1.0,1.0,1.0), Orig)
    self.assertEqual(p1.x, 1.0)

    p1.sub((1.0,1.0))
    self.assertEqual(p1.x, 0.0)

    p1.sub(TexCoord2f(5.0,5.0))
    self.assertEqual(p1.x, -5.0)
    
    p1.set(0.0, 100.0)
    p1.set(TexCoord2f(-1.0, -1.0))


  def testFileGeom(self):
    self.assertFalse( existGeom('srcdata/') )

    self.assertFalse( existGeom('srcdata/PoserRoot/Runtime/Geometries/phf.obz'))

    self.assertTrue( existGeom('srcdata/cube_gris.obj') )

    self.assertTrue( existGeom('srcdata/cube_gris.obz') )
    
    # Only in .obz
    self.assertTrue( existGeom('srcdata/PoserRoot/Runtime/Geometries/SbootsVic.obj') )
    
    
    #f = getOBJFile('srcdata/PoserRoot/Runtime/Geometries/phf.obz')
    f = getOBJFile('srcdata/cube_gris.obj')
    f = getOBJFile('srcdata/cube_gris.obz')
    f = getOBJFile('srcdata/PoserRoot/Runtime/Geometries/SbootsVic.obj')




  def testOtherMath(self):
    orig = Point3d(100.0,100.0,0.5)
    
    v, k = LinePlaneInterSect(Point3d(), Point3d(0.0,0.0,1.0), \
                              orig, orig+Vector3d(1.0,0.0,0.0), \
                              orig+Vector3d(0.0,1.0,0.0))
    print(str(v) + 'k='+str(k))
    self.assertEqual(v, Point3d(0.0,0.0,0.5))
    self.assertEqual(k, 0.5)

    try:
      v, k = LinePlaneInterSect(Point3d(), Point3d(0.0,5.0,0.0), \
                              orig, orig+Vector3d(1.0,0.0,0.0), \
                              orig+Vector3d(0.0,1.0,0.0))
      print(str(v) + 'k='+str(k))
    except RuntimeError as e:
      print("")

    v = FaceVisibility(None, Vector3d(1.0,0.0,0.0))
    self.assertTrue(v==0.0)




if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testPoint3dOps']
    unittest.main()