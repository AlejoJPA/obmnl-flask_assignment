# Import libraries
from flask import Flask, request, url_for, redirect, render_template

# Instantiate Flask functionality
app = Flask(__name__)

# Sample data
transactions = [
        {'id': 1, 'date': '2023-06-01', 'amount': 100},
        {'id': 2, 'date': '2023-06-02', 'amount': -200},
        {'id': 3, 'date': '2023-06-03', 'amount': 300}
]

# Read operation
@app.route("/")
def get_transactions():
    return render_template("transactions.html", transactions=transactions)    

# CRUD Operations
# Create operation: Display add transaction form

# CREATE: Route to handle the creation of a new transaction
@app.route("/add", methods=["GET", "POST"])
def add_transaction():
    # Check if the request method is POST (form submission)
    if request.method == 'POST':
        # Create a new transaction object using form field values
        transaction = {
            'id': len(transactions) + 1,            # Generate a new ID based on the current length of the transactions list
            'date': request.form['date'],           # Get the 'date' field value from the form
            'amount': float(request.form['amount']) # Get the 'amount' field value from the form and convert it to a float
        }
        # Append the new transaction to the transactions list
        transactions.append(transaction)

        # Redirect to the transactions list page after adding the new transaction
        return redirect(url_for("get_transactions"))
    
    # If the request method is GET, render the form template to display the add transaction form
    return render_template("form.html")

# UPDATE: Route to handle the Update of a transaction
@app.route("/edit/<int:transaction_id>", methods=["GET", "POST"])
def edit_transaction(transaction_id):
    # Check if the request method is POST (form submission)
    if request.method == 'POST':
        # Extract the updated values from the form fields
        date = request.form['date']
        amount = float(request.form['amount'])

        # Update the 'date' and 'amount' fields of the transaction
        # Exit the loop once the transaction is found and updated
        for transaction in transactions:
            if transaction['id'] == transaction_id:
                transaction['date'] =  date
                transaction['amount'] = amount
                break
        #then redirect the user back to the list of transactions
        return redirect(url_for("get_transactions"))
    
    # If the request method is GET, find the transaction with the matching ID and render the edit form
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            return render_template("edit.html", transaction=transaction)
    
    #Error handler
    # If the transaction with the specified ID is not found, handle this case
    return {"message": "Transaction not found"}, 404

#DELETE Operation
@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
    # Find the transaction with the matching ID and remove it from the list
    # Exit the loop once the transaction is deleted
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            transactions.remove(transaction)
            break
    
    # Redirect to the transactions list page after deleting the new transaction
    return redirect(url_for("get_transactions"))

#SEARCH AMOUNT
@app.route("/search", methods=["GET", "POST"])
def search_transaction():
    if request.method == 'POST':
        max_amount = float(request.form.get("max_amount", "inf"))
        min_amount = float(request.form.get("min_amount", "-inf"))

        filtered_transactions = [ t for t in transactions if min_amount <= t["amount"] <= max_amount]

        return render_template("transactions.html", transactions=filtered_transactions)
    
    return render_template("search.html")

#Calculate a total balance
@app.route("/balance")
def total_balance():
    balance = sum(t["amount"] for t in transactions)
    return f"Total Balance: {balance}"


# Run the Flask app
#By default, Flask launches the application on LocalHost:5000.
if __name__ == "__main__":
    app.run(debug=True)
    #By changing the port number, the port has to be explicitly stated
    #By default, Flask launches the application on LocalHost:5000.
    #app.run(host="0.0.0.0", port=8080)


