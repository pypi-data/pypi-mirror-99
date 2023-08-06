import os, getpass, yaml
from datetime import datetime
from iatorch.db.utils import MIGRATIONS, migrate_all

PROJECT_DIRS = ['origin', 'dataset', 'results', 'assets', 'extracted']

def start_project(name):
    '''
    start_project
    '''
    
    print(f"Start Project '{name}'")
    
    ################################
    # create project
    ################################
    root = os.path.join(os.path.abspath('.'), name.strip('/'))
    
    if os.path.exists(root):
        itry = 0
        reinit = ''
        options = ['yes', 'No']
        while reinit not in options and itry < 5:
            itry += 1
            reinit = input(f"  - Directory './{name}' already exists. Re-initialize it? ({' or '.join(options)})")
        if reinit == 'No':
            print("  - [EXIT] Stop creating new project.")
            return
            
    if not os.path.exists(root):
        print(f"  - Make project directory '{root}'")
        os.makedirs(root)
        os.chmod(root, 0o775)

    ################################
    # create db and directories
    ################################
    # make subdirs
    print(f"  - Make project's subdirs '{', '.join([f'{sd}' for sd in PROJECT_DIRS])}'")
    for d in PROJECT_DIRS:
        _dir = os.path.join(root, d)
        if not os.path.exists(_dir):
            os.makedirs(_dir)
            os.chmod(_dir, 0o775)            
        
    # migrate databases
    print(f"  - Migrate databases '{', '.join([v['fn'] for _, v in MIGRATIONS.items()])}'")
    uris = migrate_all(root)
    
    # create project.yaml
    info = {
        'project': name,
        'creator': getpass.getuser(),
        'created': datetime.now().strftime("%Y-%m-%d"),
        'db': {k: uri.replace(root.rstrip('/'), '.') for k, uri in uris.items()}
    }
    with open(os.path.join(root, 'project.yaml'), 'w') as fw:
        yaml.dump(info, fw, sort_keys=False)
    
    # finish
    print(f"  - [DONE] Project '{name}' is ready!")
