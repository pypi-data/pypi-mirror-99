import typer, pydantic


class Block(pydantic.BaseModel):
    alias: str = pydantic.Field(title="Алиас")
    hostname: str = pydantic.Field(title="Адрес")
    port: int = pydantic.Field(title="Порт", default=22)
    login: str = pydantic.Field(title="Логин")
    password: str = pydantic.Field(title="Пароль")
    dir_to_backup: str = pydantic.Field(title="Директория для бэкапа", default="/")


    def print_block(self):
        schema = self.schema().get('properties')
        for key, value in schema.items():
            title = typer.style(value.get('title'), fg=typer.colors.GREEN, bold=True)
            val = typer.style(f"{getattr(self, key)}", fg=typer.colors.WHITE, underline=True)
            typer.echo(f"{title}: {val}")


BlockSchema = Block.schema().get('properties')


class Config(pydantic.BaseModel):
    blocks: list[Block]

    @classmethod
    def default(cls) -> 'Config':
        return cls.parse_obj({"blocks": []})
