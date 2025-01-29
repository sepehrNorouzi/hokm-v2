from celery import shared_task


@shared_task
def close_leaderboard_task(leaderboard_type_id: int):
    pass
