django_frontend/
├── manage.py
├── rural_management/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── producers/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── services.py
│   └── templates/
│       └── producers/
│           ├── base.html
│           ├── dashboard.html
│           ├── producer_list.html
│           ├── producer_form.html
│           ├── farm_list.html
│           └── farm_form.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── charts.js
└── requirements.txt

# Execução Django
bash# Instalar dependências Django
pip install django psycopg2-binary

# Configurar projeto
cd django_frontend
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# Executar servidor
python manage.py runserver
Interface web disponível em: http://localhost:8000

# Execução
bash# Clonar e configurar
git clone <repo>
cd rural_producer_management

# Instalar dependências
pip install -r requirements.txt

# Executar com Docker
docker-compose up -d

# Executar testes
pytest

# Executar aplicação local
uvicorn app.main:app --reload

# Endpoints
POST /producers - Criar produtor
GET /producers - Listar produtores
GET /producers/{id} - Obter produtor
PUT /producers/{id} - Atualizar produtor
`
