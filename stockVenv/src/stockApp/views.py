from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
import csv
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.core.paginator import Paginator

# Create your views here.

@login_required
def home(request):
	return render(request, "home.html")


@login_required
def list_items(request):
	form = StockSearchForm(request.POST or None)
	queryset = Stock.objects.all()

	context = {
		"form": form,
		"queryset": queryset,
	}


	if request.method == "POST":
		category = form["category"].value()
		queryset = Stock.objects.filter(item_name__icontains=form["item_name"].value())

		if category != "":
			queryset = queryset.filter(category_id = category)
		
		if form["export_to_CSV"].value() == True:
			response = HttpResponse(content_type="text/csv")
			response["Content-Disposition"] = "attachment; filename=List of Stock Items.csv"
			writer = csv.writer(response)
			writer.writerow(["CATEGORY", "ITEM NAME", "QUANTITY"])
			for x in queryset:
				writer.writerow([x.category, x.item_name, x.quantity])
			return response
		

		context = {
			"form": form,
			"queryset": queryset
		}
	
	return render(request, "list_items.html", context)


@login_required
def add_items(request):
	form = StockCreateForm(request.POST or None)
	if form.is_valid():
		form.save()
		messages.success(request, "Successfully Added")
		return redirect("/list_items")
	context = {
		"addUpdateItemTitle": "ADD ITEM",
		"addUpdateItemBtn": "SAVE",
		"form": form
	}
	return render(request, "add_items.html", context)


@login_required
def update_items(request, pk):
	queryset = Stock.objects.get(id=pk)
	form = StockUpdateForm(instance=queryset)
	if request.method == "POST":
		form = StockUpdateForm(request.POST or None, instance=queryset)
		if form.is_valid():
			form.save()
			messages.success(request, "Successfully Updated")
			return redirect("/list_items")
	context = {
		"addUpdateItemTitle": "UPDATE ITEM",
		"addUpdateItemBtn": "UPDATE",
		"form": form
	}
	return render(request, "add_items.html", context)


@login_required
def delete_items(request, pk):
	queryset = Stock.objects.get(id=pk)
	context = {
		"queryset": queryset
	}
	if request.method == "POST":
		queryset.delete()
		messages.success(request, "Successfully Deleted")
		return redirect("/list_items")
	
	return render(request, "delete_items.html", context)


@login_required
def stock_details(request, pk):
	queryset = Stock.objects.get(id=pk)
	context = {
		"queryset": queryset
	}
	return render(request, "stock_details.html", context)


@login_required
def issue_items(request, pk):
	queryset = Stock.objects.get(id=pk)
	form = IssueForm(request.POST or None, instance=queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.receive_quantity = 0
		instance.quantity -= instance.issue_quantity
		instance.issue_by = str(request.user)
		instance.save()
		messages.success(request, "Successfully Issued. " + str(instance.quantity) + " " + str(instance.item_name) + "(s) Left in Stock Now.")
		return redirect("/stock_details/"+str(instance.id))

	context = {
		"addUpdateItemTitle": "ISSUE \"" + str(queryset.item_name) + "\"",
		"queryset": queryset,
		"form": form,
		"addUpdateItemBtn": "ISSUE",
		"username": "Issue By: " + str(request.user)
	}
	return render(request, "add_items.html", context)


@login_required
def receive_items(request, pk):
	queryset = Stock.objects.get(id=pk)
	form = ReceiveForm(request.POST or None, instance=queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.issue_quantity = 0
		instance.quantity += instance.receive_quantity
		instance.receive_by = str(request.user)
		instance.save()	
		messages.success(request, "Successfully Received. " + str(instance.quantity) + " " + str(instance.item_name)+"(s) in Stock Now.")
		return redirect("/stock_details/"+str(instance.id))
	context = {
			"addUpdateItemTitle": "RECEIVE \"" + str(queryset.item_name) + "\"",
			"queryset": queryset,
			"form": form,
			"addUpdateItemBtn": "RECEIVE",
			"username": "Receive By: " + str(request.user)
		}
	return render(request, "add_items.html", context)


@login_required
def reorder_level_details(request, pk):
	queryset = Stock.objects.get(id=pk)
	form = StockReorderLevelForm(instance=queryset)
	if request.method == "POST":
		form = StockReorderLevelForm(request.POST or None, instance=queryset)
		if form.is_valid():
			form.save()
			messages.success(request, "Successfully Updated. Reorder Level for " + str(queryset.item_name) + " is Updated to " + str(queryset.reorder_level) + ".")
			return redirect("/list_items")
	context = {
		"addUpdateItemTitle": "UPDATE REORDER LEVEL",
		"addUpdateItemBtn": "UPDATE",
		"form": form
	}
	return render(request, "add_items.html", context)


@login_required
def history_items(request):
	form = StockHistorySearchForm(request.POST or None)
	queryset = StockHistory.objects.all()

	# Pagination: Set the number of items per page to 10 & pass page to queryset
	# items_per_page = 10
	# paginator = Paginator(queryset, items_per_page)
	# page_number = request.GET.get('page')
	# page = paginator.get_page(page_number)
	

	context = {
		"form": form,
		"queryset": queryset
	}
	if request.method == "POST":
		category = form["category"].value()
		if form["start_date"].value() and form["end_date"].value():
			queryset = StockHistory.objects.filter(
						item_name__icontains=form["item_name"].value(),
						last_updated__range = [form["start_date"].value(), form["end_date"].value()]
						)
		else:
			queryset = StockHistory.objects.filter(
						item_name__icontains=form["item_name"].value()
						)

		if category != "":
			queryset = queryset.filter(category_id = category)
		
		if form["export_to_CSV"].value() == True:
			response = HttpResponse(content_type="text/csv")
			response["Content-Disposition"] = "attachment; filename=History of Stock Items.csv"
			writer = csv.writer(response)
			writer.writerow(["CATEGORY", "ITEM NAME", "QUANTITY", "ISSUE QUANTITY", "RECEIVE QUANTITY", "ISSUE BY", "RECEIVE BY", "LAST UPDATED"])
			for x in queryset:
				writer.writerow([x.category, x.item_name, x.quantity, x.issue_quantity, x.receive_quantity, x.issue_by, x.receive_by, x.last_updated])
			return response
		

		context = {
			"form": form,
			"queryset": queryset
		}
	return render(request, "list_history.html",context)
