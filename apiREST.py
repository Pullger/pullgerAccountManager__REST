from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from pullgerAccountManager import apiAM
from pullgerInternalControl.pullgerAccountManager import api as exceptions
from . import serializers
import logging


class Ping(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        content ={'message': 'Pong. Account Manager.'}
        return Response(content)


class PingAuth(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Pong. Account Manager.'}
        return Response(content)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def get_account_list(request):
    logger = logging.getLogger('pullgerAccountManager.REST.getAccountList')

    if request.method == 'GET':
        accountList = apiAM.get_account_list()

        serializedContent = serializers.AccountListSerializer(accountList, many=True)
        content ={'message': 'OK', 'data': serializedContent.data}

        response = Response(content)
        response['Cache-Control'] = 'no-cache'

        return response
    elif request.method == 'POST':
        returnMessage = ''
        requestData = request.data.copy()

        content = {
            'message': 'OK',
            'data': {}
        }

        parameters = {}
        # -----------------login----------------
        login = requestData.get('login')
        if login is None:
            returnMessage = returnMessage + "[Login] is required field."
        else:
            parameters['login'] = login
        # -------------------password---------------
        password = requestData.get('password')
        if password is None:
            returnMessage = returnMessage + "[Password] is required field."
        else:
            parameters['password'] = password
        # --------------------authorization---------------
        authorization = requestData.get('authorization')
        if authorization is None:
            returnMessage = returnMessage + "[Authorization] is required field."
        else:
            parameters['authorization'] = authorization
        # --------------------------------------------------

        if returnMessage != '':
            if 'password' in requestData:
                requestData['password'] = '*****'

            statusResp = status.HTTP_400_BAD_REQUEST
            logger.info({'requestData': requestData, 'discription': returnMessage, 'path': request.stream.path})
        else:
            try:
                newUUID = apiAM.add_account(**parameters)
                content['data']['uuid'] = newUUID
                statusResp = status.HTTP_200_OK
                returnMessage = 'OK'
            except exceptions.IncorrectInputData as e:
                statusResp = status.HTTP_400_BAD_REQUEST
                returnMessage = str(e)
                requestData['password'] = '*****'
                logger.info({'requestData': requestData, 'description': returnMessage, 'path': request.stream.path})
            except BaseException as e:
                statusResp = status.HTTP_500_INTERNAL_SERVER_ERROR
                requestData['password'] = '*****'
                logger.error({'requestData':requestData , 'description': str(e), 'path': request.stream.path})
                returnMessage = 'Internal system error. Contact to support.'

        content['message'] = returnMessage

        return Response(content, status=statusResp)


# @api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
# def pingParam(request, uuid):
#     if request.method == 'GET':
#         content = {'message': 'GET Pong:' + uuid}
#         return Response(content)
#     elif request.method == 'POST':
#         content = {'message': 'POST Pong:' + uuid}
#         return Response(content)
#
# @api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
# def sessionOperations(request, uuid):
#     if request.method == 'DELETE':
#         statusResp = status.HTTP_200_OK
#         try:
#             api.killSession(uuid=uuid)
#             content = {'message': f'Session {uuid} deleted:'}
#         except:
#             content = {'message': 'error'}
#             statusResp = status.HTTP_500_INTERNAL_SERVER_ERROR
#
#         return Response(content, status=statusResp)
#
# @api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
# def sessionOperationsGeneral(request):
#     if request.method == 'GET':
#         sessionList = api.getSessionsList()
#
#         serializedContent = serializers.SessionsListSerializer(sessionList, many=True)
#         content ={'message': 'OK', 'data': serializedContent.data}
#
#         response = Response(content)
#         response['Cache-Control'] = 'no-cache'
#
#         return response
#     elif request.method == 'POST':
#         try:
#             api.addNewSession()
#             content = {'message': 'Session added'}
#         except BaseException as e:
#             content ={'message': f'error: {str(e)}'}
#
#         return Response(content)