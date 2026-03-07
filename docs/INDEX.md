# 📚 Índice de Documentação - LOTO

## 🎯 Início Rápido

- **[README.md](../README.md)** - Visão geral do projeto e instruções de início
- **[QUICK_START_AUTH.md](QUICK_START_AUTH.md)** - Início rápido com autenticação

## 🏗️ Arquitetura e Design

- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Arquitetura geral da aplicação
- **[PROJECT_STATUS.md](PROJECT_STATUS.md)** - Status do projeto e histórico

## 🔐 Autenticação

- **[AUTHENTICATION.md](AUTHENTICATION.md)** - Sistema de autenticação (visão geral)
- **[AUTH_IMPLEMENTATION.md](AUTH_IMPLEMENTATION.md)** - Detalhes de implementação da autenticação
- **[KEYCLOAK_SETUP.md](KEYCLOAK_SETUP.md)** - Configuração completa do Keycloak
- **[KEYCLOAK_IMPLEMENTACAO.md](KEYCLOAK_IMPLEMENTACAO.md)** - Processo de implementação do Keycloak
- **[KEYCLOAK_RELATORIO_FINAL.md](KEYCLOAK_RELATORIO_FINAL.md)** - Relatório final da integração Keycloak
- **[SMTP_CONFIGURATION.md](SMTP_CONFIGURATION.md)** - Configuração de email (SMTP)
- **[ENCONTRAR_TOKEN.md](ENCONTRAR_TOKEN.md)** - Como encontrar tokens
- **[TOKEN_RAPIDO.md](TOKEN_RAPIDO.md)** - Geração rápida de tokens
- **[DIAGNOSTICO_TOKENS.md](DIAGNOSTICO_TOKENS.md)** - Diagnóstico de problemas com tokens

## 📋 Recursos Específicos

- **[IMPLEMENTACAO_SORTE.md](IMPLEMENTACAO_SORTE.md)** - Documentação da página "Sorte!"
- **[SORTE_PAGINA_GUIA.md](SORTE_PAGINA_GUIA.md)** - Guia de uso da página Sorte!
- **[APOSTAS_REGISTRO.md](APOSTAS_REGISTRO.md)** - Sistema de registra de apostas com análise inteligente
- **[BETTING_FEEDBACK_SYSTEM.md](BETTING_FEEDBACK_SYSTEM.md)** - Sistema de feedback de apostas
- **[COMO_ACESSAR_SORTE.md](COMO_ACESSAR_SORTE.md)** - Como acessar a página Sorte!

## 🧪 Testes

- **[TESTING.md](TESTING.md)** - Guia de testes
- **[RUN_TESTS.md](RUN_TESTS.md)** - Como executar testes
- **[TESTE_PRATICO.md](TESTE_PRATICO.md)** - Testes práticos

## 🚀 Servidor e Deploy

- **[ENCERRAMENTO_SERVIDOR.md](ENCERRAMENTO_SERVIDOR.md)** - Encerramento do servidor
- **[RESUMO_ENCERRAMENTO.md](RESUMO_ENCERRAMENTO.md)** - Resumo de encerramento
- **[INICIO_RAPIDO_AUTH.md](INICIO_RAPIDO_AUTH.md)** - Início rápido do servidor com autenticação

## 📊 Refatoração e Reorganização

- **[REFACTORING_SUMMARY.md](REFACTORING_SUMMARY.md)** - Resumo de refatorações
- **[ESTRUTURA_KEYCLOAK.md](ESTRUTURA_KEYCLOAK.md)** - Estrutura do Keycloak
- **[MIGRATION.md](MIGRATION.md)** - Guia de migração
- **[CHECKLIST_IMPLEMENTACAO.md](CHECKLIST_IMPLEMENTACAO.md)** - Checklist de implementação

## 📁 Organização de Arquivos

