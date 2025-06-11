
# TON Staking Web App (Test)

## Backend (FastAPI)

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

## Frontend (React + Vite)

```bash
cd frontend
npm install
npm run dev
```

## Notes

- Uses 30 seconds as test cycle for 28 days
- Replace manifest URL and DEV_WALLET address before going live
- Simulated TON transactions (use real TonConnect SDK for live)
