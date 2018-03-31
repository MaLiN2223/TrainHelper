import csv
import glob
import os
results_dir = '/afs/inf.ed.ac.uk/user/s17/s1793872/Desktop/cw4_results/results_logs'
a = "rsync -avr --exclude '*.h5'  mlp1:/home/s1793872/cw4/results {}".format(results_dir)
os.popen(a)

print('Lets start')
print('searching for {}'.format(results_dir+'/**/*.log'))
for filename in glob.iglob(results_dir+'/**/*.log', recursive=True):
    if 'results_old' in filename:
        pass
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        print(filename.split('/')[-1])
        data = []
        for line in reader:
            data.append(dict(line))
        print(pd.DataFrame(data[0].items()))
