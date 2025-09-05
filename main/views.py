from django.shortcuts import render

# Create your views here.
def show_main(request):
    context = {
        'nama_aplikasi' : 'Arabgokstore',
        'nama': 'Muhammad Hafizh',
        'kelas': 'PBP D'
    }

    return render(request, "main.html", context)