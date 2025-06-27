from flask import session, request, make_response, render_template

def auth_logout_user():

        session.clear()
        running_value = request.args.get('running', 'True')
        response = make_response(render_template('auth/logout.html', running=running_value))
        response.delete_cookie('session')
        return response