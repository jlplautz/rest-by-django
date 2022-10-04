# Procedimento como implementar um command

## Link na documentação Django 
[django-admin commands](https://docs.djangoproject.com/en/4.0/howto/custom-management-commands/#django.core.management.BaseCommand.create_parser)


## Estrutura de diretório para implmentação do command

    ├── core
        ├── __init__.py
            ├── management
                ├── commands
                │   ├── import_authors.py
                │   └── __init__.py
                └── __init__.py

## Conteudo do arquivo import_authors.py

    import argparse
    import csv
    from django.core.management.base import BaseCommand
    from pyprg.core.models import Author

    class Command(BaseCommand):
        help = 'importa os autores a partit de csv'

        def add_arguments(self, parser):
            parser.add_argument('csv', type=argparse.FileType('r'))

        def handle(self, *args, **options):
            with options['csv'] as f:
                reader = csv.reader(f)
                next(reader)

                batch = []
                count = 0

                # fazer leitura linha a linha do arquivo
                for row in reader:
                    batch.append(Author(name=row[0]))
                    count += 1

                    # gravar o batch com 10.000 linhas
                    if len(batch) == 10_000:
                        Author.objects.bulk_create(batch)
                        batch.clear()
                        self.stdout.write(f'{count} Dados Inportados')
                # Gravar o batch caso tenha menos que 10.000 linhas
                if batch:
                    Author.objects.bulk_create(batch)
                    self.stdout.write(f'{count} Dados Inportados')


## Depois de criar a class Command podemos verificar 

### Função para criar o arquivo de autores.


    import csv

    def main():

        with open('authors2.cvs', 'w') as f:
            writer = csv.DictWriter(f, fieldnames=['name'])
            for i in range(1_500_00):
                writer.writerow({'name':f'Author {i}'})

    if __name__ == '__main__':
        main()

### Procedimento para fazer o import do arquivo de autores

    - $ python manage.py          

      Type 'manage.py help <subcommand>' for help on a specific subcommand.
      [core]
          import_authors

    - ╰─$ python manage.py import_authors --help
      usage: manage.py import_authors [-h] [--version] [-v {0,1,2,3}]
                                  [--settings SETTINGS] [--pythonpath PYTHONPATH]
                                  [--traceback] [--no-color] [--force-color]
                                  [--skip-checks]

         optional arguments:
          -h, --help            show this help message and exit
          --version             Show program's version number and exit.
          -v {0,1,2,3}, --verbosity {0,1,2,3}
                          Verbosity level; 0=minimal output, 1=normal output,
                          2=verbose output, 3=very verbose output
          --settings SETTINGS   The Python path to a settings module, e.g.
                          "myproject.settings.main". If this isn't provided, the
                          DJANGO_SETTINGS_MODULE environment variable will be
                          used.
          --pythonpath PYTHONPATH
                          A directory to add to the Python path, e.g.
                          "/home/djangoprojects/myproject".
          --traceback           Raise on CommandError exceptions.
          --no-color            Don't colorize the command output.
          --force-color         Force colorization of the command output.
          --skip-checks         Skip system checks.

## Para fazer a leitura do arquivo csv que esta na raiz do projeto
  - mng import_authors authors.csv

        def handle(self, *args, **options):
            with options['csv'] as f:
                reader = csv.reader(f)
                next(reader)

                Author.objects.bulk_create((Author(name=row[0]) for row in reader), batch_size=5_000)
            
            self.stdout.write('Dados importados')

   - next(reader) -> pula uma linha que é a linha que tem 'name'
   - batch_size=5_000 -> grava de uma unica vez com 5000 regs.
   
   
## Para visualizar o ultimo regitro no banco usar a url

    http://localhost:8000/api/authors/?q=Author%201499999


## Entrar via manage shell e deletar os registro de Authors

    - acessar via manage shell -> mng shell
    - from pyprg.core.core.models importt Author
    - Author.objects.all().delete()