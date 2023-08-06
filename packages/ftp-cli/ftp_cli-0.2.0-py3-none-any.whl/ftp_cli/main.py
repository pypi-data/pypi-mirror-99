#!/usr/bin/env python3

import typer

from ftp_cli.src.config import config_app
from ftp_cli.src.ftp import app as backup_app

app = typer.Typer()
app.add_typer(config_app, name="config")
app.add_typer(backup_app, name="backup")

if __name__ == "__main__":
	app()

