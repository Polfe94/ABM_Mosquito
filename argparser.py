import sys, getopt
import os
#import re
#import params

def print_help():
    print('\n')
    print('## HELP ---> IMPLEMENTED OPTIONS ##')
    print('\n')
    print('-f or --fit to change the parameters of the dispersion kernel')
    print('\tCall: Which fit should be used for the kernel? See options in params.py')
    print('\tExample: -f fit2 ("-f" followed by fit function name).')
    print('\n')
    print('-n or --runs to specify number of simulations to run')
    print('\tCall: How many simulations should be run?')
    print('\tExample: -n 1000 ("-n" followed by an integer).')
    print('\n')
    print('-p or --parallel to run simulations in parallel')
    print('\tCall: Should simulations be run in parallel?')
    print('\tExample: -p True ("-p" followed by a boolean)')
    print('\n')
    print('-x or --directory to set the name to save the results of the simulations')
    print('\tCall: Name of the output file?')
    print('\tExample: -x dispersion ("-x" followed by a string)')
    print('\n')
    print('-d or --filename to set the folder to which the results will be saved')
    print('\tCall: (Absolute or relative) path to folder to save output file?')
    print('\tExample: -d ~/simulation_results/ ("-d" followed by a string)')

def argparse(argv):

    wrng_msg_1 = 'Leaving default parameter value ...'
    wrng_msg_2 = 'Exiting program ...'
    
    try:

        if '-h' in argv or '--help' in argv:
            print_help()
            print(wrng_msg_2)
            sys.exit(0)

        opts, args = getopt.getopt(argv, 'f:n:p:d:x:h',
         ["fit=", "runs=", "parallel=", "directory=", "filename=", "--help="])

    except getopt.GetoptError:
        print('Something went wrong ! Try typing -h or --help to see possible parameters.')
        print(wrng_msg_2)
        sys.exit(1)

    for opt, arg in opts:

        if opt in ('-f', '--fit'):

            if(str(arg) in dir()):
                setattr(globals()['params'], 'fit', eval('params.'+str(arg)))
            else:
                print('Could not find the specified fit function.', wrng_msg_1)

        
        elif opt in ('-n', '--runs'):
            try:
                n = int(arg)
                setattr(globals()['params'], 'n_runs', n)
            except:
                print('Could not convert %s to integer!' % arg)
                print(wrng_msg_1)

        elif opt in ('-p', '--parallel'):

            try:
                b = eval(arg) == True

            except:
                b = None

            if b == True or b == False:
                setattr(globals()['params'], 'run_parallel', b)
                
            else:
                print('Evaluation of %s did not result in a boolean output.' % arg)
                print(wrng_msg_1)

        elif opt in ('-x', '--filename'):
            globals()['params'].file_name = arg

        elif opt in ('-d', '--directory'):

            setattr(globals()['params'], 'result_path', arg)
            if not os.path.exists(arg):
                print('Path (%s) does not exist.' % arg)
                print('Program will try to create a folder in the specified directory')

        else:

            if opt not in ('-h', '--help'):
                print('Specified parameter %s is unavailable.' % opt)

            print_help()
            print(wrng_msg_2)
            sys.exit(1)