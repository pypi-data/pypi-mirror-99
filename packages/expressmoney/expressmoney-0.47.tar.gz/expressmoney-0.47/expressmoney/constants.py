from dataclasses import dataclass


class Status:
    """Утвержденные стандарт используемых статусов в Компании"""

    NEW = 'NEW'  # Активное. требует изменения на INPR
    IN_PROCESS = 'INPR'  # Активное. требует изменения на: FAIL или SCS
    SUCCESS = 'SCS'  # Активное. блокирует создание нового события
    FAILURE = 'FAIL'  # Активное. блокирует создание нового события
    ERROR = 'ERROR'  # Активное. Последнее событие завершилось ситемной ошибкой, бизнес-результат не известен
    CANCEL = 'CANCEL'  # Не активно. Отменяет предыдущий статус. В comment пишется предыдущий статус
    STATUS_CHOICES = {
        (NEW, 'Новый'),
        (IN_PROCESS, 'В процессе'),
        (SUCCESS, 'Успех'),
        (FAILURE, 'Неудача'),
        (ERROR, 'Системная ошибка'),
        (CANCEL, 'Статус отменен')
    }


class Country:
    """Страны присутствия Компании"""

    RUSSIA = 'RU'
    KAZAKHSTAN = 'KZ'
    COUNTRY_CHOICES = [
        (RUSSIA, 'Россия'),
        (KAZAKHSTAN, 'Казахстан'),
    ]


class Loan:
    """Виды займов"""

    PAYDAY_LOAN = 'PDL'
    INSTALLMENT_LOAN = 'IL'
    LOAN_CHOICES = [
        (PAYDAY_LOAN, 'Payday loan'),
        (INSTALLMENT_LOAN, 'Installment loan')
    ]


class Document:
    PASSPORT = 'PP'
    DRIVING_LICENCE = 'DL'
    SNILS = 'SNILS'
    TAX_ID = 'TAX_ID'
    DOCUMENT_CHOICES = [
        (PASSPORT, 'Паспорт'),
        (DRIVING_LICENCE, 'Выдительские права'),
        (SNILS, 'СНИЛС'),
        (TAX_ID, 'ИНН'),
    ]


class Months:
    """Месяцы года"""
    RUSSIA_MONTHS_CHOICES = {
        1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель',
        5: 'Май', 6: 'Июнь', 7: 'Июль', 8: 'Август',
        9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'
    }


class Day:
    TODAY = 'TODAY'
    TOMORROW = 'TMRW'
    DAY_CHOICES = {
        (TODAY, 'Сегодня'),
        (TOMORROW, 'Завтра'),
    }


class Messengers:
    SKYPE = 'SKYPE'
    WHATSAPP = 'WHATSAPP'
    VIBER = 'VIBER'
    TELEGRAM = 'TELEGRAM'
    FACETIME = 'FACETIME'

    MESSENGER_CHOICES = {
        (SKYPE, 'Skype'),
        (WHATSAPP, 'WhatsApp'),
        (VIBER, 'Viber'),
        (TELEGRAM, 'Telegram'),
        (FACETIME, 'FaceTime'),
    }


class Time:
    TIME_CHOICES = {
        (0, '00:00 (12:00 am)'),
        (1, '01:00 (1:00 am)'),
        (2, '02:00 (2:00 am)'),
        (3, '03:00 (3:00 am)'),
        (4, '04:00 (4:00 am)'),
        (5, '05:00 (5:00 am)'),
        (6, '06:00 (6:00 am)'),
        (7, '07:00 (7:00 am)'),
        (8, '08:00 (8:00 am)'),
        (9, '09:00 (9:00 am)'),
        (10, '10:00 (10:00 am)'),
        (11, '11:00 (11:00 am)'),
        (12, '12:00 (12:00 pm)'),
        (13, '13:00 (1:00 pm)'),
        (14, '14:00 (2:00 pm)'),
        (15, '15:00 (3:00 pm)'),
        (16, '16:00 (4:00 pm)'),
        (17, '17:00 (5:00 pm)'),
        (18, '18:00 (6:00 pm)'),
        (19, '19:00 (7:00 pm)'),
        (20, '20:00 (8:00 pm)'),
        (21, '21:00 (9:00 pm)'),
        (22, '22:00 (10:00 pm)'),
        (23, '23:00 (11:00 pm)'),
    }


class Event:

    VERIFICATION = 'VER'

    EVENT_CHOICES = {
        (VERIFICATION, 'Верификаиця'),
    }


class Gateway:
    PAYPAL = 'PP'
    CLOUDPAYMENTS = 'CP'
    GATEWAY_CHOICES = [
        (PAYPAL, 'PayPal'),
        (CLOUDPAYMENTS, 'CloudPayments')
    ]


class MethodPay:

    BANK_CARD = 'BC'
    METHOD_PAY_CHOICES = [
        (BANK_CARD, 'Bank card'),
    ]


@dataclass
class Result(Status):
    """Формат ответа адапетров"""

    status: str
    comment: any

    def __init__(self, status, comment=None):
        assert status in [
            self.NEW,
            self.IN_PROCESS,
            self.SUCCESS,
            self.FAILURE,
            self.ERROR,
            self.CANCEL
        ], 'Wrong status'
        self.status = status
        self.comment = comment
