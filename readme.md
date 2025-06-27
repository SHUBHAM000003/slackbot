# 🤖 Slack Bot for Daily Updates (with MySQL)

![Python](https://img.shields.io/badge/python-3.10-blue.svg)
![Slack Bot](https://img.shields.io/badge/slack--api-socket--mode-green)
![MySQL](https://img.shields.io/badge/database-mysql-yellow)
![Status](https://img.shields.io/badge/status-working-brightgreen)


This Slack bot interacts with users in DMs, lets them opt into daily updates, and sends a scheduled message at 9 PM every day. Preferences are stored in a MySQL database.

## 🔧 Features

- Responds to @mentions
- Listens to direct messages (`yes`/`no`)
- Stores user preferences in MySQL
- Sends daily scheduled messages at 9 PM
- Supports `/crawling_updates` slash command

## 💻 Tech Stack

- Python
- Slack Bolt SDK
- MySQL
- schedule (Python scheduler)
- Hosted locally (can deploy to AWS or Render)

## 📦 Setup Instructions

1. Clone this repo:
   ```bash
   git clone https://github.com/yourusername/slackbot-assignment.git
   cd slackbot-assignment
