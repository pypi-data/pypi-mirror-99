import os
import click


@click.group()
@click.version_option("0.1.1")
def main():
    pass

@main.command()
@click.option("-np", default=4, required=True)
@click.option("-data", required=True)
@click.option("-out", default="fastgwr_rslt.csv", required=False)
@click.option("-adaptive/-fixed" ,default=True, required=True)
@click.option("-constant", required=False, is_flag=True)
@click.option("-bw", required=False)
@click.option("-minbw", required=False)
@click.option("-chunks", required=False)
@click.option("-mgwr", default=False, required=False, is_flag=True)
def run(np, data, out, adaptive, constant, bw, minbw, mgwr, chunks):
    """Fast(M)GWR"""
    command = 'mpiexec ' + ' -np ' + str(np) + ' python ' + ' fastgwr/fastgwr_mpi.py ' + ' -data ' + data + ' -out ' + out
    if mgwr:
        command += ' -mgwr '
    
    if adaptive:
        command += ' -a '
    else:
        command += ' -f '
    if bw:
        command += (' -bw ' + bw)
    if minbw:
        command += (' -minbw ' + minbw)
    if constant:
        command += ' --constant '
    if chunks:
        command += (' -chunks ' + chunks)
        
    os.system(command)
    pass


@main.command()
def testmgwr():
    print("Testing MGWR:")
    command = "mpiexec -np 4 python fastgwr_mpi.py -data ../Zillow-test-dataset/zillow_1k.csv -c -mgwr"
    os.system(command)
    pass
    
    
@main.command()
def testgwr():
    print("Testing GWR:")
    command = "mpiexec -np 4 python fastgwr_mpi.py -data ../Zillow-test-dataset/zillow_1k.csv -c"
    os.system(command)
    pass
    

if __name__ == '__main__':
    main()
