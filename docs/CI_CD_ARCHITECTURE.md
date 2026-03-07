# 🏗️ Arquitetura da Esteira CI/CD

## Visualização do Pipeline

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          DESENVOLVIMENTO LOCAL                               │
│  make install-dev  │  make test  │  make lint  │  make format              │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                            GIT PUSH / PR                                    │
│  git push origin feature/name  →  No GitHub, criar Pull Request             │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                      GITHUB ACTIONS TRIGGERED                               │
│                                                                             │
│  ┌───────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  CI WORKFLOW  │  │SECURITY WORKFLOW│ │ LINT WORKFLOW│ │DEPLOY WORKFLOW│ │
│  ├───────────────┤  ├──────────────┤  ├──────────────┤  ├──────────────┤  │
│  │ • Test x4 PY │  │ • Bandit     │  │ • Black      │  │ • Docker     │  │
│  │ • Coverage   │  │ • Safety     │  │ • isort      │  │ • Registry   │  │
│  │ • Quality    │  │ • Semgrep    │  │ • Flake8     │  │ • Staging    │  │
│  │ • Linting    │  │ • Secrets    │  │ • Pylint     │  │ • Production │  │
│  └───────────────┘  └──────────────┘  └──────────────┘  └──────────────┘  │
│         3-5m              2-3m              1-2m            5-10m           │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                   BRANCH PROTECTION RULES CHECK                            │
│  ✓ Status checks passed     ✓ Code reviewed     ✓ Up to date               │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                             MERGE TO MAIN                                  │
│  Após aprovação, merge automático ou manual para main                      │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                      DEPLOY WORKFLOW (STAGING)                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Docker Build │  │ Docker Push  │  │ SSH Deploy   │  │Health Check  │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘  │
│  ghcr.io:staging       Registry     staging.example.com    200 OK         │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                       STAGING ENVIRONMENT                                  │
│  https://staging.seu-dominio.com  (Pronto para QA/Testes)                 │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                         CREATE RELEASE TAG                                 │
│  git tag v1.0.0  →  git push origin v1.0.0                                │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                  DEPLOY WORKFLOW (PRODUCTION)                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Docker Build │  │ GitHub Rel.  │  │ SSH Deploy   │  │Health Check  │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘  │
│  ghcr.io:v1.0.0    v1.0.0 Release   prod.example.com    200 OK           │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PRODUCTION ENVIRONMENT                                  │
│  https://seu-dominio.com  (Em produção!)     🎉                           │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Estrutura de Diretórios de Workflows

```
.github/
├── workflows/
│   ├── ci.yml               # Testes e análise (3-5 min)
│   ├── security.yml         # Segurança (2-3 min)
│   ├── lint.yml             # Formatação (1-2 min)
│   └── deploy.yml           # Deploy (5-10 min)
├── CODEOWNERS               # Proprietários do código
└── pull_request_template.md # Template para PRs
```

## Matriz de Execução dos Workflows

```
┌──────────┬────────┬────────────┬──────────┬────────┐
│ Workflow │  Push  │ Pull Req   │ Schedule │ Tag    │
├──────────┼────────┼────────────┼──────────┼────────┤
│ CI       │ develop│ any branch │ ×        │ ×      │
│          │ main   │            │          │        │
├──────────┼────────┼────────────┼──────────┼────────┤
│ Security │ develop│ any branch │ daily 2AM│ ×      │
│          │ main   │            │          │        │
├──────────┼────────┼────────────┼──────────┼────────┤
│ Lint     │ develop│ any branch │ ×        │ ×      │
│          │ main   │            │          │        │
├──────────┼────────┼────────────┼──────────┼────────┤
│ Deploy   │ main   │ ×          │ ×        │ v*.*.*│
└──────────┴────────┴────────────┴──────────┴────────┘
```

## Fluxo de Dados e Artifacts

```
┌─────────────────────────────────────────────────────────┐
│ Source Code (Repository)                                │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ↓            ↓            ↓
   ┌───────┐    ┌────────┐    ┌─────────┐
   │  CI   │    │Security│    │  Lint   │
   └───────┘    └────────┘    └─────────┘
        │            │            │
        ├────────────┼────────────┤
        │
        ↓
  ┌──────────────────┐
  │ All Checks Pass? │
  └────────┬─────────┘
           │ ✓
           ↓
  ┌──────────────────┐
  │ Code Review OK?  │
  └────────┬─────────┘
           │ ✓
           ↓
  ┌──────────────────┐
  │  Merge to Main   │
  └────────┬─────────┘
           │
           ↓
  ┌──────────────────┐
  │ Build Docker     │
  │ Image            │
  └────────┬─────────┘
           │
           ↓
  ┌──────────────────┐
  │ Push Registry    │
  │ (ghcr.io)        │
  └────────┬─────────┘
           │
           ├─────────────────┐
           │                 │
           ↓                 ↓
    ┌───────────┐      ┌───────────┐
    │ Staging   │      │ Production│
    │ Deploy    │      │ Deploy    │
    │ (main)    │      │ (tags)    │
    └───────────┘      └───────────┘
           │                 │
           ↓                 ↓
    ┌───────────┐      ┌───────────┐
    │ Staging   │      │ Production│
    │ Health OK │      │ Health OK │
    └───────────┘      └───────────┘
```

