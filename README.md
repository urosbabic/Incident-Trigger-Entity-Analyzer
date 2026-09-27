---
title: Incident Trigger Entity Analyzer
description: GitHub Actions validation for the Microsoft Sentinel incident entity analyzer playbook.
---

## Playbook

This repository contains the ARM deployment template for the [Incident-Trigger-Entity-Analyzer](https://github.com/Azure/Azure-Sentinel/tree/master/Solutions/SentinelSOARessentials/Playbooks/Incident-Trigger-Entity-Analyzer) Microsoft Sentinel playbook.

The Logic App analyzes URL and user entities from new incidents using Microsoft Sentinel and Sentinel MCP API connections.

## GitHub Actions

The `Validate Sentinel playbook` workflow runs on pushes and pull requests targeting `main`, and can also be started manually. It checks that the ARM template is valid JSON and that the expected incident trigger, entity analysis actions, and API connections are present.

These checks do not deploy or execute the Logic App. Runtime execution requires an Azure deployment, authenticated API connections, and a Sentinel workspace.

## Azure resources

The template creates a Logic App and two API connection resources. After deployment, authenticate the Microsoft Sentinel and Sentinel MCP connections before enabling the playbook for incident processing.

The default Logic App name is `Entity-Analyzer-Incident-Trigger`; set the `PlaybookName` parameter to a unique value when deploying a test instance.