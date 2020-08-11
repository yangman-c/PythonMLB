import numpy as np
arr = [[18.93, 19.16, 19.67, 18.46],[18.91, 18.93, 19.43, 18.53],[19.47, 19.48, 19.92, 19.06]]
m = np.array(arr)
print(np.round([np.sum(m[:, i])/3 for i in range(m.shape[1])], 2))