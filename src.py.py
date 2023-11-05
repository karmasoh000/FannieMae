import csv

MAX_RECORDS = 10  # Adjust this as needed

class Record:
  def __init__(self, ID, GrossMonthlyIncome, CreditCardPayment, CarPayment, 
StudentLoanPayments, AppraisedValue, DownPayment, LoanAmount, MonthlyMortgagePayment, CreditScore):
         self.ID = ID
         self.GrossMonthlyIncome = GrossMonthlyIncome
         self.CreditCardPayment = CreditCardPayment
         self.CarPayment = CarPayment
         self.StudentLoanPayments = StudentLoanPayments
         self.AppraisedValue = AppraisedValue
         self.DownPayment = DownPayment
         self.LoanAmount = LoanAmount
         self.MonthlyMortgagePayment = MonthlyMortgagePayment
         self.CreditScore = CreditScore

def monthly_debt(car_payment, credit_card_payment, student_loan_payments, monthly_mortgage_payment):
     return car_payment + credit_card_payment + student_loan_payments + monthly_mortgage_payment

def credit_rating(credit_score):
     return credit_score >= 640

def is_LTV_acceptable(appraised_value, loan_amount, down_payment):
     if down_payment < 0 or appraised_value <= 0:
         print("Invalid down payment or appraised value.")
         return False
     ltv_ratio = (loan_amount / appraised_value) * 100
     pmi_cost = (appraised_value * 0.01) / 12
     if ltv_ratio < 80:
         print("LTV Ratio is Acceptable")
         return True
     else:
         print("LTV Ratio is Not Acceptable")
         print(f"PMI Cost: ${pmi_cost} per month")
         return False

def is_DTI_acceptable(gross_monthly_income, dti_threshold, monthly_debt):
     if gross_monthly_income <= 0 or dti_threshold <= 0:
         print("Invalid gross monthly income or DTI threshold.")
         return False
     dti_ratio = (monthly_debt / gross_monthly_income) * 100
     return dti_ratio <= dti_threshold

def is_front_end_DTI_acceptable(monthly_mortgage_payment, gross_monthly_income):
     if gross_monthly_income <= 0:
         print("Invalid gross monthly income.")
         return False
     front_end_dti_ratio = (monthly_mortgage_payment / gross_monthly_income) * 100
     if front_end_dti_ratio <= 28:
         return True
     else:
         return False

def main():
     filename = "HackUTD-2023-HomeBuyerInfo.csv"
     try:
         with open(filename, mode='r') as file:
             reader = csv.reader(file)
             header = next(reader)
             record_count = 0
             total_debt = 0.0

             for row in reader:
                 record = Record(*map(float, row))
                 car_payment = record.CarPayment
                 credit_card_payment = record.CreditCardPayment
                 student_loan_payments = record.StudentLoanPayments
                 monthly_mortgage_payment = record.MonthlyMortgagePayment
                 record_debt = monthly_debt(car_payment, credit_card_payment, student_loan_payments, monthly_mortgage_payment)

                 appraised_value = record.AppraisedValue
                 loan_amount = record.LoanAmount
                 down_payment = record.DownPayment
                 is_acceptable_ltv = is_LTV_acceptable(appraised_value, loan_amount, down_payment)

                 gross_monthly_income = record.GrossMonthlyIncome
                 eligible = credit_rating(record.CreditScore)

                 total_debt += record_debt

                 print(f"ID: {record.ID} Total Monthly Debt: {record_debt} Credit Score: {record.CreditScore} Credit Rating: {'Eligible' if eligible else 'Not Eligible'}")

                 dti_threshold = 36.0
                 is_acceptable_dti = is_DTI_acceptable(gross_monthly_income, dti_threshold, record_debt)
                 if is_acceptable_dti:
                     print("DTI Ratio is Acceptable")
                 else:
                     print("DTI Ratio is Not Acceptable")

                 is_acceptable_front_end = is_front_end_DTI_acceptable(record.MonthlyMortgagePayment, gross_monthly_income)
                 if is_acceptable_front_end:
                     print("Front-end DTI Ratio is Acceptable")
                 else:
                     print("Front-end DTI Ratio is Not Acceptable")

                 record_count += 1
                 print()

             print(f"Total Monthly Debt for all records: {total_debt}")
     except FileNotFoundError:
         print("Failed to open the file.")

if __name__ == "__main__":
     main()
