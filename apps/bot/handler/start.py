import logging
import os

from aiogram import F
from aiogram import Router
from aiogram.enums import ContentType
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import Message
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from dotenv import load_dotenv

from apps.bot.button.Inline import get_contact_keyboard, attachment_question, \
    confirm_buttons, murajat_button, back_button, \
    get_contact_yes_not_keyboard, get_contact_phone_keyboard, restart_button, to_answer, murajat_button2
from apps.bot.button.Inline import personal_info_buttons
from apps.bot.main import bot
from apps.bot.save_to_database import save_to_model
from apps.bot.state.leader import ComplaintForm
from apps.models import Request

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
User = get_user_model()

load_dotenv()
main_router = Router()


@main_router.message(CommandStart())
async def cmd_start(message: Message):
    telegram_id = message.from_user.id
    username = message.from_user.username
    last_name = message.from_user.last_name
    first_name = message.from_user.first_name

    async def create_or_get_user():
        user_exists = await sync_to_async(User.objects.filter(telegram_id=telegram_id).exists)()
        if not user_exists:
            await sync_to_async(User.objects.create)(
                telegram_id=telegram_id,
                username=username,
                first_name=first_name,
                last_name=last_name,
                is_active=True,
            )

    await create_or_get_user()
    begin_text = (
        """📩 Ходимлар учун аноним ёки очиқ мурожаат имконияти! 📩

        Ҳурматли фойдаланувчи, эндиликда аноним ёки очиқ равишда ўз фикрларингиз, таклифларингиз ёки муаммоларингизни бот орқали раҳбарга жўнатишингиз мумкин.

        🤐 (Ихтиёрий) анонимлик кафолатланади! Агар аноним мурожаатни танласангиз, шахсий маълумотларингиз сақланмайди ва ошкор қилинмайди.

        👤 Қандай ишлайди?
        1️⃣ 📝 Сўров ёки таклифингизни ёзинг.
        2️⃣ 📷 Агар хоҳласангиз, расм ёки видео юкланг.
        3️⃣ 🔒 Аноним ёки очиқ тарзда юборишни танланг.
        4️⃣ ✅ Тасдиқланг ва юборинг !

        📨 Ишончли, тезкор ва эркин алоқа – раҳбарга бевосита етказилади!
        ⬇️ Тугмани босиб, мурожаатингизни юборинг ⬇️
        """
    )
    await message.answer(begin_text, reply_markup=get_contact_keyboard())


@main_router.callback_query(lambda c: c.data == "rahbarga")
async def cb_rahbarga(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "Муражатингизни ёзиб қолдиринг....",
        reply_markup=murajat_button()
    )
    await state.set_state(ComplaintForm.waiting_for_complaint)
    await callback.answer()


@main_router.callback_query(lambda c: c.data in ["murajat", "cancel"])
async def handle_callback(callback: CallbackQuery, state: FSMContext):
    if callback.data == "murajat":
        await callback.message.delete()
        await callback.message.answer(
            "Muammo haqida batafsil yozib qoldiring.\n"
            "Agar bekor qilmoqchi bo‘lsangiz, 'Bekor qilish' tugmasini bosing.",
        )
        await state.set_state(ComplaintForm.waiting_for_complaint)
    elif callback.data == "cancel":
        await state.clear()
        await callback.message.delete()
        await callback.message.answer("Сизнинг мурожаатингиз бекор қилинди.", back_button())
    await callback.answer()


@main_router.callback_query(lambda c: c.data == "back_button_cancel")
async def handle_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await cb_rahbarga(callback, state)
    await callback.answer()


@main_router.message(ComplaintForm.waiting_for_complaint)
async def process_complaint(message: Message, state: FSMContext):
    user_input = message.text.strip()
    word_count = len(user_input.split())

    if word_count < 1:
        await message.answer("Мурожаатингизда камида 2 та сўз ёзишингиз керак. Илтимос, батафсилроқ ёзинг.")
        return

    await state.update_data(complaint=user_input)
    await message.answer("Мурожаатингиз қабул қилинди. *Расм ёки видео юбормоқчимисиз..?*", parse_mode="Markdown",
                         reply_markup=attachment_question())
    await state.set_state(ComplaintForm.waiting_for_attachment)


