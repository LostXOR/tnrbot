"""Rip level data from MEE6 leaderboards. Useful if you're moving on from MEE6."""

import sqlite3
import requests
import config

guild_id = input("Guild ID: ")
url = f"https://mee6.xyz/api/plugins/levels/leaderboard/{guild_id}?page="
db = sqlite3.connect(config.DATABASE_PATH, isolation_level = None)
cursor = db.cursor()
query = f"CREATE TABLE IF NOT EXISTS '{guild_id}' (id, xp, lastxptime, cachedname, UNIQUE(id))"
cursor.execute(query)

index = 0 # pylint: disable=C0103
while True:
    print(f"Requesting page {index}")
    response = requests.get(url + str(index)).json()

    if len(response["players"]) == 0:
        break
    for user in response["players"]:
        cursor.execute(f"INSERT OR REPLACE INTO '{guild_id}' VALUES (?, ?, ?, ?)", [
            int(user["id"]),
            user["xp"],
            0,
            user["username"]
        ])
    index += 1

db.close()
print("Done")
