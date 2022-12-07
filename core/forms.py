from django import forms
from django.forms.fields import Field  
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit

PAY_CHOICES = [
    ('1', "ACCOUNT BALANCE"),
    ("2", "NONE")
    ]

class RefundForm(forms.Form):
    ref_code = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))
    email = forms.EmailField()


#class CheckoutForm(forms.Form):
#    payment_choice = forms.ChoiceField(widget=forms.CheckboxInput, choices = PAY_CHOICES,)
    
    
class TransactionForm(forms.Form):
    order = forms.CharField()
    amount = forms.DecimalField(widget=forms.DecimalField)
    success = forms.BooleanField(widget=forms.CheckboxInput)
    

class PaymentForm(forms.Form):
    
    payment_choice = forms.ChoiceField(
        choices=(
            ('1', "ACCOUNT BALANCE"),
        ),
        widget=forms.RadioSelect(),
        initial='1',
        required=True,
        label="How would you like to pay?",
        #help_text="Select the balance option?.",
        error_messages={
            "required": "Select the best way to send a confirmation message"
        },
    )
    
    
'''
    def __init__(self, *args, **kwargs):
        super(CheckoutForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field.radios("name", legend_size=Size.MEDIUM, legend_tag="h1", inline=True),
            Field.radios(
                "method",
                legend_size=Size.MEDIUM,
                small=True,
            ),
            Submit("submit", "Submit"),
        )
        '''