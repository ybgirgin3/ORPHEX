from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Data
from .serializers import DataSerializer
import pandas as pd

class DataViewSet(viewsets.ViewSet):
    queryset = Data.objects.all()

    @action(detail=False, methods=['get'], url_path='conversion-rate')
    def conversion_rate(self, request):
        data = self.queryset
        serializer = DataSerializer(data, many=True)
        df = pd.DataFrame(serializer.data)
        df['conversion_rate'] = df['conversions'] / df['revenue']
        highest_conversion_rate = df.loc[df['conversion_rate'].idxmax()]
        lowest_conversion_rate = df.loc[df['conversion_rate'].idxmin()]
        response = {
            'conversion_rates': df.to_dict(orient='records'),
            'highest_conversion_rate': highest_conversion_rate.to_dict(),
            'lowest_conversion_rate': lowest_conversion_rate.to_dict()
        }
        return Response(response)

    @action(detail=False, methods=['get'], url_path='status-distribution')
    def status_distribution(self, request):
        data = self.queryset
        serializer = DataSerializer(data, many=True)
        df = pd.DataFrame(serializer.data)
        status_distribution = df.groupby(['status', 'type']).agg({'revenue': 'sum', 'conversions': 'sum'}).reset_index()
        response = status_distribution.to_dict(orient='records')
        return Response(response)

    @action(detail=False, methods=['get'], url_path='category-type-performance')
    def category_type_performance(self, request):
        data = self.queryset
        serializer = DataSerializer(data, many=True)
        df = pd.DataFrame(serializer.data)
        category_type_performance = df.groupby(['category', 'type']).agg({'revenue': 'sum', 'conversions': 'sum'}).reset_index()
        top_performance = category_type_performance.sort_values(by='conversions', ascending=False).head(1)
        response = {
            'performance': category_type_performance.to_dict(orient='records'),
            'top_performance': top_performance.to_dict(orient='records')
        }
        return Response(response)

    @action(detail=False, methods=['get'], url_path='filtered-aggregation')
    def filtered_aggregation(self, request):
        data = self.queryset.filter(type='CONVERSION')
        serializer = DataSerializer(data, many=True)
        df = pd.DataFrame(serializer.data)
        aggregated_data = df.groupby('customer_id').agg({'revenue': 'mean', 'conversions': 'mean'}).reset_index()
        response = aggregated_data.to_dict(orient='records')
        return Response(response)
