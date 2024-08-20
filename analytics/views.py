from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from analytics.models import Data
from analytics.serializers import DataSerializer
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


class FilteredAggregationView(APIView):
    def get(self, request):
        data = pd.DataFrame(list(Data.objects.filter(type="CONVERSION").values()))
        aggregated_data = (
            data.groupby("customer_id")
            .agg({"revenue": "mean", "conversions": "mean"})
            .reset_index()
        )
        response = aggregated_data.to_dict(orient="records")
        return Response(response, status=status.HTTP_200_OK)
