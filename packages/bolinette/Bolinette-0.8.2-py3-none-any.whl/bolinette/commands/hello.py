from bolinette import Console
from bolinette.decorators import command


@command('hello', 'Says hello!')
@command.argument('argument', 'name', summary='Who I am greeting?')
async def hello(name: str):
    console = Console()
    console.print(f'Hello {name}!')
