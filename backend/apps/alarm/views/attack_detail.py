# -*- coding: utf-8 -*-
import base64

from rest_framework.views import APIView

from apps.alarm.models import DetailDomain, DetailTagInfo, DetailLocation
from apps.alarm.serializers.attack_detail_ser import DetailDomainSerializer, DetailTagInfoSerializer, \
    DetailLocationSerializer
from apps.alarm.utils.fofa import FofaClient
from apps.alarm.utils.zeye import ZeyeClient

from common.drf.response import Response
from common.drf.viewsets import GenericViewSet, ListModelMixin


class DetailModelMixin(ListModelMixin, GenericViewSet):
    def list(self, request, *args, **kwargs):
        attack_id = request.query_params.get("attack_id")
        if not attack_id:
            return Response(success=False, data=[], message="参数错误！")
        queryset = self.filter_queryset(self.get_queryset().filter(attack_id=attack_id).order_by('-updated_at'))
        serializer = self.get_serializer(queryset, many=True)
        data = {}
        if serializer.data:
            data = serializer.data[0]
        return Response(success=True, data=data, message="查询成功！")


class DetailDomainViewSet(DetailModelMixin):
    queryset = DetailDomain.objects.all()
    serializer_class = DetailDomainSerializer

    def list(self, request, *args, **kwargs):
        attack_id = request.query_params.get("attack_id")
        if not attack_id:
            return Response(success=False, data=[], message="参数错误！")
        queryset = self.filter_queryset(self.get_queryset().filter(attack_id=attack_id).order_by('-updated_at'))
        serializer = self.get_serializer(queryset, many=True)
        data = {}
        if serializer.data:
            data = serializer.data[0]
        return Response(success=True, data=data, message="查询成功！")


class DetailTagInfoViewSet(DetailModelMixin):
    queryset = DetailTagInfo.objects.all()
    serializer_class = DetailTagInfoSerializer


class DetailLocationViewSet(DetailModelMixin):
    queryset = DetailLocation.objects.all()
    serializer_class = DetailLocationSerializer


