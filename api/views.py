from uuid import uuid4
from django.db import models
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions

from .models import (
    CmsPage,
    CmsShortcodeCategory,
    CmsShortcodeTemplate,
    CmsShortcodeInstance,
    SiteLayout,
)
from .serializers import (
    CmsCategorySerializer,
    PageCardSerializer,
    PageSerializer,
    SiteLayoutSerializer,
    TemplateSerializer,
    InstanceSerializer,
)


class ShortcodeCategoryViewSet(viewsets.ModelViewSet):
    queryset = CmsShortcodeCategory.objects.all()
    serializer_class = CmsCategorySerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]


class TemplateViewSet(viewsets.ModelViewSet):
    queryset = CmsShortcodeTemplate.objects.all()
    serializer_class = TemplateSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class PageViewSet(viewsets.ModelViewSet):
    queryset = CmsPage.objects.all()
    serializer_class = PageSerializer
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['name', 'slug', 'is_homepage']
    ordering_fields = ['date_of_creation', 'name']
    ordering = ['-date_of_creation']

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'latest']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        qs = super().get_queryset()
        limit = self.request.query_params.get('limit')
        if limit and limit.isdigit():
            qs = qs[:int(limit)]
        return qs

    def get_serializer_class(self):
        if self.action == 'latest':
            return PageCardSerializer
        return super().get_serializer_class()

    @action(detail=False, methods=['get'], url_path='latest', permission_classes=[AllowAny])
    def latest(self, request):
        limit = min(int(request.query_params.get('limit', 6)), 20)
        qs = CmsPage.objects.order_by('-date_of_creation')[:limit]
        ser = PageCardSerializer(qs, many=True, context={'request': request})
        return Response(ser.data)


class PageByFullPathView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        path = (request.query_params.get("full_path") or "").strip("/")
        if path in ("", "home"):
            page = CmsPage.get_homepage()
            if page:
                return Response(PageSerializer(page).data)
            return Response({"detail": "Главная страница не назначена"}, status=404)
        slug = path.split("/")[-1] if path else ""
        page = CmsPage.objects.filter(slug=slug).first()
        if not page:
            return Response({"detail": "Страница не найдена"}, status=404)
        return Response(PageSerializer(page).data)


class InstanceViewSet(viewsets.ModelViewSet):
    queryset = CmsShortcodeInstance.objects.all()
    serializer_class = InstanceSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'tree']:
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['get'], url_path='tree', permission_classes=[AllowAny])
    def tree(self, request):
        page_id = request.query_params.get('page')
        if not page_id:
            return Response({'detail': 'Необходим id страницы'}, status=400)
        roots = CmsShortcodeInstance.objects.filter(page_id=page_id, parent=None)
        serializer = self.get_serializer(roots, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        parent_id = self.request.data.get('parent')
        page_id = self.request.data.get('page')
        if 'position' not in self.request.data:
            siblings = CmsShortcodeInstance.objects.filter(
                parent=parent_id, page=page_id
            )
            max_pos = siblings.aggregate(models.Max('position'))['position__max'] or 0
            serializer.save(
                position=max_pos + 1,
                parent_id=parent_id,
                page_id=page_id
            )
        else:
            serializer.save(parent_id=parent_id, page_id=page_id)

    @action(detail=False, methods=['post'], url_path='bulk_create', permission_classes=[IsAuthenticated])
    def bulk_create(self, request):
        data = request.data
        if not data or not isinstance(data, list):
            return Response({'detail': 'Должен быть передан список'}, status=400)
        page_id = data[0].get('page')
        if not page_id:
            return Response({'detail': 'Нет page id в первом элементе'}, status=400)
        CmsShortcodeInstance.objects.filter(page_id=page_id).delete()
        uid_to_dbid = {}
        instances = []
        for item in data:
            instance = CmsShortcodeInstance.objects.create(
                template_id=item['template'],
                class_list=item.get('class_list', []),
                extra_data=item.get('extra_data', {}),
                page_id=page_id,
                position=item.get('position', 0),
                uid=item.get('uid'),
                is_active=item.get('is_active', True),
                icon_name=item.get('icon_name'),
                allow_children=item.get('allow_children', False),
            )
            uid_to_dbid[item['uid']] = instance.id
            instances.append((instance, item.get('parent')))
        for instance, parent_uid in instances:
            if parent_uid:
                parent_id = uid_to_dbid.get(parent_uid)
                if parent_id:
                    instance.parent_id = parent_id
                    instance.save(update_fields=['parent'])
        instances = CmsShortcodeInstance.objects.filter(page_id=page_id)
        serializer = self.get_serializer(instances, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SiteLayoutViewSet(viewsets.ModelViewSet):
    queryset = SiteLayout.objects.all()
    serializer_class = SiteLayoutSerializer

    def get_queryset(self):
        return SiteLayout.objects.filter(pk=1)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]


class SiteLayoutView(generics.RetrieveUpdateAPIView):
    serializer_class = SiteLayoutSerializer
    queryset = SiteLayout.objects.all()

    def get_permissions(self):
        if self.request.method in ('GET', 'HEAD', 'OPTIONS'):
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_object(self):
        obj, _ = SiteLayout.objects.get_or_create(pk=1)
        return obj
