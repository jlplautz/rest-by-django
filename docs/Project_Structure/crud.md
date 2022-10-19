# Criar um CRUD para BOOK
  - Criar um endpoint para que o usuario passa todo os campos para criar um livro.
  - vamos organizar um teste

  To create a book you need to send this payload (in json format) below:
    
    {
        "name": // Name of the book;
        "edition": // Edition number;
        "publication_year": // Publication year of the book;
        "authors": // List of author ids, same ids of previous imported data
    }

  Obs: Payload -> é a carga util que se esta enviando para algum lugar.
    Neste exemplo acima estamos encaminhando para o servidor os dados.

      Varios metodos (POST,PUT, PATCH), podem carregar payload no corpo da requisição
      - create -> method POST       (method HTTP)
      - read   -> method GET        (method HTTP)
      - update -> method PUT/PATCH  (method HTTP)  -> para atualizar um pagamento
      - delete -> method DELETE     (method HTTP)


## Test para criação do Livro(s)

[Django links para testes](https://docs.djangoproject.com/en/4.0/topics/testing/tools/)

[HTTP STATUS](https://www.httpstatus.com.br/)