class DetailFofaAPIView(APIView):

    def get(self, request, format=None):

        query = request.query_params.get("query")
        page = request.query_params.get("page", 1)
        page_size = request.query_params.get("page_size", 10)
        # print(type(page))
        try:
            if not query:
                return Response(success=False, message="参数错误！")
            page = int(page)
            page_size = int(page_size)
            if not (isinstance(page, int) or isinstance(page_size, int)):
                return Response(success=False, message="参数错误！")
        except Exception:
            return Response(success=False, message="参数错误！")

        # print(type(page), type(page_size))
        # 解码
        # try:
        # decode_str = base64.b64decode(query)
        # query = str(base64.b64decode(query), "utf-8")

        # except Exception:
        #     return Response(success=False, message="参数错误！")
        fc = FofaClient()
        data = fc.search(query=query, page=page, page_size=page_size)
        # data = {'page': 1, 'qbase64': 'dGl0bGU9IuWkp+aVsOaNriI=', 'count': 37207, 'page_size': 10, 'results': [
        #     {'host': 'https://sky.memehs.com', 'title': '天擎大数据平台', 'ip': '117.50.158.198', 'domain': 'memehs.com',
        #      'port': '443', 'country': 'CN', 'province': '', 'city': '', 'country_name': 'China',
        #      'header': 'HTTP/1.1 200 OK\r\nConnection: close\r\nContent-Length: 580\r\nAccept-Ranges: bytes\r\nContent-Type: text/html\r\nDate: Sun, 24 Apr 2022 08:42:19 GMT\r\nEtag: "625f5c1b-244"\r\nLast-Modified: Wed, 20 Apr 2022 01:04:27 GMT\r\nServer: nginx/1.16.1\r\n',
        #      'server': 'nginx/1.16.1', 'protocol': 'https', 'banner': '',
        #      'cert': 'Version:  v3\nSerial Number: 14010541196828421591573906082435440804\nSignature Algorithm: SHA256-RSA\n\nIssuer:\n  Country: US\n  Organization: DigiCert Inc\n  Organizational Unit: www.digicert.com\n  CommonName: Encryption Everywhere DV TLS CA - G1\n\nValidity:\n  Not Before: 2022-03-12 00:00 UTC\n  Not After : 2023-03-12 23:59 UTC\n\nSubject:\n  CommonName: sky.memehs.com\n\nSubject Public Key Info:\n  Public Key Algorithm: RSA\n  Public Key:\n    Exponent: 65537\n    Public Key Modulus: (2048 bits) :\n      E6:1C:0A:8B:08:AB:95:BA:D3:68:F2:C6:99:DF:3B:18:\n      B9:7D:8C:43:4B:59:C8:64:D1:49:7A:E3:07:D4:AE:EE:\n      7D:FA:DC:B3:2F:FD:88:EE:BA:3F:3F:F0:21:C5:36:B0:\n      67:80:6E:4E:2D:73:69:F9:D0:03:A2:18:72:E8:F9:A5:\n      22:1B:77:39:5D:96:2B:F8:44:32:C9:2B:A2:23:C9:E1:\n      D2:38:3F:B6:8B:D9:AD:7D:7B:52:AF:D9:B6:4A:6B:DF:\n      F0:E2:F7:77:8C:5B:22:09:BB:68:89:DC:6D:FE:1E:D9:\n      57:5B:38:81:CD:CE:C0:B3:32:68:C0:2C:FE:04:50:3C:\n      DC:7B:4C:9F:12:F7:9B:F3:C8:1B:CF:E1:57:14:E2:D9:\n      5C:DE:76:59:4A:2B:CE:E6:C8:F7:7D:6F:0C:F0:D8:24:\n      58:8C:4A:34:1B:78:BB:BF:59:38:86:9A:6F:2A:52:56:\n      40:1D:A5:97:FD:47:ED:BB:6F:6D:AA:C1:FA:22:C4:73:\n      15:1C:7A:B2:7F:E4:80:F4:E3:F9:75:42:D5:55:2B:6E:\n      A5:E7:6E:F6:1C:A1:E0:9B:3D:36:3C:1D:12:FE:05:02:\n      42:E2:FF:82:80:6A:80:04:F9:83:A2:44:7A:1F:A7:44:\n      B1:F6:4C:6A:0C:CB:C3:6E:53:96:C9:93:BE:A7:9A:61\n\nAuthority Key Identifier:\n  55:74:4F:B2:72:4F:F5:60:BA:50:D1:D7:E6:51:5C:9A:01:87:1A:D7\n\nSubject Key Identifier:\n  FC:1A:19:AA:DE:63:7B:5C:26:3A:76:87:4D:39:1B:B7:2A:B9:5E:92\n\nBasic Constraints:\n  CA : false\n  Path Length Constraint: UNLIMITED\n\nOCSP Server:\n  http://ocsp.digicert.com\n\nIssuing Certificate URL:\n  http://cacerts.digicert.com/EncryptionEverywhereDVTLSCA-G1.crt\n\nKey Usage:\n  Digital Signature\n  Key Encipherment\n\nExtended Key Usage:\n  Server Auth\n  Client Auth\n\nDNS Names:\n  sky.memehs.com\n\nCertificate Signature Algorithm: SHA256-RSA\nCertificate Signature:\n  7C:A5:86:F1:25:00:53:55:CE:4D:C7:C3:CB:A0:BC:25:\n  85:6F:36:D0:F1:B4:E4:2C:32:CA:E7:65:9A:1A:EB:60:\n  0A:B1:12:87:73:3D:E0:55:5F:C5:8E:CF:5C:0A:68:BB:\n  57:BF:F3:26:62:49:50:E8:39:AE:0C:00:B3:6D:47:85:\n  42:A2:B7:E5:ED:B6:6A:3A:8B:6E:E2:02:BB:F9:51:CC:\n  BA:C8:DF:70:06:51:6C:1D:4F:E5:53:1A:FA:10:65:A8:\n  7D:04:DC:9D:4D:86:20:68:C4:2F:66:51:89:08:36:96:\n  2B:F7:CF:6E:9D:90:67:81:57:18:B1:16:E6:74:9E:BC:\n  39:C8:87:9E:01:17:88:B8:3A:42:6F:4A:70:2A:F0:CF:\n  A6:89:6A:8D:7E:7A:18:B8:C8:17:89:74:B0:14:25:36:\n  5C:3C:10:4F:0E:A3:75:6C:F8:C1:C6:62:E4:9F:46:5B:\n  DF:08:30:F2:AE:23:0F:98:6F:7E:4F:A3:08:28:54:8D:\n  6C:54:E1:FB:13:C3:2E:C4:E9:0B:03:33:2C:D9:99:B4:\n  EA:3A:EF:E6:FD:CF:5E:DB:85:DD:AE:B5:18:33:71:2A:\n  F6:49:B6:2F:70:7B:25:FC:91:E5:A4:97:C5:8A:C4:53:\n  56:0F:31:AB:0D:6A:9D:2D:D3:B5:2A:53:76:B1:CD:9B',
        #      'isp': '', 'as_number': 0, 'as_organization': '', 'latitude': 0, 'ongitude': '', 'icp': '', 'mtime': '',
        #      'uuid': '0be606b9f2615db246e644ac1403cf37'},
        #     {'host': 'geekroom.cn', 'title': '首页-极客公社大数据', 'ip': '106.13.51.113', 'domain': 'geekroom.cn', 'port': '80',
        #      'country': 'CN', 'province': '', 'city': '', 'country_name': 'China',
        #      'header': 'HTTP/1.1 200 OK\r\nConnection: close\r\nTransfer-Encoding: chunked\r\nContent-Type: text/html; charset=utf-8\r\nDate: Sun, 24 Apr 2022 08:44:58 GMT\r\nServer: nginx\r\nStrict-Transport-Security: max-age=31536000\r\nVary: Accept-Encoding\r\n',
        #      'server': 'nginx', 'protocol': 'http', 'banner': '', 'cert': '', 'isp': '', 'as_number': 0,
        #      'as_organization': '', 'latitude': 0, 'ongitude': '', 'icp': '', 'mtime': '',
        #      'uuid': '1c23e1ae8adc997adad53d2432bdbcf1'},
        #     {'host': 'www.geekroom.cn', 'title': '首页-极客公社大数据', 'ip': '106.13.51.113', 'domain': 'geekroom.cn',
        #      'port': '80', 'country': 'CN', 'province': '', 'city': '', 'country_name': 'China',
        #      'header': 'HTTP/1.1 200 OK\r\nConnection: close\r\nTransfer-Encoding: chunked\r\nContent-Type: text/html; charset=utf-8\r\nDate: Sun, 24 Apr 2022 08:44:58 GMT\r\nServer: nginx\r\nStrict-Transport-Security: max-age=31536000\r\nVary: Accept-Encoding\r\n',
        #      'server': 'nginx', 'protocol': 'http', 'banner': '', 'cert': '', 'isp': '', 'as_number': 0,
        #      'as_organization': '', 'latitude': 0, 'ongitude': '', 'icp': '', 'mtime': '',
        #      'uuid': 'cabac83379d736ea13555b0e296d55ce'},
        #     {'host': 'https://106.13.51.113', 'title': '首页-极客公社大数据', 'ip': '106.13.51.113', 'domain': '', 'port': '443',
        #      'country': 'CN', 'province': '', 'city': '', 'country_name': 'China',
        #      'header': 'HTTP/1.1 200 OK\r\nConnection: close\r\nTransfer-Encoding: chunked\r\nContent-Type: text/html; charset=utf-8\r\nDate: Sun, 24 Apr 2022 08:42:57 GMT\r\nServer: nginx\r\nStrict-Transport-Security: max-age=31536000\r\nVary: Accept-Encoding\r\n',
        #      'server': 'nginx', 'protocol': 'https', 'banner': '',
        #      'cert': 'Version:  v3\nSerial Number: 17281084706912139387324926802027147947\nSignature Algorithm: SHA256-RSA\n\nIssuer:\n  Country: US\n  Organization: DigiCert Inc\n  Organizational Unit: www.digicert.com\n  CommonName: Encryption Everywhere DV TLS CA - G1\n\nValidity:\n  Not Before: 2021-09-30 00:00 UTC\n  Not After : 2022-09-30 23:59 UTC\n\nSubject:\n  CommonName: www.geekroom.cn\n\nSubject Public Key Info:\n  Public Key Algorithm: RSA\n  Public Key:\n    Exponent: 65537\n    Public Key Modulus: (2048 bits) :\n      AF:72:1C:23:F4:EA:2E:44:C7:D5:67:36:2A:19:F8:1D:\n      17:DC:90:88:0D:F4:2E:5B:64:37:13:19:0B:B7:72:25:\n      93:B9:6C:E1:A2:56:1A:94:9C:A7:0B:E0:AC:A7:9B:60:\n      D4:55:C1:8C:4B:0E:EE:86:E1:43:F9:27:47:6C:49:C6:\n      85:BB:C7:9D:BD:4E:D6:A0:97:45:70:19:40:84:E3:E5:\n      EC:6E:64:93:55:CB:68:67:4A:26:B8:D6:F8:A6:51:10:\n      96:8D:2D:46:77:1A:9A:46:5E:15:81:5A:96:44:4C:79:\n      76:77:21:91:1E:D9:C3:D6:11:8F:50:CA:16:E3:9B:AB:\n      B2:3E:6C:C7:96:7A:8F:35:14:76:70:80:B1:90:65:E4:\n      81:E9:C3:68:B5:4F:37:4B:11:B3:01:B1:C5:F5:07:EB:\n      67:2D:E3:AD:E5:82:B0:61:CA:BB:F8:21:7B:B1:08:FD:\n      97:6F:E9:26:9C:54:D7:8A:21:48:08:F1:1B:AE:E2:1B:\n      16:D5:18:61:D8:5F:DA:31:5C:98:BB:DA:55:67:6E:4C:\n      99:AD:29:7B:34:D8:44:60:F1:04:17:2F:87:D4:C8:A7:\n      2C:D7:8A:A4:10:59:2E:A3:04:9E:CB:AD:2F:CA:17:53:\n      0C:5E:44:EF:03:7A:B7:CA:0C:79:45:28:9E:29:D3:5F\n\nAuthority Key Identifier:\n  55:74:4F:B2:72:4F:F5:60:BA:50:D1:D7:E6:51:5C:9A:01:87:1A:D7\n\nSubject Key Identifier:\n  BB:B9:F3:79:F3:EA:AE:8F:E1:85:0C:5A:E6:71:A8:3B:CD:94:72:BD\n\nBasic Constraints:\n  CA : false\n  Path Length Constraint: UNLIMITED\n\nOCSP Server:\n  http://ocsp.digicert.com\n\nIssuing Certificate URL:\n  http://cacerts.digicert.com/EncryptionEverywhereDVTLSCA-G1.crt\n\nKey Usage:\n  Digital Signature\n  Key Encipherment\n\nExtended Key Usage:\n  Server Auth\n  Client Auth\n\nDNS Names:\n  www.geekroom.cn\n  geekroom.cn\n\nCertificate Signature Algorithm: SHA256-RSA\nCertificate Signature:\n  79:19:F9:3F:AB:A6:F1:D7:A3:74:C3:EF:12:2B:EA:95:\n  91:C4:CE:E1:48:98:FF:2A:D5:8F:32:23:A3:11:0C:B7:\n  87:53:A2:54:E7:D6:D0:F5:D7:D3:00:70:45:05:72:1E:\n  85:10:84:CD:1E:C5:3F:6E:3B:D3:70:09:50:6B:9C:0E:\n  B7:B7:07:F8:E1:D8:16:95:7B:77:FC:1F:09:BE:47:9C:\n  33:ED:36:22:95:77:B1:C2:F5:4B:14:35:78:89:2E:A2:\n  13:1F:12:74:53:9B:07:8E:76:0F:94:7E:1A:00:5C:FB:\n  C8:63:3A:48:E9:2B:7E:46:CD:DC:17:20:AA:4D:93:BC:\n  4C:6E:7E:D4:CC:B6:AB:FB:ED:E8:5D:83:59:60:88:69:\n  4A:EE:EC:E6:D8:5F:C8:B1:0E:BA:88:3E:6A:7C:23:B5:\n  62:45:9E:85:E9:06:AA:C7:F7:23:5D:75:97:6D:8C:D4:\n  78:04:40:EA:6E:BB:59:65:83:C3:1B:8B:9F:DB:2B:A6:\n  FE:97:09:4C:1E:47:AA:37:D4:31:41:B0:53:A4:2A:74:\n  51:2C:34:20:CF:95:22:B8:4D:BC:24:18:28:34:1E:9D:\n  D4:E1:34:C8:9E:BB:AC:51:AB:FA:43:DE:C1:A4:85:01:\n  9A:E0:FF:83:AC:5F:5F:DB:51:C2:77:5A:EA:1B:77:68',
        #      'isp': '', 'as_number': 0, 'as_organization': '', 'latitude': 0, 'ongitude': '', 'icp': '', 'mtime': '',
        #      'uuid': 'e93b4ae2a15a58d5688c6e1d639403c1'},
        #     {'host': '58.211.54.147:8088', 'title': '智慧公交大数据管理平台', 'ip': '58.211.54.147', 'domain': '', 'port': '8088',
        #      'country': 'CN', 'province': '', 'city': '', 'country_name': 'China',
        #      'header': 'HTTP/1.1 200 OK\r\nConnection: close\r\nContent-Length: 5464\r\nAccept-Ranges: bytes\r\nContent-Type: text/html\r\nDate: Sun, 24 Apr 2022 08:37:35 GMT\r\nEtag: "5f880c40-1558"\r\nLast-Modified: Thu, 15 Oct 2020 08:45:52 GMT\r\nServer: nginx/1.13.11\r\n',
        #      'server': 'nginx/1.13.11', 'protocol': 'http', 'banner': '', 'cert': '', 'isp': '', 'as_number': 0,
        #      'as_organization': '', 'latitude': 0, 'ongitude': '', 'icp': '', 'mtime': '',
        #      'uuid': 'b832a19fdf2435d9e467e7076ad535a7'},
        #     {'host': 'https://map.hengtianyi.com', 'title': '青岛恒天翼海洋气象大数据平台', 'ip': '121.36.109.26',
        #      'domain': 'hengtianyi.com', 'port': '443', 'country': 'CN', 'province': '', 'city': '',
        #      'country_name': 'China',
        #      'header': 'HTTP/1.1 200 OK\r\nConnection: close\r\nContent-Length: 10952\r\nAccept-Ranges: bytes\r\nContent-Type: text/html\r\nDate: Sun, 24 Apr 2022 08:17:55 GMT\r\nEtag: "61cea62c-2ac8"\r\nLast-Modified: Fri, 31 Dec 2021 06:41:48 GMT\r\nServer: nginx\r\nVary: Accept-Encoding\r\n',
        #      'server': 'nginx', 'protocol': 'https', 'banner': '',
        #      'cert': "Version:  v3\nSerial Number: 419945395695578341951901504775473916779242\nSignature Algorithm: SHA256-RSA\n\nIssuer:\n  Country: US\n  Organization: Let's Encrypt\n  CommonName: R3\n\nValidity:\n  Not Before: 2022-02-14 07:03 UTC\n  Not After : 2022-05-15 07:03 UTC\n\nSubject:\n  CommonName: map.hengtianyi.com\n\nSubject Public Key Info:\n  Public Key Algorithm: RSA\n  Public Key:\n    Exponent: 65537\n    Public Key Modulus: (2048 bits) :\n      C6:2E:40:2B:04:F8:21:DD:84:E1:08:60:AB:5C:59:70:\n      23:9E:44:EA:76:0E:2E:A3:C5:8B:2A:9C:40:55:70:AC:\n      A2:9C:96:69:20:4A:51:11:CD:DE:E5:63:92:71:B2:C0:\n      F0:7A:87:6A:B2:94:DF:A7:FE:B7:31:DA:84:88:7C:78:\n      38:F6:3A:9A:5C:E5:36:A3:A8:81:77:8F:22:A9:C4:67:\n      B5:61:A4:01:0B:6C:84:BC:D8:1E:A5:6C:FE:E5:3F:A4:\n      89:E5:A7:E0:22:CB:66:34:52:7E:66:23:2D:2D:70:9B:\n      0F:F1:E4:56:11:49:46:97:AB:8C:B8:B9:8C:75:09:38:\n      BF:32:2E:61:21:8C:9F:DF:B8:45:C2:CC:3A:B6:42:94:\n      59:4A:4F:06:61:A0:81:89:16:03:57:5A:0B:32:FE:93:\n      64:61:E2:BA:24:42:61:43:CA:8A:40:40:AF:25:3D:F4:\n      57:AC:DF:4B:0D:0C:BF:9F:F0:94:91:F2:C4:1E:26:06:\n      45:42:F7:D6:25:CE:60:48:D5:E7:3A:3F:08:25:61:E0:\n      E7:CB:B7:9E:F7:9B:DD:3F:CA:1B:32:84:28:49:D7:92:\n      E2:BC:8C:92:18:89:81:33:F2:EA:C3:22:B1:17:8A:0E:\n      5E:1A:3E:13:40:0E:18:5E:72:AB:52:07:9A:08:F8:8D\n\nAuthority Key Identifier:\n  14:2E:B3:17:B7:58:56:CB:AE:50:09:40:E6:1F:AF:9D:8B:14:C2:C6\n\nSubject Key Identifier:\n  21:F6:82:29:3F:1F:B4:85:F9:CE:80:12:3D:59:8A:92:9C:D6:BA:7A\n\nBasic Constraints:\n  CA : false\n  Path Length Constraint: UNLIMITED\n\nOCSP Server:\n  http://r3.o.lencr.org\n\nIssuing Certificate URL:\n  http://r3.i.lencr.org/\n\nKey Usage:\n  Digital Signature\n  Key Encipherment\n\nExtended Key Usage:\n  Server Auth\n  Client Auth\n\nDNS Names:\n  map.hengtianyi.com\n\nCertificate Signature Algorithm: SHA256-RSA\nCertificate Signature:\n  87:2C:6C:E5:B1:0F:F9:4A:3D:DD:2D:A6:38:8B:7D:90:\n  EE:FA:D0:22:D5:8E:2D:42:33:C3:AB:1C:9B:B1:8E:90:\n  89:39:9B:90:30:0C:3D:81:34:EB:76:80:58:60:6C:E5:\n  6F:04:82:9E:0A:A6:2E:B1:33:30:A7:A3:A6:C5:66:8E:\n  DB:14:1D:7A:75:43:46:33:33:2E:F3:6D:0B:AC:DE:EE:\n  FC:DD:11:E5:42:55:03:E1:27:FC:1C:68:CB:A1:42:A6:\n  40:52:B1:8B:60:75:5C:DA:9E:40:76:37:FB:4D:5B:90:\n  27:2B:E3:99:CA:81:C8:6A:E8:97:A6:46:56:8F:8D:73:\n  6F:8D:3A:D4:BA:65:C8:FA:EE:67:36:AD:11:3E:35:FA:\n  33:CC:85:26:8A:17:93:24:C8:86:3C:E0:F0:38:1B:BE:\n  06:76:8D:61:4D:A2:33:E5:A9:C9:43:39:83:0B:B5:CB:\n  7F:D0:58:B3:36:9F:77:31:F0:EF:EA:33:40:87:7E:A5:\n  03:39:47:C8:64:00:89:DA:45:BC:8E:E9:1E:46:AC:B1:\n  1C:F4:D4:67:2C:57:B1:32:57:70:90:C8:35:B5:E6:61:\n  EF:70:70:B2:5C:39:65:2D:2B:83:97:C8:A3:1F:AA:5C:\n  03:76:5D:49:1B:FE:59:9B:D1:E5:AD:97:D2:10:9C:83",
        #      'isp': '', 'as_number': 0, 'as_organization': '', 'latitude': 0, 'ongitude': '', 'icp': '', 'mtime': '',
        #      'uuid': '7cf6c42db9c2f54230dbd93fc6c05658'},
        #     {'host': '112.44.109.221:9999', 'title': '\t医疗大数据综合应用平台', 'ip': '112.44.109.221', 'domain': '',
        #      'port': '9999', 'country': 'CN', 'province': 'Sichuan', 'city': 'Chengdu', 'country_name': 'China',
        #      'header': 'HTTP/1.1 200 OK\r\nConnection: close\r\nContent-Length: 4779\r\nAccess-Control-Allow-Headers: *\r\nAccess-Control-Allow-Methods: GET, POST, PUT, DELETE\r\nAccess-Control-Allow-Origin: *\r\nCache-Control: private\r\nContent-Type: text/html; charset=utf-8\r\nDate: Sun, 24 Apr 2022 08:16:51 GMT\r\nServer: Microsoft-IIS/7.5\r\nSet-Cookie: ASP.NET_SessionId=enltap3hgoyruo5vsfx1srix; path=/; HttpOnly\r\nX-Aspnet-Version: 4.0.30319\r\nX-Powered-By: ASP.NET\r\n',
        #      'server': 'Microsoft-IIS/7.5', 'protocol': 'http', 'banner': '', 'cert': '', 'isp': '', 'as_number': 0,
        #      'as_organization': '', 'latitude': 0, 'ongitude': '', 'icp': '', 'mtime': '',
        #      'uuid': '8d7300d00b1a727ae98679c860128822'},
        #     {'host': '39.102.196.146:8098', 'title': '册亨县岩架镇大数据平台', 'ip': '39.102.196.146', 'domain': '',
        #      'port': '8098', 'country': 'CN', 'province': 'Beijing', 'city': 'Beijing', 'country_name': 'China',
        #      'header': 'HTTP/1.1 200 OK\r\nConnection: close\r\nContent-Length: 3035\r\nAccept-Ranges: bytes\r\nContent-Type: text/html\r\nDate: Sun, 24 Apr 2022 08:16:54 GMT\r\nEtag: "61b08098-bdb"\r\nLast-Modified: Wed, 08 Dec 2021 09:53:28 GMT\r\nServer: nginx/1.20.0\r\n',
        #      'server': 'nginx/1.20.0', 'protocol': 'http', 'banner': '', 'cert': '', 'isp': '', 'as_number': 0,
        #      'as_organization': '', 'latitude': 0, 'ongitude': '', 'icp': '', 'mtime': '',
        #      'uuid': '20f80deec7128d2359b7039a9bf72016'},
        #     {'host': 'https://121.36.109.26', 'title': '青岛恒天翼海洋气象大数据平台', 'ip': '121.36.109.26', 'domain': '',
        #      'port': '443', 'country': 'CN', 'province': '', 'city': '', 'country_name': 'China',
        #      'header': 'HTTP/1.1 200 OK\r\nConnection: close\r\nContent-Length: 10952\r\nAccept-Ranges: bytes\r\nContent-Type: text/html\r\nDate: Sun, 24 Apr 2022 08:13:54 GMT\r\nEtag: "61cea62c-2ac8"\r\nLast-Modified: Fri, 31 Dec 2021 06:41:48 GMT\r\nServer: nginx\r\nVary: Accept-Encoding\r\n',
        #      'server': 'nginx', 'protocol': 'https', 'banner': '',
        #      'cert': "Version:  v3\nSerial Number: 419945395695578341951901504775473916779242\nSignature Algorithm: SHA256-RSA\n\nIssuer:\n  Country: US\n  Organization: Let's Encrypt\n  CommonName: R3\n\nValidity:\n  Not Before: 2022-02-14 07:03 UTC\n  Not After : 2022-05-15 07:03 UTC\n\nSubject:\n  CommonName: map.hengtianyi.com\n\nSubject Public Key Info:\n  Public Key Algorithm: RSA\n  Public Key:\n    Exponent: 65537\n    Public Key Modulus: (2048 bits) :\n      C6:2E:40:2B:04:F8:21:DD:84:E1:08:60:AB:5C:59:70:\n      23:9E:44:EA:76:0E:2E:A3:C5:8B:2A:9C:40:55:70:AC:\n      A2:9C:96:69:20:4A:51:11:CD:DE:E5:63:92:71:B2:C0:\n      F0:7A:87:6A:B2:94:DF:A7:FE:B7:31:DA:84:88:7C:78:\n      38:F6:3A:9A:5C:E5:36:A3:A8:81:77:8F:22:A9:C4:67:\n      B5:61:A4:01:0B:6C:84:BC:D8:1E:A5:6C:FE:E5:3F:A4:\n      89:E5:A7:E0:22:CB:66:34:52:7E:66:23:2D:2D:70:9B:\n      0F:F1:E4:56:11:49:46:97:AB:8C:B8:B9:8C:75:09:38:\n      BF:32:2E:61:21:8C:9F:DF:B8:45:C2:CC:3A:B6:42:94:\n      59:4A:4F:06:61:A0:81:89:16:03:57:5A:0B:32:FE:93:\n      64:61:E2:BA:24:42:61:43:CA:8A:40:40:AF:25:3D:F4:\n      57:AC:DF:4B:0D:0C:BF:9F:F0:94:91:F2:C4:1E:26:06:\n      45:42:F7:D6:25:CE:60:48:D5:E7:3A:3F:08:25:61:E0:\n      E7:CB:B7:9E:F7:9B:DD:3F:CA:1B:32:84:28:49:D7:92:\n      E2:BC:8C:92:18:89:81:33:F2:EA:C3:22:B1:17:8A:0E:\n      5E:1A:3E:13:40:0E:18:5E:72:AB:52:07:9A:08:F8:8D\n\nAuthority Key Identifier:\n  14:2E:B3:17:B7:58:56:CB:AE:50:09:40:E6:1F:AF:9D:8B:14:C2:C6\n\nSubject Key Identifier:\n  21:F6:82:29:3F:1F:B4:85:F9:CE:80:12:3D:59:8A:92:9C:D6:BA:7A\n\nBasic Constraints:\n  CA : false\n  Path Length Constraint: UNLIMITED\n\nOCSP Server:\n  http://r3.o.lencr.org\n\nIssuing Certificate URL:\n  http://r3.i.lencr.org/\n\nKey Usage:\n  Digital Signature\n  Key Encipherment\n\nExtended Key Usage:\n  Server Auth\n  Client Auth\n\nDNS Names:\n  map.hengtianyi.com\n\nCertificate Signature Algorithm: SHA256-RSA\nCertificate Signature:\n  87:2C:6C:E5:B1:0F:F9:4A:3D:DD:2D:A6:38:8B:7D:90:\n  EE:FA:D0:22:D5:8E:2D:42:33:C3:AB:1C:9B:B1:8E:90:\n  89:39:9B:90:30:0C:3D:81:34:EB:76:80:58:60:6C:E5:\n  6F:04:82:9E:0A:A6:2E:B1:33:30:A7:A3:A6:C5:66:8E:\n  DB:14:1D:7A:75:43:46:33:33:2E:F3:6D:0B:AC:DE:EE:\n  FC:DD:11:E5:42:55:03:E1:27:FC:1C:68:CB:A1:42:A6:\n  40:52:B1:8B:60:75:5C:DA:9E:40:76:37:FB:4D:5B:90:\n  27:2B:E3:99:CA:81:C8:6A:E8:97:A6:46:56:8F:8D:73:\n  6F:8D:3A:D4:BA:65:C8:FA:EE:67:36:AD:11:3E:35:FA:\n  33:CC:85:26:8A:17:93:24:C8:86:3C:E0:F0:38:1B:BE:\n  06:76:8D:61:4D:A2:33:E5:A9:C9:43:39:83:0B:B5:CB:\n  7F:D0:58:B3:36:9F:77:31:F0:EF:EA:33:40:87:7E:A5:\n  03:39:47:C8:64:00:89:DA:45:BC:8E:E9:1E:46:AC:B1:\n  1C:F4:D4:67:2C:57:B1:32:57:70:90:C8:35:B5:E6:61:\n  EF:70:70:B2:5C:39:65:2D:2B:83:97:C8:A3:1F:AA:5C:\n  03:76:5D:49:1B:FE:59:9B:D1:E5:AD:97:D2:10:9C:83",
        #      'isp': '', 'as_number': 0, 'as_organization': '', 'latitude': 0, 'ongitude': '', 'icp': '', 'mtime': '',
        #      'uuid': '1da13f571e3a759bdcd87a7cc12f453f'}]}

        return Response(success=True, data=data, message="查询成功！")


class DetailZoomeyeAPIView(APIView):

    def get(self, request, format=None):

        query = request.query_params.get("query")
        page = request.query_params.get("page", 1)
        # page_size = request.query_params.get("page_size")
        # print(type(page))
        try:
            if not query:
                return Response(success=False, message="参数错误！")
            page = int(page)
            # page_size = int(page_size)
            if not isinstance(page, int):
                return Response(success=False, message="参数错误！")
        except Exception:
            return Response(success=False, message="参数错误！")

        # print(type(page), type(page_size))
        # 解码
        # try:
        # decode_str = base64.b64decode(query)
        # query = str(base64.b64decode(query), "utf-8")

        # except Exception:
        #     return Response(success=False, message="参数错误！")
        client = ZeyeClient()
        # +ip: "156.240.109.234" + port:"80" + after: "2021-01-25 16:37:59"]
        try:
            raw_data = client.get(query_str=query, page=page)
            return Response(success=True, data=raw_data, message="查询成功！")
        except Exception as e:
            print(e)
            return Response(success=False, data=[], message="查询失败！")
