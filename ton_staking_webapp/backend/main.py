from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
import uuid
import json
import os
import threading
import time

app = FastAPI()

STAKE_FILE = "staking_data.json"
DEV_WALLET = "0QBEufBFrRrUJsKdy4e9XRugBQeKIzu8joLUA4daHnUk3-9F"  # Replace with real dev wallet address
REWARD_PERCENTAGE = 0.30
CYCLE_DURATION = timedelta(seconds=30)  # Simulate 28 days with 30 seconds

def load_stakes():
    if not os.path.exists(STAKE_FILE):
        return {}
    with open(STAKE_FILE, 'r') as f:
        return json.load(f)

def save_stakes(data):
    with open(STAKE_FILE, 'w') as f:
        json.dump(data, f, indent=4)

stakes = load_stakes()

class StakeRequest(BaseModel):
    user_wallet: str
    amount: float

@app.post("/stake")
def stake_tokens(req: StakeRequest):
    stake_id = str(uuid.uuid4())
    now = datetime.utcnow()
    stakes[stake_id] = {
        "user_wallet": req.user_wallet,
        "amount": req.amount,
        "start_time": now.isoformat(),
        "active": True,
        "cycle_start": now.isoformat()
    }
    save_stakes(stakes)
    return {"message": "Stake recorded", "stake_id": stake_id}

@app.post("/unstake/{stake_id}")
def unstake(stake_id: str):
    if stake_id not in stakes:
        raise HTTPException(status_code=404, detail="Stake not found")
    stake = stakes[stake_id]
    if not stake["active"]:
        raise HTTPException(status_code=400, detail="Already unstaked")
    cycle_start = datetime.fromisoformat(stake["cycle_start"])
    if datetime.utcnow() < cycle_start + CYCLE_DURATION:
        raise HTTPException(status_code=400, detail="Cannot unstake before cycle ends")
    stake["active"] = False
    save_stakes(stakes)
    return {"message": "Unstake successful. You may now withdraw your principal."}

@app.get("/status/{stake_id}")
def status(stake_id: str):
    if stake_id not in stakes:
        raise HTTPException(status_code=404, detail="Stake not found")
    return stakes[stake_id]

def reward_worker():
    while True:
        now = datetime.utcnow()
        changed = False
        for stake_id, data in stakes.items():
            if not data["active"]:
                continue
            cycle_start = datetime.fromisoformat(data["cycle_start"])
            if now >= cycle_start + CYCLE_DURATION:
                reward = data["amount"] * REWARD_PERCENTAGE
                print(f"[REWARD] Sent {reward} TON from dev wallet to {data['user_wallet']}")
                data["cycle_start"] = now.isoformat()
                changed = True
        if changed:
            save_stakes(stakes)
        time.sleep(5)

threading.Thread(target=reward_worker, daemon=True).start()
