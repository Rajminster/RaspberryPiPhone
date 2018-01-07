def func(array):

  def flipNorm(i):
    if 0 <= i <= 0.5:
      return (False,0)               # no penalty
    elif 0.5 <= i <= 1:
      return (True,0)    
    else:
      return (False,math.log(math.abs(i.item()))      # log-barrier penalty

  def rotateNorm(i):
    if 0 <= i < 1:
      return (0,0)
    elif 1 <= i < 2:
      return (1,0)
    elif 2 <= i < 3:
      return (2,0)
    elif 3<= i < 4:
      return (3,0)
    else:
      return (0,math.log(math.abs(i.item()))          # log-barrier penalty

  flipIndex   = range(3,45,5)
  rotateIndex = range(4,45,5)

  flip = np.vectorize(flipNorm)
  rotate = np.vectorize(rotateNorm)

  flipP = flip(array[flipIndex])
  flipSeparate = zip(*flipP)
  flipArray = list(flipSeperate[0])
  flipPenalties = np.sum(list(flipSeperate[1]))

  rotateP = rotate(array[rotateIndex])
  rotateSeparate = zip(*rotateP)
  rotateArray = list(rotateSeperate[0])
  rotatePenalties = np.sum(list(rotateSeperate[1]))

  list_of_bodies = [
    audioAmp(    array[ 0:3 ].tolist(),flipArray[0],rotateArray[0]),
    camera(      array[ 5:8 ].tolist(),flipArray[1],rotateArray[1]),
    powerBoost(  array[10:13].tolist(),flipArray[2],rotateArray[2]),
    speaker(     array[15:18].tolist(),flipArray[3],rotateArray[3]),
    screen(      array[20:23].tolist(),flipArray[4],rotateArray[4]),
    screenDriver(array[25:28].tolist(),flipArray[5],rotateArray[5]),
    piZero(      array[30:33].tolist(),flipArray[6],rotateArray[6]),
    battery(     array[35:38].tolist(),flipArray[7],rotateArray[7]),
    gsmChip(     array[40:43].tolist(),flipArray[8],rotateArray[8])]

  body = functools.reduce(lambda x,y: x + y,list_of_bodies)
  [xmin,xmax,ymin,ymax,zmin,zmax] = boundaryBox(body)
  volume = (xmax - xmin)*(ymax - ymin)*(zmax - zmin)

  return np.sum(np.array([volume,flipPenalties,rotatePenalties]))
