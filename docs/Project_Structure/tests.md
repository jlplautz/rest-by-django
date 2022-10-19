# Um descrição dos testes que foram criados

## 1- test_views.py

#### Primeiro teste response.status_code

   - Inicialmente o teste foi iniciado com a verificação do status_code da URL.
   Foi usado um Client do pytest para elaborar o teste. Usamos a função -> *client.get(resolve_url('core:list-authors'))* 


#### test_list_all_authors 
   - Este teste mais focado na API. Teste com resposta json com uma lista [id, nome autores ]
   - Interessante: a pratica definine que um recurso de uma API deve ter um identificador < id > 
   - no file models foi implementado a função to_dict -> representação do object como DICT
   - existe outra forma de implementar seria usar um method encoder (transforma um obj em um DICT )
   - django tem tem o [json encoder](https://docs.djangoproject.com/en/4.1/topics/serialization/)
   - a função foi decorada @pytest.mark.django_db -> feature do pytest
   - na views foi feito uma query -> authors = [a.to_dict() for a in Author.objects.all()]
   - no return da view a lista de autores é  transformada em um json com  
      ```HttpResponse(json.dumps(authors), content_type='application/json')```
   - podemos retornar na view com com safe=False -> evitando assim de gerar um resposta duvidosa da API
      ```return JsonResponse(authors, safe=False)```

#### teste fazer paginação
   - from django.core.paginator import Paginator
   - na views importar o django.core.paginator import Paginator
   - [django pagination](https://simpleisbetterthancomplex.com/tutorial/2016/08/03/how-to-paginate-with-django.html) 
   - [django paginator](https://docs.djangoproject.com/en/4.0/ref/paginator/)
   - na função authors a variavel page vai receber da url o num da pagina, sendo default o valor 1
   - definir a constante DEFAULT_PAGE_SIZE = 25
   - criado o obj Paginator que vai receber o queryset Author_objects.all() e a qtdade de registros por pagina
   - o paginator apresenta o numero da pagina
   - agora alteramos para retornar somente os registros que temos na pagina
   - no retorno da função teremos:
      - os registros por pagina
      - Total  de registros
      - Pagina corrente
      - Num_de_pagina
   - No teste vamos criar 10 authors, com objects.bulk_create
   - vamos fazer o teste com a segunda pagina com os 5 ultimos registros, se o nome dentro da lista esta corretos
   - Boa pratica. Para garantir uma paginação consistente os queryset devem ser ordenados. Portanto vamos definir um Class Meta no modelo (deixando ordenado pelo name)
   - teste para  verificar o numero de paginas.
   
   ```  assert response.json()['num_pages'] == 2 ```

   - com estes testes podemos garantir que o endpoint da apĺicação esta funcionando


#### teste fazer buscar do author pelo nome

   - Criar dois autores e esperar que somente o registro com o nome sugerido na busca seja retornado
   - na views.py precisa implementar

         name = request.GET.get('name')

         queryset = Author.objects.all()
         if name:
            queryset = queryset.filter(name__icontains=name)

         paginator = Paginator(queryset, per_page=page_size)

   - O pytest tem um marcador que marca tudo, dispensando o uso do    
   DECORADOR para marcar os testes
     ``` pytestmark = pytest.mark.django_db ```

   Portanto todos os testes neste modulos serão marcados com django_db

   - Um ponto importante que o Django cria um banco de dados temporário para cada teste.

   - fazer os teste via url. para ver se esta funcional
     - http://127.0.0.1:8000/api/authors/?page_size=2
     - http://127.0.0.1:8000/api/authors/?page_size=2&page=3
     - http://127.0.0.1:8000/api/authors/?q=Luciano



#### test create a book


#### test read a book

   - para ler um livro precisamos ter um livro criado
   - criado o livro podemos acessar o livro com method get com id do livro
   - na views a função read_book tems que inserir o parametro PK
   - na view temos que buscar o livro com o (pk=pk)
      
         book = Book.objects.get(pk=pk)

   - na view temos que retorna  um JsonResponse(book.to_dict())


#### test read a book doesn't exist
   - Não precisa cria livro para este teste
   - buscar um livro por um id que não exista
   - temos uma resposta padrão "404_Not_Found"
   - na view temos que fazer a tratativa

         try:
            book = get_object_or_404()
         except Book.DoesNotExist:
            return HttpResponseNotFound()
   
   - get_object_or_404 pede a classe Book e passamos os filtros pk=pk como parametro nomeado


#### test book update
   - fazer um requisição para atualisar um recurso, o method que faz mais sentido PUT 
   - usando o method PUT temos que mandar a representação completa do recurso (todos os campos), Enqunato o metjhod Patch -> podemos mandar somente o campo especifico para ser alterado.
   - encaminhamos a requisição para o mesmo endpoint (recurso livro com id)
   - depois da requisição for tratada em caso de sucesso temos:
     - 200 OK - melhor retornar o recurso atualizado (objecto)
     - 204 No Content - (mas sem conteudo retornado na resposta)
   - tem que inserir a alteração no data -> edition=3  e publication_yer=2024
   - na view a função book_read(request, pk) faz a tratativa da busca do livro
   - na view vamos alterar a função para book_read_update_delete()
   - na view capturamos o payload e o book é atualizado e retornamos book.to_dict()

   - pytest --lf (last fail) pytest vai executar o ultimo teste que falhou

   - na updade do livro vamos criar mai um author. observamos que o author antigo é desvinculado


#### test book update que não existe
   - teste para update de um livro que não existe, não precisa se quer inserir data
   - esperamos um 404 



#### test book delete 
   - precisamos ter um livro criado pata poder deletar
   - montmos um requisição

      response = client.delete(f'/api/books/{book.id}')

   - esperamos receber um 204_No_Content. pois o recurso foi deletado


#### test book delete que  não existe
   - teste para deletar um livro que não existe, não precisa se quer inserir data
   - esperamos um 404 (NOT_FOUND)


#### Alteração da função book_read_update_delete
   - como a função book_read_update_delete estava com muitas funçoes
     alteramos para um manuseio melhor
   - a função agora faz a query do livro, pois todas as açoes depende de um livro
   - depois repassamos a requisição e o livro para cada sub-função

      def book_read_update_delete(request, pk):
         book = get_object_or_404(Book, pk=pk)

         handlers = {
            'GET': _book_read,
            'PUT': _book_update,
            'DELETE': _book_delete
         }
         try:
            handler = handlers[request.method]
         except KeyError:
            return HttpResponseNotAllowed()
   
         return handler(request, book)



#### Test list_books(client)
   - um requisição com get com somente o url do endpoint client.get('/api/books/')
   - a resposta tem que ser um ok
   - precisa ter pelo meno um livro criado
   - iniciamos trazendo todos os livros, muito embora fica dificil caso existe muitos
   - Correto seria paginar
   