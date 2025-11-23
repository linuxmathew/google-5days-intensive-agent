from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.genai import types
from google.adk.tools import google_search
from google.adk.runners import InMemoryRunner
import asyncio
from dotenv import load_dotenv


load_dotenv()
retry_config= types.HttpRetryOptions(
     attempts= 5, 
     exp_base= 7, 
     initial_delay= 1,  
     http_status_codes= [429, 500, 503, 504]
)




# tool declaration

def get_fee_for_payment_method(method: str)-> dict:
    """Looks up the transaction fee percentage for a given payment method.

    This tool simulates looking up a company's internal fee structure based on
    the name of the payment method provided by the user.

    Args:
        method: The name of the payment method. It should be descriptive,
                e.g., "platinum credit card" or "bank transfer".

    Returns:
        Dictionary with status and fee information.
        Success: {"status": "success", "fee_percentage": 0.02}
        Error: {"status": "error", "error_message": "Payment method not found"}
    """


    method_fee_rate = {
        "visa": 0.75,
        "verve":0.1,
        "mastercard":0.11
    }

    rate = method_fee_rate.get(method.lower())

    if rate is not None:
        return {
            "status": 'success',
            'rate': rate
        }
    else:
        return {
            "status": "error",
            "error_message": f"Payment method: {method} not found"
        }
    

print("payment method calculated successfully")


def get_exchange_rate(base_currency: str, target_currency:str) -> dict:
    """Looks up and returns the exchange rate between two currencies.

    Args:
        base_currency: The ISO 4217 currency code of the currency you
                       are converting from (e.g., "USD").
        target_currency: The ISO 4217 currency code of the currency you
                         are converting to (e.g., "EUR").

    Returns:
        Dictionary with status and rate information.
        Success: {"status": "success", "rate": 0.93}
        Error: {"status": "error", "error_message": "Unsupported currency pair"}
    """


    lookup_db_currencies ={
        "usd":{
            "ngn": 1500,
            'eur': 0.96,
            'jpy': 192
        }
    }

    base = base_currency.lower()
    target = target_currency.lower()

    rate = lookup_db_currencies.get(base).get(target)

    if rate is not None:
        return {"status":"success", "rate": rate}
    else:
        return {"status":"error", "error_message": f"equivalent currencies, {base, target} cannot be found"}

print("exchange rate calculated successfully")



currency_agent = Agent(
    name = "currency_agent",
    model = Gemini(
        model="gemini-2.5-flash-lite",
        retry_options = retry_config
    ),
    
    instruction="""You are a smart currency conversion assistant.

    For currency conversion requests:
    1. Use `get_fee_for_payment_method()` to find transaction fees
    2. Use `get_exchange_rate()` to get currency conversion rates
    3. Check the "status" field in each tool's response for errors
    4. Calculate the final amount after fees based on the output from `get_fee_for_payment_method` and `get_exchange_rate` methods and provide a clear breakdown.
    5. First, state the final converted amount.
        Then, explain how you got that result by showing the intermediate amounts. Your explanation must include: the fee percentage and its
        value in the original currency, the amount remaining after the fee, and the exchange rate used for the final conversion.

    If any tool returns status "error", explain the issue to the user clearly.
    """,
    tools=[get_fee_for_payment_method, get_exchange_rate]
)

# Test the currency agent

currency_runner = InMemoryRunner(agent = currency_agent)

async def main():
    result = await currency_runner.run_debug("I want to convert 500 USD to Nigerian Naira using visa")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())