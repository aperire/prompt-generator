# Minting/Borrowing zSOL

zSOL is a over collateralized synthetic asset, which can be minted after depositing collateral. Even if the UX is identical to lending protocols, borrowing/repaying is performed as minting/burning zSOL.

The collateral accepted on LP Finance are as follows.

* SOL
* mSOL
* USDC

It is only possible to deposit one collateral per account. To deposit other collateral, account should fully withdraw collateral.

Once an account borrows zSOL, stability fee would be applied which is equivalent to borrow interest on lending protocols. Stability fee is applied daily and compounding which is calculated as follows.

```
daily_stability_fee = stability_fee_apr / 365
```

Stability fee is dynamic which is decided by LP Finance DAO through governance. Unlike lending protocols, there are no "zSOL suppliers". Therefore stability fee is paid to zSOL-SOL liquidity providers to allow liquidity to linearly scale in respect of zSOL supply.

### Mint Halt

zSOL mint is halted if zSOL's market price is 5% below SOL price.

Following is the UI to mint/borrow zSOL. ([Link](https://app.lp.finance))

<figure><img src="../.gitbook/assets/Screenshot 2023-02-15 at 12.10.25 AM.png" alt=""><figcaption></figcaption></figure>

