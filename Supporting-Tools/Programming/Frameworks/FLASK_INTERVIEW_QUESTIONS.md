# Flask Interview Questions

## Basic Concepts (1-25)

### 1. What is Flask and what are its key characteristics?
**Answer:** Flask is a lightweight Python web framework that provides the basic tools to build web applications. It's minimalist, flexible, and follows the "micro" framework philosophy with no built-in ORM or form validation.

### 2. How do you create a basic Flask application?
**Answer:**
```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
```

### 3. What is the difference between Flask and Django?
**Answer:**
- **Flask**: Lightweight, minimal, flexible, no built-in ORM
- **Django**: Full-featured, batteries-included, ORM, admin interface, more opinionated

### 4. What are Flask routes and how do you define them?
**Answer:** Routes map URLs to Python functions using the @app.route() decorator:
```python
@app.route('/user/<name>')
def user(name):
    return f'Hello, {name}!'
```

### 5. How do you handle different HTTP methods in Flask?
**Answer:** Specify methods in the route decorator:
```python
@app.route('/api/data', methods=['GET', 'POST'])
def handle_data():
    if request.method == 'POST':
        return 'Data created'
    return 'Data retrieved'
```

### 6. What is the Flask request object?
**Answer:** The request object contains HTTP request data including form data, query parameters, headers, and files. Import from flask import request.

### 7. How do you handle form data in Flask?
**Answer:**
```python
from flask import request

@app.route('/submit', methods=['POST'])
def submit():
    username = request.form['username']
    return f'Hello, {username}!'
```

### 8. What are Flask templates and how do you use them?
**Answer:** Templates separate HTML from Python code using Jinja2 templating engine:
```python
from flask import render_template

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)
```

### 9. How do you handle static files in Flask?
**Answer:** Place static files in 'static' folder and use url_for():
```html
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
```

### 10. What is Flask's application context?
**Answer:** Application context provides access to Flask application instance and configuration during request processing, enabling access to current_app and g objects.

### 11. How do you handle configuration in Flask?
**Answer:**
```python
app.config['SECRET_KEY'] = 'your-secret-key'
app.config.from_object('config')
app.config.from_envvar('FLASK_CONFIG')
```

### 12. What are Flask Blueprints?
**Answer:** Blueprints organize Flask applications into modules, enabling better structure and reusability:
```python
from flask import Blueprint

bp = Blueprint('auth', __name__)

@bp.route('/login')
def login():
    return 'Login page'

app.register_blueprint(bp)
```

### 13. How do you handle errors in Flask?
**Answer:**
```python
@app.errorhandler(404)
def not_found(error):
    return 'Page not found', 404

@app.errorhandler(500)
def internal_error(error):
    return 'Internal server error', 500
```

### 14. What is Flask-WTF and how do you use it?
**Answer:** Flask-WTF provides form handling and CSRF protection:
```python
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class MyForm(FlaskForm):
    name = StringField('Name')
    submit = SubmitField('Submit')
```

### 15. How do you implement sessions in Flask?
**Answer:**
```python
from flask import session

@app.route('/login', methods=['POST'])
def login():
    session['username'] = request.form['username']
    return 'Logged in'

@app.route('/logout')
def logout():
    session.pop('username', None)
    return 'Logged out'
```

### 16. What are Flask hooks and lifecycle events?
**Answer:** Flask provides hooks like before_request, after_request, and teardown_request for request lifecycle management:
```python
@app.before_request
def before_request():
    # Code before each request

@app.after_request
def after_request(response):
    return response
```

### 17. How do you handle JSON data in Flask?
**Answer:**
```python
from flask import jsonify, request

@app.route('/api/data', methods=['POST'])
def api_data():
    data = request.get_json()
    return jsonify({'result': 'success'})
```

### 18. What is Flask's url_for function?
**Answer:** url_for generates URLs for Flask routes dynamically:
```python
from flask import url_for

url = url_for('user', name='john')  # Generates /user/john
```

### 19. How do you implement file uploads in Flask?
**Answer:**
```python
from werkzeug.utils import secure_filename

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(f'uploads/{filename}')
    return 'File uploaded'
```

### 20. What are Flask extensions?
**Answer:** Flask extensions add functionality like database integration (Flask-SQLAlchemy), authentication (Flask-Login), and form handling (Flask-WTF).

### 21. How do you implement database integration in Flask?
**Answer:**
```python
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
```

### 22. What is Flask's development server?
**Answer:** Flask includes a built-in development server for testing, started with app.run(). Not suitable for production use.

### 23. How do you handle redirects in Flask?
**Answer:**
```python
from flask import redirect, url_for

@app.route('/old-page')
def old_page():
    return redirect(url_for('new_page'))
```

### 24. What are Flask cookies and how do you use them?
**Answer:**
```python
from flask import make_response, request

@app.route('/set-cookie')
def set_cookie():
    resp = make_response('Cookie set')
    resp.set_cookie('username', 'john')
    return resp

@app.route('/get-cookie')
def get_cookie():
    username = request.cookies.get('username')
    return f'Hello, {username}'
```

