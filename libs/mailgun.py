import os
from requests import post, Response
from typing import List
from libs.strings import gettext


# her sınıf için böyle exceptionlar yazmka analizi kolay hale getirir
class MailGunException(Exception):
    def __init__(self, messages: str):
        super().__init__(messages)


class Mailgun:
    # .env dosyasında cekiyoruz bunları güvenlik için. githubta paylaşmıyoruz .env.example olanı paylasıyoruz
    MAILGUN_DOMAIN = os.environ.get("MAILGUN_DOMAIN", "sandbox77f3dc67f6a84afca63b56ca07ba417c.mailgun.org")
    MAILGUN_API_KEY = os.environ.get("MAILGUN_API_KEY", "f61b7686fb3e920a834b8fe67b91f440-ea44b6dc-7a3a0d1a")
    FROM_TITLE = "Stores Rest API"
    FROM_EMAIL = f"postmaster@{MAILGUN_DOMAIN}"

    # html i ekleyince mailgun calısmadı
    @classmethod
    def send_email(cls, email: List[str], subject: str, text: str) -> Response:
        if cls.MAILGUN_API_KEY is None:
            raise MailGunException(gettext("mailgun_failed_load_api_key"))

        if cls.MAILGUN_DOMAIN is None:
            raise MailGunException(gettext("mailgun_failed_load_domain"))

        response = post(f"https://api.mailgun.net/v3/{cls.MAILGUN_DOMAIN}/messages",
                        auth=("api", cls.MAILGUN_API_KEY),
                        data={
                            "from": f"{cls.FROM_TITLE} <{cls.FROM_EMAIL}>",
                            "to": email,
                            "subject": subject,
                            "text": text,

                        }, )

        # if response != 201:
        #     raise MailGunException(ERROR_ENDING_EMAIL)

        return response