## Ambientes de Execução

```
┌────────────────────────────────────────────────────────┐
│ Local Development                                      │
│ ─────────────────────────────────────────────────────  │
│ • Docker Compose (dev)                                 │
│ • Jupyter Notebook                                     │
│ • PostgreSQL, Keycloak                                 │
│ • Python 3.10 (local)                                  │
└────────────────────────────────────────────────────────┘
                        ↓
┌────────────────────────────────────────────────────────┐
│ GitHub Actions (Ephemeral)                             │
│ ─────────────────────────────────────────────────────  │
│ • Ubuntu Latest                                        │
│ • Python 3.8, 3.9, 3.10, 3.11                         │
│ • PostgreSQL Service                                   │
│ • Docker Buildx (multi-platform)                       │
└────────────────────────────────────────────────────────┘
                        ↓
┌────────────────────────────────────────────────────────┐
│ Staging Environment                                    │
│ ─────────────────────────────────────────────────────  │
│ • Docker Container (Linux)                             │
│ • PostgreSQL (persistente)                             │
│ • Keycloak (persistente)                               │
│ • Domain: staging.seu-dominio.com:5000                │
└────────────────────────────────────────────────────────┘
                        ↓
┌────────────────────────────────────────────────────────┐
│ Production Environment                                 │
│ ─────────────────────────────────────────────────────  │
│ • Docker Swarm/Kubernetes (prod)                       │
│ • PostgreSQL (RDS/managed)                             │
│ • Keycloak (managed)                                   │
│ • Domain: seu-dominio.com:5000                        │
│ • Load Balancer, CDN, SSL                             │
└────────────────────────────────────────────────────────┘
```

## Relatórios Gerados

```
CI Workflow Generates:
├── pytest HTML Report → htmlcov/
├── Coverage XML → coverage.xml (→ Codecov)
┣── JUnit XML → junit.xml
└── Artifacts (uploaded to GitHub)

Security Workflow Generates:
├── Bandit JSON → bandit-report.json
├── Safety JSON → safety-report.json
├── Semgrep Results
└── Artifacts (uploaded to GitHub)

Deploy Workflow Generates:
├── Docker Image Tag
├── GitHub Release
├── Deployment Log
└── Health Check Report
```

## Status Badges para README

```markdown
<!-- Seu README.md -->

## CI/CD Status

[![CI Tests](https://github.com/USUARIO/Loto/actions/workflows/ci.yml/badge.svg)](https://github.com/USUARIO/Loto/actions/workflows/ci.yml)
[![Security](https://github.com/USUARIO/Loto/actions/workflows/security.yml/badge.svg)](https://github.com/USUARIO/Loto/actions/workflows/security.yml)
[![Lint](https://github.com/USUARIO/Loto/actions/workflows/lint.yml/badge.svg)](https://github.com/USUARIO/Loto/actions/workflows/lint.yml)
[![Deploy](https://github.com/USUARIO/Loto/actions/workflows/deploy.yml/badge.svg)](https://github.com/USUARIO/Loto/actions/workflows/deploy.yml)

[![codecov](https://codecov.io/gh/USUARIO/Loto/branch/main/graph/badge.svg)](https://codecov.io/gh/USUARIO/Loto)

[![Python 3.10](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Flask 2.3](https://img.shields.io/badge/flask-2.3-green.svg)](https://flask.palletsprojects.com/)
```

## Matriz de Testes (Python Versions)

```
Test Matrix:
├── Python 3.8  (EOL Sept 2024)  [Tests]
├── Python 3.9  (EOL Oct 2025)   [Tests]
├── Python 3.10 (EOL Oct 2026)   [Tests + Coverage]
└── Python 3.11 (EOL Oct 2027)   [Tests + Security]

All tests against:
├── PostgreSQL 15 (via Service Container)
├── Latest pip
└── requirements.txt
```

---

**Visualização criada em:** Março 2025