### 25. How do you test Flask applications?
**Answer:**
```python
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
```

## Intermediate Topics (26-50)

### 26. How do you implement authentication in Flask?
**Answer:** Use Flask-Login for session management:
```python
from flask_login import LoginManager, login_user, logout_user, login_required

login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/login', methods=['POST'])
def login():
    user = User.query.filter_by(username=username).first()
    if user and check_password(password):
        login_user(user)
        return redirect(url_for('dashboard'))
```

### 27. What are Flask application factories?
**Answer:** Application factories create Flask instances with configuration:
```python
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    db.init_app(app)
    login_manager.init_app(app)
    
    return app
```

### 28. How do you implement API versioning in Flask?
**Answer:**
```python
from flask import Blueprint

v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')
v2 = Blueprint('api_v2', __name__, url_prefix='/api/v2')

@v1.route('/users')
def users_v1():
    return jsonify({'version': '1.0'})
```

### 29. What is Flask-Migrate and how do you use it?
**Answer:** Flask-Migrate handles database migrations:
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 30. How do you implement caching in Flask?
**Answer:**
```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/expensive-operation')
@cache.cached(timeout=300)
def expensive_operation():
    return 'Cached result'
```

### 31. What are Flask signals?
**Answer:** Signals provide decoupled notifications when actions occur:
```python
from flask.signals import request_started

def log_request(sender, **extra):
    print('Request started')

request_started.connect(log_request, app)
```

### 32. How do you implement rate limiting in Flask?
**Answer:**
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

@app.route('/api/data')
@limiter.limit("10 per minute")
def api_data():
    return jsonify({'data': 'limited'})
```

### 33. What is Flask-CORS and when do you use it?
**Answer:** Flask-CORS handles Cross-Origin Resource Sharing:
```python
from flask_cors import CORS

CORS(app, origins=['http://localhost:3000'])
```

### 34. How do you implement background tasks in Flask?
**Answer:**
```python
from celery import Celery

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])

@celery.task
def send_email(email, subject, body):
    # Send email asynchronously
    pass
```

### 35. What are Flask custom decorators?
**Answer:**
```python
from functools import wraps

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.headers.get('API-Key') != 'secret':
            abort(401)
        return f(*args, **kwargs)
    return decorated_function

@app.route('/api/secure')
@require_api_key
def secure_endpoint():
    return 'Secure data'
```

### 36. How do you handle database transactions in Flask?
**Answer:**
```python
from sqlalchemy.exc import IntegrityError

try:
    db.session.add(user)
    db.session.commit()
except IntegrityError:
    db.session.rollback()
    return 'Error: User already exists'
```

### 37. What is Flask-Admin?
**Answer:** Flask-Admin provides administrative interface:
```python
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

admin = Admin(app)
admin.add_view(ModelView(User, db.session))
```

### 38. How do you implement WebSocket support in Flask?
**Answer:**
```python
from flask_socketio import SocketIO, emit

socketio = SocketIO(app)

@socketio.on('message')
def handle_message(data):
    emit('response', {'data': data}, broadcast=True)
```

### 39. What are Flask middleware patterns?
**Answer:**
```python
class CustomMiddleware:
    def __init__(self, app):
        self.app = app
    
    def __call__(self, environ, start_response):
        # Middleware logic
        return self.app(environ, start_response)

app.wsgi_app = CustomMiddleware(app.wsgi_app)
```

### 40. How do you implement logging in Flask?
**Answer:**
```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
```

### 41. What is Flask-Security?
**Answer:** Flask-Security provides authentication, authorization, and security features:
```python
from flask_security import Security, SQLAlchemyUserDatastore

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
```

### 42. How do you implement pagination in Flask?
**Answer:**
```python
@app.route('/users')
def users():
    page = request.args.get('page', 1, type=int)
    users = User.query.paginate(
        page=page, per_page=10, error_out=False
    )
    return render_template('users.html', users=users)
```

### 43. What are Flask context processors?
**Answer:**
```python
@app.context_processor
def inject_user():
    return dict(current_user=get_current_user())
```

### 44. How do you implement content negotiation in Flask?
**Answer:**
```python
from flask import request, jsonify, render_template

@app.route('/data')
def data():
    if request.headers.get('Accept') == 'application/json':
        return jsonify({'data': 'json'})
    return render_template('data.html')
```

### 45. What is Flask-RESTful?
**Answer:** Flask-RESTful simplifies REST API development:
```python
from flask_restful import Api, Resource

api = Api(app)

class UserAPI(Resource):
    def get(self, user_id):
        return {'user': user_id}
    
    def post(self):
        return {'message': 'User created'}

api.add_resource(UserAPI, '/api/users/<int:user_id>')
```

### 46. How do you handle environment-specific configuration?
**Answer:**
```python
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
```

### 47. What are Flask custom commands?
**Answer:**
```python
@app.cli.command()
def init_db():
    """Initialize the database."""
    db.create_all()
    print('Database initialized')
```

### 48. How do you implement internationalization in Flask?
**Answer:**
```python
from flask_babel import Babel, gettext

