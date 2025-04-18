import fastapi

accounts = []
messages = []

app = fastapi.FastAPI()

@app.post("/signup")
def signup(username: str, password: str):
    for account in accounts:
        if account["username"] == username:
            return {"error": "invalid username"}
    accounts.append({"username": username, "password": password, "messages": [], "number": 10, "points": 0})
    return {"username": username}


@app.post("/login")
def login(username: str, password: str):
    found = False
    for user in accounts:
        if user["username"] == username:
            found = True
            break
    if not found:
        return {"error": "invalid username"}
    else:
        return {"username": username}


@app.post("/send/original")
def sendmessage(username: str, message: str):
    # Find the account by username
    account = next((user for user in accounts if user["username"] == username), None)
    if account is None:
        return {"error": "User not found"}

    # Check if the user has remaining message slots
    if account["number"] <= 0:
        return {"error": "sent 10 messages already"}
    else:
        if message not in messages:
            account["messages"].append(message)
            messages.append(message)
            account["number"] -= 1
            return {"message": "Message sent!"}
        else:
            return {"error": "unoriginal message"}


@app.post("/send/copy")
def send_copy(username: str, message: str):
    # Find the account by username
    account = next((user for user in accounts if user["username"] == username), None)
    if account is None:
        return {"error": "User not found"}

    # Check if the message exists and is original
    if message not in messages:
        return {"error": "Message not found"}

    # Award points to the original sender only
    for user in accounts:
        if message in user["messages"]:
            # Only award points to the user who originally sent the message
            if user["username"] == username:
                user["points"] += 1
                return {"message": "Message copied, points awarded to the original sender!"}
    return {"error": "Message not found in any user's sent messages"}


@app.post("/buy")
def buy(username: str):
    # Find the account by username
    account = next((user for user in accounts if user["username"] == username), None)
    if account is None:
        return {"error": "User not found"}

    # Allow the user to buy a message slot if they have enough points
    if account["points"] >= 100:
        account["points"] -= 100
        account["number"] += 1
        return {"message": "Message slot purchased!"}
    else:
        return {"message": "Not enough points"}


@app.get("/messages")
def get_messages():
    return {"messages":messages}
