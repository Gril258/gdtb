from flask import views, render_template, request, make_response, redirect, url_for, send_from_directory
import app

class StaticView(views.MethodView):
    """Main page for admin"""
    def get(self, path):
        if 'Auth' in request.cookies:
            if request.cookies['Auth'] == 'yes':
                return send_from_directory('static', path)
        else:
        	return redirect(url_for('login'))