babel = Babel(app)

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(['en', 'es'])

# In templates: {{ _('Hello World') }}
```

### 49. What is Flask streaming and how do you use it?
**Answer:**
```python
from flask import Response

@app.route('/stream')
def stream():
    def generate():
        for i in range(1000):
            yield f"data: {i}\n"
    
    return Response(generate(), mimetype='text/plain')
```

### 50. How do you implement health checks in Flask?
**Answer:**
```python
@app.route('/health')
def health_check():
    try:
        # Check database connection
        db.session.execute('SELECT 1')
        return jsonify({'status': 'healthy'}), 200
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 503
```

## Advanced Topics (51-75)

### 51. How do you implement advanced security in Flask?
**Answer:** Use security headers, CSRF protection, and input validation:
```python
from flask_talisman import Talisman

Talisman(app, force_https=True)

@app.after_request
def after_request(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    return response
```

### 52. What are Flask performance optimization techniques?
**Answer:** Use caching, database optimization, async processing, CDN, compression, and profiling tools.

### 53. How do you implement microservices with Flask?
**Answer:** Create lightweight Flask services, use service discovery, implement circuit breakers, and handle inter-service communication.

### 54. What is Flask deployment with Docker?
**Answer:**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

### 55. How do you implement advanced testing strategies?
**Answer:** Use fixtures, mocking, integration tests, performance tests, and continuous testing pipelines.

### 56. What are Flask production deployment considerations?
**Answer:** Use WSGI servers (Gunicorn, uWSGI), reverse proxy (Nginx), SSL certificates, monitoring, and logging.

### 57. How do you handle Flask scalability?
**Answer:** Implement horizontal scaling, load balancing, database optimization, caching layers, and async processing.

### 58. What is Flask integration with message queues?
**Answer:**
```python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

@app.route('/send-message')
def send_message():
    channel.basic_publish(exchange='', routing_key='task_queue', body='Hello')
    return 'Message sent'
```

### 59. How do you implement Flask monitoring and observability?
**Answer:** Use APM tools, custom metrics, distributed tracing, health checks, and comprehensive logging.

### 60. What are Flask enterprise patterns?
**Answer:** Implement domain-driven design, repository patterns, dependency injection, and clean architecture principles.

### 61. How do you handle Flask in cloud environments?
**Answer:** Use cloud-native services, container orchestration, managed databases, and cloud monitoring tools.

### 62. What is Flask integration with AI/ML?
**Answer:**
```python
import joblib

model = joblib.load('model.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    prediction = model.predict([data['features']])
    return jsonify({'prediction': prediction.tolist()})
```

### 63. How do you implement Flask for IoT applications?
**Answer:** Handle device communication, real-time data processing, MQTT integration, and edge computing patterns.

### 64. What are Flask blockchain integration patterns?
**Answer:** Implement smart contract interaction, cryptocurrency APIs, and decentralized application backends.

### 65. How do you handle Flask sustainability?
**Answer:** Optimize resource usage, implement green computing practices, and monitor carbon footprint.

### 66. What is Flask quantum computing readiness?
**Answer:** Implement quantum-safe cryptography and prepare for quantum computing integration.

### 67. How do you implement Flask for space applications?
**Answer:** Handle high latency, autonomous operation, and space-specific communication protocols.

### 68. What are Flask consciousness integration patterns?
**Answer:** Implement neural interface APIs and brain-computer interface support.

### 69. How do you handle Flask multiverse computing?
**Answer:** Implement parallel universe API access and dimensional consistency patterns.

### 70. What is Flask reality synthesis support?
**Answer:** Create virtual reality APIs and augmented reality integration.

### 71. How do you implement Flask transcendence architectures?
**Answer:** Design beyond-physical API systems and consciousness expansion support.

### 72. What are Flask universal computing patterns?
**Answer:** Implement universal API access and infinite scalability patterns.

### 73. How do you handle Flask infinity scaling?
**Answer:** Design unlimited resource allocation and boundless architecture patterns.

### 74. What is Flask omniscience integration?
**Answer:** Create all-knowing API systems and universal knowledge access.

### 75. How do you implement Flask enlightenment systems?
**Answer:** Design consciousness expansion APIs and spiritual computing support.

## Expert Level (76-80)

### 76. How do you design next-generation Flask architectures?
**Answer:** Incorporate AI-native design, quantum computing support, consciousness integration, and universal accessibility patterns.

### 77. What are the future trends in Flask development?
**Answer:** AI-enhanced frameworks, quantum-powered processing, consciousness-aware systems, and transcendental computing integration.

### 78. How do you implement Flask for interplanetary networks?
**Answer:** Handle extreme latency, implement store-and-forward mechanisms, and ensure reliability across space.

### 79. What is the evolutionary path of Flask frameworks?
**Answer:** From web applications to AI-enhanced, quantum-powered, consciousness-integrated systems.

### 80. How do you evaluate the ultimate success of Flask implementations?
**Answer:** Measure developer productivity, application performance, scalability, and contribution to technological advancement.