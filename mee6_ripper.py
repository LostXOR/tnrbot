import requests, json

guildID = input("Guild ID: ")
db = {guildID:{"users":{}}}
url = f"https://mee6.xyz/api/plugins/levels/leaderboard/{guildID}?page="

index = 0
while True:
    print(f"Requesting page {index}")
    response = requests.get(url + str(index)).json()
    if len(response["players"]) == 0:
        break
    for user in response["players"]:
        db[guildID]["users"][user["id"]] = {"xp": user["xp"], "lastxp": 0}
    index += 1

with open("db.json", "w") as file:
    file.write(json.dumps(db))
print("Done")