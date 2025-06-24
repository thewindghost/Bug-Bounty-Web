from flask import request, render_template

def update_balance_user():
    
    try:
        if request.method == 'POST':
            balance = request.form.get('balance', '')
            eval(balance)
            return render_template('user/wallet.html', result=balance)

    except Exception as e:
            error = str(e)
            return render_template('user/wallet.html', error=error)
