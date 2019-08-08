from jcamp import JCAMP_reader
import matplotlib.pyplot as plt
filename = './infrared_spectra/1-butanol.jdx'
jcamp_dict = JCAMP_reader(filename)
plt.plot(jcamp_dict['x'], jcamp_dict['y'])
plt.title(filename)
plt.xlabel(jcamp_dict['xunits'])
plt.ylabel(jcamp_dict['yunits'])

plt.show()


from sklearn import datasets
iris = datasets.load_iris()
digits = datasets.load_digits()
print(digits.data)
