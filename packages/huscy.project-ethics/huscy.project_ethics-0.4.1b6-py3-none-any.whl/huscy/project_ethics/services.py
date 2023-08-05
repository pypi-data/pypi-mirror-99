from huscy.project_ethics.models import Ethic, EthicBoard, EthicFile


def create_ethic(project, ethic_board, code=''):
    return Ethic.objects.create(project=project, ethic_board=ethic_board, code=code)


def create_ethic_file(ethic, filehandle, filetype, creator):
    filename = filehandle.name.split('/')[-1]

    return EthicFile.objects.create(
        ethic=ethic,
        filehandle=filehandle,
        filename=filename,
        filetype=filetype,
        uploaded_by=creator.get_full_name(),
    )


def get_ethic_files(ethic):
    return EthicFile.objects.filter(ethic=ethic)


def get_ethics(project):
    return Ethic.objects.filter(project=project)


def get_ethic_boards():
    return EthicBoard.objects.order_by('name')
