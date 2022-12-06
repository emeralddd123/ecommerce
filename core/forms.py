from django import forms


class RefundForm(forms.Form):
    ref_code = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))
    email = forms.EmailField()


class CheckoutForm(forms.Form):
    amount = forms.DecimalField( widget=forms.RadioSelect)
    
class TransactionForm(forms.Form):
    order = forms.CharField()
    amount = forms.DecimalField(widget=forms.DecimalField)
    success = forms.BooleanField(widget=forms.CheckboxInput)
    
