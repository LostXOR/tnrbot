import requests, sqlite3
import config


guild_id = input("Guild ID: ")
url = f"https://mee6.xyz/api/plugins/levels/leaderboard/{guild_id}?page="
db = sqlite3.connect(config.database_path, isolation_level = None)
cursor = db.cursor()
cursor.execute(f"CREATE TABLE IF NOT EXISTS '{guildID}' (id, xp, lastxptime, cachedname, UNIQUE(id))")

index = 0
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