from UI import app_ui
from db import db

"""
TODO: Sunucuda oyuncu verilerini sakla, leaderboard oluştur
TODO: Socket.io ile kapışma ekle (kişi sayısı 2'den fazla olabilsin)
TODO: Topluluktan gelen dil destkleri için dokümantasyon
"""

app_ui( db() ).run()