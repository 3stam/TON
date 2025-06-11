import React, { useEffect } from 'react';
import { TonConnectUIProvider, TonConnectButton, useTonConnectUI } from '@tonconnect/ui-react';

export const TonConnectButtonComponent = ({ onWalletChange }: { onWalletChange: (address: string) => void }) => {
  const [tonConnectUI] = useTonConnectUI();

  useEffect(() => {
    tonConnectUI.onStatusChange(wallet => {
      if (wallet && wallet.account?.address) {
        onWalletChange(wallet.account.address);
      }
    });
  }, []);

  return (
    <TonConnectUIProvider manifestUrl="https://yourdomain.com/tonconnect-manifest.json">
      <TonConnectButton />
    </TonConnectUIProvider>
  );
};

export const TonConnectButton = TonConnectButtonComponent;