import datetime
from parser.models import Entry
from parser.serializers import EntrySerializer

from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView


def handle_file(file):
    list = []
    for line in file:
        line = line.decode(encoding='UTF-8')
        if len(line) < 80:
            raise Exception("Invalid data format (line).") 
        type = line[0:1]
        date = line[1:9]
        value = line[9:19]
        cpf = line[19:30]
        card = line[31:42]
        time = line[42:48]
        owner = line[48:62]
        outlet = line[62:80]
        entry = EntrySerializer(data={
            'type': int(type),
            'date': datetime.date(int(date[0:4]),int(date[4:6]),int(date[6:8])),
            'value': int(value),
            'cpf': cpf,
            'card': card,
            'time': datetime.time(int(time[0:2]),int(time[2:4]),int(time[4:6])),
            'owner': owner,
            'outlet': outlet})
        if (not entry.is_valid()):
            print(entry)
            raise Exception("Invalid data format.") 
        list.append(entry)
    return list


class FileUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        try:
            file = handle_file(request.FILES['file'])
            for entry in file:
                entry.save()
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': f"{len(file)} {'entries' if len(file) > 1 else 'entry'} were saved."}, status=status.HTTP_201_CREATED)

class EntryList(APIView):

    def get(self, *args, **kwargs):
        owner_cpf = self.kwargs['owner_cpf']
        check = Entry.objects.filter(cpf=owner_cpf).first()
        report = {
            'owner': check.owner,
            'debito': 0,
            'boleto': 0,
            'financimento': 0,
            'credito': 0,
            'recebimento_emprestimo': 0,
            'vendas': 0,
            'recebimento_ted': 0,
            'recebimento_doc': 0,
            'aluguel': 0,
            'total': 0
        }
        
        debito = Entry.objects.filter(cpf=owner_cpf, type=1)
        for item in debito:
            report['debito'] += item.value
        boleto = Entry.objects.filter(cpf=owner_cpf, type=2)
        for item in boleto:
            report['boleto'] += item.value
        financimento = Entry.objects.filter(cpf=owner_cpf, type=3)
        for item in financimento:
            report['financimento'] += item.value
        credito = Entry.objects.filter(cpf=owner_cpf, type=4)
        for item in credito:
            report['credito'] += item.value
        recebimento_emprestimo = Entry.objects.filter(cpf=owner_cpf, type=5)
        for item in recebimento_emprestimo:
            report['recebimento_emprestimo'] += item.value
        vendas = Entry.objects.filter(cpf=owner_cpf, type=6)
        for item in vendas:
            report['vendas'] += item.value
        recebimento_ted = Entry.objects.filter(cpf=owner_cpf, type=7)
        for item in recebimento_ted:
            report['recebimento_ted'] += item.value
        recebimento_doc = Entry.objects.filter(cpf=owner_cpf, type=8)
        for item in recebimento_doc:
            report['recebimento_doc'] += item.value
        aluguel = Entry.objects.filter(cpf=owner_cpf, type=9)
        for item in aluguel:
            report['aluguel'] += item.value
        report['total'] = \
            + report['debito'] \
            - report['boleto'] \
            - report['financimento'] \
            + report['credito'] \
            + report['recebimento_emprestimo'] \
            + report['vendas'] \
            + report['recebimento_ted'] \
            + report['recebimento_doc'] \
            - report['aluguel']

        return Response({f'report': report},
                        status=status.HTTP_201_CREATED)
            
    #permission_classes = [IsAdminUser]

