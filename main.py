from app.initialize import create_app

app = create_app()
app.app_context().push()

if __name__ == "__main__":
    app.run()
    # app.run(debug=True)
    # app.run(debug=True, use_reloader=False)
