import pandas as pd
import numpy as np
import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.environ.get("OPENAI_KEY")

uri = [
    "https://docs.lp.finance/",
    "https://docs.lp.finance/lp-finance-protocol/quick-user-guide",
    "https://docs.lp.finance/lp-finance-protocol/view-protocol-data",
    "https://docs.lp.finance/lp-finance-protocol/user-faq",
    "https://docs.lp.finance/protocol/minting-borrowing-zsol",
    "https://docs.lp.finance/protocol/zsol-sol-liquidity-providers",
    "https://docs.lp.finance/protocol/peg-stability-module",
    "https://docs.lp.finance/protocol/liquidation",
    "https://docs.lp.finance/lpfi-staking/lpfi-staking",
    "https://docs.lp.finance/governance/governance",
    "https://docs.lp.finance/addresses/programs",
    "https://docs.lp.finance/addresses/tokens",
    "https://docs.lp.finance/links/links"
]

data = {
    "title": [
        "LP Finance Protocol",
        "LP Finance Protocol",
        "LP Finance Protocol",
        "LP Finance Protocol",
        "Architecture",
        "Architecture",
        "Architecture",
        "Architecture",
        "LPFi Staking",
        "Governance",
        "Address",
        "Address",
        "Links"
    ],
    "heading": [
        "LP Finance Protocol",
        "Quick User Guide",
        "View Protocol Data",
        "User FAQ",
        "Minting/Borrowing zSOL",
        "zSOL-SOL Liquidity Providers",
        "Peg-stability Module",
        "Liquidation",
        "LPFi Staking",
        "Governance",
        "Programs",
        "Tokens",
        "Links"
    ],
    "content": [
        """
        In this document, the background behind the protocol design and economic model is explained.\n
        LP Finance is a decentralized synthetic asset issuance protocol on Solana. LP Finance designed Protocol Debt Vault (PDV) and liquidity provider incentives advancing stability fees to dramatically enhance scalability of synthetic assets.
        At a high level, the protocol allows users to leverage zSOL to create strategies such as leveraged liquid staking and short selling. Liquidity providers can earn interest rates and swap fees at the same time.
        On LP Finance, users can do the following: Leverage SOL staking yields, Short-sell, Earn interest by providing liquidity
        """,
        """
        ## Deposit Collateral: Select a token and amount to deposit. Confirm the minimum amount to deposit and deposit fee. Click "Deposit" and approve transaction.
        ## Borrow zSOL: Select amount of zSOL to borrow or click "Max" to borrow maximum amount. There is no borrow fee. Click "Borrow" and approve transaction.
        ## View Account Data: After performing the prior steps, users can view the account's data on "Your Account" section. Here are definitions of the terms
        - Borrow Limit: Maximum value (USD) of zSOL that can be borrowed.
        - Liquidation Threshold: A threshold of collateral value where the account would be liquidated. If collateral value drops below "Liquidation Threshold" liquidation might occur.
        - LTV: Loan to Value ratio, which is calculated as follows.
        `LTV = borrowedValueUsd / collateralValueUsd * 100`
        ## Repay zSOL: Select amount of zSOL to repay or click "Max" to fully repay the debt. Click "Repay" and confirm transaction.
        ## Withdraw Collateral: Select a token and amount to withdraw. If there is zSOL debt remaining, it is impossible to withdraw full amount. Click "Withdraw" and confirm transaction.
        """,
        """
        Following is the default page on LP Finance, https://app.lp.finance. Users can view protocol data. Following are the definitions.
        - Stability Fee Epoch: Period left until stability fee is applied
        - TVL: Total Value Locked
        - Global LTV: Global LTV (Protocol net LTV)
        - Stability Fee: Current borrow interest (APR)
        - Max mSOL APY: Maximum APY users can earn when fully leveraging mSOL position
        ## Collateral Composition: Click the pie chart on "Protocol Overview" to view current collateral composition. 
        ## Historical Data: Click "Data" on "Protocol Overview" to view historical data.
        """,
        """
        Question: Why is "Your Account" page not updating after transaction?
        Answer: If the account info does not update, plz try refreshing the app and reconnecting wallet.
        
        Question: When is the borrow interest applied?
        Answer: On the main page, "Stability Fee Epoch" is the time left until next borrow interest is applied. Borrow interest is applied every 24h.
        """,
        """
        zSOL is a over collateralized synthetic asset, which can be minted after depositing collateral. Even if the UX is identical to lending protocols, borrowing/repaying is performed as minting/burning zSOL.
        The collateral accepted on LP Finance are as follows.
        - SOL
        - mSOL
        - USDC
        It is only possible to deposit one collateral per account. To deposit other collateral, account should fully withdraw collateral.
        Once an account borrows zSOL, stability fee would be applied which is equivalent to borrow interest on lending protocols. Stability fee is applied daily and compounding which is calculated as follows.
        `daily_stability_fee = stability_fee_apr / 365`
        Stability fee is dynamic which is decided by LP Finance DAO through governance. Unlike lending protocols, there are no "zSOL suppliers". Therefore stability fee is paid to zSOL-SOL liquidity providers to allow liquidity to linearly scale in respect of zSOL supply.
        ## Mint Halt: zSOL mint is halted if zSOL's market price is 5% below SOL price.
        """,
        """
        zSOL-SOL liquidty providers can deposit Saber zSOL-SOL LP tokens to earn stability fee for zSOL borrowers. This allows zSOL market liquidity to scale linearly in respect to zSOL supply, increasing the capacity of zSOL to be used for leveraging purposes.
        Same as zSOL stability fee epoch, the zSOL rewards are distributed every 24h and can claim by interacting with the program.
        """,
        """
        Peg-stability module (PSM) is a common function in most stablecoin issuance protocols. PSM allows 1:1 swap between a stablecoin issued by a protocol and quote token (ex. USDC).
        For zSOL PSM should allow zSOL <-> SOL at 1:1 ratio, however LP Finance uses mSOL, which is a liquid staking derivative of SOL.
        ## Pricing of mSOL & zSOL: mSOL and zSOL's market price is not correctly accounted to SOL price. Therefore the program treats the price as follows.
        - mSOL: True price (value when delayed unstake)
        - zSOL: SOL price
        This prevents oracle exploits where zSOL or mSOL price depegs, causing higher redemption of mSOL or higher issuance of zSOL, causing zSOL to be undercollateralized.
        ## Risk of using mSOL
        mSOL is not always pegged to staked SOL's value. As mSOL to be fully claimed for SOL, a full epoch has to pass, which means in a volatile market condition, people would rather sell mSOL on market rather than wait to claim.
        Here is an example of mSOL depegging during FTX collapse event. (mSOL-SOL Saber)
        In case of mSOL depeg event, zSOL would be depegged at an equivalent rate. This is not a bug but a "design". Short-sellers can take benefit by shorting zSOL instead of SOL as zSOL is likely to fall more in price where SOL price crashes.
        ## Mechanism: Unlike other PSM, LP Finance implement "Protocol Debt Vault" which is an account managed by LP Finance DAO. It acts same as other accounts, but have solely mSOL as collateral, maximum LTV of 100%, and cannot be liquidated.
        PSM interacts with the Protocol Debt Vault in the backend as follows.
        - Swap mSOL-->zSOL: Deposit mSOL as collateral & borrow zSOL
        - Swap zSOL-->mSOL: Repay zSOL & withdraw mSOL collateral
        There is a swap fee for claiming mSOL (zSOL-->mSOL), which is a revenue source for LP Finance DAO. Additionally, when PSM activities are static, Protocol Debt Vault earns staking yields which is more efficient than having SOL.
        """,
        """
        On LP Finance, there are two types of liquidation.
        - T1: Accounts with SOL or mSOL as collateral
        - T2: Accounts with USDC as collateral
        ## T1 Liquidation: T1 liquidation is likely to happen when stability fee exceeds the value accural of SOL or mSOL. When using SOL as collateral, account is in higher risk of liquidation when not managed continuously. However, mSOL has a low risk of liquidation due to staking yields.
        Additionally, as mSOL price is calculated using "True price" liquidation does not occur even if mSOL depegs.
        Following are steps of T1 liquidation.
        1. Liquidator triggers liquidation of target account
        2. IF SOL, mint mSOL via calling Marinade Finance CPI
        3. Target account's mSOL collateral transferred to Protocol Debt Vault
        4. Target account's zSOL debt transferred to Protocol Debt Vault
        5. Target account initialized
        There is near-to-zero risk of bad debt for T1 liquidation. In case liquidation occurs, Protocol Debt Vault earns liquidation fees which is normally (100 - liquidation_threshold)%.
        ## T2 Liquidation: T2 liquidation occurs when SOL price rises, which triggers LTV to increase. Following are steps of T2 liquidation.
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
        - Collateral: 1000 USDC (1000 USD)
        - Debt: 32.5 zSOL (650 USD)
        If liquidator transfers 16.25 zSOL (325 USD, assume 1 mSOL= 1 SOL),
        ```
        usdc_claim_amt = 1000 * (16.25 * (20/20)) / 32.5
        >> usdc_claim_amt = 500
        In this case, liquidator was able to earn 175 USDC. The script is currently closed source, but users can interact with the UI to perform liquidation on https://app.lp.finance/liquidate.
        ```
        """,
        """
        Revenue genereated by protocol is distributed to LPFi staking pool. Users can stake LPFi to earn SOL. 
        In order to concentrate staking rewards to long-term holders, unstaking fee exists, which can be checked by clicking "Unstaking Fee" on "Staking Overview".
        Staking is possible on the website https://staking.lp.finance
        """,
        """
        LP Finance is governed by xLPFi token. Details can be found in the links below.
        - xLPFi Governance Document: https://x.lp.finance
        - Mint xLPFi: https://staking.lp.finance/xlpfi-minting
        - Realms: https://app.realms.today/dao/xLPFi
        """,
        """
        zSOL Issuance Program Address: 8Hka1oR6uoNLqjpYXXDKpF6NwiYidD6L3ncQdfu11aWw
        LP Incentives Program Address: FzTfrps1jZstduuSJ3ePsMTTR4rYX1hp73AcJ22ip4Gu
        LPFi Staking Program Address: HDXUGdC2hJNmwDY8DtfuWumnPyd4u2BvHhrvy5or8BZP
        xLPFi Minting Program Address: J8ttQ7yrZ3s1gkgjkXNCLRzhS6SyQnwLTL2FwxFgEBeN
        """,
        """
        zSOL Address: So111DzVTTNpDq81EbeyKZMi4SkhU9yekqB8xmMpqzA
        LPFi Address: LPFiNAybMobY5oHfYVdy9jPozFBGKpPiEGoobK2xCe3
        xLPFi Address: xLPFiPmWve5rUnAYcHZSZWjwgyqEdcV6dDzoBJRtNw9
        """,
        """
        LP Finance App Link: https://app.lp.finance
        LPFi Staking Link: https://staking.lp.finance
        Realms Governance Link: https://app.realms.today/dao/xLPFi
        Governance Document Link: https://x.lp.finance
        Twitter Link: https://twitter.com/LPFinance_
        Github Link: https://github.com/LP-Finance-Inc
        """
    ]
}

