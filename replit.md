# Telegram Auto-Delete Bot

## Overview

This project is a Telegram bot designed to automatically delete join/leave messages in group chats. The bot is built using Python with the python-telegram-bot library and includes a Flask web server for uptime monitoring on the Replit platform.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Core Architecture
- **Bot Framework**: Python-telegram-bot library for Telegram API integration
- **Web Server**: Flask server for health checks and uptime maintenance
- **Platform**: Designed for deployment on Replit with automatic uptime monitoring
- **Concurrency**: Threading-based architecture for running Flask server alongside bot

### Key Design Decisions
- **Uptime Strategy**: Uses Flask web server with periodic self-pinging to maintain Replit instance alive
- **Security**: Environment variable-based token management for secure bot authentication
- **Logging**: Comprehensive logging system for monitoring bot operations and debugging
- **Error Handling**: Try-catch blocks around critical operations to prevent bot crashes

## Key Components

### 1. Telegram Bot Handler
- **Purpose**: Handles incoming Telegram messages and commands
- **Key Functions**: 
  - Auto-deletion of join/leave messages
  - Command processing (/start, /help, /status)
  - Message filtering and processing

### 2. Flask Web Server
- **Purpose**: Provides HTTP endpoints for uptime monitoring
- **Endpoints**:
  - `/` - Main health check endpoint
  - `/health` - Additional health status endpoint
- **Port**: Runs on port 5000 (configurable for Replit)

### 3. Uptime Maintenance System
- **Self-Ping Mechanism**: Periodic HTTP requests to keep Replit instance active
- **Threading**: Separate thread for Flask server to avoid blocking bot operations
- **Monitoring**: Health status reporting and error logging

## Data Flow

1. **Bot Initialization**: 
   - Load environment variables (bot token)
   - Initialize logging system
   - Start Flask server in background thread

2. **Message Processing**:
   - Receive Telegram updates
   - Filter for join/leave messages
   - Auto-delete matching messages
   - Log operations for monitoring

3. **Uptime Maintenance**:
   - Flask server responds to health checks
   - Periodic self-pinging prevents Replit sleep
   - Error handling for network issues

## External Dependencies

### Required Libraries
- `python-telegram-bot` - Telegram Bot API wrapper
- `flask` - Web framework for uptime server
- `requests` - HTTP client for self-pinging
- `threading` - Built-in Python threading support

### Environment Variables
- `TELEGRAM_BOT_TOKEN` - Bot authentication token from BotFather

### External Services
- **Telegram Bot API** - Core bot functionality
- **Replit Platform** - Hosting and deployment environment

## Deployment Strategy

### Replit-Specific Optimizations
- **Always-On Strategy**: Flask server + self-pinging to prevent instance sleep
- **Port Configuration**: Uses port 5000 for web server (Replit compatible)
- **Environment Management**: Secure token storage via Replit environment variables

### Deployment Steps
1. Set up Telegram bot via BotFather
2. Configure `TELEGRAM_BOT_TOKEN` environment variable in Replit
3. Run main.py to start both bot and web server
4. Replit URL can be used for external uptime monitoring

### Monitoring and Maintenance
- **Health Endpoints**: Multiple endpoints for status checking
- **Comprehensive Logging**: All operations logged with timestamps
- **Error Recovery**: Graceful error handling to maintain bot availability
- **Self-Healing**: Automatic restart capabilities through Replit platform