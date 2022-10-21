import pandas as pd
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class FileDownloadTest(APIView):
    file_name = 'quantity.xlsx'

    def get(self, request):
        dfs = []
        for _ in range(2):
            df = self.calculate_quantities()
            dfs.append(df)

        overview = pd.concat(dfs)
        overview.set_index(['date', 'name'], inplace=True)

        file_path = f'{settings.MEDIA_DIR_NAME}/invoice/{self.file_name}'
        with open(file_path, 'wb+') as file:
            overview.to_excel(file, sheet_name='products')
            file_url = file_path
        return Response({'path': file_url}, status.HTTP_200_OK)

    @staticmethod
    def calculate_quantities():
        names = [x for x in range(10)]
        quantities = [x for x in range(10)]
        df = pd.DataFrame({'name': names, 'quantity': quantities})
        df['date'] = 'test date'
        return df


__all__ = [
    'FileDownloadTest',
]
