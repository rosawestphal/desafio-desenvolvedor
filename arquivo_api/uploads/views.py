from django.shortcuts import render

import pandas as pd
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CarregarArquivo
from .serializers import CarregarArquivoSerializer
from django.db.models import Q


@api_view(['POST'])
def carregar_arquivo(request):
    if 'file' not in request.FILES:
        return Response({"detail": "Nenhum arquivo fornecido."}, status=status.HTTP_400_BAD_REQUEST)

    uploaded_file = request.FILES['file']
    file_name = uploaded_file.name

    # Verificar se o arquivo já foi carregado
    if CarregarArquivo.objects.filter(filename=file_name).exists():
        return Response({"detail": "Arquivo já carregado."}, status=status.HTTP_400_BAD_REQUEST)

    # Validar formato do arquivo
    if not file_name.endswith(('.csv', '.xlsx', 'xls')):
        return Response({"detail": "Formato de arquivo inválido. Somente arquivos CSV e Excel são permitidos."}, status=status.HTTP_400_BAD_REQUEST)

    # Salvar o arquivo
    file_instance = CarregarArquivo(filename=file_name, file=uploaded_file)
    file_instance.save()

    return Response({"detail": "Arquivo enviado com sucesso."}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def historia_arquivo(request):
    filename = request.query_params.get('filename', None)
    date = request.query_params.get('date', None)

    filters = Q()

    if filename:
        filters &= Q(filename__icontains=filename)
    if date:
        filters &= Q(uploaded_at__date=date)

    files = CarregarArquivo.objects.filter(filters)

    serializer = CarregarArquivoSerializer(files, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def pesquisar_conteudo_arquivo(request):
    tckr_symb = request.query_params.get('TckrSymb', None)
    rpt_dt = request.query_params.get('RptDt', None)

    # Pegar arquivos carregados
    files = CarregarArquivo

    results_list = []
    
    for file in files:
        try:
            # Abrir o arquivo com pandas
            if file.filename.endswith('.csv'):
                data = pd.read_csv(file.file)
            elif file.filename.endswith('.xlsx'):
                data = pd.read_excel(file.file)
            elif file.filename.endswith('.xls'):
                data = pd.read_excel(file.file)

            # Verificar parâmetros de busca
            if tckr_symb and rpt_dt:
                filtered_data = data[(data['TckrSymb'] == tckr_symb) & (data['RptDt'] == rpt_dt)]
            elif tckr_symb:
                filtered_data = data[data['TckrSymb'] == tckr_symb]
            elif rpt_dt:
                filtered_data = data[data['RptDt'] == rpt_dt]
            else:
                filtered_data = data

            # Processar os resultados
            for _, row in filtered_data.iterrows():
                result_dict = {
                    "RptDt": row.get("RptDt"),
                    "TckrSymb": row.get("TckrSymb"),
                    "MktNm": row.get("MktNm"),
                    "SctyCtgyNm": row.get("SctyCtgyNm"),
                    "ISIN": row.get("ISIN"),
                    "CrpnNm": row.get("CrpnNm")
                }
                results_list.append(result_dict)

        except Exception as e:
            return Response({"detail": f"Erro ao processar o arquivo {file.filename}: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    # Paginação
    page = request.query_params.get('página', 1)
    results_list = results_list[(int(page) - 1) * 10:int(page) * 10]

    return Response(results_list)

