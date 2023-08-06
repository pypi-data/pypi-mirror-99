import typer, time, copy
from ftp_cli.src.config.controllers import ConfigController
from ftp_cli.src.config.schema import BlockSchema, Block
from ..utils import ERROR, SUCCESS, WARNING


config_app = typer.Typer()


@config_app.command()
def show():
    config = ConfigController.parse_config()
    for block in config.blocks:
        typer.echo(f"".center(30, "="))
        block.print_block()


@config_app.command()
def add():
    typer.secho("Создание новой учетной записи FTP...", fg=typer.colors.BLUE)
    time.sleep(0.5)
    data = {key: "" for key in BlockSchema.keys()}
    for key, value in BlockSchema.items():
        data[key] = typer.prompt(
            typer.style(value.get('title'), fg=typer.colors.GREEN, bold=True), default=value.get('default', None)
        )
    for key, value in BlockSchema.items():
        typer.echo("{}: {}".format(value.get('title'), typer.style(f"{data.get(key, '')}", fg=typer.colors.WHITE)))
    add = typer.confirm(f"{WARNING}Вы уверены, что хотите добавить эти данные?")
    if add:
        new_block = Block(**data)
        config = ConfigController.parse_config()
        config.blocks.append(new_block)
        ConfigController.write_config(config)
        typer.echo(f"{SUCCESS}Учетная запись для «" + typer.style(new_block.alias, fg=typer.colors.GREEN) + "» добавлена!")


@config_app.command()
def delete(alias: str = typer.Argument(...)):
    config = ConfigController.parse_config()
    if len(config.blocks):
        filtered_blocks = list(filter(lambda x: x.alias == alias, config.blocks))
        if not len(filtered_blocks):
            alias_styled = typer.style(alias, fg=typer.colors.GREEN)
            typer.echo(f"{ERROR}Записи с алиасом {alias_styled} не существует.")
        else:
            filtered_blocks[0].print_block()
            delete = typer.confirm(f"{WARNING}Удалить?")
            if delete:
                config.blocks.pop(config.blocks.index(filtered_blocks[0]))
                ConfigController.write_config(config)
                typer.echo(f"{SUCCESS}Запись удалена.")
    else:
        typer.echo(f"{ERROR}В базе данных отсутсвуют записи!")


@config_app.command()
def edit(alias: str = typer.Argument(...)):
    config = ConfigController.parse_config()
    if len(config.blocks):
        filtered_blocks = list(filter(lambda x: x.alias == alias, config.blocks))
        if not len(filtered_blocks):
            alias_styled = typer.style(alias, fg=typer.colors.GREEN)
            typer.echo(f"{ERROR}Записи с алиасом «{alias_styled}» не существует.")
        else:
            new_block = copy.copy(filtered_blocks[0])
            schema = Block.schema().get('properties')
            for key, value in schema.items():
                setattr(new_block, key, typer.prompt(
                    typer.style(value.get('title'), fg=typer.colors.GREEN, bold=True), default=getattr(new_block, key)
                ))
            prompt_edit = typer.confirm(f"{WARNING}Изменить?")
            if prompt_edit:
                config.blocks[config.blocks.index(filtered_blocks[0])] = new_block
                ConfigController.write_config(config)
                typer.echo(f"{SUCCESS}Запись изменена.")
    else:
        typer.echo(f"{ERROR}В базе данных отсутсвуют записи!")