COMPLETIONS_MODEL = "text-davinci-003"
EMBEDDING_MODEL = "text-embedding-ada-002"
SEPARATOR = "\n* "
ENCODING = "gpt2"  # encoding for text-davinci-003
COMPLETIONS_API_PARAMS = {
    # We use temperature of 0.0 because it gives the most predictable, factual answer.
    "temperature": 0.0,
    "max_tokens": 150,
    "model": COMPLETIONS_MODEL,
}

def get_embedding(text: str, model: str=EMBEDDING_MODEL) -> list[float]:
    result = openai.Embedding.create(
      model=model,
      input=text
    )
    return result["data"][0]["embedding"]

def compute_doc_embeddings(df: pd.DataFrame) -> dict[tuple[str, str], list[float]]:
    """
    Create an embedding for each row in the dataframe using the OpenAI Embeddings API.
    
    Return a dictionary that maps between each embedding vector and the index of the row that it corresponds to.
    """
    return {
        idx: get_embedding(r.content) for idx, r in df.iterrows()
    }

def load_embeddings(fname: str) -> dict[tuple[str, str], list[float]]:
    """
    Read the document embeddings and their keys from a CSV.
    
    fname is the path to a CSV with exactly these named columns: 
        "title", "heading", "0", "1", ... up to the length of the embedding vectors.
    """
    
    df = pd.read_csv(fname, header=0)
    max_dim = max([int(c) for c in df.columns if c != "title" and c != "heading"])
    return {
           (r.title, r.heading): [r[str(i)] for i in range(max_dim + 1)] for _, r in df.iterrows()
    }

