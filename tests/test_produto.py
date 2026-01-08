import pytest
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_acessar_produto_sem_autenticacao(tenants, produtos):
    client = APIClient()

    response = client.get("/v1/produto/")
    assert response.status_code == 401, f"Listar todos produtos (status: {response.status_code})"

    response = client.post(
        "/v1/produto/",
        {    
        "id_api": "43232454",
        "referencia": "produto de teste 45",
        "descricao": "produto de teste",
        "grupo": "produto de teste",
        "id_grupo_api": "415435",
        "marca": "produto de teste",
        "id_marca_api": "45454",
        "unidade": "un",
        "codigo_gtin": "5454",
        "ncm": "5468",
        "ativo": "true",
        "tenant": tenants[0].id
        },
        format="json"
    )
    assert response.status_code == 401, f"Inserir 1 produto (status: {response.status_code})"


@pytest.mark.django_db
def test_acessar_produto_com_autenticacao(api_client ,tenants, usuarios, get_token):
    user = usuarios[0]
    token_user = get_token(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"JWT {token_user}")

    response = api_client.get("/v1/produto/")
    assert response.status_code == 200, f"Listar todos produtos (status: {response.status_code})"

    response = api_client.post(
        "/v1/produto/",
        {    
            "id_origem": "dasdsaff",
            "id_api": "43232454",
            "referencia": "produto de teste 45",
            "descricao": "produto de teste",
            "grupo": "produto de teste",
            "id_grupo_api": "415435",
            "marca": "produto de teste",
            "id_marca_api": "45454",
            "unidade": "un",
            "codigo_gtin": "5454",
            "ncm": "5468",
            "ativo": "true",
            "tenant": tenants[0].id
        },
        format="json"
    )
    assert response.status_code == 201, f"Inserir 1 produto (status: {response.status_code})"
