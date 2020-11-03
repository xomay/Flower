from rest_framework import serializers

# from .models import Etude

# class EtudeSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Etude
#         fields = ('nomEtude',)
class CustomListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        # Maps for id->instance and id->data item.
        obj_mapping = {obj.id: obj for obj in instance}
        data_mapping = {item['id']: item for item in validated_data}

        # Perform creations and updates.
        ret = []
        for obj_id, data in data_mapping.items():
            obj = obj_mapping.get(obj_id, None)
            if obj is None:
                ret.append(self.child.create(data))
            else:
                ret.append(self.child.update(obj, data))

        # Could be used if the project's phase are in the Serializer query
        # Perform deletions.
        # for obj_id, phase in obj_mapping.items():
        #     if obj_id not in data_mapping:
        #         obj.delete()

        return ret