import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import yfinance as yf  # For fetching real stock data (if available)
import requests
from PIL import Image
import os
import base64
import matplotlib.pyplot as plt

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sahm - Stock Search</title>
    <style>
        :root {
            --primary: #006064;
            --secondary: #00acc1;
            --accent: #e0f7fa;
            --text: #263238;
            --background: #f5f5f5;
            --white: #ffffff;
            --error: #d32f2f;
            --success: #388e3c;
            --warning: #f57c00;
            --info: #1976d2;
            --chart-up: #4caf50;
            --chart-down: #f44336;
        }
       
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
       
        body {
            background-color: var(--background);
            color: var(--text);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
       
        .navbar {
            background-color: var(--primary);
            color: var(--white);
            padding: 1rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
       
        .logo {
            display: flex;
            align-items: center;
            font-size: 1.5rem;
            font-weight: bold;
        }
       
        .logo-icon {
            margin-right: 0.5rem;
            font-size: 1.8rem;
        }
       
        .nav-links {
            display: flex;
            gap: 1.5rem;
        }
       
        .nav-links a {
            color: var(--white);
            text-decoration: none;
            font-weight: 500;
            padding: 0.5rem;
            border-radius: 4px;
            transition: background-color 0.3s;
        }
       
        .nav-links a:hover {
            background-color: rgba(255,255,255,0.1);
        }
       
        .container {
            flex: 1;
            padding: 2rem;
            max-width: 1200px;
            margin: 0 auto;
        }
       
        .card {
            background-color: var(--white);
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            padding: 2rem;
            margin-bottom: 2rem;
        }
       
        .card-title {
            color: var(--primary);
            margin-bottom: 1.5rem;
            font-size: 1.75rem;
            text-align: center;
        }
       
        .search-container {
            display: flex;
            margin-bottom: 2rem;
        }
       
        .search-input {
            flex: 1;
            padding: 0.75rem;
            border: 1px solid #ccc;
            border-radius: 4px 0 0 4px;
            font-size: 1rem;
        }
       
        .search-btn {
            background-color: var(--primary);
            color: var(--white);
            border: none;
            border-radius: 0 4px 4px 0;
            padding: 0.75rem 1.5rem;
            font-size: 1rem;
            font-weight: 500;
            cursor: pointer;
            transition: background-color 0.3s;
        }
       
        .search-btn:hover {
            background-color: var(--secondary);
        }
       
        .stock-header {
            display: flex;
            align-items: center;
            margin-bottom: 2rem;
        }
       
        .stock-info {
            flex: 1;
        }
       
        .stock-name {
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }
       
        .stock-meta {
            display: flex;
            gap: 1.5rem;
            font-size: 0.9rem;
            color: #666;
        }
       
        .stock-price {
            display: flex;
            flex-direction: column;
            align-items: flex-end;
        }
       
        .price-value {
            font-size: 2rem;
            font-weight: 600;
        }
       
        .price-change {
            display: flex;
            align-items: center;
            font-size: 1rem;
            margin-top: 0.25rem;
        }
       
        .positive {
            color: var(--success);
        }
       
        .negative {
            color: var(--error);
        }
       
        .chart-container {
            height: 400px;
            margin-bottom: 2rem;
            position: relative;
            overflow: hidden;
            background-color: var(--white);
            border-radius: 8px;
            padding: 1.5rem;
            border: 1px solid #eee;
        }
       
        .chart-toolbar {
            display: flex;
            justify-content: space-between;
            margin-bottom: 1rem;
        }
       
        .chart-periods {
            display: flex;
            gap: 0.5rem;
        }
       
        .period-btn {
            padding: 0.5rem 1rem;
            background-color: #eee;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.9rem;
            transition: all 0.3s;
        }
       
        .period-btn.active {
            background-color: var(--primary);
            color: var(--white);
        }
       
        .chart-indicators {
            display: flex;
            gap: 0.5rem;
        }
       
        .indicator-btn {
            padding: 0.5rem;
            background-color: #eee;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.9rem;
            transition: all 0.3s;
        }
       
        .indicator-btn:hover {
            background-color: #ddd;
        }
       
        /* Candlestick chart simulation */
        .candlestick-chart {
            height: 300px;
            display: flex;
            align-items: flex-end;
            padding: 20px 0;
            position: relative;
        }
       
        .price-axis {
            position: absolute;
            top: 0;
            bottom: 0;
            right: 0;
            width: 60px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            padding: 20px 0;
            font-size: 0.8rem;
            color: #666;
        }
       
        .candle {
            width: 16px;
            position: relative;
            margin: 0 6px;
        }
       
        .candle-wick {
            position: absolute;
            width: 2px;
            background-color: #333;
            left: 50%;
            transform: translateX(-50%);
        }
       
        .candle-body {
            width: 100%;
            position: absolute;
            border-radius: 1px;
        }
       
        .candle-up .candle-body {
            background-color: var(--chart-up);
        }
       
        .candle-down .candle-body {
            background-color: var(--chart-down);
        }
       
        .time-axis {
            display: flex;
            justify-content: space-between;
            padding: 0 30px;
            margin-top: 10px;
            font-size: 0.8rem;
            color: #666;
        }
       
        .stock-details {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 2rem;
            margin-bottom: 2rem;
        }
       
        .detail-card {
            background-color: var(--white);
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            padding: 1.5rem;
            border: 1px solid #eee;
        }
       
        .detail-title {
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 1rem;
            color: var(--primary);
            border-bottom: 2px solid var(--accent);
            padding-bottom: 0.5rem;
        }
       
        .detail-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
        }
       
        .detail-item {
            margin-bottom: 0.75rem;
        }
       
        .detail-label {
            font-size: 0.85rem;
            color: #666;
            margin-bottom: 0.25rem;
        }
       
        .detail-value {
            font-size: 1rem;
            font-weight: 500;
        }
       
        .company-info {
            line-height: 1.6;
        }
       
        .download-section {
            margin-top: 1.5rem;
        }
       
        .download-title {
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 1rem;
            color: var(--primary);
        }
       
        .download-links {
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
        }
       
        .download-link {
            display: flex;
            align-items: center;
            text-decoration: none;
            color: var(--info);
            font-size: 0.9rem;
            padding: 0.5rem;
            border-radius: 4px;
            transition: background-color 0.3s;
        }
       
        .download-link:hover {
            background-color: var(--accent);
        }
       
        .download-icon {
            margin-right: 0.5rem;
        }
       
        .similar-stocks {
            margin-top: 2rem;
        }
       
        .similar-title {
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 1rem;
            color: var(--primary);
        }
       
        .similar-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 1rem;
        }
       
        .similar-card {
            background-color: var(--white);
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            padding: 1rem;
            border: 1px solid #eee;
            transition: transform 0.3s, box-shadow 0.3s;
            cursor: pointer;
        }
       
        .similar-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
       
        .similar-name {
            font-size: 1rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }
       
        .similar-meta {
            display: flex;
            justify-content: space-between;
            font-size: 0.85rem;
        }
       
        .similar-price {
            font-weight: 500;
        }
       
        .footer {
            background-color: var(--primary);
            color: var(--white);
            text-align: center;
            padding: 1rem;
            margin-top: auto;
        }
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="logo">
            <span class="logo-icon">
                <svg class="icon" viewBox="0 0 24 24">
                    <path d="M21,18V19H3V18H21M3,5H21V17H3V5M5,7V15H11V7H5M13,7V15H19V7H13Z"/>
                </svg>
            </span>
            <span>Sahm</span>
        </div>
        <div class="nav-links">
            <a href="#" id="portfolio-link">My Portfolio</a>
            <a href="#" id="stocks-link" class="active">Stocks</a>
            <a href="#" id="education-link">Education</a>
            <a href="#" id="logout-link">Logout</a>
        </div>
    </nav>
   
    <div class="container">
        <div class="card">
            <h2 class="card-title">Stock Search</h2>
           
            <div class="search-container">
                <input type="text" class="search-input" placeholder="Search for a stock (e.g., Attijariwafa Bank, Maroc Telecom)" value="Attijariwafa Bank">
                <button class="search-btn">Search</button>
            </div>
           
            <div class="stock-header">
                <div class="stock-info">
                    <div class="stock-name">Attijariwafa Bank (ATW)</div>
                    <div class="stock-meta">
                        <span>Casablanca Stock Exchange</span>
                        <span>Banking Sector</span>
                        <span>Updated: May 06, 2025, 14:30</span>
                    </div>
                </div>
                <div class="stock-price">
                    <div class="price-value">500.50 MAD</div>
                    <div class="price-change positive">
                        <svg viewBox="0 0 24 24" width="18" height="18">
                            <path fill="currentColor" d="M7,15L12,10L17,15H7Z" />
                        </svg>
                        <span>+4.00 (+0.80%)</span>
                    </div>
                </div>
            </div>
           
            <div class="chart-toolbar">
                <div class="chart-periods">
                    <button class="period-btn">1D</button>
                    <button class="period-btn">1W</button>
                    <button class="period-btn active">1M</button>
                    <button class="period-btn">3M</button>
                    <button class="period-btn">6M</button>
                    <button class="period-btn">1Y</button>
                    <button class="period-btn">5Y</button>
                </div>
                <div class="chart-indicators">
                    <button class="indicator-btn">Moving Average</button>
                    <button class="indicator-btn">Volume</button>
                    <button class="indicator-btn">RSI</button>
                </div>
            </div>
           
            <div class="chart-container">
                <div class="candlestick-chart">
                    <div class="price-axis">
                        <div>510 MAD</div>
                        <div>505 MAD</div>
                        <div>500 MAD</div>
                        <div>495 MAD</div>
                        <div>490 MAD</div>
                    </div>
                   
                    <!-- Simulated candlestick chart for demo purposes -->
                    <div class="candle candle-up" style="height: 100px; margin-left: 40px;">
                        <div class="candle-wick" style="height: 80px; bottom: 20px;"></div>
                        <div class="candle-body" style="height: 40px; bottom: 40px;"></div>
                    </div>
                    <div class="candle candle-down" style="height: 100px;">
                        <div class="candle-wick" style="height: 70px; bottom: 30px;"></div>
                        <div class="candle-body" style="height: 35px; bottom: 30px;"></div>
                    </div>
                    <div class="candle candle-down" style="height: 100px;">
                        <div class="candle-wick" style="height: 90px; bottom: 10px;"></div>
                        <div class="candle-body" style="height: 50px; bottom: 10px;"></div>
                    </div>
                    <div class="candle candle-up" style="height: 100px;">
                        <div class="candle-wick" style="height: 100px; bottom: 0px;"></div>
                        <div class="candle-body" style="height: 60px; bottom: 20px;"></div>
                    </div>
                    <div class="candle candle-up" style="height: 100px;">
                        <div class="candle-wick" style="height: 90px; bottom: 10px;"></div>
                        <div class="candle-body" style="height: 45px; bottom: 35px;"></div>
                    </div>
                    <div class="candle candle-down" style="height: 100px;">
                        <div class="candle-wick" style="height: 75px; bottom: 25px;"></div>
                        <div class="candle-body" style="height: 30px; bottom: 25px;"></div>
                    </div>
                    <div class="candle candle-down" style="height: 100px;">
                        <div class="candle-wick" style="height: 65px; bottom: 35px;"></div>
                        <div class="candle-body" style="height: 25px; bottom: 35px;"></div>
                    </div>
                    <div class="candle candle-up" style="height: 100px;">
                        <div class="candle-wick" style="height: 85px; bottom: 15px;"></div>
                        <div class="candle-body" style="height: 50px; bottom: 15px;"></div>
                    </div>
                    <div class="candle candle-up" style="height: 100px;">
                        <div class="candle-wick" style="height: 95px; bottom: 5px;"></div>
                        <div class="candle-body" style="height: 55px; bottom: 25px;"></div>
                    </div>
                    <div class="candle candle-up" style="height: 100px;">
                        <div class="candle-wick" style="height: 100px; bottom: 0px;"></div>
                        <div class="candle-body" style="height: 65px; bottom: 15px;"></div>
                    </div>
                    <div class="candle candle-down" style="height: 100px;">
                        <div class="candle-wick" style="height: 80px; bottom: 20px;"></div>
                        <div class="candle-body" style="height: 30px; bottom: 40px;"></div>
                    </div>
                    <div class="candle candle-down" style="height: 100px;">
                        <div class="candle-wick" style="height: 70px; bottom: 30px;"></div>
                        <div class="candle-body" style="height: 25px; bottom: 30px;"></div>
                    </div>
                    <div class="candle candle-up" style="height: 100px;">
                        <div class="candle-wick" style="height: 90px; bottom: 10px;"></div>
                        <div class="candle-body" style="height: 40px; bottom: 30px;"></div>
                    </div>
                    <div class="candle candle-up" style="height: 100px;">
                        <div class="candle-wick" style="height: 90px; bottom: 10px;"></div>
                        <div class="candle-body" style="height: 45px; bottom: 30px;"></div>
                    </div>
                    <div class="candle candle-up" style="height: 100px;">
                        <div class="candle-wick" style="height: 95px; bottom: 5px;"></div>
                        <div class="candle-body" style="height: 50px; bottom: 25px;"></div>
                    </div>
                </div>
                <div class="time-axis">
                    <div>April 15</div>
                    <div>April 20</div>
                    <div>April 25</div>
                    <div>April 30</div>
                    <div>May 5</div>
                </div>
            </div>
           
            <div class="stock-details">
                <div class="detail-card">
                    <h3 class="detail-title">Trading Data</h3>
                    <div class="detail-grid">
                        <div class="detail-item">
                            <div class="detail-label">Opening Price</div>
                            <div class="detail-value">498.00 MAD</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Previous Close</div>
                            <div class="detail-value">496.50 MAD</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Day High</div>
                            <div class="detail-value">502.30 MAD</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Day Low</div>
                            <div class="detail-value">497.40 MAD</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Trading Volume</div>
                            <div class="detail-value">45,728</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Trading Value</div>
                            <div class="detail-value">22.9 million MAD</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">52-Week High</div>
                            <div class="detail-value">520.00 MAD</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">52-Week Low</div>
                            <div class="detail-value">470.10 MAD</div>
                        </div>
                    </div>
                </div>
               
                <div class="detail-card">
                    <h3 class="detail-title">Fundamentals</h3>
                    <div class="detail-grid">
                        <div class="detail-item">
                            <div class="detail-label">Market Cap</div>
                            <div class="detail-value">104.6 billion MAD</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Shares Outstanding</div>
                            <div class="detail-value">209.9 million</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Earnings Per Share</div>
                            <div class="detail-value">48.25 MAD</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">P/E Ratio</div>
                            <div class="detail-value">10.38</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Dividend Yield</div>
                            <div class="detail-value">4.2%</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Book Value</div>
                            <div class="detail-value">415.30 MAD</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Price/Book</div>
                            <div class="detail-value">1.21</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Return on Assets</div>
                            <div class="detail-value">1.8%</div>
                        </div>
                    </div>
                </div>
               
                <div class="detail-card">
                    <h3 class="detail-title">Company Overview</h3>
                    <div class="company-info">
                        <p>Attijariwafa Bank is the largest bank in Morocco by assets and market capitalization. Founded in 1904, it has a presence in over 25 countries, primarily in Africa, Europe, and the Middle East.</p>
                        <p>The bank provides a comprehensive range of commercial and investment banking and insurance services to individuals and companies, and is a leader in digital banking transformation in the region.</p>
                    </div>
                   
                    <div class="download-section">
                        <h4 class="download-title">Financial Reports</h4>
                        <div class="download-links">
                            <a href="#" class="download-link">
                                <svg class="download-icon" viewBox="0 0 24 24" width="18" height="18">
                                    <path fill="currentColor" d="M5,20H19V18H5M19,9H15V3H9V9H5L12,16L19,9Z" />
                                </svg>
                                2024 Annual Report
                            </a>
                            <a href="#" class="download-link">
                                <svg class="download-icon" viewBox="0 0 24 24" width="18" height="18">
                                    <path fill="currentColor" d="M5,20H19V18H5M19,9H15V3H9V9H5L12,16L19,9Z" />
                                </svg>
                                Q1 2025 Report
                            </a>
                            <a href="#" class="download-link">
                                <svg class="download-icon" viewBox="0 0 24 24" width="18" height="18">
                                    <path fill="currentColor" d="M5,20H19V18H5M19,9H15V3H9V9H5L12,16L19,9Z" />
                                </svg>
                                Investor Presentation (Q1 2025)
                            </a>
                        </div>
                    </div>
                </div>
            </div>
           
            <div class="similar-stocks">
                <h3 class="similar-title">Similar Stocks in the Same Sector</h3>
                <div class="similar-grid">
                    <div class="similar-card">
                        <div class="similar-name">Bank of Africa (BOA)</div>
                        <div class="similar-meta">
                            <span>Banking</span>
                            <span class="similar-price positive">205.10 MAD (+1.2%)</span>
                        </div>
                    </div>
                    <div class="similar-card">
                        <div class="similar-name">Banque Centrale Populaire (BCP)</div>
                        <div class="similar-meta">
                            <span>Banking</span>
                            <span class="similar-price positive">272.50 MAD (+0.6%)</span>
                        </div>
                    </div>
                    <div class="similar-card">
                        <div class="similar-name">Crédit du Maroc (CDM)</div>
                        <div class="similar-meta">
                            <span>Banking</span>
                            <span class="similar-price negative">628.00 MAD (-0.3%)</span>
                        </div>
                    </div>
                    <div class="similar-card">
                        <div class="similar-name">BMCI</div>
                        <div class="similar-meta">
                            <span>Banking</span>
                            <span class="similar-price positive">785.50 MAD (+0.2%)</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
   
    <footer class="footer">
        <p>Sahm ©️ 2025 - Moroccan Investment Platform</p>
    </footer>

    <script>
        // Simple period button functionality
        document.querySelectorAll('.period-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                // Remove active class from all period buttons
                document.querySelectorAll('.period-btn').forEach(b => b.classList.remove('active'));
               
                // Add active class to clicked button
                btn.classList.add('active');
               
                // In a real application, this would update the chart data based on the selected period
                alert('Chart will be updated for period: ' + btn.textContent);
            });
        });
       
        // Simple indicator button functionality
        document.querySelectorAll('.indicator-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                // Toggle active class on indicator buttons
                btn.classList.toggle('active');
               
                // In a real application, this would toggle the display of the selected indicator
                alert('Toggling indicator display: ' + btn.textContent);
            });
        });
       
        // Similar stock card functionality
        document.querySelectorAll('.similar-card').forEach(card => {
            card.addEventListener('click', () => {
                const stockName = card.querySelector('.similar-name').textContent.split('(')[0].trim();
                alert('Loading data for: ' + stockName);
            });
        });
    </script>
</body>
</html>
