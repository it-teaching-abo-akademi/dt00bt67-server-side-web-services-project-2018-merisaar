from rest_framework.views import APIView
from rest_framework.decorators import api_view, renderer_classes, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from.models import *
from newApp.serializers import *

@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
@renderer_classes([JSONRenderer,])
def auction_list(request):
    auctions = Auction.objects.all()
    serializer = AuctionShortSerializer(auctions, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def auction_detail(request, pk):
    auction = get_object_or_404(Auction, pk=pk)
    serializer = AuctionDetailSerializer(auction)
    return Response(serializer.data)


class AuctionDetail(APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        auction = get_object_or_404(Auction, pk=pk)
        serializer = AuctionDetailSerializer(auction)
        return Response(serializer.data)

    def post(self, request, pk):
        auction = get_object_or_404(Auction, pk=pk)
        data = request.data
        print(request.data)
        serializer = AuctionDetailSerializer(auction, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

class AuctionDetailSearch(APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, searchString):
        auctions = Auction.objects.filter(auctionTitle__icontains = searchString)
        serializer = AuctionDetailSerializer(auctions, many=True)
        return Response(serializer.data)

@permission_classes((IsAuthenticated, ))
class AuctionBidding(APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    def get(self,request, id):
        auction = get_object_or_404(Auction, id=id)
        auctionbids=BidAuction.objects.filter(auction = auction)
        serializer=BidAuctionSerializer(auctionbids,many=True)
        return Response(serializer.data)

    def post(self, request, id):
        serializer = BidAuctionSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.validated_data)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     bidder = models.ForeignKey(
        # get_user_model(), on_delete=models.CASCADE
     # )
     # timestamp = models.DateTimeField(auto_now_add=True)
     # auction = models.ForeignKey(
     #    Auction, on_delete=models.CASCADE, null = True, related_name = "auctionBid"
     # )
     # value = models.DecimalField(max_digits=5, decimal_places=2, default = 0.0)
     # hasWon = models.BooleanField(default =False)
# class SearchList(ListView):
#     paginate_by = 10
#     template_name = 'homePage/show.html'
#     def get_queryset(self):
#         result = Auction.objects.filter(banned = False, active=True)
#         query = self.request.GET.get('q')
#         if query:
#             query_list = query.split()
#             result = result.filter(auctionTitle__icontains=query)
#                 # reduce(operator.and_,
#                 #        (Q(auctionTitle__icontains=q) for q in query_list))
#             # )
#
#         return result
