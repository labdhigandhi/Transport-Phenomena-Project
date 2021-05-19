
def fd1d_heat_explicit_alpha ( k, t_num, t_min, t_max, x_num, x_min, x_max ):
  from sys import exit
  x_step = ( x_max - x_min ) / ( x_num - 1 )
  t_step = ( t_max - t_min ) / ( t_num - 1 )
  alpha = k * t_step / x_step / x_step
  if ( 0.5 < alpha ):
    print ( '' )
    print ( 'FD1D_HEAT_EXPLICIT_alpha - Fatal error!' )
    print ( '  alpha condition failed.' )
    print ( '  0.5 < K * dT / dX / dX = %f' % ( alpha ) )
    exit ( 'FD1D_HEAT_EXPLICIT_alpha - Fatal error!' )
  return alpha
def fd1d_heat_explicit ( x_num, x, t, dt, alpha, bc, h ):
  import numpy as np
  h_new = np.zeros ( x_num )
  for c in range ( 1, x_num - 1 ):
    l = c - 1
    r = c + 1
    h_new[c] = h[c] + alpha * ( h[l] - 2.0 * h[c] + h[r] )
  h_new = bc ( x_num, x, t + dt, h_new, h[1] )
  return h_new
def fd1d_heat_explicit_test ( ):
  import matplotlib.pyplot as plt
  import numpy as np
  import platform
  from mpl_toolkits.mplot3d import Axes3D
  from matplotlib import cm
  from matplotlib.ticker import LinearLocator, FormatStrFormatter
  print ( '  one dimensional heat equation:' )
  print ( '' )
  print ( '    dH/dt - K * d2H/dx2 = 0' )
  print ( '' )
  k = 1.5*(10**(-6))
  x_num = 5
  x_min = 0.0
  x_max = 0.12
  dx = ( x_max - x_min ) / ( x_num - 1 )
  x = np.linspace ( x_min, x_max, x_num )
  t_num = 10
  t_min = 0.0
  t_max = 45*60
  dt = ( t_max - t_min ) / ( t_num - 1 )
  t = np.linspace ( t_min, t_max, t_num )
  alpha = fd1d_heat_explicit_alpha ( k, t_num, t_min, t_max, x_num, x_min, x_max )
  print ( '' )
  print ( '  Number of X nodes = %d' % ( x_num ) )
  print ( '  X interval is [%f,%f]' % ( x_min, x_max ) )
  print ( '  X spacing is %f' % ( dx ) )
  print ( '  Number of T values = %d' % ( t_num ) )
  print ( '  T interval is [%f,%f]' % ( t_min, t_max ) )
  print ( '  T spacing is %f' % ( dt ) )
  print ( '  Constant K = %g' % ( k ) )
  print ( '  alpha = %g' % ( alpha ) )
  hmat = np.zeros ( ( x_num, t_num ) )
  for j in range ( 0, t_num ):
    if ( j == 0 ):
      h = ic_test ( x_num, x, t[j] )
      h = bc_test ( x_num, x, t[j], h , h[1])
    else:
      h = fd1d_heat_explicit ( x_num, x, t[j-1], dt, alpha, bc_test, h )
    for i in range ( 0, x_num ):
      hmat[i,j] = h[i]
  tmat, xmat = np.meshgrid ( t, x )
  fig = plt.figure ( )
  ax = Axes3D ( fig )
  surf = ax.plot_surface ( xmat, tmat, hmat )
  plt.xlabel ( '<---X--->' )
  plt.ylabel ( '<---Time--->' )
  plt.title ( 'Temperature' )
  plt.savefig ( 'plot_test01.png' )
  plt.show ( block = False )
  r8mat_write ( 'h_test01.txt', x_num, t_num, hmat )
  r8vec_write ( 't_test01.txt', t_num, t )
  r8vec_write ( 'x_test01.txt', x_num, x )
  print ( '' )
  print ( '  H(X,T) written to "h_test01.txt"' )
  print ( '  T values written to "t_test01.txt"' )
  print ( '  X values written to "x_test01.txt"' )
  print('Temperature Matrix :- ')
  print(hmat)
  print ( '' )
  return
def bc_test ( x_num, x, t, h ,m):
  h[0]       = m
  h[x_num-1] = 20.0
  return h
def ic_test ( x_num, x, t ):
  import numpy as np
  h = np.zeros ( x_num )
  for i in range ( 0, x_num ):
    h[i] = 85.0
  return h
def r8mat_write ( filename, m, n, a ):
  output = open ( filename, 'w' )
  for i in range ( 0, m ):
    for j in range ( 0, n ):
      s = '  %g' % ( a[i,j] )
      output.write ( s )
    output.write ( '\n' )
  output.close ( )
  return
def r8mat_write_test ( ):
  import numpy as np
  import platform
  print ( '' )
  print ( 'R8MAT_WRITE_TEST:' )
  print ( '  Python version: %s' % ( platform.python_version ( ) ) )
  print ( '  Test R8MAT_WRITE, which writes an R8MAT to a file.' )
  filename = 'r8mat_write_test.txt'
  m = 5
  n = 3
  a = np.array ( (  \
    ( 1.1, 1.2, 1.3 ), \
    ( 2.1, 2.2, 2.3 ), \
    ( 3.1, 3.2, 3.3 ), \
    ( 4.1, 4.2, 4.3 ), \
    ( 5.1, 5.2, 5.3 ) ) )
  r8mat_write ( filename, m, n, a )
  print ( '' )
  print ( '  Created file "%s".' % ( filename ) )
  print ( '' )
  return
def r8vec_write ( filename, n, a ):
  output = open ( filename, 'w' )
  for i in range ( 0, n ):
    s = '  %g\n' % ( a[i] )
    output.write ( s )
  output.close ( )
  return
def r8vec_write_test ( ):
  import numpy as np
  import platform
  print ( '' )
  print ( 'R8VEC_WRITE_TEST:' )
  print ( '  Python version: %s' % ( platform.python_version ( ) ) )
  print ( '  Test R8VEC_WRITE, which writes an R8VEC to a file.' )
  filename = 'r8vec_write_test.txt'
  n = 5
  a = np.array ( ( 1.1, 2.2, 3.3, 4.4, 5.5 ) )
  r8vec_write ( filename, n, a )
  print ( '' )
  print ( '  Created file "%s".' % ( filename ) )
  print ( '' )
  return
if ( __name__ == '__main__' ):
  fd1d_heat_explicit_test ( )

