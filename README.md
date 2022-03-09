# crypto-tax-report

## Table of Contents
1. [Overview](#overview)
   1. [A glimpse into history](#a-glimpse-into-history)
2. [Inventory Methods](#inventory-methods)
   1. [FIFO (First-In-First-Out)](#fifo-first-in-first-out)
3. [Getting Started](#getting-started)
   1. [Prerequisites](#prerequisites)
   2. [Pull Source Code](#pull-source-code)
   3. [Configuration](#configuration)
4. [Disclaimer](#disclaimer)

## Overview
The Crypto Tax Report calculates your taxable profits from crypto based on your transaction history.
The used inventory method to calculate your profits is FIFO (First-In-First-Out).

Sell transactions that are apart from their corresponding buy transactions by more than or equal to a configurable time 
difference, e. g. 360 days (1 year), are considered non-taxable or "tax-free" so to say.

#### A glimpse into history
I created this project when I almost finished my tax declaration 2021 but still had one procrastinated part left to do -
the crypto taxes. I knew what I needed to do when I would have the purchase value and the sell value but how to get to 
the purchase value of every sell transaction while considering FIFO was a mind-numbing obstacle for me. So I looked for 
software online that does the job for me, and I was faced with prices of three-digits for every tax year. I considered 
those prices ridiculous when you barely made four digits with crypto so far. Then I became aware of my basic Python 
skills and thought maybe I could just programm it myself. So here it is!

## Inventory Methods
### FIFO (First-In-First-Out)
In the FIFO inventory method, it is assumed that crypto assets that have been purchased first (First-In) are also sold 
first (First-Out).

For example, consider the following buy transactions:
- 1st March 2020; Quantity: 1.00; Costs: 100 EUR
- 1st March 2021; Quantity: 2.00; Costs: 400 EUR

If you sell now 1.00 tokens for 200 EUR, you would sell the tokens from the 1st transaction that happened first and not 
from the 2nd transaction that happened later.
This results in a cost-basis of 100 EUR and you received 200 EUR.

Your capital gains would be 200 - 100 = 100 EUR.

Let us rewind and say you did sell not 1.00 but 2.00 tokens for 500 EUR. Now it gets tricky: you then would sell 1.00
from the 1st transaction and 1.00 from the 2nd transaction.
This results in a cost-basis of 100 EUR + 1/2 × 400 EUR = 300 EUR because one half of 2.00 tokens you sold have been 
costing you 100 EUR and the other half of 2.00 tokens you sold have been costing you half of 400 EUR. This results in a 
cost-basis of 300 EUR and you received 500 EUR.

Your capital gains would be 500 - 300 = 200 EUR.

<!--### LIFO (Last-In-First-Out)
tbd-->

## Getting Started

### Prerequisites
The following prerequisites are necessary to execute the Python script:
- Python 3+
- Ability to create .XLSX files, e.g. Microsoft Excel or Numbers by Apple.

### Pull Source Code
Pull the source code from GitHub to your local machine:
```
git clone https://github.com/ericvancoffee/crypto-tax-report.git
```

### Configuration
In the Python file ```generate_tax_report.py``` at the top, you can define:
1. ```LOG_LEVEL```: log level of the script
2. ```TRANSACTIONS_DIR```: directory from which to import the crypto transactions
3. ```TAX_REPORTS_DIR```: directory to which to export the crypto tax reports
4. ```tokens```: token abbreviations for which to generate a tax report
5. ```USE_FIFO```: whether to use inventory method FIFO (only one available so far)
6. ```TAXFREE_TIMEDELTA```: the time difference between buy and sell transactions so they are considered non-taxable/tax-free

The transactions are imported from preformatted .XLSX files. To see an example of such a file, please refer to the 
```transations_example.xlsx``` file in the ```/transactions``` directory.
The transactions files need to be named as ```[token]_transactions.xlsx```, e.g. ```BTC_transactions.xlsx``` and 
placed in the ```TRANSACTIONS_DIR```.

### Run Script
After configuring the script, run the script via command line: ```python generate_tax_report.py```
or via an IDE run configuration.

### Troubleshooting
If you cannot run the script, make sure you activated your Python virtual environment 
(https://docs.python.org/3/tutorial/venv.html) in case you are using one. 
Usually you can easily run ```source path/to/venv/Scripts/activate``` in command line or git bash.

## Disclaimer
Tax laws differ from country to country. This script does not necessarily comply with the tax law in your country and 
does not provide any numbers directly usable for tax declaration. It is advised to review the code of the script and 
verify whether it fits the intended purpose and whether it complies with the tax law in your country. You agree that 
the use of any numbers calculated by this script for a tax declaration is at your sole and exclusive risk. Grossly 
negligent or willingly incorrect tax declaration may constitute an offense of tax evasion. Further, we make no warranty 
that the script will be uninterrupted or error-free.