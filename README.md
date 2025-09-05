https://muhammad-hafizh47-arabgokstore.pbp.cs.ui.ac.id/

1. - Membuat sebuah proyek django baru:
Pertama-tama dalam membuat projek django baru, saya membuat repository github terlebih dahulu sesuai dengan nama aplikasi saya yaitu arabgokstore. Lalu, saya membuat direktori baru dan membuka cmd untuk mengaktifkan virtual environtment. Setelah itu, saya membuat file baru yaitu "requirements.txt" pada direktori yang sama dan melakukan instalasi terhadap apa yang ada pada isi file tersebut. Selesai instalasi, saya membuat proyek django baru dengan perintah "django-admin startproject arabgokstore .".
- Membuat aplikasi dengan nama main pada proyek tersebut:
Pertama, saya membuka direktori utama dulu yaitu arabgokstore dan mengaktifkan virtual environments nya pada cmd yang telah dipakai sebelumnya. Lalu, saya membuat aplikasi dengan nama main dengan menjalankan perintah "python manage.py startapp main" maka aplikasi main akan terbentuk dan berisi struktur awal sebagai pengembangan aplikasi ini.
- Melakukan routing agar dapat menjalankan aplikasi main:
Jikalau sudah mengerjakan bagian models dan views untuk pengembangan tampilan aplikasi main tersebut, maka buatlah file urls.py dalam folder main tersebut dan mengisi file tersebut dengan konfigurasi routing yang akan digunakan. Setelah itu, melengkapi kode rute URL pada folder proyek (bukan main) dengan meng-include rute URL dari aplikasi main. Lalu, tinggal jalankan proyek tersebut dengan runserver dan membuka localhost untuk mengecek web yang telah saya buat
- Membuat model pada aplikasi main dengan nama Product dan atribut wajib :
Pertama, saya buka dulu file models.py yang ada pada folder aplikasi main. Lalu, saya mengisi atribut-atribut yang dibutuhkan ke dalam class Product sesuai dengan tipe masing-masing.
- embuat sebuah fungsi pada views.py untuk dikembalikan ke dalam sebuah template HTML :
Pertama, buka terlebih dahulu file views.py yang ada pada folder aplikasi main. Lalu, saya membuat 3 variabel dalam fungsi show_main ini agar membantu menampilkan ke template HTML. Tiga variabel tersebut berisi nama aplikasi saya, lalu nama saya, dan kelas saya.
- Membuat sebuah routing pada urls.py aplikasi main untuk memetakan fungsi yang telah dibuat pada views.py :
membuat file urls.py sebagai konfigurasi routing aplikasi main, lalu saya mengimpor fungsi path untuk mendefinisikan pola URL yang akan dipakai. Lalu, fungsi path tersebut memanggil fungsi show_main yang telah dibuat pada views.py
Django akan mencocokkan URL tersebut dengan yang ada di urls.py, jika cocok maka akan menjalankan yang ada di views
- Melakukan deployment ke PWS terhadap aplikasi yang dibuat:
Pertama, membuat new project terlebih dahulu di PWS dan memberi nama projeknya yaitu arabgokstore. Lalu, PWS memberikan informasi project credentials nya dan project command nya yang akan digunakan nanti nya. Setelah itu, saya mengubah raw editor pada tab environs yang ada di PWS dengan code yang ada dari .env.prod. Lalu, saya menambahkan URL deployment PWS saya ke allowed hosts pada settings.py aplikasi saya. Setelah itu, saya melakukan push ke PWS dan memasukkan username dan password credentials yang telah diberikan oleh PWS sebelumnya. Terakhir, saya hanya perlu menjalankan git push pws master setelah melakukan add dan commit untuk deployment aplikasi saya.

2. ini adalah link gambar bagan yang berisi request client ke web aplikasi : https://drive.google.com/file/d/1-55tYEYnPfqzJMagaxpb124xBIS35KlT/view?usp=sharing
Penjelasan: Kaitan antara urls.py, views.py, models.py, dan html adalah pertama-tama browser kirim request dan dicek oleh urls.py pada direktori projek arabgokstore, lalu kalau cocok akan diteruskan ke urls.py pada direktori aplikasi main, urls.py pada direktori main menunjuk ke fungsi di views.py, views.py dapat mengambil data dari models.py, lalu views.py me-render HTML template dengan data context, dan browser menampilkan hasil HTML ke user.

3. Peran settings.py dalam proyek django adalah adalah sebagai pusat konfigurasi yang mengatur segala aspek aplikasi, mulai dari daftar aplikasi aktif (INSTALLED_APPS), database, dan lainnya. Semua komponen Django merujuk ke file ini agar proyek bisa berjalan sesuai aturan yang ditentukan. Tanpa settings.py, Django tidak akan tahu cara menghubungkan ke database, menampilkan template, atau memproses request sehingga proyek tidak akan bisa dijalankan maupun diakses di browser. 

4. Cara kerja migrasi database di Django adalah
- Saat kita menambah atau mengubah file models.py, django akan mendeteksi perubahan tersebut.
- Lalu, menjalankan perintah python manage.py makemigrations, perintah ini membuat file migration (0001_initial.py) di folder migrations. File ini berisi instruksi Python yang menjelaskan perubahan apa yang harus dilakukan pada database.
- Setelah itu, menjalankan perintah python manage.py migrate, perintah ini menjalankan file migrasi tadi ke dalam database. 
- Terkhir, django akan membuat riwayat migrasi bernama django_migrations di database untuk melacak migrasi mana saja yang udah dijalankan. Jadi, ketika ada migrasi baru, maka hanya migrasi tersebut yang dijalankan, bukan semuanya dari awal.

5. Menurut saya, alasan framework Django dijadikan permulaan pembelajaran adalah karena django sudah menyediakan kebutuhan-kebutuhan dasar, seperti database ORM, routing URL, sistem autentikasi, dan lainnya. Hal ini menurut saya membantu mahasiswa untuk langsung belajar konsep pengembangan web tanpa harus melakukan instalasi dan coding dari 0. Django juga menggunakan bahasa Python, yang sintaksnya sederhana dan mudah dibaca dibandingkan bahasa lain sehingga lebih mudah dipahami untuk dijadikan permulaan pembelajaran. Django juga menggunakan konsep MVT, konsep ini menurut saya memperkenalkan bagaimana cara kerja pengembangan software yang rapi dan terstruktur.

6. Feedback saya untuk asdos tutorial 1 adalah asdos nya sangat baik, responsif, dan sangat membantu mahasiswa yang kesulitan.