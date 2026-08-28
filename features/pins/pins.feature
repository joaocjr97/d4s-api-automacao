# language: pt

Funcionalidade: Pins de assinatura na API D4Sign
  Como consumidor da API D4Sign
  Quero posicionar pins de assinatura, rubrica e selo
  Para validar o endpoint de pins

  Contexto:
    Dado que a API D4Sign está configurada

  @api @upload @signature @critical @pins @regression
  Cenário: Adicionar, listar e remover pins de assinatura, rubrica e selo no documento
    Quando eu faço upload de um PDF para o cofre configurado
    E eu adiciono um signatário por e-mail ao documento criado
    E eu adiciono pins de assinatura, rubrica e selo ao documento
    Então a resposta deve ter status 200
    E a mensagem da resposta deve ser "success"
    Quando eu consulto os pins cadastrados no documento
    Então a resposta deve ter status 200
    E o corpo da resposta não deve estar vazio
    E a lista de pins deve conter os pins cadastrados no documento
    Quando eu removo os pins cadastrados do documento
    Então a resposta deve ter status 200
    E a mensagem da resposta deve ser "success"
    E os pins removidos não devem mais aparecer na listagem do documento
