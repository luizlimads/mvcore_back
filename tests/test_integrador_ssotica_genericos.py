import pytest

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