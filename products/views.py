from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from user_profile.models import UserProfile

from .models import Category, OrderProduct, Orders, Product
from .permissions import ReadOnlyOrIsAdmin
from .serializers import CategorySerializer, ProductSerializer


class ProductManagement(APIView):
    permission_classes = [ReadOnlyOrIsAdmin]

    def get(self, request):
        all_product_data = Product.objects.all()
        serializer = ProductSerializer(all_product_data, many=True)
        return Response(
            data={
                "message": f"Total Product Count: {len(serializer.data)}",
                "data": serializer.data
            }
        )

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data={
                "message": "Product Created Successfully",
                "product_info": serializer.data
            },
            status=status.HTTP_201_CREATED
        )

    def put(self, request):
        data_obj = Product.objects.filter(name=request.data['name']).first()
        if data_obj is None:
            return Response(
                data={
                    "error": "Product Not Found",
                    "product_info": request.data
                },
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProductSerializer(data_obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data={
                "message": "Product Modified Successfully",
                "product_info": serializer.data
            },
            status=status.HTTP_200_OK
        )

    def delete(self, request):
        data_obj = Product.objects.filter(name=request.data['name']).first()
        if data_obj is None:
            return Response(
                data={
                    "error": "Product Not Found",
                    "product_info": request.data
                },
                status=status.HTTP_404_NOT_FOUND
            )
        data_obj.delete()

        return Response(
            data={
                "message": "Product Deleted Successfully",
                "product_info": request.data
            },
            status=status.HTTP_404_NOT_FOUND
        )


class CategoryManagement(APIView):
    permission_classes = [ReadOnlyOrIsAdmin]

    def get(self, request):
        all_category_data = Category.objects.all()
        serializer = CategorySerializer(all_category_data, many=True)
        return Response(
            data={
                "message": f"Total Category : {len(serializer.data)}",
                "data": serializer.data
            }
        )

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data={
                "message": "Category Created Successfully",
                "product_info": serializer.data
            },
            status=status.HTTP_201_CREATED
        )

    def put(self, request):
        data_obj = Category.objects.filter(name=request.data['name']).first()
        if data_obj is None:
            return Response(
                data={
                    "error": "Category Not Found",
                    "category_info": request.data
                },
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = CategorySerializer(data_obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data={
                "message": "Category Modified Successfully",
                "product_info": serializer.data
            },
            status=status.HTTP_200_OK
        )

    def delete(self, request):
        data_obj = Category.objects.filter(name=request.data['name']).first()
        if data_obj is None:
            return Response(
                data={
                    "error": "Category Not Found",
                    "category_info": request.data
                },
                status=status.HTTP_404_NOT_FOUND
            )
        data_obj.delete()

        return Response(
            data={
                "message": "Category Deleted Successfully",
                "category_info": request.data
            },
            status=status.HTTP_404_NOT_FOUND
        )


class OrderCartOperation(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_order_info = Orders.objects.all()
        return Response(
            data={
                "message": "All Order Info",
                "data": all_order_info
            }
        )

    def post(self, request):
        # Get the user profile
        user_obj = UserProfile.objects.filter(user_id=request.user.user_id).first()
        if user_obj is None:
            raise ValidationError(
                detail={
                    "error": f"User Not Found with user_id: {request.user.user_id}"
                },
                code=status.HTTP_404_NOT_FOUND
            )

        # Validate request data
        if not isinstance(request.data, list):
            raise ValidationError(
                detail={"error": "Invalid data format. Expected a list of products."},
                code=status.HTTP_400_BAD_REQUEST
            )

        # Create the order
        order = Orders.objects.create(user=user_obj)

        # Process products in the order
        product_names = [product_info['name'] for product_info in request.data]
        products = Product.objects.filter(name__in=product_names)
        product_map = {product.name: product for product in products}

        order_products = []
        for product_info in request.data:
            product_name = product_info.get('name')
            product_count = product_info.get('count', 1)

            # Validate product existence
            product_obj = product_map.get(product_name)
            if product_obj is None:
                raise ValidationError(
                    detail={
                        "error": f"Product Not Found with name: {product_name}"
                    },
                    code=status.HTTP_404_NOT_FOUND
                )

            # Create OrderProduct entries
            order_product = OrderProduct(
                order=order,
                product=product_obj,
                quantity=product_count,
                price_per_unit=product_obj.price
            )
            order_products.append(order_product)

        # Bulk create OrderProduct entries
        OrderProduct.objects.bulk_create(order_products)

        # Calculate total price
        order.total_price = sum(
            op.quantity * op.price_per_unit for op in order_products
        )
        order.save()

        # Prepare response data
        response_data = {
            "message": "Order Placed Successfully",
            "order_id": order.id,
            "total_price": order.total_price,
            "products": [
                {
                    "name": op.product.name,
                    "quantity": op.quantity,
                    "price_per_unit": op.price_per_unit
                }
                for op in order_products
            ]
        }

        return Response(data=response_data, status=status.HTTP_201_CREATED)
