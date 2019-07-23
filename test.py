from jcamp import JCAMP_reader
import matplotlib.pyplot as plt
filename = './ftirdb/data/infrared_spectra/acetone.jdx'
jcamp_dict = JCAMP_reader(filename)
plt.plot(jcamp_dict['x'], jcamp_dict['y'])
plt.title(filename)
plt.xlabel(jcamp_dict['xunits'])
plt.ylabel(jcamp_dict['yunits'])
plt.savefig('./ftirdb/static/fig.png')
