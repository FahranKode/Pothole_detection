"""
TODO:
1. membaca data menggunakan serial
2. melakukan parse


Fun Fact:
gps bakal kirim data menggunakan format ascii dan dibaca oleh pemrograman menggunkaan byte(b)
Gps bakal kirim banyak format jadi kita cumna perlu akses satu format aja yaitu:

b'$GPRMC,045320.00,A,0610.52352,S,10649.62918,E,022.4,084.4,011126,,,A*7C'

Penjelasan Komponen:
0 Komponen => Header, Contoh Nilai => $GPRMCI, Keterangan format => Identifikasi tipe data RMC
1 Komponen => UTC Time, Contoh Nilai => 045320.00 Keterangan Format => Jam 04:53:20.00 UTC (hhmmss.ss)
2 Status Fix A = Active (Valid), V = Void (Invalid/No Fix)
3 Latitude 0610.52352 Lintang format DDMM.MMMM (06° 10.52352')
4 Lintang DirSN (North/Utara), S (South/Selatan)
5 Longitude 10649.62918 Bujur format DDDMM.MMMM (106° 49.62918')
6 Bujur DirEE (East/Timur), W (West/Barat) 
7 Speed 022.4 Kecepatan bergerak (Speed over ground) dalam Knot
8 Heading084.4 Sudut arah pergerakan relatif terhadap Utara Sejati ($0^\circ - 359.9^\circ$)
9 Date 011126 Tanggal UTC format DDMMYY (01 November 2026)
10 Mag Var,,Magnetic Variation (umumnya kosong di NEO-6M)
11 Mode A Mode posisi (A = Autonomous, D = DGPS, E = Estimated)
12 Checksum *7C Kode validasi integritas data



"""
import serial 
import threading
import pynmea2

class GPS:
    def __init__(self, port:str, baudrate:int = 9600):
        self.port = port
        self.baudrate=baudrate
        self.running=False

    def read(self):
        if not self.running:
            self.running=True
            """ Thread digunain buat jalanin kode secara paralel """
            self.thread=threading.Thread(target=self.serial_proses, daemon=True)
            self.thread.start()
    def serial_proses(self):
        with serial.Serial(self.port, self.baudrate) as ser:
            while self.running:
                try:
                        data=ser.readline().decode("ascii", "replace").strip()
                        if data.startswith("$GPRMC"):
                            msg=pynmea2.parse(data)
                            if msg.status=="A":
                                self.lat=msg.latitude
                                self.lon=msg.longitude
                                self.status=True
                            else:
                                self.lat=None
                                self.lon=None
                                self.status=False
                except serial.SerialException as e:
                    print(f"error: {e}")
    def get_location(self):
        return {
            "latitude":self.lat,
            "longitude":self.lon,
            "status":self.status
        }
    def stop_read(self):
        self.running=False
        
        