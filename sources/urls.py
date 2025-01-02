from django.urls import path
from . import views
from sources.api import Sources

urlpatterns = [
	path("tables", views.getTables),
	path("sheets", views.getSheets),
	path("sourcerecords",views.sourceRecords),
    path("source", views.getSource),
    path("source/<int:id>", views.sourceData),
	path("gettablelist",views.getTableList),
	path("gettabledata",views.getTableData),
    path("sources", Sources.get),
    path("gettables", Sources.getTables),
    path("getdata", Sources.getData),
    path("showtables", Sources.showTables),
    path("showsheets", Sources.showSheets),
    # path("report/<int:id>", views.reports),
    path("barchart/<int:id>", views.barChart),
    path("piechart/<int:id>",views.pieChart),
    path("linechart/<int:id>", views.lineChart)
]