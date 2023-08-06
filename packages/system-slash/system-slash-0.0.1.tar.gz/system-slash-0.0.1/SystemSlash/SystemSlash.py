import platform

#This programe is create by Sujit Mandal
# Github: https://github.com/sujitmandal
# Pypi : https://pypi.org/user/sujitmandal/
# LinkedIn : https://www.linkedin.com/in/sujit-mandal-91215013a/


def slash():

    if platform.system() == 'Linux':
        system = '/'
    elif platform.system() == 'Windows':
        syste = ' \ '
        system = syste.strip()

    print(system)
    return(system)

if __name__ == "__main__":
    slash()