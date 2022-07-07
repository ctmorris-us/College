#CS HW 3
print('Welcome to the Student Loan Calculator')

principle = float(input('Enter the amount of the loan in dollars with (no commas):\n'))
years = float(input('Enter the number of years the loan will be for:\n'))

time = 12
interest = .034
fee_rate = .01051
monthly_payments = (principle * interest)/(time * (1 - (1 + interest/time)**(-years * time)))
balance = monthly_payments * time * years
interest_paid = balance - principle
fee = principle * fee_rate
extra_cost = fee * interest_paid

print('-' * 30)
print('Subsidized Federal Direct Loan')
print('Priniple:', principle)
print('Interest Rate:', round(interest * 100,2))
print('Years:', int(years))
print('Monthly Payment:', round(monthly_payments, 2))
print('Total Paid on Load:', round(balance, 2))
print('Total Interest Paid:', round(interest_paid, 2))
print('Additional Fees Paid:', round(fee, 2))
print('Total Costs Over Principle:', round(extra_cost, 2))
print('-' * 30)

interest = .068
old_principle = principle
principle *= (1 + interest * 4.25)
monthly_payments = (principle * interest)/(time * (1 - (1 + interest/time)**(-years * time)))
balance = monthly_payments * time * years
interest_paid = balance - principle
fee = principle * fee_rate
extra_cost = fee * interest_paid

print('Subsidized Federal Direct Loan')
print('Priniple:', principle)
print('Interest Rate:', round(interest * 100,2))
print('Years:', int(years))
print('Monthly Payment:', round(monthly_payments, 2))
print('Total Paid on Load:', round(balance, 2))
print('Total Interest Paid:', round(interest_paid, 2))
print('Additional Fees Paid:', round(fee, 2))
print('Total Costs Over Principle:', round(extra_cost, 2))
print('-' * 30)

interest = .079
fee_rate = .04204
monthly_payments = (principle * interest)/(time * (1 - (1 + interest/time)**(-years * time)))
balance = monthly_payments * time * years
interest_paid = balance - principle
fee = principle * fee_rate
extra_cost = fee * interest_paid

print('Federal Plus Loan')
print('Priniple:', old_principle)
print('Interest Rate:', format(interest * 100, '1.1f'))
print('Years:', int(years))
print('Monthly Payment:', format(monthly_payments, '1.2f'))
print('Total Paid on Load:', format(balance, '.2f'))
print('Total Interest Paid:', format(interest_paid, '.2f'))
print('Additional Fees Paid:', format(fee, '.2f'))
print('Total Costs Over Principle:', format(extra_cost, '.2f'))
