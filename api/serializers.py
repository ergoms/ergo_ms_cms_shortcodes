from rest_framework import serializers

from .models import (
    CmsPage,
    CmsShortcodeCategory,
    CmsShortcodeTemplate,
    CmsShortcodeInstance,
    SiteLayout,
)


class CmsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CmsShortcodeCategory
        fields = ['id', 'name']


class TemplateSerializer(serializers.ModelSerializer):
    component_type = serializers.SlugRelatedField(
        queryset=CmsShortcodeCategory.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = CmsShortcodeTemplate
        fields = [
            'id', 'name', 'component_type', 'class_list', 'extra_data',
            'is_active', 'icon_name', 'allow_children'
        ]


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class InstanceSerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True, read_only=True)
    template_name = serializers.CharField(source='template.name', read_only=True)
    component_type = serializers.CharField(source='template.component_type.name', read_only=True)
    parent = serializers.PrimaryKeyRelatedField(
        queryset=CmsShortcodeInstance.objects.all(), allow_null=True, required=False
    )
    uid = serializers.CharField()

    class Meta:
        model = CmsShortcodeInstance
        fields = [
            'id', 'template', 'template_name', 'component_type', 'page', 'parent',
            'class_list', 'extra_data', 'position', 'children', 'uid', 'allow_children'
        ]


class SiteLayoutSerializer(serializers.ModelSerializer):
    menu_pages = serializers.PrimaryKeyRelatedField(
        queryset=CmsPage.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = SiteLayout
        fields = ['id', 'header_template', 'footer_template', 'menu_pages']


class PageCardSerializer(serializers.ModelSerializer):
    preview_image = serializers.SerializerMethodField()

    class Meta:
        model = CmsPage
        fields = ['id', 'name', 'full_url', 'preview_image']

    def get_preview_image(self, page):
        img_inst = (
            page.instances
            .filter(template__component_type__name='Image')
            .order_by('position')
            .first()
        )
        return (
            img_inst.extra_data.get('src')
            if img_inst and img_inst.extra_data
            else None
        )


class PageSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(required=False, allow_null=True, allow_blank=True)
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())
    instances = InstanceSerializer(many=True, read_only=True)
    full_url = serializers.SerializerMethodField()

    class Meta:
        model = CmsPage
        fields = [
            'id', 'name', 'slug', 'is_homepage', 'instances', 'full_url', 'creator'
        ]

    def get_full_url(self, obj):
        return obj.get_full_url()

    def validate(self, attrs):
        slug = attrs.get('slug') or ''
        if not slug and not attrs.get('is_homepage'):
            raise serializers.ValidationError({'slug': 'Обязательное поле.'})
        return attrs
