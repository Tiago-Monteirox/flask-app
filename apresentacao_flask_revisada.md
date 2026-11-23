## Visão geral

## Divisão por participante

| Slide | Conteúdo | Responsável |
| --- | --- | --- |
| 1 | Abertura e apresentação do grupo | Emili |
| 2 | O que é Flask e como surgiu | Gabriel |
| 3 | Caminho de uma requisição | Gabriel |
| 4 | Vantagens e limitações | Igor |
| 5 | Comparação entre Flask, Django e FastAPI | Igor |
| 6 | Projeto prático: Agenda REST | Tiago Monteiro |
| 7 | Organização e explicação do `app.py` | Tiago Monteiro |
| 8 | Demonstração ao vivo | Tiago Monteiro |
| 9 | Dificuldades e aprendizados | Igor |
| 10 | Conclusão e referências | Gabriel e Tiago |

## Slide 1 — Emili

### Flask: do conceito à API

### Flask: do conceito à API

> Boa noite.
>
> Nosso tema é o Flask, um microframework utilizado para desenvolver aplicações web com Python.
>
> Durante a apresentação, vamos explicar o que é Flask, como ele processa uma requisição, suas vantagens e limitações e como ele se compara com Django e FastAPI.
>
> Depois dessa parte conceitual, o Tiago vai apresentar o projeto prático desenvolvido pelo grupo: uma API REST para gerenciar eventos de uma agenda. Ele também vai explicar o código e fazer uma demonstração ao vivo.
>
> Para começar, o Gabriel vai explicar o que é Flask e como esse framework surgiu.

---

## Slide 2 — Gabriel

### O que é o Flask?

> Flask é um microframework web de código aberto para Python, criado por Armin Ronacher e lançado em 2010.
>
> Sua origem está relacionada ao denied, um pequeno framework apresentado inicialmente como uma brincadeira de 1º de abril. A ideia recebeu atenção e, pouco tempo depois, evoluiu para o projeto real chamado Flask.
>
> O termo microframework significa que ele oferece um núcleo pequeno e extensível. O Flask fornece recursos essenciais, como rotas, requisições e respostas HTTP, mas deixa outras decisões para o desenvolvedor.
>
> Por exemplo, ele não determina qual banco de dados, ORM ou biblioteca de validação precisa ser utilizada.
>
> Essa proposta permite começar rapidamente e adicionar somente as ferramentas necessárias para cada projeto.
>
> Mesmo sendo chamado de microframework, Flask pode ser utilizado em aplicações maiores. Nesse caso, o projeto exige mais organização e decisões arquiteturais por parte dos desenvolvedores.

---

## Slide 3 — Gabriel

### O caminho de uma requisição

> Para entender como Flask funciona, podemos acompanhar o caminho de uma requisição.
>
> Neste exemplo, o cliente deseja consultar os eventos cadastrados e envia uma requisição GET para o endereço `/events`.
>
> Quando a aplicação recebe essa requisição, o Flask procura qual rota foi associada ao caminho `/events` e ao método HTTP GET.
>
> Depois de encontrar a rota, ele executa a função Python correspondente. No nosso projeto, essa função lê os eventos armazenados e os ordena pela data.
>
> Por fim, o Flask transforma o resultado em uma resposta JSON e devolve ao cliente o código HTTP 200, indicando que a operação foi realizada com sucesso.
>
> O Werkzeug auxilia o Flask no processamento HTTP e na comunicação por meio do padrão WSGI. Já o Jinja é utilizado quando uma aplicação precisa gerar páginas HTML a partir de templates. Como nosso projeto é uma API, trabalhamos principalmente com respostas JSON.
>
> Agora que entendemos o funcionamento básico, o Igor vai apresentar as principais vantagens e limitações do Flask.

---

## Slide 5 — Igor

### Flask, Django e FastAPI

