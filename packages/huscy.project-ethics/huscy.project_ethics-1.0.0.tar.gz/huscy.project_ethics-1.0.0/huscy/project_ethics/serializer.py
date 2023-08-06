from rest_framework import serializers

from huscy.project_ethics import models, services


class EthicBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EthicBoard
        fields = 'id', 'name'

    def create(self, validated_data):
        return services.create_ethic_board(**validated_data)

    def update(self, ethic_board, validated_data):
        return services.update_ethic_board(ethic_board, **validated_data)


class EthicFileSerializer(serializers.ModelSerializer):
    filename = serializers.CharField(required=False, default='')
    filetype_name = serializers.CharField(source='get_filetype_display', read_only=True)

    class Meta:
        model = models.EthicFile
        fields = (
            'ethic',
            'filehandle',
            'filename',
            'filetype',
            'filetype_name',
            'uploaded_at',
            'uploaded_by',
        )

    def create(self, validated_data):
        creator = self.context['request'].user
        ethic = self.context['ethic']
        return services.create_ethic_file(creator=creator, ethic=ethic, **validated_data)


class UpdateEthicFileSerializer(EthicFileSerializer):
    filename = serializers.CharField()

    class Meta:
        model = models.EthicFile
        fields = 'ethic', 'filename', 'filetype', 'filetype_name'

    def update(self, ethic_file, validated_data):
        return services.update_ethic_file(ethic_file, **validated_data)


class EthicSerializer(serializers.ModelSerializer):
    ethic_board_name = serializers.CharField(source='ethic_board.name', read_only=True)
    ethic_files = EthicFileSerializer(many=True, read_only=True)

    class Meta:
        model = models.Ethic
        fields = 'code', 'ethic_board', 'ethic_board_name', 'ethic_files', 'id', 'project'
        read_only_fields = 'project',

    def create(self, validated_data):
        project = self.context['project']
        return services.create_ethic(project, **validated_data)

    def update(self, ethic, validated_data):
        return services.update_ethic(ethic, **validated_data)
