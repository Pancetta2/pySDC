import numpy as np
from matplotlib import pyplot as plt

fs = 18
order  = np.array([])
nsteps = np.array([])
error  = np.array([])

file = open('conv-data.txt', 'r')
while True:
  line = file.readline()
  if not line: break
  items  = str.split(line, "    ", 3)
  order  = np.append(order,  int(items[0]))
  nsteps = np.append(nsteps, int(items[1]))
  error  = np.append(error,  float(items[2]))

print order
print nsteps
print error

assert np.size(order)==np.size(nsteps), 'Found different number of entries in order and nsteps'
assert np.size(nsteps)==np.size(error), 'Found different number of entries in nsteps and error'

N = np.size(nsteps)/3
assert isinstance(N, int), 'Number of entries not a multiple of three'

error_plot  = np.zeros((3, N))
nsteps_plot = np.zeros((3, N))
convline    = np.zeros((3, N))
order_plot  = np.zeros(3)

for ii in range(0,3):
  order_plot[ii] = order[3*ii]
  for jj in range(0,N):
    error_plot[ii,jj]  = error[3*ii+jj]
    nsteps_plot[ii,jj] = nsteps[3*ii+jj]
    convline[ii,jj]    = error_plot[ii,0]*(float(nsteps_plot[ii,0])/float(nsteps_plot[ii,jj]))**order[3*ii+jj]

color = [ 'r', 'b', 'g' ]
fig = plt.figure(figsize=(8,8))
for ii in range(0,3):
  plt.loglog(nsteps_plot[ii,:], error_plot[ii,:], 'o', markersize=12, color=color[ii], label='p='+str(int(order_plot[ii])))
  plt.loglog(nsteps_plot[ii,:], convline[ii,:], '-', color=color[ii])

plt.legend()
plt.xlabel(r'$N_t$')
plt.ylabel('Relative error')
plt.show()
