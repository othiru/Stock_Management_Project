from django import forms
from .models import *

class StockCreateForm(forms.ModelForm):
   class Meta:
      model = Stock
      fields = ["category", "item_name", "quantity"]

   def clean_category(self):
      category = self.cleaned_data.get("category")
      if not category:
         raise forms.ValidationError("This field is required")
      return category

   def clean_item_name(self):
      category = self.clean_category()
      item_name = self.cleaned_data.get("item_name")
      if not item_name:
         raise forms.ValidationError("This field is required")
      for instance in Stock.objects.all():
         if instance.category == category and instance.item_name == item_name:
            raise forms.ValidationError(f"{item_name} under {category} category is already created")
      return item_name

         

class StockSearchForm(forms.ModelForm):
   # category = forms.CharField(required=False)
   # item_name = forms.CharField(required=False)
   export_to_CSV = forms.BooleanField(required=False)
   class Meta:
      model = Stock
      fields = ["category", "item_name"]



class StockUpdateForm(forms.ModelForm):
   class Meta:
      model = Stock
      fields = ["category", "item_name", "quantity"]

      
class IssueForm(forms.ModelForm):
   class Meta:
      model = Stock
      fields = ["issue_quantity", "issue_to"]

      
class ReceiveForm(forms.ModelForm):
   class Meta:
      model = Stock
      fields = ["receive_quantity"]


class StockReorderLevelForm(forms.ModelForm):
   class Meta:
      model = Stock
      fields = ["reorder_level"]


class StockHistorySearchForm(forms.ModelForm):
   # category = forms.CharField(required=False)
   # item_name = forms.CharField(required=False)
   export_to_CSV = forms.BooleanField(required=False)
   start_date = forms.DateTimeField(required=False, widget=forms.TextInput(attrs={"class": "datetimeinput", "placeholder": "YYYY-MM-DD"}))
   end_date = forms.DateTimeField(required=False, widget=forms.TextInput(attrs={"class": "datetimeinput", "placeholder": "YYYY-MM-DD"}))
   class Meta:
      model = StockHistory
      fields = ["category", "item_name", "start_date", "end_date"]