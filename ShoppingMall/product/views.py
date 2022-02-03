from tkinter.tix import Form
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from rest_framework import generics, mixins
from .models import Product
from .forms import RegisterForm
from order.forms import RegisterForm as OrderForm
from user.decorators import admin_required
from .serializers import ProductSerializer
# Create your views here.


# rest_framework에서 제공하는 view 생성
class ProductListAPI(generics.GenericAPIView, mixins.ListModelMixin):
    # 데이터에 대한 검증을 해야한다 -> serializer를 등록해주어야 한다
    serializer_class = ProductSerializer

    # 어떤 데이터를 가지고, restAPI를 제공할 것인지 명시해야 한다
    def get_queryset(self):
        return Product.objects.all().order_by('id')

    def get(self, request, *args, **kwargs):
        # list라는 함수를 호출하게 되면, 모델로부터 데이터를 가져와서 JSON 형태로 변환해준다
        # mixins 안에 존재
        return self.list(request, *args, **kwargs)


# RetrieveModelMixin은 상세보기를 위한 Mixin이다
class ProductDetailAPI(generics.GenericAPIView, mixins.RetrieveModelMixin):
    # 데이터에 대한 검증을 해야한다 -> serializer를 등록해주어야 한다
    serializer_class = ProductSerializer

    # 어떤 데이터를 가지고, restAPI를 제공할 것인지 명시해야 한다
    def get_queryset(self):
        # list를 가져오는 것이 아닌, 하나의 상품 정보를 가져오는 것인데 왜 all을 가지고 오나
        # -> RetrieveModelMixin을 상속받고 get 함수를 사용하게 되면, url에서 pk값을 연결해 주어야하기 때문에, queryset안에서 해당 pk에 맞는 상품을 준다
        return Product.objects.all().order_by('id')

    def get(self, request, *args, **kwargs):
        # list라는 함수를 호출하게 되면, 모델로부터 데이터를 가져와서 JSON 형태로 변환해준다
        # mixins 안에 존재
        return self.retrieve(request, *args, **kwargs)


class ProductList(ListView):
    model = Product
    template_name = 'product.html'
    context_object_name = 'product_list'


@method_decorator(admin_required, name='dispatch')
class ProductCreate(FormView):
    template_name = 'register_product.html'
    form_class = RegisterForm
    success_url = '/product/'

    def form_valid(self, form):
        product = Product(
            name=form.data.get('name'),
            price=form.data.get('price'),
            description=form.data.get('description'),
            stock=form.data.get('stock')
        )
        product.save()

        return super().form_valid(form)


class ProductDetail(DetailView):
    template_name = 'product_detail.html'
    queryset = Product.objects.all()
    context_object_name = 'product'

    def get_context_data(self, **kwargs):  # detail 뷰에 form을 전달
        context = super().get_context_data(**kwargs)
        context['form'] = OrderForm(self.request)
        return context
