from django.db import models

# Create your models here.

# Notes:
# blank=False means required field.

class Category(models.Model):
	name = models.CharField(max_length=50, blank=True, null=True)

	class Meta:
		verbose_name_plural = "Category Information"
		app_label = "stockApp"
	
	def __str__(self):
		return self.name
	

class Stock(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True)
	item_name = models.CharField(max_length=50, blank=True, null=True)
	quantity = models.IntegerField(default="0", blank=False, null=True)
	receive_quantity = models.IntegerField(default="0", blank=True, null=True)
	receive_by = models.CharField(max_length=50, blank=True, null=True)
	issue_quantity = models.IntegerField(default="0", blank=True, null=True)
	issue_by = models.CharField(max_length=50, blank=True, null=True)
	issue_to = models.CharField(max_length=50, blank=True, null=True)
	phone_number = models.CharField(max_length=50, blank=True, null=True)
	created_by = models.CharField(max_length=50, blank=True, null=True)
	reorder_level = models.IntegerField(default="0", blank=True, null=True)
	last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	
	class Meta:
		verbose_name_plural = "Stock Information"
		app_label = "stockApp"

	def __str__(self):
		return self.item_name
	

class StockHistory(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
	item_name = models.CharField(max_length=50, blank=True, null=True)
	quantity = models.IntegerField(default="0", blank=True, null=True)
	receive_quantity = models.IntegerField(default="0", blank=True, null=True)
	receive_by = models.CharField(max_length=50, blank=True, null=True)
	issue_quantity = models.IntegerField(default="0", blank=True, null=True)
	issue_by = models.CharField(max_length=50, blank=True, null=True)
	issue_to = models.CharField(max_length=50, blank=True, null=True)
	phone_number = models.CharField(max_length=50, blank=True, null=True)
	created_by = models.CharField(max_length=50, blank=True, null=True)
	reorder_level = models.IntegerField(default="0", blank=True, null=True)
	last_updated = models.DateTimeField(auto_now_add=False, auto_now=False, null=True)
	timestamp = models.DateTimeField(auto_now_add=False, auto_now=False, null=True)

	class Meta:
		verbose_name_plural = "Stock History"
		app_label = "stockApp"

	def __str__(self):
		return self.item_name
