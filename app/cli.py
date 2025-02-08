from app.app import App


cli = App().build_cli()

if __name__ == "__main__":
    cli()
