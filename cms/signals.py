from django.db.models.signals import post_save
from django.dispatch import	receiver
from .models import Journalism

#sender for ranking determination
@receiver(post_save, sender=Journalism.number_of_views)
@receiver(post_save, sender=Journalism.claps)
def journalism_ranking_signal(sender, instance, **kwargs):
    cal_claps = 60/100 * instance.claps
    cal_view_count = 40/100 * instance.number_of_views
    instance.ranking_determination = cal_claps + cal_view_count
    instance.save()