import pytest
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_financeiro_sem_autenticacao():
    client = APIClient()

    # Requisição SEM o token JWT no header
    response = client.post(
        "/v1/integrador/ssotica/financeiro/",
        {
            "token": "92YuEdT7BtrZSRnWPYe4yvSXUMzGvSVwtT8KjC561XjtAcdXio0PN6V7RXRD",
            "cnpj": "11406800000123",
            "inicio_periodo": "2025-01-01",
            "fim_periodo": "2025-01-02"
        },
        format="json"
    )

    # Verifica se o status é 401 Unauthorized
    assert response.status_code == 401


@pytest.mark.django_db
def test_financeiro_somente_para_usuarios_da_ssotica(api_client, usuarios, get_token, tenants):
    # Usuário vinculado à MVcore(negar)
    user_mvcore = usuarios[0]
    token_mvcore = get_token(user_mvcore)
    api_client.credentials(HTTP_AUTHORIZATION=f"JWT {token_mvcore}")
    response_negado = api_client.post(
        "/v1/integrador/ssotica/financeiro/",
        {
            "token": "92YuEdT7BtrZSRnWPYe4yvSXUMzGvSVwtT8KjC561XjtAcdXio0PN6V7RXRD",
            "cnpj": "11406800000123",
            "inicio_periodo": "2025-01-01",
            "fim_periodo": "2025-01-02"
        },
        format="json"
    )
    # Verifica se o status é 403 Forbidden
    assert response_negado.status_code == 403, f"Usuário fora da ssOtica não deveria acessar (status: {response_negado.status_code})"

    # Usuário vinculado à ssOtica (permitir)
    user_ssotica = usuarios[1]
    token_ssotica = get_token(user_ssotica)
    api_client.credentials(HTTP_AUTHORIZATION=f"JWT {token_ssotica}")
    response_ok = api_client.post(
        "/v1/integrador/ssotica/financeiro/",
        {
            "token": "92YuEdT7BtrZSRnWPYe4yvSXUMzGvSVwtT8KjC561XjtAcdXio0PN6V7RXRD",
            "cnpj": "11406800000123",
            "inicio_periodo": "2025-01-01",
            "fim_periodo": "2025-01-02"
        },
        format="json"
    )
    # Verifica se o status é 200 OK
    assert response_ok.status_code == 200, f"(status: {response_negado.status_code})"
