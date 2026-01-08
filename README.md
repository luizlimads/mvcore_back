# API MVCORE

### Como executar o projeto localmente
Siga as instruções abaixo para que possa executar o projeto em seu ambiente e realizar alterações.

---
### Prepare o banco de dados
Instale o PgAdmin 4 em seu ambiente. Essa versão pode ser obtida no link abaixo.

https://www.pgadmin.org/download/pgadmin-4-windows/

Acesse, configure um servidor na porta 5433 e crie um banco de dados vazio chamado "**mvcore**".

---
### Prepare o ambiente de desenvolvimento
Instale o Python 3.11 em seu ambiente. É importante que essa versão seja respeitada para que não dê conflitos com o Django Rest Framework. Essa versão pode ser obtida no link a seguir.

https://www.python.org/downloads/release/python-3110/

Utilize um editor de texto avançado para simplificar o desenvolvimento. Caso opte por utilizar o VS Code, há algumas extensões que facilitam o trabalho, como as sugeridas abaixo.

* Django (Roberth Solis)
* Django Snippets (bibhasdn)
* django-intellisense (shamanu4)
* Pylance (Microsoft)
* Python (Microsoft)
* Python Debugger (Microsoft)
* REST Client (Huachao Mao)

https://code.visualstudio.com/download

Por fim, instale o Git caso ainda não o tenha feito e clone o repositório desse projeto.

https://git-scm.com/downloads

---
### Inicialize o projeto

No terminal do PowerShell, navegue até a pasta **mvcore-api**.

Ative o ambiente virtual do Python: ```.\venv\Scripts\Activate.ps1```

Instale os pacotes requeridos na aplicação: ```pip install -r requirements.txt```

Execute as migrações: ```py manage.py migrate``` 

Inicie o servidor: ```py manage.py runserver```

---
### Documentação

A documentação das APIs foi construída utilizando o pacote *drf-spectacular*. Para ver os endpoints disponíveis, acesse 
``` localhost/schema/swagger-ui/ ```

Caso você modifique ou crie APIs, atualize a documentação executando o comando: ```py manage.py spectacular --file schema.yml```

Foi adicionado também o pacote *silk*, que nos mostra o desempenho das consultas SQL. Para avaliar, acesse ``` localhost/silk/ ```

---
### Outras orientações

Foram adicionadas duas migrações responsáveis por criar os dados iniciais no banco. Esses dados se referem à um sistema integrado e um tenant padrões com id zerado, ambos para serem utilizados pelo usuário admin, e o próprio usuário admin do sistema.

Caso necessite trocar a senha do superusuário (admin), utilize o comando a seguir: ```py manage.py changepassword [SEU E_MAIL]```

---
### Recriando as migrations

Caso necessite apagar as migrations e reiniciar o teste, use o comando abaixo, e em seguida aplique os comandos de inicialização do projeto apresentados acima. Lembre-se de apagar e recriar o banco antes disso.

Obs: NÃO FAÇA ISSO EM PRODUÇÃO.

```
Get-ChildItem -Recurse -Include *.py -Exclude __init__.py | Where-Object { $_.FullName -match "\\migrations\\" -and $_.FullName -notmatch "\\venv\\" } | Remove-Item -Force
``` 

[Voltar](../README.md)