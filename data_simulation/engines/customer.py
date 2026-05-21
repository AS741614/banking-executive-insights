import random
import uuid
from faker import Faker
from datetime import date, timedelta
from typing import List, Tuple
from models.core import Customer, Account, CustomerSegment, AccountType

fake = Faker()

class CustomerEngine:
    """
    Generates realistic customer demographics and account hierarchies.
    """
    def __init__(self, seed: int = 42):
        Faker.seed(seed)
        random.seed(seed)
        
        self.regions = ["North", "South", "East", "West", "APAC", "EMEA"]
        self.countries = ["US", "UK", "CA", "SG", "DE", "JP"]
        self.branches = [f"BR-{str(i).zfill(3)}" for i in range(1, 51)]

    def generate_population(self, start_date: date, count: int) -> Tuple[List[Customer], List[Account]]:
        customers = []
        accounts = []

        for _ in range(count):
            segment_roll = random.random()
            if segment_roll < 0.70:
                segment = CustomerSegment.RETAIL
                account_types = [AccountType.CHECKING, AccountType.SAVINGS]
                risk_base = random.uniform(0.1, 0.4)
            elif segment_roll < 0.90:
                segment = CustomerSegment.PREMIER
                account_types = [AccountType.CHECKING, AccountType.INVESTMENT]
                risk_base = random.uniform(0.05, 0.2)
            elif segment_roll < 0.98:
                segment = CustomerSegment.BUSINESS
                account_types = [AccountType.CHECKING, AccountType.CREDIT]
                risk_base = random.uniform(0.3, 0.7)
            else:
                segment = CustomerSegment.INSTITUTIONAL
                account_types = [AccountType.TREASURY, AccountType.CHECKING]
                risk_base = random.uniform(0.2, 0.5)

            cust_id = f"CUST-{uuid.uuid4().hex[:8].upper()}"
            
            # Stagger onboarding dates to simulate historical growth
            onboarding_offset = random.randint(0, 365 * 3) # Up to 3 years prior to simulation start
            onboarding_date = start_date - timedelta(days=onboarding_offset)
            
            customer = Customer(
                customer_sk=cust_id,
                first_name=fake.first_name(),
                last_name=fake.last_name() if segment in [CustomerSegment.RETAIL, CustomerSegment.PREMIER] else fake.company(),
                segment=segment,
                country=random.choice(self.countries),
                region=random.choice(self.regions),
                kyc_status="CLEARED" if random.random() > 0.05 else "PENDING_REVIEW",
                onboarding_date=onboarding_date,
                risk_score=min(1.0, risk_base * random.uniform(0.8, 1.2))
            )
            customers.append(customer)

            # Generate Accounts for Customer
            num_accounts = random.randint(1, len(account_types))
            for i in range(num_accounts):
                acct_id = f"ACCT-{uuid.uuid4().hex[:10].upper()}"
                
                # Institutional accounts have significantly higher balances
                base_balance = random.uniform(100, 10000)
                if segment == CustomerSegment.PREMIER:
                    base_balance *= 10
                elif segment == CustomerSegment.BUSINESS:
                    base_balance *= 50
                elif segment == CustomerSegment.INSTITUTIONAL:
                    base_balance *= 1000

                account = Account(
                    account_sk=acct_id,
                    customer_sk=cust_id,
                    branch_sk=random.choice(self.branches),
                    product_sk=f"PROD-{random.randint(10, 99)}",
                    account_type=random.choice(account_types),
                    open_date=onboarding_date + timedelta(days=random.randint(0, 30)),
                    balance=base_balance,
                    status="ACTIVE"
                )
                accounts.append(account)

        return customers, accounts
