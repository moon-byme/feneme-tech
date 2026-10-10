# Feneme

Sistema web inteligente para gestão de cargas e recomendação de rotas com base em condições climáticas.

## Resumo do projeto

O Feneme é uma aplicação web voltada ao apoio da gestão logística no transporte de alimentos. O sistema reunirá informações sobre cargas, entregas, rotas e condições climáticas para auxiliar no planejamento e acompanhamento dos transportes.

A proposta busca apoiar decisões mais eficientes, considerando fatores como distância, tempo estimado de viagem, temperatura, condições climáticas e características da carga.

## Problema

O transporte de alimentos envolve variáveis como distância, tempo de viagem, temperatura, condições climáticas e características da carga. Atualmente, essas informações nem sempre são analisadas de forma integrada, o que pode levar à escolha de rotas inadequadas. Assim, esse problema afeta gestores, equipes de expedição, transportadores e destinatários, podendo causar atrasos, perda de qualidade dos produtos, descarte de alimentos e prejuízos financeiros.

## Objetivo

Desenvolver um sistema web que auxilie no gerenciamento do transporte de alimentos e na escolha de rotas, considerando informações logísticas e condições climáticas.

## Usuários e perfis de acesso

O Feneme possuirá diferentes perfis de acesso de acordo com a participação de cada usuário no processo de transporte. Cada perfil terá permissões específicas e acesso às funcionalidades relacionadas às suas responsabilidades. Um mesmo usuário poderá possuir mais de um perfil, quando necessário.

- **Administrador:** possui acesso completo ao sistema. É responsável pelo gerenciamento de usuários, perfis de acesso, permissões e parâmetros gerais da plataforma, além de poder acessar as funcionalidades disponíveis aos demais perfis.

- **Gestor:** responsável pelo planejamento e acompanhamento das operações de transporte. Poderá cadastrar cargas e entregas, informar origem e destino, definir características da carga, atribuir transportadores, consultar e comparar rotas e acompanhar o andamento das viagens.

- **Carregador:** atua na etapa anterior ao início do transporte. Poderá consultar cargas programadas, registrar o carregamento, confirmar a saída da carga, informar suas condições iniciais e registrar ocorrências identificadas nessa etapa.

- **Transportador:** responsável pela execução do transporte. Poderá consultar as viagens atribuídas, visualizar informações da carga e a rota recomendada, atualizar o status da viagem e registrar ocorrências durante o percurso.

- **Destinatário:** responsável pelo recebimento da carga. Poderá acompanhar o andamento da entrega, consultar informações do transporte, confirmar o recebimento e registrar ocorrências identificadas na chegada.

## Funcionalidades principais

- autenticação e controle de acesso por perfil;
- cadastro e gerenciamento de usuários;
- cadastro de cargas, veículos e entregas;
- atribuição de entregas a transportadores;
- consulta de condições climáticas;
- visualização e comparação de rotas;
- recomendação de trajetos;
- atualização do status das viagens;
- registro de ocorrências;
- histórico de entregas realizadas.

## Stack tecnológica

- **Back-end:** Python;
- **Framework:** Django + Django REST Framework;
- **Banco de dados:** PostgreSQL;
- **Front-end:** React + TypeScript;
- **Mapas:** Leaflet + OpenStreetMap;
- **Rotas:** OSRM;
- **Clima:** Open-Meteo;
- **Versionamento:** Git + GitHub.

## Especificações iniciais

- aplicação web acessível por navegador;
- interface responsiva para computadores e dispositivos móveis;
- suporte a múltiplos usuários;
- diferentes perfis e permissões de acesso;
- dados associados aos usuários e às operações realizadas;
- persistência dos dados em PostgreSQL;
- integração com serviços de mapas, rotas e dados climáticos;
- acompanhamento do transporte e histórico das entregas.

## Equipe e papéis da Release 1

| Integrante | Papel |
|---|---|
| José Araujo Agra Neto | Product Owner / DevOps |
| João Paulo de Araujo | Scrum Master |
| Lethycia Zenaide Queiroz Melo | QA |

## Organização do projeto

O desenvolvimento será realizado em sprints, utilizando o GitHub para versionamento do código e Jira para gerenciamento das atividades.

## Status

Projeto em fase inicial de definição e organização da Release 1.