def vector_similarity(x: list[float], y: list[float]) -> float:
    """
    Returns the similarity between two vectors.
    
    Because OpenAI Embeddings are normalized to length 1, the cosine similarity is the same as the dot product.
    """
    return np.dot(np.array(x), np.array(y))

def order_document_sections_by_query_similarity(query: str, contexts: dict[(str, str), np.array]) -> list[(float, (str, str))]:
    """
    Find the query embedding for the supplied query, and compare it against all of the pre-calculated document embeddings
    to find the most relevant sections. 
    
    Return the list of document sections, sorted by relevance in descending order.
    """
    query_embedding = get_embedding(query)
    
    document_similarities = sorted([
        (vector_similarity(query_embedding, doc_embedding), doc_index) for doc_index, doc_embedding in contexts.items()
    ], reverse=True)
    
    return document_similarities

def construct_prompt(question: str, context_embeddings: dict, df: pd.DataFrame) -> str:
    """
    Fetch relevant 
    """
    most_relevant_document_sections = order_document_sections_by_query_similarity(question, context_embeddings)
    
    chosen_sections = []
    chosen_sections_indexes = []
    
    # change most_relevant_document_sections[:n] to select n docs
    for _, section_index in most_relevant_document_sections[:1]:

        # Add contexts until we run out of space.        
