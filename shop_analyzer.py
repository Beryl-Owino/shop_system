# Adding imports for visualization
import matplotlib.pyplot as plt
import numpy as np 

# step 1: creating the sales data, stored in nested dic item - variant - details
sales = {
    "chips":{
        "regular":{'qty': 100,'price': 120,'cost': 70},
        "chips_masala":{'qty': 10,'price': 200,'cost': 170}
        },
         
    "sodas":{
        "300ml":{'qty': 24,'price': 40,'cost': 28},
        "500ml":{'qty': 12,'price': 60,'cost': 55},
        "1_litre":{'qty': 12,'price': 100,'cost': 80}
        
    },

    "pilau":{
         "regular":{'qty': 14,'price': 150,'cost': 100}

    },
    
    "smokies":{
         "regular":{'qty': 22,'price': 40,'cost': 30}

    },
    "chicken":{
        "coated_100s":{'qty': 8,'price': 100,'cost': 70},
        "coated_50s":{'qty': 4,'price': 50,'cost': 30},
        "uncoated_quaters":{'qty': 2,'price': 200,'cost': 100}

    }
    
    
}

# step 2: Reusable function to calculate report
def calculate_sales_report(sales_data):
        report = {}
        total_revenue = 0
        total_cost = 0
        max_revenue = 0
        best_item = ""

        for item, variants in sales_data.items():
            report[item] = {}
            for variant, details in variants.items(): 
                
        # Extracting values
                qty = details['qty']
                price  = details['price']
                cost = details['cost']

        # calculating per items(per variant)
                revenue = qty * price
                item_cost = qty * cost
                profit = revenue - item_cost

        # Store in report
                report[item][variant] = {
                     'qty':qty,
                     'revenue':revenue,
                     'cost': item_cost,
                     'profit':profit

                }

        # Updating tools
                total_revenue += revenue
                total_cost += item_cost


        #Tracking best performing variant
                if revenue > max_revenue:
                    max_revenue = revenue
                    best_item = item + "-" + variant

        # calculating profits
        total_profit = total_revenue - total_cost
        
        # Returning evrything in a dictionary
        return report, total_revenue, total_cost, total_profit,best_item

# Function to print the report nicely
def print_report(report):
    for item, variants in report.items():
        print(f"\nItem: {item}")
        print(f"{'Variant':<20}{'Qty':<5}{'Revenue':<10}{'Cost':<10}{'Profit':<10}")
        print("-"*55)
        for variant, stats in variants.items():
            print(f"{variant:<20}{stats['qty']:<5}{stats['revenue']:<10}{stats['cost']:<10}{stats['profit']:<10}")
# Calling the function to calculate the report
report, total_revenue, total_cost, total_profit, best_item = calculate_sales_report(sales)

# Print the table report
print_report(report) 

# Aggregating revenue, cost, and profit for visualization
items = []
revenues = []
costs = []
profits = []
for item, variants in report.items():
     item_revenue = sum(stats['revenue'] for stats in variants.values())
     item_cost = sum(stats['cost'] for stats in variants.values())
     item_profit = sum(stats['profit'] for stats in variants.values())

    #for variant, stats in variants.items():
        #items.append(f"{item}-{variant}")
        #revenues.append(stats['revenue'])
        #costs.append(stats['cost'])
        #profits.append(stats['profit'])
     items.append(item)
     revenues.append(item_revenue)
     costs.append(item_cost)
     profits.append(item_profit)
    
    # Bar chart for revenue, cost, and profit
x = np.arange(len(items))
width = 0.2

plt.bar(x - width, revenues, width, label='Revenue', color='green')
plt.bar(x, costs, width, label='Cost', color='red')
plt.bar(x + width, profits, width, label='Profit', color='blue')

plt.xlabel('Items')
plt.ylabel('Amount ($)')
plt.title('Sales Performance')
plt.legend()
plt.xticks(x, items)
plt.tight_layout()
plt.show()

# pie chart for profit contribution
plt.figure(figsize=(8, 8))
plt.pie(profits, labels=items, autopct='%1.1f%%', startangle=140,
colors=['gold', 'lightblue', 'lightgreen', 'orange', 'pink'])
plt.title('Profit Contribution by Item')
plt.axis('equal')
plt.show()
       
# Print of the output
print("\nSummary:")
print("Total Revenue:", total_revenue)
print("Total Cost:", total_cost)
print("Total Profit:", total_profit)
print("Best Performing Item:", best_item)


