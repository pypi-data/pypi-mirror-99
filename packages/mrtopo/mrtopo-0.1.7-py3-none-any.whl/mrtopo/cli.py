import click
from mrtopo.__main__ import main_routine, validate_routine, test_routine, analyze_routine
from mrtopo.util.filetype import FileType

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group()
def cli():
    '''
    MrTopo is a python application that generates mutant Mininet topology files for network testing purposes.
    To get information on specific subcommands, use `mrtopo [COMMAND] --help`.
    '''
    pass


@click.group()
def mutator():
    '''
    MrTopo mutator
    '''
    pass


@click.command()
@click.option('-f', '--file', type=str, required=True, help="Python file that MrTopo should mutate.")
@click.option('-n', '--number-of-mutations', type=int, help="Number of mutations MrTopo should generate (default = 30)")
def python_file(file, number_of_mutations):
    '''
    Mutate a Mininet python file.
    '''
    if file != "":
        main_routine((file, FileType.PYTHON), number_of_mutations)


@click.command()
@click.option('-f', '--file', type=str, required=True, help="MrTopo config file.")
def config_file(file):
    '''
    Generate mutations from a configuration file.
    '''
    if file != "":
        click.echo("This option has not been implemented yet!")


@click.group()
def validator():
    pass


@click.command()
@click.option('-f', '--file', type=str, required=True, help="Validate a Mininet topology python file.")
@click.option('-t', '--topology-name', type=str, default=None,
              help="Name of topology found in python file.\nExample: \'topos = { 'someName': ... } - someName would "
                   "be the topology-name. Only use this option if you know the topology name.")
@click.option('--long/--not-long', default=False,
              help="Long test flag (i.e. pingall)")
def validate_file(file, topology_name, long):
    '''
    Validate a Mininet topology python file.
    '''
    if file != "":
        validate_routine((file, FileType.PYTHON), topology_name, long)


@click.command()
@click.option('-d', '--dir', type=str, required=True, help="Validate a directory of Mininet topologies.")
@click.option('-t', '--topology-name', type=str, default=None,
              help="Name of topology found in python file.\nExample: \'topos = { 'someName': ... } - someName would "
                   "be the topology-name. Only use this option if you know that all python files in the specified dir"
                   " follow the topology name given.")
@click.option('--long/--not-long', default=False,
              help="Long test flag (i.e. pingall)")
def validate_dir(dir, topology_name, long):
    '''
    Validate a directory of Mininet topologies.
    '''
    if dir != "":
        validate_routine((dir, FileType.DIRECTORY), topology_name, long)


@click.group()
def tester():
    pass


@click.command()
@click.option('-d', '--dir', type=str, required=True, help="A directory of Mininet topologies.")
@click.option('-tf', '--target-file', type=str, required=True,
              help="Name of file that MrTopo mutated and should substitute out during testing.")
@click.option('-cf', '--command-file', type=str, required=True,
              help="Bash file that contains ONOS testing commands to execute.")
def test_mutation_dir(dir, target_file, command_file):
    '''
    Test a mutated set of networks (directory) against a given Mininet topology file.
    '''
    if dir != "" and target_file != "" and command_file != "":
        test_routine(dir, target_file, command_file)


@click.command()
@click.option('-f', '--file', type=str, required=True, help="Python file that MrTopo should mutate.")
@click.option('-cf', '--command-file', type=str, required=True,
              help="Bash file that contains ONOS testing commands to execute.")
@click.option('-n', '--number-of-mutations', type=int, help="Number of mutations MrTopo should generate (default = 30)")
def mutate_and_test(file, command_file, number_of_mutations):
    '''
    Mutate and Test a Mininet Topology file.
    '''
    if file != "":
        main_routine((file, FileType.PYTHON), number_of_mutations)

    test_routine("MrTopoGenerated/", file, command_file)


@click.group()
def analyzer():
    pass


@click.command()
@click.option('-mf', '--mutation-file', type=str, required=True,
              help="Description file found in MrTopoGenerated directory `desc.txt`.")
@click.option('-rf', '--results-file', type=str, required=True,
              help="Test results file found in MrTopoTest directory `test.txt`.")
def analyze(mutation_file, results_file):
    '''
    Analyze given results from a topology mutation and the tests run.
    '''
    if mutation_file != "" and results_file != "":
        analyze_routine(mutation_file, results_file, 1)


# build mutator
mutator.add_command(python_file)
mutator.add_command(config_file)

# build validator
validator.add_command(validate_file)
validator.add_command(validate_dir)

# build tester
tester.add_command(test_mutation_dir)
tester.add_command(mutate_and_test)

# build analyzer
analyzer.add_command(analyze)

# build cli
cli = click.CommandCollection(sources=[mutator, validator, tester, analyzer])

# DEBUG

if __name__ == '__main__':
    cli()
