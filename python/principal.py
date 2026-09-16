from banco.conexao import conectar

from usuarios.usuarios import cadastrar_usuario
from motoristas.motoristas import cadastrar_motorista
from veiculos.veiculos import cadastrar_veiculo
from corridas.corridas import cadastrar_corrida
from pagamentos.pagamentos import cadastrar_pagamento
from avaliacoes.avaliacoes import cadastrar_avaliacao

from historico.historico import (
    registrar_historico,
    listar_historico_corrida,
    listar_historico_motorista
)

from consultas.consultas import (
    cinco_corridas_mais_caras,
    motorista_mais_corridas,
    forma_pagamento_mais_utilizada,
    usuarios_mais_corridas,
    motoristas_disponiveis,
    historico_determinada_corrida,
    arrecadacao_periodo,
    media_avaliacao_motoristas,
    media_geral_motoristas
)

print("Imports realizados com sucesso!")