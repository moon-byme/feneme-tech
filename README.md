# Feneme

Sistema web inteligente para gestão de cargas e recomendação de rotas com base em condições climáticas.

## Resumo do projeto

O Feneme é uma aplicação web voltada ao apoio da gestão logística no transporte de alimentos. O sistema reunirá informações sobre cargas, entregas, trajetos e temperatura prevista para auxiliar no planejamento e acompanhamento dos transportes.

A proposta busca apoiar decisões mais eficientes, considerando fatores como distância, tempo estimado de viagem, temperatura e características da carga.

## Problema

O transporte de alimentos envolve variáveis como distância, tempo de viagem e temperatura. Atualmente, essas informações nem sempre são analisadas de forma integrada, o que pode levar à escolha de trajetos inadequados. Assim, esse problema afeta gestores e transportadores, podendo causar atrasos, perda de qualidade dos produtos, descarte de alimentos e prejuízos financeiros.

## Objetivo

Desenvolver um sistema web que auxilie no gerenciamento do transporte de alimentos e na escolha de trajetos, considerando informações logísticas e a previsão de temperatura.

## Usuários e perfis de acesso

O Feneme possuirá dois perfis de acesso, de acordo com a participação de cada usuário no processo de transporte. Cada perfil terá permissões específicas e acesso às funcionalidades relacionadas às suas responsabilidades.

- **Gestor:** responsável pelo planejamento e acompanhamento das operações de transporte. Poderá cadastrar cargas e entregas, atribuir motoristas, informar até duas alternativas de trajeto, consultar recomendações e acompanhar o histórico das entregas.

- **Motorista:** responsável pela execução do transporte. Poderá consultar as entregas atribuídas, visualizar informações da carga e do trajeto e atualizar o status da entrega.

## Funcionalidades principais

- autenticação e controle de acesso por perfil;
- cadastro e gerenciamento de usuários;
- cadastro de cargas e entregas;
- atribuição de entregas a motoristas;
- consulta de temperatura prevista;
- registro e comparação de até duas alternativas de trajeto;
- recomendação indicativa de trajetos;
- atualização do status das entregas;
- histórico de entregas realizadas.

## Stack tecnológica

- **Back-end:** Python;
- **Framework:** Django + Django REST Framework;
- **Banco de dados:** PostgreSQL;
- **Front-end:** React + TypeScript;
- **Clima:** Open-Meteo;
- **Versionamento:** Git + GitHub.

## Especificações iniciais

- aplicação web acessível por navegador;
- interface responsiva para computadores e dispositivos móveis;
- suporte a múltiplos usuários;
- dois perfis com permissões específicas de acesso;
- dados associados aos usuários e às operações realizadas;
- persistência dos dados em PostgreSQL;
- integração com serviço de previsão de temperatura;
- comparação de trajetos com distância e tempo informados manualmente;
- acompanhamento do transporte e histórico das entregas.

## Equipe e papéis da Release 1

| Integrante | Papel |
|---|---|
| José Araujo Agra Neto | Product Owner / DevOps |
| João Paulo de Araujo | Scrum Master |
| Lethycia Zenaide Queiroz Melo | QA |

### Responsabilidades

- **Product Owner (PO):** responsável por definir e priorizar os requisitos do produto, organizar o backlog e validar as funcionalidades desenvolvidas conforme os critérios de aceitação.

- **Scrum Master (SM):** responsável por acompanhar o andamento das sprints, facilitar a comunicação entre os integrantes e auxiliar na resolução de impedimentos.

- **Quality Assurance (QA):** responsável por planejar e acompanhar os testes, verificar os critérios de aceitação, registrar falhas e acompanhar suas correções, contribuindo para a qualidade das entregas.

- **DevOps:** responsável por organizar os ambientes de desenvolvimento, apoiar a integração do código, manter o versionamento e acompanhar os processos de build, testes e implantação.

Todos os integrantes também poderão participar do desenvolvimento e das revisões das funcionalidades, conforme as necessidades de cada sprint.

## Organização do projeto

O desenvolvimento será realizado em sprints, utilizando o GitHub para versionamento do código e Jira para gerenciamento das atividades. A equipe seguirá os critérios estabelecidos no Plano de Qualidade, Plano de Testes e Definition of Done (DoD) para acompanhar e validar as entregas.

## Executar localmente

O Django serve a interface React compilada e a API em `http://localhost:8000`, usando PostgreSQL local. Veja a preparação do ambiente, a criação de contas e o comando `iniciar.ps1` no [guia de implementação](README_IMPLEMENTACAO_SPRINT1.md).

## Status

Projeto em fase inicial de definição e organização da Release 1.