#         document_section = df.loc[section_index]
        idx = df.heading.tolist().index(section_index[1])
        content_section = df.content[idx]
        eligible_uri = uri[idx]
            
        chosen_sections.append(SEPARATOR + content_section.replace("\n", " "))
        chosen_sections_indexes.append(str(section_index))
        
            
    # Useful diagnostic information
    print(f"Selected {len(chosen_sections)} document sections:")
    print("\n".join(chosen_sections_indexes))
    
    header = """Answer the question as truthfully as possible using the provided context. if the answer is not contained within the text below, tell the user 'This might be out of context' and respond to question in a comical way."\n\nContext:\n"""
    
    return header + "".join(chosen_sections) + "\n\n Q: " + question + "\n A:", eligible_uri

def answer_query_with_context(
    query: str,
    df: pd.DataFrame,
    document_embeddings: dict[(str, str), np.array],
    show_prompt: bool = False
) -> str:
    prompt, eligible_uri = construct_prompt(
        query,
        document_embeddings,
        df
    )
    
    if show_prompt:
        print(prompt)

    response = openai.Completion.create(
                prompt=prompt,
                **COMPLETIONS_API_PARAMS
            )

    return response["choices"][0]["text"].strip(" \n")


def process(query):
    print("Run Start")
    df = pd.read_csv("../df.csv")
    document_embeddings = load_embeddings("../data.csv")

    response = answer_query_with_context(
        query, df, document_embeddings, show_prompt=False
    )
    print(response)
    return response
