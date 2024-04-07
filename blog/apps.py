from django.apps import AppConfig
#from django.contrib.admin.apps import AdminConfig



# Based on Tutorial: https://www.youtube.com/watch?v=fNMTKxO8HsI&list=PLOLrQ9Pn6cazhaxNDhcOIPYXt2zZhAXKO&index=6
#class BlogAdminConfig(AdminConfig):
#    default_site = 'blog.admin.BlogAdminArea'


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
