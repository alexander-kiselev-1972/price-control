from datetime import timedelta, datetime
from typing import Any, Union
from django.core.exceptions import ObjectDoesNotExist

import xlrd
from Leks6.wsgi import *

from price.models import MNN, Lek, HistoryPrice
from django.utils import timezone
import datetime


def set_to_base(NameWorkList, NameTable):
    book = xlrd.open_workbook('1.xls')
    # print("The number of worksheets is {0}".format(book.nsheets))
    # print("Worksheet name(s): {0}".format(book.sheet_names()))

    # создаем объект листа

    sh = book.sheet_by_index(NameWorkList)

    # количество строк в таблице
    max_rows = sh.nrows

    # получаем количество столбцов в таблице
    max_column = sh.ncols

    for row in range(3, max_rows):
        mnn = sh.cell_value(rowx=row, colx=0)
        name = sh.cell_value(rowx=row, colx=1)
        lek_form = sh.cell_value(rowx=row, colx=2)
        owner_ru = sh.cell_value(rowx=row, colx=3)
        kol_v_upak = sh.cell_value(rowx=row, colx=5)
        price = sh.cell_value(rowx=row, colx=6)
        ru = sh.cell_value(rowx=row, colx=8)
        date_reg = sh.cell_value(rowx=row, colx=9)
        barcode = sh.cell_value(rowx=row, colx=10)
        date_run = sh.cell_value(rowx=row, colx=11)
        date_run = xlrd.xldate.xldate_as_datetime(date_run, 0)

        new_lek = NameTable.objects.create(mnn=mnn, name=name, lek_form=lek_form, owner_ru=owner_ru,
                                           kol_v_upak=kol_v_upak, price=price, ru=ru,
                                           date_reg=date_reg, barcode=barcode, date_run=date_run)
        new_lek.save()


def pars_xls(path):
    book_work = xlrd.open_workbook(path)

    return book_work


def set_to_mnn_table(current_book):
    count_work_sheet = current_book.nsheets
    for sheet in range(0, count_work_sheet):
        sh = book.sheet_by_index(sheet)
        max_rows = sh.nrows

        print('set_to_mnn_table - sheet: ', sheet)
        for row in range(3, max_rows):
            mnn = sh.cell_value(rowx=row, colx=0)
            if MNN.objects.filter(name=mnn).count() == 0:
                new_lek = MNN.objects.create(name=mnn)
                new_lek.save()


def set_to_lek(current_book):
    # Получаем количество листов в книге
    count_work_sheet = current_book.nsheets

    # Идем по каждому листу отдельно
    for sheet in range(0, count_work_sheet):
        # Получаем объект листа
        sh = book.sheet_by_index(sheet)

        # Получаем количество строк в листе
        max_rows = sh.nrows
        print('set_to_lek - sheet: ', sheet)

        # Идем по каждой строке
        for row in range(3, max_rows):
            mnn = sh.cell_value(rowx=row, colx=0)
            name = sh.cell_value(rowx=row, colx=1)
            lek_form = sh.cell_value(rowx=row, colx=2)
            name_factory = sh.cell_value(rowx=row, colx=3)
            barcode = sh.cell_value(rowx=row, colx=10)

            # Проверяем запись на уникальность (есть ли она в базе)
            if Lek.objects.filter(barcode=barcode).count() == 0:
                try:
                    id_mnn = MNN.objects.get(name=mnn).id

                    new_lek = Lek.objects.create(name=name, lek_form=lek_form,
                                                 name_factory=name_factory, barcode=barcode, mnn_id=id_mnn)
                    new_lek.save()
                except Exception as e:
                    print('Ошибка: ', e, ' ', name, ' ', mnn)


def control_dubles1(price, date_out,id_lek):
    duble_lek = 0
    try:
        duble_lek = HistoryPrice.objects.filter(lek_id=id_lek, price=price, date_out=date_out)
        print(duble_lek)
        duble_lek = duble_lek.count()
    except ObjectDoesNotExist as e:
        print('get неотработал {} duble_lek = {}'.format(e, duble_lek))
    return duble_lek


def control_dubles2(price, date_in, id_lek):
    duble_lek = 0
    try:
        duble_lek = HistoryPrice.objects.filter(lek_id=id_lek, price=price, date_in=date_in)
        print(duble_lek)
        duble_lek = duble_lek.count()
    except ObjectDoesNotExist as e:
        print('get неотработал {} duble_lek = {}'.format(e, duble_lek))
    return duble_lek


def set_to_history_price(file_object):
    # получаем количество листов в книге
    count_work_sheet = file_object.nsheets
    print(count_work_sheet)

    # Проходим по каждому листу
    for sheet in range(0, count_work_sheet):
        # Получаем объект листа
        sh = file_object.sheet_by_index(sheet)
        # Получаем максимальное количество строк
        max_rows = sh.nrows

        # Проходим по всем строкам минуя заголовок
        for row in range(3, max_rows):
            # Для третьей страницы меняем правила обхода полей - нумерация столбцов тут иная
            if sheet == 2:
                # Получаем цену
                price = sh.cell_value(rowx=row, colx=6)
                try:
                    # Дату прекращения действия
                    date_out = sh.cell_value(rowx=row, colx=13)

                    date_out = xlrd.xldate.xldate_as_datetime(date_out, 0)

                    date_out = date_out.astimezone(timezone.get_current_timezone())

                except Exception as e:
                    print("error in row: ", row)

                finally:

                    solution = sh.cell_value(rowx=row, colx=8)
                    barcode = sh.cell_value(rowx=row, colx=10)

                    id_lek = Lek.objects.get(barcode=barcode).id

                    duble_lek = control_dubles1(price, date_out, id_lek)
                    if duble_lek == 0:
                        HistoryPrice.objects.create(price=price, date_out=date_out, solution=solution,
                                                    lek_id=id_lek)



            else:
                price = sh.cell_value(rowx=row, colx=6)
                date_in = sh.cell_value(rowx=row, colx=11)
                date_in = xlrd.xldate.xldate_as_datetime(date_in, 0)

                date_in = date_in.astimezone(timezone.get_current_timezone())
                print('date_in= ', date_in)
                solution = sh.cell_value(rowx=row, colx=8)
                barcode = sh.cell_value(rowx=row, colx=10)

                id_lek = Lek.objects.get(barcode=barcode).id
                print("id_lek {}".format(id_lek))
                duble_lek = control_dubles2(price=price, date_in=date_in, id_lek=id_lek)

                if duble_lek == 0:
                    HistoryPrice.objects.create(price=price, date_in=date_in, solution=solution,
                                                lek_id=id_lek)


book = pars_xls('1.xls')

set_to_mnn_table(book)
set_to_lek(book)
set_to_history_price(book)