> Flask, Django e FastAPI são frameworks Python relacionados ao desenvolvimento web, mas cada um possui uma proposta diferente.
>
> Flask oferece uma base leve e flexível. Ele disponibiliza recursos essenciais, como rotas e tratamento de requisições, enquanto o desenvolvedor escolhe os outros componentes.
>
> Django é um framework mais completo. Ele já possui ORM, sistema de migrações, autenticação, templates e painel administrativo. Por isso, costuma ser uma escolha adequada para sistemas web maiores que precisam dessas funcionalidades integradas.
>
> FastAPI possui foco na construção de APIs. Ele utiliza os tipos do Python e modelos do Pydantic para fazer validação, serialização e geração automática da documentação OpenAPI.
>
> Para APIs novas, FastAPI pode reduzir a quantidade de validação e documentação que o desenvolvedor precisa escrever manualmente.
>
> Isso não significa que um framework seja sempre superior aos outros. A escolha depende dos requisitos da aplicação, da experiência da equipe e das ferramentas que o projeto precisa.
>
> Para visualizar na prática como Flask funciona, o Tiago vai apresentar a API de agenda desenvolvida pelo grupo.

---

## Slide 6 — Tiago Monteiro

### Projeto prático: Agenda REST

Para aplicar esses conceitos, nós desenvolvemos uma API REST de agenda.

O objetivo da aplicação é permitir o cadastro e o gerenciamento de eventos. Cada evento possui um identificador, um título e uma data.

A API possui **cinco rotas principais**.

A primeira é `GET /events`, utilizada para listar todos os eventos em ordem cronológica.

A segunda é `GET /events/<id>`, que consulta um evento específico pelo seu identificador.

Para criar um evento, utilizamos `POST /events`.

Para atualizar completamente um evento existente, utilizamos `PUT /events/<id>`.

Por fim, `DELETE /events/<id>` remove um evento.

Essas cinco rotas formam um **CRUD**. A criação é feita com POST, as leituras com GET, a atualização com PUT e a remoção com DELETE.

Agora eu vou abrir o `app.py` e mostrar como essas operações foram implementadas.

---

## Slide 7

### Como o `app.py` foi organizado

**Imports:** Flask é utilizado para criar a aplicação, o `request` permite acessar os dados enviados pelo cliente, também utilizamos `datetime` para fazer validação e ordenação das datas, e o Swagger, fornecido pelo Flasgger, para gerar a documentação da API.

### Swagger

Foram definidos os modelos utilizados na documentação. `EventInput` representa os dados recebidos na criação e atualização de um evento. Ele exige `title` e `date`.

`Event` representa um evento completo e acrescenta o campo `id`.

O Flasgger combina esses modelos com docstrings para gerar a documentação Swagger.

### Armazenamento em memória

Para manter a simplicidade, os dados ficam em memória. Em um app real, essa lista seria substituída por um banco de dados.

### Limites dos campos

Também criamos o dicionário `limits` para centralizar os tamanhos máximos permitidos:

```python
limits = {
    "max_title_length": 100,
    "max_date_length": 10,
}
```

O título pode ter no máximo 100 caracteres.

A data pode ter no máximo 10 caracteres, que corresponde ao tamanho do formato `YYYY-MM-DD`.

### Validação

Função criada para centralizar validações utilizadas pelas rotas de POST e PUT.

1. Verificamos se o corpo da request é um objeto JSON.
2. Verificamos se o título é string e se não está vazio.
3. Verificamos se o título possui no máximo 100 caracteres.
4. Fazemos a mesma verificação para a data de string não vazia.
5. Por fim, utilizamos o `datetime.strptime` para confirmar que a data segue o formato de ano/mês/dia.
6. Quando algum dado é inválido, a função devolve uma mensagem acompanhada do código HTTP 400.

### Listagem (`get_events`)

O decorator `app.route` associa uma URL e um método HTTP a uma função Python, ou seja, `GET /events` a `get_events()`. A função usa `sorted` para ordenar a lista pela data antes de devolver os eventos.

### Consulta por ID (`get_event_by_id`)

Nessa rota, o identificador faz parte da URL. O trecho `<int:event_id>` informa que o Flask deve converter esse valor para `int`. Depois, os eventos são percorridos até encontrar o ID solicitado. Se o evento existir, é retornado; se não, a API devolve a mensagem "evento não encontrado", com 404.

### Criação (`create_event`)

