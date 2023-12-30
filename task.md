2) Develop a Telegram bot that monitors our reward distribution process and sends daily statistics to our group.

Bot Functionality:
- The bot reads events from the contract that occurred in the last 24 hours.

Contract Details:
- Contract Link: [https://etherscan.io/address/0xaBE235136562a5C2B02557E1CaE7E8c85F2a5da0](https://etherscan.io/address/0xaBE235136562a5C2B02557E1CaE7E8c85F2a5da0)
- Event of Interest: TotalDistribution (Refer to the transaction example: [https://etherscan.io/tx/0x0c5be95b537942b1f0f2e2cfb459d974bb419faa4877d5074d7fd025b563188c#eventlog](https://etherscan.io/tx/0x0c5be95b537942b1f0f2e2cfb459d974bb419faa4877d5074d7fd025b563188c#eventlog))

Requirements:
- Calculate and send the daily sum of all four parameters through the bot to a Telegram chat.
- The bot should not only listen for messages but also fetch history, as it may not operate continuously (e.g., during reboots) and should be able to backfill history, especially on the first launch.
- Ideally, record all events in a PostgreSQL database for future statistical analysis and report generation.
- Generate and send reports every four hours.

Example Report Format:
```
Daily $AIX Stats:
        - First TX: 23h50m ago
        - Last TX: 1h30m ago
        - AIX processed: 2,068,102.33
        - AIX distributed: 79,473.32
        - ETH bought: 149.71
        - ETH distributed: 149.71
        
        Distributor wallet: 0x9A0A9594Aa626EE911207DC001f535c9eb590b34
        Distributor balance: 2.5 ETH
```
(Feel free to ask GPT-4 for a draft of the code for this task.)