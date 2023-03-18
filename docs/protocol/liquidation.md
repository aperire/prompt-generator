# Liquidation

On LP Finance, there are two types of liquidation.

* **T1**: Account with SOL or mSOL collateral
* **T2**: Account with USDC collateral

### T1 Liquidation

T1 liquidation is likely to happen when stability fee exceeds the value accural of SOL or mSOL. When using SOL as collateral, account is in higher risk of liquidation when not managed continuously. However, mSOL has a low risk of liquidation due to staking yields.

Additionally, as mSOL price is calculated using "True price" liquidation does not occur even if mSOL depegs.

Following are steps of T1 liquidation.

1. Liquidator triggers liquidation of target account
2. IF SOL, mint mSOL via calling Marinade Finance CPI
3. Target account's mSOL collateral transferred to Protocol Debt Vault
4. Target account's zSOL debt transferred to Protocol Debt Vault
5. Target account initialized

There is near-to-zero risk of bad debt for T1 liquidation. In case liquidation occurs, Protocol Debt Vault earns liquidation fees which is normally (100 - liquidation\_threshold)%.

### T2 Liquidation

T2 liquidation occurs when SOL price rises, which triggers LTV to increase. Following are steps of T2 liquidation.

1. Liquidator triggers liquidation of target account
2. Liquidator transfers mSOL to Protocol Debt Vault
3. Liquidator redeems USDC from target account
4. Target account's zSOL debt transferred to Protocol Debt Vault

The amount of USDC to be claimed with mSOL is calculated as follows.

```
repaid_zsol_amt = msol_transfer_amt * (msol_price / sol_price)
repaid_ratio = repaid_zsol_amt / borrowed_zsol_amt
usdc_claim_amt = usdc_collateral_amt * repaid_ratio
```

Let's assume liquidating the following account

* Collateral: 1000 USDC (1000 USD)
* Debt: 32.5 zSOL (650 USD)

If liquidator transfers 16.25 zSOL (325 USD, assume 1 mSOL= 1 SOL),

```
usdc_claim_amt = 1000 * (16.25 * (20/20)) / 32.5
>> usdc_claim_amt = 500
```

In this case, liquidator was able to earn 175 USDC. The script is currently closed source, but users can interact with the UI to perform liquidation [here](https://app.lp.finance/liquidate).

![](<../.gitbook/assets/Screenshot 2023-02-15 at 1.14.43 AM.png>)
