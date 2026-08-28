# language: pt

Funcionalidade: Webhooks na API D4Sign
  Como consumidor da API D4Sign
  Quero cadastrar webhook em um documento
  Para receber notificações de eventos

  Contexto:
    Dado que a API D4Sign está configurada

  @api @regression @webhooks
  Cenário: Adicionar e listar webhook cadastrado no documento configurado
    Quando eu adiciono um webhook ao documento configurado
    Então a resposta deve ter status 200
    E a mensagem da resposta deve ser "Webhook successfully registered"
    Quando eu consulto o webhook cadastrado no documento
    Então a resposta deve ter status 200
    E o corpo da resposta não deve estar vazio
    E o webhook retornado deve refletir a url cadastrada
