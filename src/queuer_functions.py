#
# import os
# def execute(command):
#     return os.popen(command).read()
#
# def queue(config, file_name, run_script='run', args=None):
#     job = config.name
#     a = execute('squeue')
#     if len(a) == 0 :
#         print('Something is wrong')
#         return
#     jobs = [q.strip(' ') for q in a.split('\n')[1:] if q.strip(' ')!='' and 'interacti {}'.format(job) in q]
#     if(len(jobs)>0):
#         print('Job with name {} is already running'.format(job))
#         return
#     output_location = config.results_dir+'/'+job
#     aviable = ''
#     aviable = '--exclude='
#     for i in range(10,25):
#         aviable+='landonia{},'.format(i)
#     aviable = aviable[:-1]
#     command = 'sbatch --job-name {0} --error=error-{0} --output=output-{0} {3} {2}.sh {1} '.format(job,file_name,run_script, aviable)
#
#     if args:
#         command +=args
#     print(command)
#     execute(command)