Utiliza o método POST. `request.get_json` lê o corpo JSON da request. Em seguida, a função de validação é chamada. Se os dados estiverem corretos, o próximo ID é calculado com base no maior ID existente. Depois de calcular o ID, o evento é adicionado à lista e retornado com 201.

### Atualização (`update_event`)

Segue um fluxo semelhante: recebe um ID pela URL e os novos dados pelo corpo do JSON. Os dados são validados, o evento é localizado e título e data são substituídos. OK 200, dados inválidos 400, ID inexistente 404.

### Remoção (`delete_event`)

No DELETE, percorremos a lista até encontrar o evento solicitado. Quando encontramos, utilizamos o `remove` e devolvemos uma mensagem de sucesso com 200. Caso o ID não exista, é retornado 404.

---

## Fazer demonstração

A demonstração confirma o funcionamento das 5 rotas, as validações e os pontos principais dos códigos HTTP.

## Slide 9 — Igor

### Dificuldades e aprendizados

Durante o desenvolvimento, entendemos de forma prática como as rotas conectam URLs e métodos HTTP a funções Python.

Também percebemos a importância dos códigos de status. Eles permitem que o cliente identifique se uma operação funcionou, se os dados são inválidos ou se um recurso não foi encontrado.

Os testes ajudaram a encontrar problemas de entrada, principalmente no título e na data dos eventos.

Uma das dificuldades foi garantir que as validações fossem aplicadas tanto na criação quanto na atualização. Para evitar duplicação de código, concentramos essas regras em uma única função.

Outra limitação do projeto é o armazenamento em memória. Essa solução foi suficiente para a atividade, mas os dados são perdidos quando a aplicação é reiniciada.

Como próximos passos, poderíamos adicionar um banco de dados, criar testes automatizados e separar a aplicação em módulos.

Para concluir a apresentação, o Gabriel e o Tiago vão retomar os principais pontos estudados.

**Tempo estimado:** aproximadamente 1 minuto.

---

## Slide 10 — Gabriel e Tiago

### Gabriel — Retomada do conteúdo

Para concluir, o projeto mostrou como Flask torna visíveis os principais fundamentos de uma API REST.

Durante o desenvolvimento, trabalhamos diretamente com rotas, métodos HTTP, requisições JSON, validações e códigos de resposta.

Flask continua sendo um framework mantido e utilizado profissionalmente. Porém, para projetos novos, frameworks como FastAPI e Django podem oferecer mais recursos integrados e reduzir parte do trabalho manual.

Para relacionar essa conclusão com uma situação real, o Tiago vai comentar brevemente sua experiência profissional com Flask e Django.

### Tiago — Experiência profissional

Na Gedanken, empresa onde trabalho, temos uma situação que representa bem essa discussão.

Mantemos um sistema legado desenvolvido em Flask. Embora seja uma tecnologia mais antiga dentro da nossa arquitetura, esse sistema continua importante porque ainda executa quase 200 serviços utilizados pela operação.

Paralelamente, um novo sistema está sendo desenvolvido com Django, aproveitando recursos integrados como o ORM e uma estrutura mais padronizada para o crescimento da aplicação.

Porém, a existência do novo sistema não significa que podemos simplesmente desligar o legado. Enquanto os serviços ainda dependem dele, precisamos continuar garantindo sua manutenção, estabilidade e funcionamento.

Essa experiência mostra que a escolha de um framework não acontece somente por preferência técnica. Também precisamos considerar o sistema existente, o risco de uma migração, a continuidade dos serviços e o custo de substituir uma aplicação que já está em produção.

Portanto, Flask não deixou de ter utilidade. Ele continua presente em sistemas reais e importantes, mesmo quando novas aplicações passam a utilizar outras tecnologias.

### Gabriel — Encerramento

Esse exemplo reforça a conclusão do grupo: não existe um framework universalmente melhor.

Flask oferece simplicidade e flexibilidade. Django oferece uma estrutura mais completa para sistemas maiores, enquanto FastAPI se destaca no desenvolvimento de APIs modernas.

A escolha depende dos requisitos do projeto, da arquitetura existente e do contexto da organização.
