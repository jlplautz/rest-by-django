# Um descrição dos testes que foram criados

## 1- test_views.py

#### Primeiro teste  😀 response.status_code

   - Inicialmente o teste foi iniciado com a verificação do status_code da URL.
   Foi usado um Client do pytest para elaborar o teste. Usamos a função -> *client.get(resolve_url('core:list-authors'))* 


#### Segundo teste 😀 test_list_all_authors 
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

#### Terceiro teste 😀 fazer paginação
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
   - Boa pratica. Para garantir uma paginação consistente os queryset devem ser ordenados. Portanto vamos definir um Class Meta no modelo (deixando ordenado poelo name)
   - teste para  verificar o numero de paginas.
   ```  assert response.json()['num_pages'] == 2 ```

   - com estes testes podemos garantir que o endpoint da apĺicação esta funcionando