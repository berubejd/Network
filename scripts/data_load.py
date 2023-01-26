import csv
from datetime import timedelta
from random import randint

from django.utils import timezone
from network.models import Post, User


def run():
    filename = "scripts/data.csv"
    current_timestamp = timezone.now()

    for field in Post._meta.local_fields:
        if field.name == "updated_at":
            field.auto_now = False
        elif field.name == "created_at":
            field.auto_now_add = False

    with open(filename) as file:
        reader = csv.DictReader(file)

        for row in reader:
            # Create user
            # "username", "first_name", "last_name", "email", "photo_url"
            u = User(
                username=f'{row["first_name"]}_{row["last_name"]}',
                first_name=row["first_name"],
                last_name=row["last_name"],
                email=row["email"],
                photo_url=row["photo_url"],
            )
            u.save()

            # Add posts
            # "text", "user", "created_at"
            for post in ["post_1", "post_2", "post_3", "post_4", "post_5"]:
                post_time = current_timestamp - timedelta(
                    minutes=randint(0, 60 * 24 * 3)
                )

                p = Post(
                    text=row[post],
                    user=u,
                    created_at=post_time,
                    updated_at=post_time,
                )
                p.save()
