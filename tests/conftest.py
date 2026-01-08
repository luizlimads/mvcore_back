import pytest
from rest_framework.test import APIClient
from tenant.models import SistemaIntegrado, Tenant
from usuario.models import Usuario
from produto.models import Produto

@pytest.fixture
def sistemas_integrados():
    return [
        SistemaIntegrado.objects.create(nome="MVcore"),
        SistemaIntegrado.objects.create(nome="ssOtica"),
    ]

@pytest.fixture
def tenants(sistemas_integrados):
    tenants_list = [
        Tenant.objects.create(
            documento=f"0000000000000{i}",
            razao_social=f"Empresa {i}",
            nome_fantasia=f"Fantasia {i}",
            sistema_integrado=sistemas_integrados[i],
            documento_api=f"API_DOC_{i}",
            id_origem=f"ID_API_{i}"
        )
        for i in range(len(sistemas_integrados))
    ]
    return tenants_list


@pytest.fixture
def usuarios(tenants):
    return [
        Usuario.objects.create_user(
            email="ssotica@test.com",
            password="12345678",
            tenant=tenants[0].id  # vinculado a MVcore
        ),
        Usuario.objects.create_user(
            email="mvcore@test.com",
            password="12345678",
            tenant=tenants[1].id  # vinculado a ssOtica
        ),
    ]

@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def get_token(api_client):
    def _get_token(usuario):
        response = api_client.post("/auth/jwt/create/", {
            "email": usuario.email,
            "password": "12345678"
        }, format="json")
        return response.data["access"]
    return _get_token

@pytest.fixture
def produtos(tenants):
    product_list = [
        Produto.objects.create(
            id_origem=f"00{i}",
            referencia=f"REF00{i}",
            descricao=f"Produto de teste {i}",
            grupo=f"Grupo {i}",
            id_grupo_api=f"G00{i}",
            marca=f"Marca X{i}",
            id_marca_api=f"M00{i}",
            gtin=f"781234567890{i}",
            ativo=True,
            tenant=tenants[i]
        )
        for i in range(len(tenants))
    ]
    return product_list