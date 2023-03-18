# Peg-stability Module

Peg-stability module (PSM) is a common function in most stablecoin issuance protocols. PSM allows 1:1 swap between a stablecoin issued by a protocol and quote token (ex. USDC).

For zSOL PSM should allow zSOL <-> SOL at 1:1 ratio, however LP Finance uses mSOL, which is a liquid staking derivative of SOL.

### Pricing of mSOL & zSOL

mSOL and zSOL's market price is not correctly accounted to SOL price. Therefore the program treats the price as follows.

* mSOL: True price (value when delayed unstake)
* zSOL: SOL price

This prevents oracle exploits where zSOL or mSOL price depegs, causing higher redemption of mSOL or higher issuance of zSOL, causing zSOL to be undercollateralized.

### Risk of using mSOL

mSOL is not always pegged to staked SOL's value. As mSOL to be fully claimed for SOL, a full epoch has to pass, which means in a volatile market condition, people would rather sell mSOL on market rather than wait to claim.

Here is an example of mSOL depegging during FTX collapse event. (mSOL-SOL Saber)

<figure><img src="../.gitbook/assets/Screenshot 2023-02-15 at 12.34.44 AM.png" alt=""><figcaption></figcaption></figure>

In case of mSOL depeg event, zSOL would be depegged at an equivalent rate. This is not a bug but a "design". Short-sellers can take benefit by shorting zSOL instead of SOL as zSOL is likely to fall more in price where SOL price crashes.

### Mechanism

Unlike other PSM, LP Finance implement "Protocol Debt Vault" which is an account managed by LP Finance DAO. It acts same as other accounts, but have solely mSOL as collateral, maximum LTV of 100%, and cannot be liquidated.

PSM interacts with the Protocol Debt Vault in the backend as follows.

* Swap mSOL-->zSOL: Deposit mSOL as collateral & borrow zSOL
* Swap zSOL-->mSOL: Repay zSOL & withdraw mSOL collateral

There is a swap fee for claiming mSOL (zSOL-->mSOL), which is a revenue source for LP Finance DAO. Additionally, when PSM activities are static, Protocol Debt Vault earns staking yields which is more efficient than having SOL.

Following is the UI for PSM swap. ([Link](https://app.lp.finance/psm))

<figure><img src="../.gitbook/assets/Screenshot 2023-02-15 at 12.54.33 AM.png" alt=""><figcaption></figcaption></figure>
