from django import forms
from product.models import Product
from user.models import User
from .models import Order
from django.db import transaction


class RegisterForm(forms.Form):

    # init(생성자) 함수를 만들면서 request를 form에 전달할 수 있게 한다
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    quantity = forms.IntegerField(
        error_messages={
            'required': '수량을 입력해주세요.'
        }, label='수량'
    )
    # user에 대한 정보는 로그인한 사용자 정보가 자동으로 전달되게 할 것
    # product에 대한 정보는 id로 받을 것 -> 마찬가지로 forn에서 작성하는 것이 아닌 주문하기를 누르면 그 상품이 주문되도록 할 것
    product = forms.IntegerField(
        error_messages={
            'required': '상품명을 입력해주세요.'
        }, label='상품명', widget=forms.HiddenInput
    )

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity')
        product = cleaned_data.get('product')

        if not (quantity and product):
            self.add_error('quantity', '값이 없습니다.')
            self.add_error('product', '값이 없습니다.')
