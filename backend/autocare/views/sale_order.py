
from autocare.models import EmployeeModel
from autocare.models import SaleOrderModel
from rest_framework import serializers
from rest_framework.filters import BaseFilterBackend
from dvadmin.utils.viewset import CustomModelViewSet
from dvadmin.utils.serializers import CustomModelSerializer
from autocare.views.vehicle import VehicleModelSerializer
from autocare.views.employee import EmployeeModelSerializer, EmployeeModelCreateUpdateSerializer
from autocare.views.sale_order_part import SaleOrderPartModelSerializer
class SaleOrderModelSerializer(CustomModelSerializer):
    """
    序列化器
    """
    employees = EmployeeModelSerializer(many=True, read_only=True)
    parts = SaleOrderPartModelSerializer(read_only=True, many=True)
    # vehicle = VehicleModelSerializer(read_only=True) 前端只需要这个 vehicle 的 id
    class Meta:
        model = SaleOrderModel
        fields = [
            'id', 'total_price', 'real_price', 'discounted_price', 'datetime',
            'vehicle', 'employees', 'current_mile', 'status', 'parts', 'payee', 'pay_method',
        ]

class SaleOrderModelCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """
    employees = serializers.PrimaryKeyRelatedField(many=True, queryset=EmployeeModel.objects.all())
    class Meta:
        model = SaleOrderModel
        fields = [
            'id', 'total_price', 'real_price', 'discounted_price', 'datetime',
            'vehicle', 'employees', 'current_mile', 'status', 'payee', 'pay_method',
        ]
    def update(self, instance, validated_data):
        # 自定义更新逻辑
        status = validated_data.get('status', None)
        if status == 0:
            # 如果status为0，清空payee和pay_method的值
            validated_data['payee'] = None
            validated_data['pay_method'] = -1  # 设置为默认值或者你认为合适的值

        return super().update(instance, validated_data)

class CustomFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        params = request.query_params
        if view.action == 'list':
            #TODO: 根据是否包含某个配件(VehiclePart)筛选订单 not (SaleVehiclePart)
            return queryset
        return queryset
class SaleOrderViewSet(CustomModelViewSet):
    """
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = SaleOrderModel.objects.all()
    # filter_backends = [CustomFilter]
    serializer_class = SaleOrderModelSerializer
    create_serializer_class = SaleOrderModelCreateUpdateSerializer
    update_serializer_class = SaleOrderModelCreateUpdateSerializer
    filter_fields = {
        'vehicle': ['exact'],
        'status': ['exact'],
    }
    search_fields = ['vehicle', 'status']
