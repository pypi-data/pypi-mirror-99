from enum import Enum

from django.db import models
from django.utils.translation import gettext_lazy as _

from huscy.projects.models import Project


class EthicBoard(models.Model):
    name = models.CharField(_('Name'), max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = 'name',
        verbose_name = _('Ethic board')
        verbose_name_plural = _('Ethic boards')


class Ethic(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='ethics',
                                verbose_name=_('Project'))
    ethic_board = models.ForeignKey(EthicBoard, on_delete=models.PROTECT,
                                    verbose_name=_('Ethic board'))
    code = models.CharField(_('Code'), max_length=255, blank=True, default='')

    class Meta:
        ordering = '-project', 'ethic_board__name'
        unique_together = 'project', 'ethic_board'
        verbose_name = _('Ethic')
        verbose_name_plural = _('Ethics')


class EthicFile(models.Model):
    class TYPE(Enum):
        proposal = (0, _('Ethic proposal'))
        votum = (1, _('Ethic votum'))
        amendment = (2, _('Ethic amendment'))

        @classmethod
        def get_value(cls, member):
            return cls[member].value[0]

    def get_upload_path(self, filename):
        return f'{self.ethic.project.local_id_name}/ethics/{filename}'

    ethic = models.ForeignKey(Ethic, on_delete=models.CASCADE, related_name='ethic_files',
                              editable=False, verbose_name=_('Ethic'))

    filetype = models.PositiveSmallIntegerField(_('File type'), choices=[x.value for x in TYPE])

    filehandle = models.FileField(_('File handle'), upload_to=get_upload_path)
    filename = models.CharField(_('File name'), max_length=255)

    uploaded_at = models.DateTimeField(_('Uploaded at'), auto_now_add=True, editable=False)
    uploaded_by = models.CharField(_('Uploaded by'), max_length=126, editable=False)

    class Meta:
        ordering = '-ethic__project', '-ethic', 'filename'
        verbose_name = _('Ethic file')
        verbose_name_plural = _('Ethic files')
