from flask import Blueprint, render_template
from flask_login import login_required, current_user
main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required # route데코레이터와 함수사이에 위치
def profile():
    name = current_user.name
    return render_template('profile.html', name=current_user.name)

if __name__ == '__main__':
    app.run(FLASK_DEBUG=True)