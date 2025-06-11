import React, { useState } from 'react';
import { TonConnectButton } from './tonconnect/TonConnectButton';

export default function App() {
  const [amount, setAmount] = useState('');
  const [wallet, setWallet] = useState('');

  const handleStake = async () => {
    const response = await fetch('http://localhost:8000/stake', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_wallet: wallet, amount: parseFloat(amount) })
    });
    const data = await response.json();
    alert(JSON.stringify(data));
  };

  return (
    <div>
      <h1>TON Staking DApp (Test)</h1>
      <TonConnectButton onWalletChange={setWallet} />
      <input type="number" value={amount} onChange={e => setAmount(e.target.value)} placeholder="Amount" />
      <button onClick={handleStake}>Stake</button>
    </div>
  );
}