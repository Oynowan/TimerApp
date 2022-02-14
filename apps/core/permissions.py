
def user_required_group(user, level):
    return user_has_permission(user, level)

def user_has_permission(user, level_required):
    groups_user = user.groups.all()
    level = 0
    if level_required == 'User':
        level_required = 1
    elif level_required == 'CFO':
        level_required = 2
    elif level_required == 'HR':
        level_required = 3
    elif level_required == 'Supervisor':
        level_required = 4
    elif level_required == 'Administrator':
        level_required = 5
    else:
        level_required = 0

    for group in groups_user:
        if group.name == 'User' and level < 1:
            level = 1
        elif group.name== 'CFO' and level < 2:
            level = 2
        elif group.name == 'HR' and level < 3:
            level = 3
        elif group.name == 'Supervisor' and level < 4:
            level = 4
        elif group.name == 'Administrator' and level < 5:
            level = 5
 
    return level >= level_required