import logging

from asgiref.sync import sync_to_async

from apps.models import Request, User


async def save_to_model(
        telegram_id: str,
        reason: str,
        attachment: str = None,
        phone_number: str = None,
        full_name: str = None,
) -> Request:
    try:
        user, created = await sync_to_async(User.objects.get_or_create)(
            telegram_id=telegram_id,
            defaults={
                "is_active": True,
                "username": f"user_{telegram_id}",
            }
        )

        updated = False
        if phone_number and user.phone != phone_number:
            user.phone = phone_number
            updated = True

        if full_name and user.name != full_name:
            user.name = full_name
            updated = True

        if updated:
            await sync_to_async(user.save)()

        # Request obyektini yaratish
        complaint = Request(
            user=user,
            reason=reason,
        )

        if attachment:
            complaint.attachment = attachment

        if phone_number:
            complaint.phone_number = phone_number

        if full_name:
            complaint.full_name = full_name

        await sync_to_async(complaint.save)()

        return complaint

    except Exception as e:
        logging.error(f"Xatolik yuz berdi: {e}")
        return None
