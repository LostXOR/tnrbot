"""Rip level data from MEE6 leaderboards. Useful if you're moving on from MEE6."""

import sqlite3
import requests
import config

guild_id = input("Guild ID: ")
URL = f"https://mee6.xyz/api/plugins/levels/leaderboard/{guild_id}?page="
db = sqlite3.connect(config.DATABASE_PATH, isolation_level = None)
cursor = db.cursor()
cursor.execute(
    f"CREATE TABLE IF NOT EXISTS '{guild_id}' (id, xp, lastxptime, cachedname, UNIQUE(id))")

index = 0 # pylint: disable=C0103
while True:
    print(f"Requesting page {index}")
    response = requests.get(URL + str(index), timeout = 10).json()

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
