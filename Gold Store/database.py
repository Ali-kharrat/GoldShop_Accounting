import sqlite3
from PIL import Image
from PIL import ImageDraw, ImageFont
from bidi.algorithm import get_display
import arabic_reshaper


def create_image(name, phone, serial, weight, price):
    # -*- coding: utf-8 -*-
    img = Image.open('image.jpg')

    I1 = ImageDraw.Draw(img)
    reshaped_text = arabic_reshaper.reshape(name)
    name_new = get_display(reshaped_text)

    font = ImageFont.truetype("DiodrumArabic-Medium", 16, encoding='unic')
    I1.text((355, 140), f"{name_new}", fill=(0, 0, 0), font=font)
    I1.text((120, 140), f"{phone}", fill=(16, 0, 0), font=font)
    I1.text((450, 215), f"{serial}", fill=(16, 0, 0), font=font)
    I1.text((370, 215), "18", fill=(255, 0, 0), font=font)
    I1.text((330, 215), f"{weight}", fill=(16, 0, 0), font=font)
    I1.text((280, 215), f"{weight}", fill=(16, 0, 0), font=font)
    I1.text((140, 215), f"{price}", fill=(16, 0, 0), font=font)
    img.save(f"{name}_{serial}.png")


conn = sqlite3.connect("Gold_Store.db", check_same_thread=False)
c = conn.cursor()


def create_database():
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS product
        (serial, weight_gold NUMERIC, buy_price NUMERIC)
        """
    )

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS Client
        (name TEXT, number NUMERIC, serial NUMERIC, price NUMERIC, weight NUMERIC, final_price NUMERIC)
        """
    )

    conn.commit()


def add_clinet(name, number, serial, price, weight, final_price):
    c.execute(
        """
        INSERT INTO Client (name, number, serial, price, weight, final_price)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (name, number, serial, price, weight, final_price)
    )

    conn.commit()


def add_products(serial, weight_gold, buy_price):
    show_data = c.execute(
        f"""
    SELECT serial FROM product
    """
    )
    if (f'{serial}',) in show_data.fetchall():
        return "serial number is exist"
    else:
        c.execute(
            f"""
            INSERT INTO product (serial, weight_gold, buy_price)
            VALUES
            ('{serial}',{weight_gold},{buy_price})
            """
        )

    conn.commit()


def get_data_sels():
    all_price = c.execute(
        """SELECT SUM(final_price) FROM Client"""
    )

    all_weight = c.execute(
        """SELECT SUM(weight) FROM Client"""
    )

    all_buy = c.execute(
        """SELECT SUM(buy_price) FROM product"""
    )

    all_buy_weight = c.execute(
        """SELECT SUM(weight_gold) FROM product"""
    )

    return all_price, all_weight, all_buy, all_buy_weight


def show(serial):
    show_data_ = c.execute(
        f"""
    SELECT * FROM product WHERE serial='{serial}'
    """
    )
    all = show_data_.fetchall()
    # gheymat = all[0][1]
    try:
        vazn = all[0][1]
        return vazn
    except:
        return ''
