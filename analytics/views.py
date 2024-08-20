from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
import pandas as pd
from .models import Data
from .serializers import DataSerializer

class DataViewSet(viewsets.ViewSet):
    "Data viewset for handling API requests related to data analysis."
    
    queryset = Data.objects.all()  # Define the queryset to be used for all actions

    @action(detail=False, methods=['get'], url_path='conversion-rate')
    def conversion_rate(self, request):
        """
        Endpoint to get conversion rates, highest and lowest conversion rates.
        """
        # Get all data from the database
        data = self.queryset
        # Serialize data into a format suitable for DataFrame conversion
        serializer = DataSerializer(data, many=True)
        # Convert serialized data to a pandas DataFrame
        df = pd.DataFrame(serializer.data)

        # Calculate conversion rate as conversions divided by revenue
        df['conversion_rate'] = df['conversions'] / df['revenue']
        # Find the customer with the highest conversion rate
        highest_conversion_rate = df.loc[df['conversion_rate'].idxmax()]
        # Find the customer with the lowest conversion rate
        lowest_conversion_rate = df.loc[df['conversion_rate'].idxmin()]
        response = {
            'conversion_rates': df.to_dict(orient='records'),
            'highest_conversion_rate': highest_conversion_rate.to_dict(),
            'lowest_conversion_rate': lowest_conversion_rate.to_dict()
        }
        return Response(response)

    @action(detail=False, methods=['get'], url_path='status-distribution')
    def status_distribution(self, request):
        """
        Endpoint to get distribution of status based on type, including total revenue and conversions.
        """
        # Get all data from the database
        data = self.queryset
        # Serialize data
        serializer = DataSerializer(data, many=True)
        # Convert serialized data to a pandas DataFrame
        df = pd.DataFrame(serializer.data)
        # Group by status and type, then aggregate revenue and conversions
        status_distribution = df.groupby(['status', 'type']).agg({'revenue': 'sum', 'conversions': 'sum'}).reset_index()
        response = status_distribution.to_dict(orient='records')
        return Response(response)

    @action(detail=False, methods=['get'], url_path='category-type-performance')
    def category_type_performance(self, request):
        """
        Endpoint to get performance metrics by category and type, and highlight the top-performing category and type.
        """
        # Get all data from the database
        data = self.queryset
        # Serialize data
        serializer = DataSerializer(data, many=True)
        # Convert serialized data to a pandas DataFrame
        df = pd.DataFrame(serializer.data)
        # Group by category and type, then aggregate revenue and conversions
        category_type_performance = df.groupby(['category', 'type']).agg({'revenue': 'sum', 'conversions': 'sum'}).reset_index()
        # Identify the top-performing category and type based on conversions
        top_performance = category_type_performance.sort_values(by='conversions', ascending=False).head(1)
        response = {
            'performance': category_type_performance.to_dict(orient='records'),
            'top_performance': top_performance.to_dict(orient='records')
        }
        return Response(response)

    @action(detail=False, methods=['get'], url_path='filtered-aggregation')
    def filtered_aggregation(self, request):
        """
        Endpoint to get aggregated data for rows where type is 'CONVERSION', including mean revenue and conversions per customer.
        """
        # Filter data where the type is 'CONVERSION'
        data = self.queryset.filter(type='CONVERSION')
        # Serialize data
        serializer = DataSerializer(data, many=True)
        # Convert serialized data to a pandas DataFrame
        df = pd.DataFrame(serializer.data)
        # Group by customer_id and calculate the mean revenue and conversions
        aggregated_data = df.groupby('customer_id').agg({'revenue': 'mean', 'conversions': 'mean'}).reset_index()
        response = aggregated_data.to_dict(orient='records')
        return Response(response)
