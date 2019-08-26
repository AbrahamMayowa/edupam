from django.urls import path
from . import views

urlpatterns = [
    path('post_form/', views.post_form_view, name='post_form'),
    path('post/<int:pk>/<slug:slug>', views.post_details, name='post_details'),
    path('post/academic/', views.academic_post_view, name='academic_post'),
    path('post/opportunity/', views.opportunity_post_view, name='opportunity_post'),
    path('post/business/', views.business_hub_view, name='business_post'),
    path('post/admission/', views.admission_view, name='admission_post'),
    path('post/events/', views.events_view, name='events_post'),
    path('post/politics/', views.politics_view, name='politics_post'),
    path('post/award/', views.award_view, name='award_post'),
    path('post/relationship/', views.relationship_view, name='relationship_post'),
    path('post/social/', views.social_life_view, name='social_post'),
    path('post/creative_writing/', views.creative_writing_view, name='creative_writing_post'),
    path('post/general/', views.general_view, name='general_post'),
    path('Thread/NYSC/', views.nysc, name='nysc_post'),
    path('post/report/<int:post_id>', views.post_flag_redirect, name='post_flag_redirect'),
    path('post/report/action/<int:post_id>', views.post_flag_ajax, name='post_flag_ajax'),
    path('post/edit/<int:post_id>', views.edit_post, name='edit_post'),
    path('post/thump/up/<int:post_id>', views.post_thumped_up, name='post_thumped_up'),
    path('post/thump/down/<int:post_id>', views.post_thumped_down, name='post_thumped_down'),
    path('post/comment/<int:pk>', views.post_comment_view, name='post_comment_view'),
    path('post/comment/<int:post_id>/<int:comment_id>/edit', views.post_comment_edit, \
        name='post_comment_edit'),
    path('post/comment/<int:comment_id>/report', views.comment_flag_redirect, name='comment_flag_redirect'),
    path('post/comment/<int:comment_id>/action', views.comment_flag_ajax, name='comment_flag_ajax'),
    path('post/<int:post_id>/comment/<int:comment_id>/thump/up', views.comment_thump_up, name='comment_thump_up'),
    path('post/<int:post_id>/comment/<int:comment_id>/thump/down', views.comment_thump_down, name='comment_thump_down'),
    path('post/comment/<int:comment_id>/reply', views.comment_reply, name='comment_reply'),
    path('post/comment/<int:comment_id>/reply/<int:reply_id>/edit', views.comment_reply_edit, name='comment_reply_edit'),
    path('post/comment/<int:reply_id>/reply/flag/redirect', views.comment_reply_flag_redirect, name='comment_reply_flag_redirect'),
    path('post/comment/int:reply_id>/reply/flag/action', views.comment_reply_flag_ajax, name='comment_reply_flag_ajax'),
    path('post/reply/<int:reply_id>/thump/up', views.reply_thump_up, name='reply_thump_up'),
    path('post/reply/<int:reply_id>/thump/down', views.reply_thump_down, name='reply_thump_down'),
    path('post/follow/<int:post_id>', views.follow_post, name='follow_post'),
    path('post/comment/<int:comment_id>/details', views.comment_details, name='comment_details'),
    path('post/home', views.post_list_and_post_create_form, name='list_and_create'),
    path('post/comment/<int:comment_id>/up/main', views.comment_thump_up_for_comment_main, name='comment_up_main'),
    path('post/comment/<int:comment_id>/down/main', views.comment_thump_down_for_comment_main, name='comment_down_main'),
    
    


]