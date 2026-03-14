from integrador.informezz.settings import SISTEMA_INTEGRADO as informezz_nome
from integrador.ssotica.settings import SISTEMA_INTEGRADO as ssotica_nome
from integrador.sti3powerstock.settings import SISTEMA_INTEGRADO as sti3powerstock_nome

from integrador.informezz.tasks.orchestration import (
    executar_frequente as informezz_frequente,
    executar_diario as informezz_diario,
)

from integrador.ssotica.tasks.orchestration import (
    executar_frequente as ssotica_frequente,
    executar_diario as ssotica_diario,
)

from integrador.sti3powerstock.tasks.orchestration import (
    executar_frequente as sti3_frequente,
    executar_diario as sti3_diario,
)


ERP_FREQUENTE_TASKS = {
    # informezz_nome: informezz_frequente,
    # ssotica_nome: ssotica_frequente,
    # sti3powerstock_nome: sti3_frequente,
}

ERP_DIARIO_TASKS = {
    informezz_nome: informezz_diario,
    # ssotica_nome: ssotica_diario,
    # sti3powerstock_nome: sti3_diario,
}
