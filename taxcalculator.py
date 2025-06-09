# Caclulates tax based on marginal tax rates
def calculate_tax(income):
    # Define the tax brackets and corresponding rates
    tax_brackets = [
        (0, 18000, 0.0),
        (18001, 45000, 0.16),
        (45001, 135000, 0.30),
        (135001, 190000, 0.37),
        (190001, float('inf'), 0.45)
    ]
    
    # Initialize the total tax to zero
    total_tax = 0
    
    # Iterate over each bracket in the tax brackets list
    for lower_bound, upper_bound, rate in tax_brackets:
        # Calculate the taxable income for this bracket
        if income > lower_bound:
            taxable_income = min(income - lower_bound, upper_bound - lower_bound)
            total_tax += taxable_income * rate
    
    return total_tax

# Example usage
income = 100000
tax = calculate_tax(income)
print(f"The tax for an income of ${income} is ${tax:.2f}")
