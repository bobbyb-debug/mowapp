from app import create_app, db
from app.models import Job, Expense, Service

app = create_app()

# Force debug mode
app.debug = True
app.env = "development"

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Job': Job, 'Expense': Expense, 'Service': Service}

if __name__ == '__main__':
    app.run(debug=True)  # Explicitly enable debug mode