@main_router.callback_query(lambda c: c.data in ["yes_attachment", "no_attachment"])
async def handle_attachment_question(callback: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    logging.info(f"Current state: {current_state}")
    logging.info(f"Callback data: {callback.data}")
    if callback.data == "yes_attachment":
        await callback.message.answer("Расм ёки видео юборинг:")
        await state.set_state(ComplaintForm.waiting_for_attachment)
    elif callback.data == "no_attachment":
        await callback.message.answer("Ўзингиз ҳақингизда маълумот берасизми...?", reply_markup=personal_info_buttons())
        await state.set_state(ComplaintForm.waiting_for_user_info)
    await callback.answer()


# Photo
@main_router.message(
    ComplaintForm.waiting_for_attachment,
    F.content_type.in_([ContentType.PHOTO, ContentType.VIDEO, ContentType.VIDEO_NOTE])
)
async def process_file_upload(message: Message, state: FSMContext):
    data = await state.get_data()
    attachments = data.get("attachments", [])  # E'tibor bering: "attachment" emas, "attachments"

    if message.photo:
        file_id = message.photo[-1].file_id
        attachments.append({"type": "photo", "file_id": file_id})
    elif message.video:
        file_id = message.video.file_id
        attachments.append({"type": "video", "file_id": file_id})
    elif message.video_note:
        file_id = message.video_note.file_id
        attachments.append({"type": "video_note", "file_id": file_id})

    # Yangilangan ro'yxatni saqlaymiz
    await state.update_data(attachments=attachments)

    await message.answer("Ўзингиз ҳақингизда маълумот берасизми..?", reply_markup=personal_info_buttons())
    await state.set_state(ComplaintForm.waiting_for_user_info)


@main_router.callback_query(ComplaintForm.waiting_for_user_info,
                            lambda c: c.data in ["skip_info_yes", "provide_info_not"])
async def handle_personal_info(callback: CallbackQuery, state: FSMContext):
    """
    Foydalanuvchi shaxsiy ma'lumotni yuborish yoki yubormaslikni tanlaydi.
    """
    if callback.data == "skip_info_yes":
        await callback.message.answer("Исмингизни киритинг:")
        await state.set_state(ComplaintForm.name)
    elif callback.data == "provide_info_not":
        data = await state.get_data()
        await send_summary(callback.message, data)
        await state.set_state(ComplaintForm.confirm_details)
    await callback.answer()


@main_router.message(ComplaintForm.name)
async def process_name(message: Message, state: FSMContext):
    full_name = message.text.strip()
    await state.update_data(full_name=full_name)
    await message.answer(
        "Телефон рақамингизни юборасизми..?",
        reply_markup=get_contact_yes_not_keyboard()
    )
    await state.set_state(ComplaintForm.phone_number)


@main_router.callback_query(lambda c: c.data in ["contact_skip_info_yes", "contact_provide_info_not"])
async def handle_phone_decision(callback: CallbackQuery, state: FSMContext):
    if callback.data == "contact_skip_info_yes":
        await callback.message.answer("Телефон рақамингизни юборинг:", reply_markup=get_contact_phone_keyboard())
        await state.set_state(ComplaintForm.phone_number)
    elif callback.data == "contact_provide_info_not":
        await state.update_data(phone_number=" ")
        data = await state.get_data()
        await send_summary(callback.message, data)
        await state.set_state(ComplaintForm.confirm_details)
    await callback.answer()


async def send_summary(message, data):
    """
    Foydalanuvchi tomonidan kiritilgan ma'lumotlarni xulosa qilib yuborish.
    """
    full_name = data.get("full_name", "")
    phone_number = data.get("phone_number", "")
    complaint = data.get("complaint", "")
    attachments = data.get("attachments", [])  # [ {"type":"photo","file_id":...}, ...]

    summary = (
        f"Маълумотларингиз:\n\n"
        f"👤 Исм: {full_name}\n"
        f"📞Телефон: {phone_number}\n"
        f"✉️ Мурожаат: {complaint}\n\n"
        f"Ҳаммаси тўғрими..?"
    )
    for attach in attachments:
        t = attach["type"]
        fid = attach["file_id"]
        if t == "photo":
            await message.answer_photo(fid)
        elif t == "video":
            await message.answer_video(fid)
        elif t == "video_note":
            await message.answer_video_note(fid)
    await message.answer(summary, reply_markup=confirm_buttons())


@main_router.message(ComplaintForm.phone_number, F.content_type == ContentType.CONTACT)
async def process_phone_number(message: Message, state: FSMContext):
    if not message.contact:
        await message.answer("Илтимос, телефон рақамингизни тугма орқали юборинг...")
        return
    phone_number = message.contact.phone_number
    await state.update_data(phone_number=phone_number)
    data = await state.get_data()
    full_name = data.get("full_name", "")
    complaint = data.get("complaint", "")

    attachments = data.get("attachments", [])

    summary = (
        f"Ma'Маълумотларингиз:\n\n\n"
        f"Исм: {full_name}\n\n"
        f"Телефон: {phone_number}\n\n"
        f"Мурожаат: {complaint}\n\n"
        f"Ҳаммаси тўғрими..?"
    )
    for attach in attachments:
        t = attach["type"]
        fid = attach["file_id"]
        if t == "photo":
            await message.answer_photo(fid, caption="Сиз юборган расм")
        elif t == "video":
            await message.answer_video(fid, caption="Сиз юборган видео")
        elif t == "video_note":
            await message.answer_video_note(fid)

    await message.answer(summary, reply_markup=confirm_buttons())
    await state.set_state(ComplaintForm.confirm_details)


@main_router.callback_query(ComplaintForm.confirm_details, lambda c: c.data == "confirm")
async def confirm_data(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    telegram_id = callback.from_user.id
    full_name = data.get("full_name", "")
    phone_number = data.get("phone_number", "")
    complaint = data.get("complaint", "")
    attachment = data.get("attachments", [])  # Ro'yxat
    single_attachment = None
    if attachment:
        single_attachment = attachment[0]["file_id"]  # faqat ro'yxatning 1-elementi

    request = await save_to_model(
        telegram_id=telegram_id,
        reason=complaint,
        attachment=single_attachment,
        phone_number=phone_number,
        full_name=full_name,
    )
    if not request:
        await callback.message.answer("Маълумотларни сақлашда хатолик юз берди.")
        return

    await callback.message.answer("Маълумотларингиз юборилди.\n қайтадан /start босинг", )

    # Rahbarga yuborish
    manager_telegram_id = os.getenv("MANAGER_TELEGRAM_ID")
    if not manager_telegram_id:
        await callback.message.answer("Раҳбар ID аниқланмади. Админ билан боғланинг.")
        return

    message_to_manager = (
        f"📩 *Янги мурожаат* қолдирилди:\n\n"
        f"👤 *Исм*: {full_name}\n"
        f"📞 *Телефон*: {phone_number}\n"
        f"✉️ *Мурожаат*: {complaint}\n"
        f"Статус: *Кутилаётган*"
    )

    try:
        await bot.send_message(
            chat_id=manager_telegram_id,
            text=message_to_manager,
            reply_markup=to_answer(request.id),  # Request ID bilan tugmalarni qo'shish
            parse_mode="Markdown"
        )
        # logger.info(message_to_manager)
        for attach in attachment:
            t = attach["type"]
            fid = attach["file_id"]
            if t == "photo":
                await bot.send_photo(manager_telegram_id, fid)
            elif t == "video":
                await bot.send_video(manager_telegram_id, fid)
            elif t == "video_note":
                await bot.send_video_note(manager_telegram_id, fid)
    except Exception as e:
        logging.error(f"Раҳбарга хабар юборишда хатолик: {e}")

    await state.clear()
    await callback.answer()


@main_router.callback_query(lambda c: c.data.startswith("reply:"))
async def start_reply(callback: CallbackQuery, state: FSMContext):
    """
    Rahbar javob berishni boshlaganida ushbu handler ishga tushadi.
    """
    request_id = callback.data.split(":")[1]  # Request ID ni ajratib olish
    logging.info(f"Request ID: {request_id}")  # Debug log

    @sync_to_async
    def mark_request_as_read_and_get_user(_id):
        request_obj = Request.objects.select_related('user').get(id=_id)
        request_obj.is_read = True
        request_obj.save()
        return request_obj, request_obj.user.telegram_id

    try:
        request_obj, user_tg_id = await mark_request_as_read_and_get_user(request_id)
        logging.info(f"Request: {request_obj}")

        await state.update_data(
            request_id=request_id,
            telegram_id=user_tg_id,
            message_id=callback.message.message_id,
        )

        logging.info(f"Request ID: {request_id}, Telegram ID: {callback.from_user.id}")

        await callback.message.answer("Жавобингизни ёзинг:")
        await state.set_state(ComplaintForm.waiting_for_reply)
        await callback.answer()

    except Request.DoesNotExist:
        await callback.message.answer("Мурожаат топилмади.")
    except Exception as e:
        logging.error(f"Xатолик yuz berdi: {e}")
        await callback.message.answer("Xатолик юз берди.")


@main_router.message(ComplaintForm.waiting_for_reply)
async def send_reply(message: Message, state: FSMContext):
    data = await state.get_data()
    request_id = data.get("request_id")
    user_telegram_id = data.get("telegram_id")
    main_msg_id = data.get("message_id")

    reply_text = message.text

    @sync_to_async
    def mark_request_as_answered(_id):
        req = Request.objects.get(id=_id)
        req.is_read = True
        req.save()
        return req

    try:
        request_obj = await mark_request_as_answered(request_id)

        await bot.send_message(
            chat_id=user_telegram_id,
            text=f"📩 *Раҳбардан жавоб бор!*\n\n{reply_text}",
            parse_mode="Markdown"
        )

        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=main_msg_id,
            text=(
                f"📩 *Янги мурожаат* қолдирилди:\n\n"
                f"👤 *Исм*: {request_obj.full_name}\n"
                f"📞 *Телефон*: {request_obj.phone_number}\n"
                f"✉️ *Мурожаат*: {request_obj.reason}\n"
                f"Статус: *Жавоб берилди.*"
            ),
            parse_mode="Markdown"
        )

    except Request.DoesNotExist:
        await message.answer("Мурожаат топилмади.")
    except Exception as e:
        logging.error(f"Жавоб юборишда хатолик: {e}")
        await message.answer("Фойдаланувчига жавоб юборишда хатолик юз берди.")
    finally:
        await state.clear()


@main_router.callback_query(lambda c: c.data.startswith("ignore:"))
async def ignore_request(callback: CallbackQuery):
    request_id = callback.data.split(":")[1]  # Request ID ни ажратиб олиш

    try:
        request = await sync_to_async(Request.objects.get)(id=request_id)
        request.is_read = True
        await sync_to_async(request.save)()  # Ўзгартиришни сақлаш

        await callback.message.edit_text(
            text=(
                f"📩 *Янги мурожаат* қолдирилди:\n\n"
                f"👤 *Исм*: {request.full_name}\n"
                f"📞 *Телефон*: {request.phone_number}\n"
                f"✉️ *Мурожаат*: {request.reason}\n"
                f"Статус: *Эътиборсиз қолдирилди.*"
            ),
            parse_mode="Markdown",
            reply_markup=None  # Тугмаларни олиб ташлаш
        )
        await callback.answer("Эътиборсиз қолдирилди.")
    except Request.DoesNotExist:
        await callback.message.answer("Мурожаат топилмади.")
    except Exception as e:
        logging.error(f"Мурожаатни эътиборсиз қолдиришда хатолик: {e}")
        await callback.message.answer("Статусни янгилашда хатолик юз берди.")


@main_router.callback_query(lambda c: c.data.startswith("reject:"))
async def ignore_request(callback: CallbackQuery):
    request_id = callback.data.split(":")[1]  # Request ID ни ажратиб олиш

    try:
        request = await sync_to_async(Request.objects.get)(id=request_id)
        request.is_read = True
        await sync_to_async(request.save)()  # Ўзгартиришни сақлаш

        await callback.message.edit_text(
            text=(
                f"📩 *Янги мурожаат* қолдирилди:\n\n"
                f"👤 *Исм*: {request.full_name}\n"
                f"📞 *Телефон*: {request.phone_number}\n"
                f"✉️ *Мурожаат*: {request.reason}\n"
                f"Статус: *Рад этилди..*"
            ),
            parse_mode="Markdown",
            reply_markup=None,  # Тугмаларни олиб ташлаш

        ),

        await callback.answer("Рад этилди..")
    except Request.DoesNotExist:
        await callback.message.answer("Мурожаат топилмади.")
    except Exception as e:
        logging.error(f"Мурожаатни эътиборсиз қолдиришда хатолик: {e}")
        await callback.message.answer("Статусни янгилашда хатолик юз берди.")


@main_router.callback_query(ComplaintForm.confirm_details, lambda c: c.data == "reject")
async def cancel_action(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer("Муражатингизин қайта юборинг..",
                                  reply_markup=restart_button())
    await callback.answer()


@main_router.callback_query(lambda c: c.data == "restart_process")
async def restart_process(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "Муражатингизни ёзиб қолдиринг....",
        reply_markup=murajat_button()
    )
    await state.set_state(ComplaintForm.waiting_for_complaint)
    await callback.answer()
