# Teste Prático

##Folder Structure
```
+-- application
|   +-- fastapi
|   |   +-- Dockerfile
|   |   +-- main.py
|   |   +-- classes
|   |   +-- routes
|   |   |   +-- doc
|   |   |   +-- api
|   |   +-- static
|   |   +-- templates
|   +-- fastapi_tests
|   |   +-- fastapi_test.py
+-- documentation
+-- infrastructure
|   +-- postgres.yml
|   +-- fastapi.yml
```
O Código está totalmente configurado para o build usando docker. Para tal acesse o diretório [./infrastructure] e rode os seguintes comandos

``
docker-compose -f postgres.yml up
``

``
docker-compose -f fastapi.yml up
``

Para compilar o código em uma versão local é aconselhável acessar o diretório [./application/fastapi] como entry point onde deve-se executar os comandos(Obs.: deve-se mudar evn no arquivo ./fastapi/routes/api linha 10 passada para a url referente ao banco de dados para localhost caso seja um build local para "localhost"):

``
pip install -r requirements.txt
``

``
python main.py
``

Para executar os testes acesse o diretório [./application/fastapi_tests] e execute o comando:

``
python -m pytest
``

