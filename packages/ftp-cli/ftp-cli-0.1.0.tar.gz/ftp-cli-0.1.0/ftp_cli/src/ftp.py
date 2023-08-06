import ftplib, os, typer, datetime, zipfile, shutil
from ftp_cli.src.config.controllers import ConfigController
from ftp_cli.src.utils import APP_NAME

app = typer.Typer()


def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(path, '..')))


def get_files_directories(ftp_obj):
    dirlist = []
    ftp_obj.retrlines('LIST', callback=dirlist.append)

    files = []
    directories = []

    for l in dirlist:
        lastspace = l.rindex(' ')
        file_name = l[lastspace+1:]
        if l[0] == 'd' and file_name != '.' and file_name != '..':
            directories.append(file_name)
        elif l[0] == '-':
            files.append(file_name)
        
    return files, directories


def backup_directory(ftp_obj, local_dir, remote_dir):
    os.chdir(local_dir)
    try:
        ftp_obj.cwd(remote_dir)
        files, directories = get_files_directories(ftp_obj)

        with typer.progressbar(files, label="Скачивание файлов") as progress:
            for f in progress:
                try:
                    ftp_obj.retrbinary('RETR ' + f, open(f, 'wb').write)
                except ftplib.error_perm:
                    typer.echo("Skipped " + typer.style(f, fg=typer.colors.RED) + " due to permissions")
        
        with typer.progressbar(directories, label="Скачивание папок") as progress:
            for d in progress:
                newremote = remote_dir+d+'/'
                newlocal = local_dir+'/'+d+'/'
                os.mkdir(newlocal)
                backup_directory(ftp_obj, newlocal, newremote)
    except ftplib.error_perm:
        typer.secho("Skipped remote dir due to permissions", fg=typer.colors.RED)


@app.command()
def create(alias: str = typer.Argument(...)):
    config = ConfigController.parse_config()
    app_dir = typer.get_app_dir(APP_NAME)
    if len(config.blocks):
        filtered_blocks = list(filter(lambda x: x.alias == alias, config.blocks))
        if not len(filtered_blocks):
            typer.secho(f"Записи с алиасом {alias} не существует.", fg=typer.colors.RED)
        else:
            backup_block = filtered_blocks[0]
            os.chdir(app_dir)
            os.mkdir('backups')
            os.chdir('backups')
            backup_path = f"{backup_block.alias}_{datetime.datetime.now().strftime('%Y-%M-%dT%H:%m')}"
            os.mkdir(backup_path)
            os.chdir(backup_path)
            local_dir = os.getcwd()
            ftp_obj = ftplib.FTP(host=backup_block.hostname, user=backup_block.login, passwd=backup_block.password)
            ftp_obj.set_pasv(False)
            backup_directory(ftp_obj=ftp_obj, local_dir=local_dir, remote_dir=backup_block.dir_to_backup)
            ftp_obj.quit()
            typer.secho("Backup created successfully. Compressing...", fg=typer.colors.BLUE)
            zipf = zipfile.ZipFile(f"{local_dir}.zip", 'w', zipfile.ZIP_DEFLATED)
            zipdir(local_dir, zipf)
            zipf.close()
            shutil.rmtree(local_dir)
            typer.secho("Backup compressed. Done", fg=typer.colors.GREEN)
    else:
        typer.echo("Nothing to backup...")