```
docs/
├── INDEX.md                           (este arquivo)
├── README.md
├── ARCHITECTURE.md
├── AUTHENTICATION.md
├── AUTH_IMPLEMENTATION.md
├── KEYCLOAK_SETUP.md
├── KEYCLOAK_IMPLEMENTACAO.md
├── KEYCLOAK_RELATORIO_FINAL.md
├── SMTP_CONFIGURATION.md
├── IMPLEMENTACAO_SORTE.md
├── SORTE_PAGINA_GUIA.md
├── APOSTAS_REGISTRO.md
├── BETTING_FEEDBACK_SYSTEM.md
├── COMO_ACESSAR_SORTE.md
├── TESTING.md
├── RUN_TESTS.md
├── TESTE_PRATICO.md
├── ENCERRAMENTO_SERVIDOR.md
├── RESUMO_ENCERRAMENTO.md
├── INICIO_RAPIDO_AUTH.md
├── REFACTORING_SUMMARY.md
├── ESTRUTURA_KEYCLOAK.md
├── MIGRATION.md
├── CHECKLIST_IMPLEMENTACAO.md
├── ENCONTRAR_TOKEN.md
├── TOKEN_RAPIDO.md
├── DIAGNOSTICO_TOKENS.md
└── PROJECT_STATUS.md
```

## 🎯 Casos de Uso por Documento

### "Quero começar a usar a aplicação"
1. Leia: [README.md](../README.md)
2. Leia: [QUICK_START_AUTH.md](QUICK_START_AUTH.md)
3. Configure: [.env](../.env.example)
4. Rodando: `python run.py`

### "Quero usar Keycloak para autenticação"
1. Leia: [KEYCLOAK_SETUP.md](KEYCLOAK_SETUP.md)
2. Execute: `docker-compose up -d`
3. Configure: Variáveis KEYCLOAK_* em `.env`
4. Inicie: `python run.py`

### "Quero entender a arquitetura"
1. [ARCHITECTURE.md](ARCHITECTURE.md)
2. [PROJECT_STATUS.md](PROJECT_STATUS.md)

### "Quero testar a aplicação"
1. [TESTING.md](TESTING.md)
2. [RUN_TESTS.md](RUN_TESTS.md)
3. Execute: `pytest`

### "Quero usar a página Sorte!"
1. [COMO_ACESSAR_SORTE.md](COMO_ACESSAR_SORTE.md)
2. [SORTE_PAGINA_GUIA.md](SORTE_PAGINA_GUIA.md)
3. [IMPLEMENTACAO_SORTE.md](IMPLEMENTACAO_SORTE.md)

### "Quero registrar minhas apostas e analisar resultados"
1. [APOSTAS_REGISTRO.md](APOSTAS_REGISTRO.md)
2. Acesse: `/apostas` (após login)
3. Registre suas apostas e o resultado
4. Receba análise inteligente com recomendações

## 🔍 Busca Rápida por Tópico

| Tópico | Documento | Descrição |
|--------|-----------|-----------|
| Autenticação | [AUTHENTICATION.md](AUTHENTICATION.md) | Sistema de login e autenticação |
| Keycloak | [KEYCLOAK_SETUP.md](KEYCLOAK_SETUP.md) | OAuth2/OIDC com Keycloak |
| Sorte! | [SORTE_PAGINA_GUIA.md](SORTE_PAGINA_GUIA.md) | Análise de números |
| Registrar Apostas | [APOSTAS_REGISTRO.md](APOSTAS_REGISTRO.md) | Registrar e analisar apostas realizadas |
| Testes | [TESTING.md](TESTING.md) | Testes automatizados |
| SMTP | [SMTP_CONFIGURATION.md](SMTP_CONFIGURATION.md) | Email configuration |
| Deploy | [ENCERRAMENTO_SERVIDOR.md](ENCERRAMENTO_SERVIDOR.md) | Deployment e shutdown |

## 📞 Suporte

Se não encontrar o que procura, consulte:
- [README.md](../README.md) - Visão geral geral
- [ARCHITECTURE.md](ARCHITECTURE.md) - Arquitetura técnica

---

**Última actualización:** 07/03/2026  
**Total de documentos:** 26
