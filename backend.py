from pydantic import BaseModel
import fastapi
class UserCredentials(BaseModel):
    username: str
    password: str

class MessageData(BaseModel):
    username: str
    message: str

class UserOnly(BaseModel):
    username: str


accounts = []
messages = []
app = fastapi.FastAPI()

@app.post("/signup")
def signup(credentials: UserCredentials):
    for account in accounts:
        if account["username"] == credentials.username:
            return {"error": "invalid username"}
    accounts.append({"username": credentials.username, "password": credentials.password, "messages": [], "number": 10, "points": 0})
    return {"username": credentials.username}

@app.post("/login")
def login(credentials: UserCredentials):
    found = False
    for user in accounts:
        if user["username"] == credentials.username:
            found = True
            break
    if not found:
        return {"error": "invalid username"}
    else:
        return {"username": credentials.username}

@app.post("/send/original")
def sendmessage(data: MessageData):
    account = next((user for user in accounts if user["username"] == data.username), None)
    if account is None:
        return {"error": "User not found"}
    if account["number"] <= 0:
        return {"error": "sent 10 messages already"}
    else:
        if data.message not in messages:
            account["messages"].append(data.message)
            messages.append(data.message)
            account["number"] -= 1
            return {"message": "Message sent!"}
        else:
            return {"error": "unoriginal message"}

@app.post("/send/copy")
def send_copy(data: MessageData):
    account = next((user for user in accounts if user["username"] == data.username), None)
    if account is None:
        return {"error": "User not found"}
    if data.message not in messages:
        return {"error": "Message not found"}

    for user in accounts:
        if data.message in user["messages"]:
            if user["username"] == data.username:
                user["points"] += 1
                return {"message": "Message copied, points awarded to the original sender!"}
    return {"error": "Message not found in any user's sent messages"}

@app.post("/buy")
def buy(user: UserOnly):
    account = next((acc for acc in accounts if acc["username"] == user.username), None)
    if account is None:
        return {"error": "User not found"}

    if account["points"] >= 100:
        account["points"] -= 100
        account["number"] += 1
        return {"message": "Message slot purchased!"}
    else:
        return {"message": "Not enough points"}
while True:
    for message in messages:
        print(message)

@app.get("/messages")
def get_messages():
    return {"messages": messages}
