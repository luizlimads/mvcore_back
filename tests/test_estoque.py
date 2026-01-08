import pytest
from rest_framework.test import APIClient
from usuario.models import Usuario

@pytest.mark.django_db
def test_estoque_sem_autenticacao():
    client = APIClient()

    # Requisição SEM o token JWT no header
    response = client.post(
        "/v1/integrador/ssotica/estoque/",
        {
            "token": "92YuEdT7BtrZSRnWPYe4yvSXUMzGvSVwtT8KjC561XjtAcdXio0PN6V7RXRD",
            "empresa": "JSCU-YOKG"
        },
        format="json"
    )

    # Verifica se o status é 401 Unauthorized
    assert response.status_code == 401


@pytest.mark.django_db
def test_estoque_somente_para_usuarios_da_ssotica(api_client, usuarios, get_token, tenants):
    # Usuário vinculado à MVcore(negar)
    user_mvcore = usuarios[0]
    token_mvcore = get_token(user_mvcore)
    api_client.credentials(HTTP_AUTHORIZATION=f"JWT {token_mvcore}")

    response_negado = api_client.post(
        "/v1/integrador/ssotica/estoque/",
        {
            "token": "92YuEdT7BtrZSRnWPYe4yvSXUMzGvSVwtT8KjC561XjtAcdXio0PN6V7RXRD",
            "empresa": "JSCU-YOKG"
        },
        format="json"
    )

    assert response_negado.status_code == 403, f"Usuário fora da ssOtica não deveria acessar (status: {response_negado.status_code})"

    # Usuário vinculado à ssOtica (permitir)
    user_ssotica = usuarios[1]
    token_ssotica = get_token(user_ssotica)
    print(token_ssotica)
    api_client.credentials(HTTP_AUTHORIZATION=f"JWT {token_ssotica}")

    response_ok = api_client.post(
        "/v1/integrador/ssotica/estoque/",
        {
            "token": "92YuEdT7BtrZSRnWPYe4yvSXUMzGvSVwtT8KjC561XjtAcdXio0PN6V7RXRD",
            "empresa": "JSCU-YOKG"
        },
        format="json"
    )

    assert response_ok.status_code == 200, f"(status: {response_negado.status_code})"

@pytest.mark.django_db
def test_fixture_tenants(tenants):
    assert len(tenants) == 2
    assert tenants[0].sistema_integrado.nome == "MVcore"
    assert tenants[1].sistema_integrado.nome == "ssOtica"

@pytest.mark.django_db
def test_usuario_vinculado_a_sistema_integrado(usuarios):
    usuario_mvcore = usuarios[0]
    usuario_ssotica = usuarios[1]

    # Verifica vínculo com sistema "MVcore"
    assert usuario_mvcore.tenant.sistema_integrado.nome == "MVcore"
    # Verifica vínculo com sistema "ssOtica"
    assert usuario_ssotica.tenant.sistema_integrado.nome == "ssOtica"