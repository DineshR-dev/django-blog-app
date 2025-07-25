from django.contrib.auth.models import Group,Permission

# Signal to create groups and permissions for the blog app
def create_groups_permissions(sender, **kwargs):

    try:
        # Create Groups
        reader,created = Group.objects.get_or_create(name='Readers')
        author,created = Group.objects.get_or_create(name='Authors')
        editor,created = Group.objects.get_or_create(name='Editors')

        # Create permissions for each group
        reader_permissions = [
            Permission.objects.get(codename='view_post')
        ]
        
        author_permissions = [
            Permission.objects.get(codename='view_post'),
            Permission.objects.get(codename='change_post'),
            Permission.objects.get(codename='delete_post'),
            Permission.objects.get(codename='add_post'),
        ]
        # Create a custom permission for publishing posts
        publish_perm,created = Permission.objects.get_or_create(codename='can_publish',content_type_id=8,name='can publish post')

        editor_permissions = [
            Permission.objects.get(codename='view_post'),
            Permission.objects.get(codename='change_post'),
            Permission.objects.get(codename='delete_post'),
            Permission.objects.get(codename='add_post'),
            publish_perm
        ]

        # Assign permissions to groups
        reader.permissions.set(reader_permissions)
        author.permissions.set(author_permissions)
        editor.permissions.set(editor_permissions)
        print("Groups and permissions created Successfully")

    except Exception as E:
        print( f"An error occurred: {E}")