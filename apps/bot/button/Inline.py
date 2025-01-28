from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def get_contact_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Мурожаат қолдириш", callback_data="rahbarga")]
        ]
    )


def murajat_button():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Бекор қилиш", callback_data="cancel")
            ]
        ]
    )


def murajat_button2():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Бекор қилиш", callback_data="cancel2")
            ]
        ]
    )


def back_button():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🔄 Қайтадан мурожаат юбориш", callback_data="back_button_cancel")
            ]
        ]
    )


def attachment_question():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🟢 Ҳа", callback_data="yes_attachment"),
                InlineKeyboardButton(text="🔴 Йўқ", callback_data="no_attachment")
            ]
        ]
    )


def personal_info_buttons():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🟢 Ҳа", callback_data="skip_info_yes"),
                InlineKeyboardButton(text="🔴 Йўқ", callback_data="provide_info_not"),
            ]
        ]
    )


def confirm_buttons():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Тасдиқлаш", callback_data="confirm"),
                InlineKeyboardButton(text="❌ Бекор қилиш", callback_data="reject")
            ]
        ]
    )


def get_contact_phone_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📞 Телефон рақамни юбориш", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def get_contact_yes_not_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🟢 Ҳа", callback_data="contact_skip_info_yes"),
                InlineKeyboardButton(text="🔴 Йўқ", callback_data="contact_provide_info_not")
            ]
        ]
    )


def to_answer(request_id):
    """
    Rahbar uchun "Жавоб бериш", "Рад этиш", ва "Эътиборсиз қолдириш" tugmalari.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Жавоб бериш", callback_data=f"reply:{request_id}"),
                InlineKeyboardButton(text="Рад этиш", callback_data=f"reject:{request_id}"),
                InlineKeyboardButton(text="Эътиборсиз қолдириш", callback_data=f"ignore:{request_id}"),
            ]
        ]
    )


def restart_button():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🔄 Қайтадан мурoжаат бериш", callback_data="restart_process")
            ]
        ]
    )



def cancel_restart_button():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🔄 Қайтадан мурoжаат бериш", callback_data="cancel_restart_button")
            ]
        ]
    )
