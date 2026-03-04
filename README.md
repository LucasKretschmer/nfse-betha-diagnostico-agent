# nfse-betha-diagnostico-agent

## Configuração do ambiente

Copie o arquivo de exemplo e preencha com seus dados:

```bash
cp .env.example .env
```

### Variáveis de ambiente

| Variável        | Descrição                          | Exemplo                          |
|-----------------|------------------------------------|----------------------------------|
| `DB_HOST`       | Host do banco de dados PostgreSQL  | `localhost`                      |
| `DB_PORT`       | Porta do PostgreSQL                | `5432`                           |
| `DB_NAME`       | Nome do banco de dados             | `nfse_betha`                     |
| `DB_USER`       | Usuário do banco de dados          | `postgres`                       |
| `DB_PASSWORD`   | Senha do banco de dados            | `sua_senha_aqui`                 |
| `OPENAI_API_KEY`| Chave de API da OpenAI             | `sk-...`                         |