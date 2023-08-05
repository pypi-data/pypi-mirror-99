from django.db import transaction

from pulpcore.app.apps import get_plugin_config


def general_multi_delete(instance_ids):
    """
    Delete a list of model instances in a transaction

    The model instances are identified using the id, app_label, and serializer_name.

    Args:
        instance_ids (list): List of tupels of id, app_label, serializer_name
    """
    instances = []
    for instance_id, app_label, serializer_name in instance_ids:
        serializer_class = get_plugin_config(app_label).named_serializers[serializer_name]
        instances.append(serializer_class.Meta.model.objects.get(pk=instance_id).cast())
    with transaction.atomic():
        for instance in instances:
            instance.delete()
