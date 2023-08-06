import typer

APP_NAME = "ftp-cli"
ERROR = typer.style("Ошибка! ", fg=typer.colors.RED)
WARNING = typer.style("Предупреждение! ", fg=typer.colors.YELLOW)
SUCCESS = typer.style("Успех! ", fg=typer.colors.GREEN)
