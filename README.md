# Keyboard Scraper

## Overview
`Keyboard Scraper` is a Node.js application designed to extract keyboard product data from various websites and store it in a SQLite database. It is the backend data collection tool for the **Keyboard Finder** platform.

## Features
- Scrapes product data, including names, prices, and descriptions.
- Stores the extracted data in a SQLite database (`keyboards.db`).
- Designed to work seamlessly with the [`keyboard-api`](https://github.com/yourusername/keyboard-api).

## Technologies
- **Node.js**
- **SQLite**
- **Cheerio / Puppeteer** (adjust based on your scraper libraries)

## Usage
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/keyboard-scraper.git
   cd keyboard-scraper
