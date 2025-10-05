<div align="center">
  <img src="logo.png" alt="Odyssey Logo" width="200" height="200">
  
  # Odyssey: Helper Functions / Services
  
  *Embark on an epic adventure to master Bitcoin and unlock the future of finance*

[![Download on the App Store](https://img.shields.io/badge/Download_on_the_App_Store-007AFF?style=for-the-badge&logo=app-store&logoColor=white)](https://apps.apple.com/us/app/odyssey-your-bitcoin-journey/id6749882142)
[![Get it on Google Play](https://img.shields.io/badge/Get_it_on_Google_Play-414141?style=for-the-badge&logo=google-play&logoColor=white)](https://play.google.com/store/apps/details?id=com.odyssey.odysseybtcapp&hl=en_US)

</div>

> **Transparency Tools for the Odyssey Bitcoin Learning App**

This repository contains helper functions and utilities that power the **Odyssey** mobile Bitcoin learning app, designed to provide complete transparency into how the app operates and sources its data.

## 🎯 About Odyssey

**Odyssey** is a mobile Bitcoin learning app designed to bridge the knowledge gap for beginners unfamiliar with Bitcoin. It guides users through an educational "journey" with interactive tools and resources, emphasizing fun, accessible learning over complex jargon or trading hype. The app focuses on building foundational knowledge through features like Bitcoin history, real-time price tracking, daily motivational quotes, quizzes, and a glossary, while encouraging long-term engagement for "regular common folk" curious about Bitcoin.

## 🔧 What's Inside

This repository contains the backend utilities that power key features of the Odyssey app:

### 📊 Bitcoin Price Tracking
- **`fetch_bitcoin_price_coingecko.py`** - Fetches real-time Bitcoin price data from CoinGecko API
- **`fetch_bitcoin_price_coinmarket.py`** - Alternative Bitcoin price fetching from CoinMarketCap API
- Both scripts store price data in Supabase for the app to display current Bitcoin prices and 24-hour changes

### 💭 Daily BitThoughts
- **`send_daily_bitthought.py`** - Powers the "Captain's Log" feature by:
  - Fetching daily motivational Bitcoin quotes from a curated collection
  - Sending push notifications to users with the daily bitthought
  - Managing the rotation of quotes to ensure users get fresh content daily

## 🌟 Why Transparency Matters

We believe in complete transparency when it comes to Bitcoin education. This repository allows anyone to:

- **Verify Data Sources** - See exactly where Bitcoin price data comes from
- **Audit Quote Collections** - Review the motivational content being shared
- **Understand Operations** - Know how often data is updated and how the system works
- **Contribute** - Suggest improvements or report issues with data sources

## 🔗 Related Repos

- **[Odyssey Resources](https://github.com/HRZN-BTC/Odyssey-Resources)** - Educational resources on Bitcoin
- **[Daily BitThought](https://github.com/HRZN-BTC/Daily-BitThought)** - Source of motivational quotes


## 🪙 Donations

If you enjoy HRZN's projects and want to support our continued development, you can contribute Bitcoin directly to help us grow and maintain our tools. Any contribution, large or small, is greatly appreciated and helps fund ongoing innovation:

Bitcoin Wallet Address: `bc1q8w4hs02l3vnyx95hanuc2lyzpvk97ty2fh5ng2`

Your support enables us to keep building educational, secure, and user-friendly Bitcoin tools for beginners and enthusiasts alike.

---

*Built with ⚡ for Bitcoin education and transparency* 🚢
