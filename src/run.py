from flask_sqlite_app import create_app

app = create_app()


def main():
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )


if __name__ == "__main__":
    main()
