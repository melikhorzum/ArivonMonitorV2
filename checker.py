import asyncio

from database import tum_hesaplar, durum_guncelle
from instagram import hesap_durumu
from config import CHECK_INTERVAL


async def kontrol_et(bot):

    while True:

        hesaplar = tum_hesaplar()

        for telegram_id, username, eski_durum in hesaplar:

            yeni_durum = hesap_durumu(username)

            print(f"Kontrol edildi: @{username} -> {yeni_durum}")

            if yeni_durum == "hata":
                continue

            if yeni_durum != eski_durum:

                if yeni_durum == "kapali":
                    await bot.send_message(
                        telegram_id,
                        f"🚨 @{username} hesabı artık erişilemiyor."
                    )

                elif yeni_durum == "aktif":
                    await bot.send_message(
                        telegram_id,
                        f"🎉 @{username} hesabı tekrar aktif oldu."
                    )

                durum_guncelle(username, yeni_durum)

        await asyncio.sleep(CHECK_INTERVAL)
